# Copyright 2023 OctoML, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import math
import operator
import os
from dataclasses import dataclass
from typing import Sequence, Any, Tuple, Optional, List, Iterator

import torch
import torch.fx as fx
from torch._ops import OpOverload
from torch.func import functional_call
from torch.fx.experimental.proxy_tensor import make_fx

from .protos import fxgraph_pb2 as pb

log = logging.getLogger(__name__)


@dataclass
class _ParameterInfo:
    parameter: torch.Tensor
    start_padding: int
    size_bytes: int


class WeightFileDescription:
    def __init__(self, total_size: int, parameters: Sequence[_ParameterInfo]):
        self._total_size = total_size
        self._parameters = parameters

    @property
    def total_size(self) -> int:
        return self._total_size

    def to_byte_chunks(self) -> Iterator[memoryview]:
        for p in self._parameters:
            if p.start_padding != 0:
                yield b'\0' * p.start_padding
            bytes = memoryview(p.parameter.data.cpu().contiguous().numpy()).cast('B')
            if len(bytes) != p.size_bytes:
                raise RuntimeError(f"Size mismatch: expected tensor of shape {p.parameter.shape}"
                                   f" and dtype {p.parameter.dtype} to take exactly {p.size_bytes}"
                                   f" bytes but it is {len(bytes)} bytes")
            yield bytes


@dataclass
class _WeightFileLocation:
    weight_file_index: int
    weight_file_offset: int
    size_bytes: int


class _WeightFilePacker:
    def __init__(self, max_packed_file_size=math.inf):
        self._max_packed_file_size = max_packed_file_size
        self._packed_files: List[WeightFileDescription] = []
        self._next_file_size = 0
        self._params_for_next_file: List[_ParameterInfo] = []

    def push(self, parameter: torch.Tensor) -> _WeightFileLocation:
        size = torch.numel(parameter) * parameter.element_size()

        # Round up offset to a multiple of 16 bytes, so that data is properly aligned
        # in memory when the weight file is mmaped.
        offset = (self._next_file_size + 0xf) & ~0xf
        start_padding = offset - self._next_file_size

        if offset + size > self._max_packed_file_size:
            self._begin_new_file()
            offset = 0
            start_padding = 0

        file_index = len(self._packed_files)
        self._params_for_next_file.append(_ParameterInfo(parameter, start_padding, size))
        self._next_file_size = offset + size
        return _WeightFileLocation(file_index, offset, size)

    def get_file_descriptions(self) -> Sequence[WeightFileDescription]:
        self._begin_new_file()
        return tuple(self._packed_files)

    def _begin_new_file(self):
        if len(self._params_for_next_file) > 0:
            self._packed_files.append(WeightFileDescription(self._next_file_size,
                                                            tuple(self._params_for_next_file)))
            self._params_for_next_file.clear()
            self._next_file_size = 0


@dataclass
class SerializedFxProtoModel:
    model: pb.Model
    weight_files: Sequence[WeightFileDescription]

    def save(self, path):
        os.mkdir(path)
        weights_path = os.path.join(path, "weights")
        os.mkdir(weights_path)
        model = self.model.SerializeToString()
        with open(os.path.join(path, "model.dat"), "wb") as f:
            f.write(model)
        for i, w in enumerate(self.weight_files):
            with open(os.path.join(weights_path, str(i)), "wb") as f:
                for buf in w.to_byte_chunks():
                    f.write(buf)


def fx_graph_to_proto(gm: fx.GraphModule, example_inputs: Sequence[Any])\
        -> SerializedFxProtoModel:
    # fx.Graph passes that transform fx.GraphModule into proto-ready
    functionalized_gm, fixed_inputs = _functionalize_fx_graph(gm, example_inputs)
    _convert_lift_to_torch_tensor(functionalized_gm)

    # fx.Graph to proto
    graph_proto = _functionalized_fx_graph_to_proto(functionalized_gm.graph)
    fixed_input_protos, weight_files = _fixed_inputs_to_proto(fixed_inputs)
    model_proto = pb.Model(graph=graph_proto, fixed_inputs=fixed_input_protos)
    return SerializedFxProtoModel(model_proto, weight_files)


def _get_fake_mode(example_inputs: Sequence[Any]):
    for x in example_inputs:
        fake_mode = getattr(x, 'fake_mode', None)
        if fake_mode is not None:
            return fake_mode
    return torch._subclasses.FakeTensorMode(allow_non_fake_inputs=True)


def _functionalize_fx_graph(gm: fx.GraphModule, example_inputs: Sequence[Any]) \
        -> Tuple[fx.GraphModule, Sequence[torch.Tensor]]:
    fake_mode = _get_fake_mode(example_inputs)

    params = sorted([
        *gm.named_parameters(remove_duplicate=False),
        *gm.named_buffers(remove_duplicate=False)
    ], key=lambda x: x[0])

    param_tensors = [p for _name, p in params]
    param_names = [name for name, _p in params]

    duplicate_name = next((n1 for n1, n2 in zip(param_names, param_names[1:]) if n1 == n2),
                          None)
    if duplicate_name is not None:
        # This should be impossible, as parameters and buffers should have unique names within
        # the module. But if this does happen, we want to make this failure explicit because
        # the code below relies on uniqueness and may fail in hard-to-debug ways.
        #
        # Note that this is unrelated to "remove_duplicate=False" above, as that option
        # keeps identical parameter objects that are stored under multiple names.
        raise ValueError(f"Duplicate parameter/buffer name {duplicate_name} found in the model")

    # tie all params and remove duplicates for functionalization
    tensor_to_fake_tensor_map = {}
    active_params = list()
    active_fake_params = list()

    for tensor in param_tensors:
        if tensor not in tensor_to_fake_tensor_map:
            fk_param = fake_mode.from_tensor(tensor, static_shapes=True)
            tensor_to_fake_tensor_map[tensor] = fk_param
            active_params.append(tensor)
            active_fake_params.append(fk_param)

    def run_functional(*all_args):
        unflattened_params = {}
        for name, tensor in params:
            unflattened_params[name] = tensor_to_fake_tensor_map[tensor]
        args = all_args[len(active_params):]
        return functional_call(gm, unflattened_params, args, {})

    with fake_mode:
        functionalized_gm = make_fx(run_functional)(*active_fake_params, *example_inputs)
    return functionalized_gm, active_params


def _is_constant_arg(arg):
    return isinstance(arg, torch.fx.node.Node) and arg.op == "get_attr"


# The "functionalize" pass above will convert torch.tensor() calls to something like
#
#       _tensor_constant0 = self._tensor_constant0
#       lift_fresh_copy = torch.ops.aten.lift_fresh_copy.default(_tensor_constant0);
#
# (See torch/fx/_symbolic_trace.py, Tracer.create_arg())
#
# The problem is that if we try to feed this graph as a source back to Dynamo again
# (as our torch.Inductor backend does), it will run into an infinite recursion error
# when trying to dispatch the call to lift_fresh_copy(). This is due to the tracer
# assuming that an input to lift_fresh_copy() is always an immediate constant Tensor,
# which is not the case here (instead, it is a symbolic output of the getattr node
# that represents the line _tensor_constant0 = self._tensor_constant0).
#
# Our workaround is to convert all calls to lift_fresh_copy()
# back to torch.tensor() calls.
#
def _convert_lift_to_torch_tensor(gm: torch.fx.GraphModule):
    for n in gm.graph.nodes:
        if n.op == 'call_function' and n.target is torch.ops.aten.lift_fresh_copy.default:
            if len(n.args) != 1 or not _is_constant_arg(n.args[0]) or len(n.kwargs) > 0:
                log.warning("Graph has a call to %s with a non-constant argument", n.target)
                continue
            c = getattr(gm, n.args[0].target)
            data = c.data.cpu().numpy().tolist()
            with gm.graph.inserting_after(n):
                new_node = gm.graph.call_function(torch.tensor, (data,), dict(dtype=c.dtype))
            n.replace_all_uses_with(new_node)
            gm.graph.erase_node(n)

    # Remove all getattr nodes that are now unused
    gm.graph.eliminate_dead_code()

    gm.recompile()


_value_serializers = {}


def _value_serializer(*dtypes):
    def decorate(f):
        for t in dtypes:
            _value_serializers[t] = f
        return f
    return decorate


@_value_serializer(fx.Node)
def _node_to_proto(node: fx.Node, _weight_packer) -> pb.Value:
    return pb.Value(node_name=node.name)


@_value_serializer(int)
def _int_to_proto(x: int, _weight_packer) -> pb.Value:
    return pb.Value(integer=str(x))


@_value_serializer(float)
def _float_to_proto(x: float, _weight_packer) -> pb.Value:
    return pb.Value(float=x)


@_value_serializer(bool)
def _bool_to_proto(x: bool, _weight_packer) -> pb.Value:
    return pb.Value(boolean=x)


@_value_serializer(type(None))
def _none_to_proto(_x, _weight_packer) -> pb.Value:
    return pb.Value(none=True)


@_value_serializer(str)
def _str_to_proto(x: str, _weight_packer) -> pb.Value:
    return pb.Value(string=x)


_dtype_map = {
    torch.bool: pb.DTYPE_BOOL,
    torch.uint8: pb.DTYPE_UINT8,
    torch.int16: pb.DTYPE_INT16,
    torch.int32: pb.DTYPE_INT32,
    torch.int64: pb.DTYPE_INT64,
    torch.int8: pb.DTYPE_INT8,
    torch.float16: pb.DTYPE_FLOAT16,
    torch.float32: pb.DTYPE_FLOAT32,
    torch.float64: pb.DTYPE_FLOAT64,
    torch.bfloat16: pb.DTYPE_BFLOAT16,
    torch.complex32: pb.DTYPE_COMPLEX32,
    torch.complex64: pb.DTYPE_COMPLEX64,
    torch.complex128: pb.DTYPE_COMPLEX128,
}


def _convert_dtype(x: torch.dtype) -> pb.DtypeValue:
    try:
        return _dtype_map[x]
    except KeyError:
        raise ValueError(f"Unsupported data type {x}")


@_value_serializer(torch.dtype)
def _dtype_to_proto(x: torch.dtype, _weight_packer) -> pb.Value:
    return pb.Value(dtype=_convert_dtype(x))


@_value_serializer(torch.device)
def _device_to_proto(x: torch.device, _weight_packer) -> pb.Value:
    return pb.Value(device=pb.DeviceValue(type=x.type,
                                          with_index=x.index is not None,
                                          index=x.index))


_memory_format_map = {
    torch.contiguous_format: pb.MEMORY_FORMAT_CONTIGUOUS,
    torch.channels_last: pb.MEMORY_FORMAT_CHANNELS_LAST,
    torch.channels_last_3d: pb.MEMORY_FORMAT_CHANNELS_LAST_3D,
    torch.preserve_format: pb.MEMORY_FORMAT_PRESERVE_FORMAT,
}


@_value_serializer(torch.memory_format)
def _memory_format_to_proto(x, _weight_packer):
    try:
        format = _memory_format_map[x]
    except KeyError:
        raise ValueError(f"Unsupported memory format {x}")
    return pb.Value(memory_format=format)


_layout_map = {
    torch.strided: pb.LAYOUT_STRIDED,
    torch.sparse_coo: pb.LAYOUT_SPARSE_COO
}


@_value_serializer(torch.layout)
def _layout_to_proto(x, _weight_packer):
    try:
        layout = _layout_map[x]
    except KeyError:
        raise ValueError(f"Unsupported layout {x}")
    return pb.Value(layout=layout)


@_value_serializer(tuple)
def _tuple_to_proto(x, weight_packer) -> pb.Value:
    items = [_value_to_proto(item, weight_packer) for item in x]
    return pb.Value(tuple=pb.ListValue(items=items))


@_value_serializer(list)
def _list_to_proto(x, weight_packer) -> pb.Value:
    items = [_value_to_proto(item, weight_packer) for item in x]
    return pb.Value(list=pb.ListValue(items=items))


def _tensor_to_proto(x, weight_packer: Optional[_WeightFilePacker]) -> pb.Value:
    if weight_packer is None:
        raise TypeError("Cannot serialize a Tensor in this context")
    location = weight_packer.push(x)
    tensor_value = pb.TensorValue(
        dtype=_convert_dtype(x.dtype),
        shape=tuple(int(s) for s in x.shape),
        weight_file_index=location.weight_file_index,
        weight_file_offset=location.weight_file_offset,
        size_bytes=location.size_bytes
    )
    ret = pb.Value(tensor=tensor_value)
    return ret


def _value_to_proto(x: Any,
                    weight_packer: Optional[_WeightFilePacker] = None) -> pb.Value:
    try:
        serializer = _value_serializers[type(x)]
    except KeyError:
        if isinstance(x, torch.Tensor):
            serializer = _tensor_to_proto
        elif isinstance(x, list):
            serializer = _list_to_proto
        else:
            raise TypeError(f"Cannot serialize a value of type {type(x)}")
        _value_serializers[type(x)] = serializer

    return serializer(x, weight_packer)


def _kwarg_to_proto(name, x) -> pb.KwArgValue:
    return pb.KwArgValue(name=name, value=_value_to_proto(x))


def _target_to_proto(target) -> pb.Function:
    if isinstance(target, OpOverload):
        # Parse the string representation to avoid poking into private fields
        namespace, op_name, overload_name = str(target).split('.')
        return pb.Function(
            op_overload=pb.OpOverload(
                namespace=namespace,
                op_name=op_name,
                overload_name=overload_name))
    elif target is operator.getitem:
        return pb.Function(python_operator="getitem")
    elif target is torch.tensor:
        return pb.Function(torch_function="tensor")
    else:
        raise TypeError(f"Cannot serialize an object {target}"
                        f" of type {type(target)} as a call target")


def _functionalized_fx_graph_to_proto(graph: fx.Graph) -> pb.Graph:
    nodes = []
    for node in graph.nodes:
        node_proto = pb.Node(name=node.name)
        if node.op == "placeholder":
            node_proto.placeholder.CopyFrom(pb.PlaceholderNode())
        elif node.op == "call_function":
            target = _target_to_proto(node.target)
            node_proto.call_function.CopyFrom(pb.CallFunctionNode(
                target=target,
                args=[_value_to_proto(x) for x in node.args],
                kwargs=[_kwarg_to_proto(name, x) for name, x in node.kwargs.items()]
            ))
        elif node.op == "output":
            result, = node.args
            result_proto = _value_to_proto(result)
            node_proto.output.CopyFrom(pb.OutputNode(result=result_proto))
        else:
            raise ValueError(f"Unexpected FX opcode {node.op}")
        nodes.append(node_proto)
    return pb.Graph(nodes=nodes)


def _fixed_inputs_to_proto(fixed_inputs: Sequence[Any])\
        -> Tuple[Sequence[pb.FixedInput], Sequence[WeightFileDescription]]:
    weight_packer = _WeightFilePacker()
    fixed_input_protos = []
    for x in fixed_inputs:
        fixed_input_protos.append(pb.FixedInput(value=_value_to_proto(x, weight_packer)))
    weight_files = weight_packer.get_file_descriptions()
    return fixed_input_protos, weight_files

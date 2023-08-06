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

import contextlib
import functools
import os
import sys
import tempfile
import threading
import time
import traceback
import warnings
import weakref
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import (Callable, Dict, Optional, Sequence, TextIO, Tuple, List,
                    Union, Any)

import numpy as np
import onnx
import torch
import torch._dynamo as torchdynamo
import torch._guards
import torch.fx
from torch._dynamo.backends.common import fake_tensor_unsupported
from torch.jit import TracerWarning

from .client import RemoteInferenceSession, MODEL_FORMAT_ONNX, MODEL_FORMAT_FXPROTO, BackendSpecType
from .errors import CompilationError, LoadModelError
from .fx2proto import SerializedFxProtoModel, fx_graph_to_proto
from .inference_session import BackendSpec, InferenceSession, ModelRunner, \
    OnDiskFile, FileDescription, LazyInMemoryFile
from .log_util import LOGFILE, get_file_logger
from .report import (PerBackendResult, Profile, ProfileReport, Segment,
                     TotalPerBackendResult, PerBackendError)
from .shape import get_dynamic_axes
from .workaround import (_in_torch_dynamo,
                         _onnx_export_diagnostic_patch)

filelog = get_file_logger(__name__)


@dataclass
class _OnnxModel:
    path: str
    active_input_names: Sequence[str]
    active_input_mask: Sequence[bool]

    def get_file_descriptions(self) -> Sequence[FileDescription]:
        return [OnDiskFile(self.path, name) for name in os.listdir(self.path)]


def _torchscript_to_onnx(torchscript,
                         example_inputs: Tuple[torch.Tensor, ...],
                         defaked_example_inputs: Tuple[torch.Tensor, ...],
                         input_names: Sequence[str],
                         output_names: Sequence[str],
                         dirpath: str) -> _OnnxModel:
    model_path = os.path.join(dirpath, "model.onnx")
    dynamic_axes = get_dynamic_axes(input_names, example_inputs)
    torch.onnx.export(
        torchscript,
        defaked_example_inputs,
        model_path,
        input_names=input_names,
        output_names=output_names,
        opset_version=17,
        training=torch.onnx.TrainingMode.EVAL,
        dynamic_axes=dynamic_axes
    )

    onnx_model = onnx.load(model_path)

    onnx_input_names = set(inp.name for inp in onnx_model.graph.input)
    active_input_mask = tuple(n in onnx_input_names for n in input_names)
    active_input_names = tuple(n for n, is_active in zip(input_names, active_input_mask)
                               if is_active)

    external_data_dir = os.path.join(dirpath, "external")
    os.mkdir(external_data_dir)
    externalized_model_path = os.path.join(external_data_dir, "model.onnx")
    onnx.save_model(onnx_model, externalized_model_path, save_as_external_data=True,
                    all_tensors_to_one_file=True, location="external_data",
                    size_threshold=1024, convert_attribute=False)
    return _OnnxModel(path=external_data_dir,
                      active_input_names=active_input_names,
                      active_input_mask=active_input_mask)


@dataclass
class _Context:
    session: weakref.ReferenceType
    trace_recorder: '_TraceRecorder'
    last_graph_id: int
    num_repeats: int
    num_runs: int = field(default=0)

    def start_run(self):
        self.num_runs += 1
        if self.num_runs == 1:
            print("Accelerated function is being compiled on its first run:",
                  file=sys.stderr)
        else:
            print(f"Running function, iteration {self.num_runs}", file=sys.stderr)

    def new_graph_id(self) -> int:
        self.last_graph_id += 1
        return self.last_graph_id

    def dec_graph_id(self):
        self.last_graph_id -= 1


@dataclass
class _GraphInfo:
    graph_id: int
    num_nodes: int
    graph_module: torch.fx.GraphModule


@dataclass
class _LocalCpuSegment:
    run_time_nanos: int

    def footprint(self):
        return None

    def add(self, sample: '_LocalCpuSegment'):
        self.run_time_nanos += sample.run_time_nanos


@dataclass
class _BackendErrors:
    count: int
    unique_errors_to_count: Dict[str, int]


@dataclass
class _CompiledSegment:
    graph: _GraphInfo
    run_times_per_backend: Dict[BackendSpec, np.ndarray]
    errors_per_backend: Dict[BackendSpec, _BackendErrors]

    def footprint(self):
        return self.graph.graph_id

    def add(self, sample: '_CompiledSegment'):
        for backend, times in sample.run_times_per_backend.items():
            self.run_times_per_backend[backend] = \
                np.concatenate((self.run_times_per_backend[backend], times))

        for backend, error in sample.errors_per_backend.items():
            agg = self.errors_per_backend[backend]
            agg.count += error.count
            for err, err_count in error.unique_errors_to_count.items():
                if err not in agg.unique_errors_to_count:
                    agg.unique_errors_to_count[err] = 0
                agg.unique_errors_to_count[err] += err_count


@dataclass
class _AggregatedResult:
    sums: Sequence[Union[_LocalCpuSegment, _CompiledSegment]]
    num_runs: int
    compilation_occurred: bool

    def add(self, sample: Sequence[Union[_LocalCpuSegment, _CompiledSegment]]):
        assert self.compilation_occurred is False, \
            "Should not aggregate to result that has compilation occurred"
        assert len(self.sums) == len(sample)
        for agg, new in zip(self.sums, sample):
            agg.add(new)
        self.num_runs += 1

    def report(self, num_repeats):
        segments = []
        total_uncompiled_ms = 0.0
        total_per_backend = OrderedDict()
        for segment_idx, segment in enumerate(self.sums):
            if isinstance(segment, _LocalCpuSegment):
                mean_ms = segment.run_time_nanos / 1.0e6 / self.num_runs
                total_uncompiled_ms += mean_ms
                r = PerBackendResult(mean_ms=mean_ms,
                                     num_samples=self.num_runs,
                                     num_failures=0)
                segments.append(Segment(graph_id=None,
                                        results_per_backend=OrderedDict(Uncompiled=r)))
            elif isinstance(segment, _CompiledSegment):
                results_per_backend = OrderedDict()
                for backend, run_times in segment.run_times_per_backend.items():
                    backend_str = str(backend)
                    if backend_str not in total_per_backend:
                        total_per_backend[backend_str] = TotalPerBackendResult(
                                estimated_total_ms=0.0,
                                errors=[])
                    backend_total = total_per_backend[backend_str]

                    if len(run_times) > 0:
                        mean_ms = np.mean(run_times / 1.0e6)
                        if backend_total.estimated_total_ms is not None:
                            backend_total.estimated_total_ms += mean_ms
                    else:
                        mean_ms = None
                        backend_total.estimated_total_ms = None

                    err = segment.errors_per_backend[backend]
                    if err.count > 0:
                        total_per_backend[backend_str].errors.append(PerBackendError(
                                graph_id=segment.graph.graph_id,
                                error_messages_to_count=err.unique_errors_to_count))
                    results_per_backend[backend_str] = PerBackendResult(
                            mean_ms=mean_ms,
                            num_samples=len(run_times),
                            num_failures=err.count)

                segments.append(Segment(graph_id=segment.graph.graph_id,
                                        results_per_backend=results_per_backend))
            else:
                assert False

        for backend_total in total_per_backend.values():
            if backend_total.estimated_total_ms is not None:
                backend_total.estimated_total_ms += total_uncompiled_ms

        return Profile(segments=segments,
                       total_uncompiled_ms=total_uncompiled_ms,
                       total_per_backend=total_per_backend,
                       compilation_occurred=self.compilation_occurred,
                       num_runs=self.num_runs,
                       num_repeats=num_repeats)


class _TraceRecorder:
    def __init__(self):
        self._start_nanos = None
        self._segments = []
        self._result_by_footprint = OrderedDict()
        self._compilation_occurred = False
        self._num_discarded_runs = 0
        self._compile_errors = []

    def start_cpu(self):
        start = time.perf_counter_ns()
        assert self._start_nanos is None
        self._start_nanos = start

    def stop_cpu(self):
        end_nanos = time.perf_counter_ns()
        assert self._start_nanos is not None
        self._segments.append(_LocalCpuSegment(end_nanos - self._start_nanos))
        self._start_nanos = None

    @contextlib.contextmanager
    def pause_cpu(self) -> Callable[[], None]:
        end_nanos = time.perf_counter_ns()
        if self._start_nanos is None:
            yield
            return
        self._segments.append(_LocalCpuSegment(end_nanos - self._start_nanos))
        self._start_nanos = None
        try:
            yield
        finally:
            self.start_cpu()

    def add_compiled_segment(self, segment: _CompiledSegment):
        assert self._start_nanos is None
        self._segments.append(segment)

    def compilation_occurred(self):
        self._compilation_occurred = True

    def add_compile_error(self, error: str):
        self._compile_errors.append(error)

    def end_run(self):
        run_footprint = tuple(s.footprint() for s in self._segments)
        agg_result = self._result_by_footprint.get(run_footprint, None)
        if self._compilation_occurred:
            assert agg_result is None
            self._result_by_footprint[run_footprint] = \
                _AggregatedResult(tuple(self._segments), 1, True)
        elif agg_result is not None:
            if agg_result.compilation_occurred:
                self._result_by_footprint[run_footprint] = \
                    _AggregatedResult(tuple(self._segments), 1, False)
            else:
                agg_result.add(self._segments)
        else:
            # got here with compilation_occurred False
            # and no agg_result means torchdynamo failed
            pass

        if self._compilation_occurred:
            self._compilation_occurred = False
            self._num_discarded_runs += 1
        self._segments.clear()

    def report(self, num_repeats):
        profiles = [r.report(num_repeats)
                    for r in self._result_by_footprint.values()]
        return ProfileReport(profiles=profiles,
                             num_discarded_runs=self._num_discarded_runs,
                             compile_errors=self._compile_errors)

    def print_results(self, num_repeats: int, file=sys.stdout):
        self.report(num_repeats).print(file=file)


class _ThreadLocalState(threading.local):
    profiling_ctx: _Context = None


_thread_local_state = _ThreadLocalState()


def _run(runner: ModelRunner, graph_info: _GraphInfo, active_input_mask: Sequence[bool],
         *inputs: torch.Tensor):
    if _in_torch_dynamo():
        # Torchdynamo may run user compiled function during compilation, e.g.
        # for verifying correctness. This adds user overhead and also has side
        # effects to recorder. We can just pretend to run eager because remote
        # run with benchmark side effect is strongly undesirable. The flip side
        # is that `verify_correctness` is not repsected, which we do not care.
        return graph_info.graph_module(*inputs)

    ctx = _thread_local_state.profiling_ctx
    recorder = ctx.trace_recorder
    with recorder.pause_cpu():
        assert len(inputs) == len(active_input_mask), "invalid number of inputs for runner"
        inputs = tuple(x if isinstance(x, torch.Tensor) else torch.tensor(x) for x in inputs)
        numpy_inputs = (x.data.cpu().numpy() for x, is_active in zip(inputs, active_input_mask)
                        if is_active)
        num_repeats = ctx.num_repeats

        if ctx.num_runs == 1 and ctx.last_graph_id == graph_info.graph_id:
            print(f"\tCompiling and running graph {graph_info.graph_id} on remote...",
                  file=sys.stderr)
        result_by_backend = runner.run(numpy_inputs, num_repeats=num_repeats)
        errors_per_backend = {}
        run_times_per_backend = {}
        for backend, r in result_by_backend.items():
            if r.error_value is None:
                err = _BackendErrors(0, {})
            else:
                err = _BackendErrors(num_repeats, {r.error_value.message: num_repeats})
                log = get_file_logger(__name__)
                log.error("Error in run graph %d for backend %s: %s",
                          graph_info.graph_id, backend, r.error_value.message)
            errors_per_backend[backend] = err

            run_times_per_backend[backend] = \
                r.result_value.run_times_nanos if r.result_value is not None else []
        recorder.add_compiled_segment(_CompiledSegment(
            graph=graph_info,
            run_times_per_backend=run_times_per_backend,
            errors_per_backend=errors_per_backend
        ))
        return graph_info.graph_module(*inputs)


# Follows torch/_dynamo/backends/onnxrt.py to disable fake tensor
def _safe_dynamo_backend(_compile_func: Callable, gm: torch.fx.GraphModule,
                         example_inputs: Tuple[torch.Tensor, ...]):
    try:
        return _compile_func(gm, example_inputs)
    except Exception as e:
        if isinstance(e, torch.onnx.errors.OnnxExporterError):
            if isinstance(e, torch.onnx.errors.UnsupportedOperatorError):
                message = "export to onnx failed: UnsupportedOperator"
            else:
                message = f"export to onnx failed: {type(e)}"
        elif isinstance(e, LoadModelError):
            message = "load graph failed"
        else:
            message = f"of {type(e)}"
        graph_id = "local"
        if _thread_local_state.profiling_ctx:
            ctx = _thread_local_state.profiling_ctx
            graph_id = ctx.last_graph_id
            error = f"Graph #{graph_id} ran locally because "
            message = error + message
            ctx.trace_recorder.add_compile_error(message)
        trace = traceback.format_exc()
        graph_dump = f"Graph #{graph_id} dump:\n{gm.print_readable(print_output=False)}"
        filelog.error("%s\n%s\n%s", message, graph_dump, trace)
    return gm.forward


@dataclass
class _LoadedModelInfo:
    active_input_mask: Sequence[bool]


def _convert_symval_to_tensor(x):
    if isinstance(x, (torch.SymInt, torch.SymBool, torch.SymFloat)):
        return torch.tensor(x.node.hint)
    else:
        return x


@fake_tensor_unsupported
def _defake_tensors(gm, defaked_example_inputs):
    return list(map(_convert_symval_to_tensor, defaked_example_inputs))


def _load_onnx_model(session: InferenceSession,
                     graph_id: int,
                     backend_ids: Sequence[int],
                     gm: torch.fx.GraphModule,
                     example_inputs: Tuple[torch.Tensor, ...]) -> _LoadedModelInfo:
    defaked_example_inputs = _defake_tensors(gm, example_inputs)
    torchscript = torch.jit.trace(gm, defaked_example_inputs)
    example_outputs = torchscript(*defaked_example_inputs)
    if isinstance(example_outputs, (tuple, list)):
        num_outputs = len(example_outputs)
    else:
        num_outputs = 1

    assert num_outputs > 0, "Internal error: onnx graph must have more than one output"

    input_names = [f'input_{i}' for i in range(len(example_inputs))]
    output_names = [f'output_{i}' for i in range(num_outputs)]

    with tempfile.TemporaryDirectory() as dirpath:
        onnx_model = _torchscript_to_onnx(torchscript, example_inputs, defaked_example_inputs,
                                          input_names, output_names, dirpath)
        session.load_model(model_id=graph_id,
                           backend_ids=backend_ids,
                           model_format=MODEL_FORMAT_ONNX,
                           model_files=onnx_model.get_file_descriptions(),
                           input_names=onnx_model.active_input_names,
                           output_names=output_names)
    return _LoadedModelInfo(active_input_mask=onnx_model.active_input_mask)


def _load_fxproto_model(session: InferenceSession,
                        graph_id: int,
                        backend_ids: Sequence[int],
                        gm: torch.fx.GraphModule,
                        example_inputs: Tuple[torch.Tensor, ...]) -> _LoadedModelInfo:
    serialized_model = fx_graph_to_proto(gm, example_inputs)
    file_descriptions = _get_fxproto_file_descriptions(serialized_model)

    session.load_model(model_id=graph_id,
                       backend_ids=backend_ids,
                       model_format=MODEL_FORMAT_FXPROTO,
                       model_files=file_descriptions,
                       input_names=[],
                       output_names=[])
    # TODO: run dead code elimination pass?
    return _LoadedModelInfo(active_input_mask=[True] * len(example_inputs))


def _get_fxproto_file_descriptions(serialized_model: SerializedFxProtoModel):
    def _model_to_byte_chunks():
        bytes = serialized_model.model.SerializeToString()
        return len(bytes), iter([bytes])

    return [
        LazyInMemoryFile("model.dat", _model_to_byte_chunks),
        *(
            LazyInMemoryFile(f"weights/{i}", lambda: (w.total_size, w.to_byte_chunks()))
            for i, w in enumerate(serialized_model.weight_files)
        )
    ]


def _get_model_loader_for_backend(software_backend: str):
    if software_backend.startswith("onnxrt-"):
        return _load_onnx_model
    else:
        return _load_fxproto_model


def _group_backends_by_loader(backends: Sequence[BackendSpec]):
    backends_by_loader = OrderedDict()
    for idx, backend in enumerate(backends):
        loader = _get_model_loader_for_backend(backend.software_backend)
        if loader not in backends_by_loader:
            backends_by_loader[loader] = []
        backends_by_loader[loader].append(idx)
    return tuple(backends_by_loader.items())


def _get_overall_active_input_mask(loaded_infos: Sequence[Tuple[_LoadedModelInfo, Sequence[int]]],
                                   num_inputs: int):
    ret = [False] * num_inputs
    for info, _backend_indices in loaded_infos:
        for i, is_active in enumerate(info.active_input_mask):
            if is_active:
                ret[i] = True
    return ret


def _get_input_maps_per_backend(loaded_infos: Sequence[Tuple[_LoadedModelInfo, Sequence[int]]],
                                overall_active_input_mask: Sequence[bool],
                                num_backends: int)\
        -> Sequence[Sequence[int]]:
    active_idx_by_original_idx = {}
    for original_idx, is_active in enumerate(overall_active_input_mask):
        if is_active:
            active_idx_by_original_idx[original_idx] = len(active_idx_by_original_idx)

    ret = [()] * num_backends
    for info, backend_indices in loaded_infos:
        active_inputs = tuple(active_idx_by_original_idx[original_idx]
                              for original_idx, is_active in enumerate(info.active_input_mask)
                              if is_active)
        for backend_idx in backend_indices:
            ret[backend_idx] = active_inputs
    return ret


def _get_graph_outputs(gm: torch.fx.GraphModule):
    output_nodes = [n for n in gm.graph.nodes if n.op == 'output']
    assert len(output_nodes) == 1, "unexpected number of output nodes in FX Graph"
    return output_nodes[0].args


def _is_empty_output(output_args: Union[Tuple[Any], Any]):
    if isinstance(output_args, (Tuple, List)):
        return len(output_args) == 0 or all(_is_empty_output(x) for x in output_args)
    else:
        return False


def _remote_dynamo_backend(gm: torch.fx.GraphModule,
                           example_inputs: Tuple[Union[torch.Tensor, torch.SymInt], ...]):
    recorder = _thread_local_state.profiling_ctx.trace_recorder
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', TracerWarning)
        warnings.simplefilter('ignore', UserWarning)
        recorder.compilation_occurred()

        if gm.training:
            gm.eval()

        graph_info = _GraphInfo(graph_id=_thread_local_state.profiling_ctx.new_graph_id(),
                                num_nodes=len(gm.graph.nodes),
                                graph_module=gm)

        graph_outputs = _get_graph_outputs(gm)
        if _is_empty_output(graph_outputs):
            _thread_local_state.profiling_ctx.dec_graph_id()
            return gm.forward

        session = _thread_local_state.profiling_ctx.session()
        loaded_infos = []
        for loader, backend_indices in _group_backends_by_loader(session.backends):
            loaded_info = loader(session, graph_info.graph_id, backend_indices, gm, example_inputs)
            loaded_infos.append((loaded_info, backend_indices))

        active_input_mask = _get_overall_active_input_mask(loaded_infos, len(example_inputs))
        input_maps = _get_input_maps_per_backend(loaded_infos, active_input_mask,
                                                 len(session.backends))

        runner = session.create_runner(graph_info.graph_id, input_maps)
        ret = functools.partial(_run, runner, graph_info, active_input_mask)
        return ret


class ProfileHandle:
    def __init__(self, ctx: _Context):
        self._ctx = ctx

    def report(self) -> ProfileReport:
        return self._ctx.trace_recorder.report(self._ctx.num_repeats)


def _set_profiling_ctx(ctx: Optional[_Context]):
    _thread_local_state.profiling_ctx = ctx


def _print_results_if_requested(ctx: _Context, file: Optional[TextIO]):
    if file is not None:
        ctx.trace_recorder.print_results(ctx.num_repeats, file=file)


@contextlib.contextmanager
def remote_profile(session: Optional[InferenceSession] = None,
                   *,
                   # Session parameters:
                   backends: Optional[BackendSpecType] = None,
                   server_addr: Optional[str] = None,
                   insecure: Optional[bool] = None,
                   access_token: Optional[str] = None,
                   # Profiling options:
                   num_repeats: int = 10,
                   print_results_to: Optional[TextIO] = sys.stdout) -> ProfileHandle:
    if _thread_local_state.profiling_ctx is not None:
        raise RuntimeError("Nested remote_profile() contexts are not allowed")

    with contextlib.ExitStack() as guard:
        if session is not None:
            for session_arg in ["backends", "access_token", "server_addr", "insecure"]:
                if locals()[session_arg] is None:
                    continue
                raise ValueError(f"`session` cannot be set at the same time as `{session_arg}`."
                                 f" Please either specify an already existing session or"
                                 f" parameters for a new session, but not both at the same time.")
        else:
            session = RemoteInferenceSession(backends=backends,
                                             server_addr=server_addr,
                                             insecure=insecure,
                                             access_token=access_token)
            guard.enter_context(session)

        ctx = _Context(session=weakref.ref(session), trace_recorder=_TraceRecorder(),
                       last_graph_id=0, num_repeats=num_repeats)
        try:
            _set_profiling_ctx(ctx)
            guard.enter_context(torch.no_grad())
            guard.enter_context(_onnx_export_diagnostic_patch())
            guard.callback(_set_profiling_ctx, None)
            guard.callback(_print_results_if_requested, ctx, print_results_to)

            # Invalidated dynamo cache because session has changed
            torchdynamo.reset()

            yield ProfileHandle(ctx)
        finally:
            # Remove from frame so that the traceback doesn't hold a strong reference to the session
            del session


@contextlib.contextmanager
def _profile_run():
    recorder = _thread_local_state.profiling_ctx.trace_recorder
    _thread_local_state.profiling_ctx.start_run()
    recorder.start_cpu()
    try:
        yield
    finally:
        recorder.stop_cpu()
        recorder.end_run()


@dataclass
class _DynamizedModuleInner:
    original_module: torch.nn.Module
    decorated_forward: Callable


class _AcceleratedModule(torch.nn.Module):
    def __init__(self, original_module: torch.nn.Module, decorated_forward):
        object.__setattr__(self, '_accelerated_module_inner', None)
        super().__init__()
        object.__setattr__(self, '_accelerated_module_inner',
                           _DynamizedModuleInner(original_module, decorated_forward))

    def __getattribute__(self, name):
        inner = object.__getattribute__(self, '_accelerated_module_inner')
        if inner is None:
            # Still in __init__
            return object.__getattribute__(self, name)
        else:
            if name == "forward":
                return inner.decorated_forward
            else:
                return getattr(inner.original_module, name)

    def __setattr__(self, key, value):
        inner = object.__getattribute__(self, '_accelerated_module_inner')
        if inner is None:
            # Still in __init__
            return object.__setattr__(self, key, value)
        else:
            return setattr(inner.original_module, key, value)


# Define remote_backend outside of accelerate() to avoid dynamo.reset() warning
_remote_backend = functools.partial(_safe_dynamo_backend, _remote_dynamo_backend)


def accelerate(*args, **kwargs):
    direct_application = len(args) == 1 and len(kwargs) == 0 and callable(args[0])

    if not direct_application and len(args) > 0:
        raise ValueError('accelerate() accepts no positional arguments')

    local_backend = kwargs.get('local_backend', 'inductor')
    available_backends = torchdynamo.list_backends() + ['eager']
    if local_backend not in available_backends:
        backends_str = ','.join(available_backends)
        raise ValueError(f'Unknown backend {local_backend}. Available torch dynamo '
                         f'backends are: {backends_str}')

    dynamic = kwargs.get('dynamic', False)
    # TODO(yuanjing): don't fall back to eager once inductor's coverage is decent
    if local_backend == "inductor":
        # For some strange reason, importing inductor can mess up CUDA state, so import it lazily
        from torch._inductor.compile_fx import compile_fx
        local_backend = functools.partial(_safe_dynamo_backend, compile_fx)
    regular_dynamo_decorator = torchdynamo.optimize(local_backend, dynamic=dynamic)
    profiling_dynamo_decorator = torchdynamo.optimize(_remote_backend, dynamic=dynamic)

    def decorate(func):
        if isinstance(func, torch.nn.Module):
            decorated_forward = decorate(func.forward)
            return _AcceleratedModule(func, decorated_forward)
        regular_dynamo_decorated = regular_dynamo_decorator(func)
        profiling_dynamo_decorated = profiling_dynamo_decorator(func)

        @functools.wraps(regular_dynamo_decorated)
        def decorated_func(*args, **kwargs):
            exception = None
            try:
                if _thread_local_state.profiling_ctx is None:
                    return regular_dynamo_decorated(*args, **kwargs)
                with _profile_run():
                    return profiling_dynamo_decorated(*args, **kwargs)
            except torchdynamo.exc.TorchDynamoException as e:
                exception = type(e).__name__.split(".")[-1]
                trace = traceback.format_exc()
            except Exception as e:
                exception = type(e).__name__
                trace = traceback.format_exc()

            if exception:
                action = "The error above may be caused by user code error in "\
                         "the decorated function "\
                         "or a bug in TorchDynamo. In the former case, please "\
                         "check the trace for user code error; "\
                         "in the latter case, please "\
                         "try refining the scope of @accelerate closer to "\
                         "model inference."
                filelog.error("%s\n%s", trace, action)
                raise CompilationError(exception, {'details': LOGFILE})

        return decorated_func

    if direct_application:
        return decorate(args[0])
    else:
        return decorate

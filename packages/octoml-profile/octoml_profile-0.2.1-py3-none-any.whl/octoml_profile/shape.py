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
import sympy
import torch
from dataclasses import dataclass
from typing import Any, List, Optional, Union


@dataclass
class Dimension:
    value: Optional[int]

    def is_dynamic(self) -> bool:
        return self.value is None


def torch_tensor_to_dims(maybe_tensor: Union[torch.Tensor, Any]) -> List[Dimension]:
    # NB: This function assumes all tensor dimensions are integers,
    # and that any non-tensor input is a scalar.
    if not isinstance(maybe_tensor, torch.Tensor) or len(maybe_tensor.size()) == 0:
        return []

    size = maybe_tensor.size()
    dims = []
    for dim in size:
        if isinstance(dim, int):
            dims.append(Dimension(value=dim))
        elif isinstance(dim, torch.SymInt):
            if isinstance(dim.node.expr, sympy.core.numbers.Integer):
                dims.append(Dimension(value=int(dim.node.expr)))
            elif dim.node.constant is not None:
                dims.append(Dimension(value=dim.node.constant))
            else:
                dims.append(Dimension(value=None))
        else:
            raise RuntimeError("Dynamo should have traced all example input dimensions as "
                               f"int or SymInt but got type {type(dim)} instead")
    return dims


def get_dynamic_axes(input_names, tensors: List[torch.Tensor]):
    assert len(input_names) == len(tensors), ("This is a bug; please file an issue. "
                                              "Number of input names must match the "
                                              "number of dynamo-traced example inputs.")
    shapes = [torch_tensor_to_dims(t) for t in tensors]
    dynamic_axes = {}
    for name, dims in zip(input_names, shapes):
        axes = []
        for i, dim in enumerate(dims):
            if dim.is_dynamic():
                axes.append(i)
        if axes:
            dynamic_axes[name] = axes
    return dynamic_axes

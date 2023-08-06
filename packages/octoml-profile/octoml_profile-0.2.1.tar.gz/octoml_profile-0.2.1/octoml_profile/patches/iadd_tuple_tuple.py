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


import functools
import operator

from torch._dynamo.variables import BuiltinVariable, ConstantVariable, TupleVariable


orig_func = BuiltinVariable._binop_handlers.__wrapped__


@functools.lru_cache(None)
def _binop_handlers():
    handlers = orig_func()
    handlers[operator.iadd].append(
        (
            (ConstantVariable, TupleVariable),
            lambda tx, a, b, options: TupleVariable(
                list(a.unpack_var_sequence(tx)) + b.items, **options
            ),
        )
    )
    return handlers


def apply_patch():
    BuiltinVariable._binop_handlers = _binop_handlers

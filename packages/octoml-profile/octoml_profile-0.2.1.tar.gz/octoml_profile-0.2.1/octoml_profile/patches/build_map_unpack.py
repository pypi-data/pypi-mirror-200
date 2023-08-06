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


# Patch Dynamo to support BUILD_MAP_UNPACK and BUILD_MAP_UNPACK_WITH_CALL opcodes.
# Note that these only exist in CPython 3.8 and earlier.

from torch._dynamo.exc import unimplemented
from torch._dynamo.symbolic_convert import InstructionTranslatorBase
from torch._dynamo.variables import VariableTracker, ConstDictVariable
from torch._dynamo.variables.base import typestr, MutableLocal


def _build_map_common(self, inst, assert_no_duplicates):
    mappings = self.popn(inst.argval)
    options = VariableTracker.propagate(mappings)
    result = dict()
    for m in mappings:
        if not isinstance(m, ConstDictVariable):
            unimplemented(f"BUILD_MAP_UNPACK_WITH_CALL {typestr(m)}")
        result.update(m.items)
    if assert_no_duplicates:
        assert len(result) == sum(len(m.items) for m in mappings)
    self.push(
        ConstDictVariable(result, dict, mutable_local=MutableLocal(), **options)
    )


def BUILD_MAP_UNPACK(self, inst):
    return _build_map_common(self, inst, assert_no_duplicates=False)


def BUILD_MAP_UNPACK_WITH_CALL(self, inst):
    return _build_map_common(self, inst, assert_no_duplicates=True)


def apply_patch():
    if not hasattr(InstructionTranslatorBase, 'BUILD_MAP_UNPACK'):
        InstructionTranslatorBase.BUILD_MAP_UNPACK = BUILD_MAP_UNPACK

    if not hasattr(InstructionTranslatorBase, 'BUILD_MAP_UNPACK_WITH_CALL'):
        InstructionTranslatorBase.BUILD_MAP_UNPACK_WITH_CALL = BUILD_MAP_UNPACK_WITH_CALL

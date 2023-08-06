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

import operator
from torch._dynamo.variables import SymNodeVariable, BuiltinVariable

# From: https://github.com/pytorch/pytorch/pull/95564


def call_neg(self, tx, a):
    if isinstance(a, SymNodeVariable):
        return SymNodeVariable.create(
            tx,
            (operator.neg)(a.as_proxy()),
            sym_num=None,
        )
    # None no-ops this handler and lets the driving function proceed
    return None


def apply_patch():
    BuiltinVariable.call_neg = call_neg

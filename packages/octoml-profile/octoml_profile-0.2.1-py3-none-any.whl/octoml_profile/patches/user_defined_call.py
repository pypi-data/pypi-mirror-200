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


import inspect

from torch._dynamo.variables.user_defined import UserDefinedVariable


orig_func = UserDefinedVariable.call_function


def call_function(self, tx, args, kwargs):
    if hasattr(self.value, "__call__") and inspect.isclass(type(self)):
        return self.var_getattr(tx, "__call__").call_function(tx, args, kwargs)
    return orig_func(self, tx, args, kwargs)


def apply_patch():
    UserDefinedVariable.call_function = call_function

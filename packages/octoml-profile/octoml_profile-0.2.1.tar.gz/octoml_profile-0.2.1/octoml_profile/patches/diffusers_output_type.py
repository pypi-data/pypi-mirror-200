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


from torch._dynamo.variables import DataClassVariable
from torch._dynamo.eval_frame import skip_code
import functools


@functools.lru_cache(None)
def _patch_once():
    try:
        from transformers.file_utils import ModelOutput
        for obj in ModelOutput.__dict__.values():
            if callable(obj):
                skip_code(obj.__code__)
    except ImportError:
        pass

    try:
        from diffusers.utils import BaseOutput
        for obj in BaseOutput.__dict__.values():
            if callable(obj):
                skip_code(obj.__code__)
    except ImportError:
        pass


@staticmethod
def is_matching_cls(cls):
    match_transformers_output = False
    match_diffusers_output = False

    try:
        from transformers.file_utils import ModelOutput
        match_transformers_output = issubclass(cls, ModelOutput)
    except ImportError:
        match_transformers_output = False

    try:
        from diffusers.utils import BaseOutput
        match_diffusers_output = issubclass(cls, BaseOutput)
    except ImportError:
        match_diffusers_output = False

    return match_transformers_output | match_diffusers_output


def apply_patch():
    DataClassVariable._patch_once = _patch_once
    DataClassVariable.is_matching_cls = is_matching_cls

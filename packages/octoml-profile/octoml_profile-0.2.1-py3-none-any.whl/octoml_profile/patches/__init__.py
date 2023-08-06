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
from importlib import import_module

log = logging.getLogger(__name__)


def _apply(name):
    try:
        import_module(f".{name}", __name__).apply_patch()
    except Exception:
        log.debug("Failed to apply patch %s", name, exc_info=True)


def apply_patches():
    _apply("build_map_unpack")
    _apply("iadd_tuple_tuple")
    _apply("user_defined_call")
    _apply("diffusers_output_type")
    _apply("dyn_shape_call_neg")

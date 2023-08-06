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

from . import report
from ._about import version
from .client import RemoteInferenceSession, get_default_backends, get_supported_backends, \
    BackendSpec
from .dynamo import accelerate, remote_profile, ProfileHandle
from .inference_session import InferenceSession
from .patches import apply_patches


__version__ = version

__all__ = [
    "accelerate", "remote_profile",
    "get_default_backends", "get_supported_backends", "BackendSpec",
    "InferenceSession", "RemoteInferenceSession",
    "report", "ProfileHandle",
]

try:
    import octoml_profile_private  # noqa: F401
except ImportError:
    pass

apply_patches()

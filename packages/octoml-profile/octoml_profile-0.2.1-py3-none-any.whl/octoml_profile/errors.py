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

from typing import Dict, Optional


class OctomlProfileError(Exception):
    """The base error for all OctoML Profile exceptions"""

    def __init__(self, message: str, kwargs: Optional[Dict[str, str]] = None):
        self.message = message
        self.kwargs = kwargs
        super().__init__(message, kwargs)


class LoadModelError(OctomlProfileError):
    """Error occurred trying to load a model on remote. Signals that the client
    shouldn't continue execution, because model loads were successful on no backends."""


class CompilationError(OctomlProfileError):
    """Error occurred attempting to compile a model"""


class CreateSessionError(OctomlProfileError):
    """Error occurred creating session from client side"""

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

"""Helper classes for authenticating via gRPC."""
from .base import MetadataInterceptorBase, StreamMetadataInterceptorBase


class AuthInterceptor(MetadataInterceptorBase):
    """
    This class intercepts outbound unary <-> unary gRPC calls and adds
    an `Authorization: Bearer` header carrying an access token.

    :param access_token: The token to send in the `Authorization` header.
    """

    def __init__(self, access_token):
        super().__init__(key="authorization", value="Bearer " + access_token)


class StreamAuthInterceptor(StreamMetadataInterceptorBase):
    """
    This class intercepts outbound stream <-> unary gRPC calls and adds
    an `Authorization: Bearer` header carrying an access token.

    :param access_token: The token to send in the `Authorization` header.
    """
    def __init__(self, access_token):
        super().__init__(key="authorization", value="Bearer " + access_token)

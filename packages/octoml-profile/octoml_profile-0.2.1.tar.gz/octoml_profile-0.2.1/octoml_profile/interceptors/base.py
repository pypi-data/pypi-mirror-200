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

"""Helper class for creating grpc interceptors"""
from dataclasses import dataclass
from typing import Any, Tuple, Sequence, Optional

import grpc


@dataclass
class _ClientCallDetails(
    grpc.ClientCallDetails
):
    """
    A helper class that allows updating fields of a client call.
    """

    method: str
    timeout: Optional[float]
    metadata: Optional[Sequence[Tuple[str, Any]]]
    credentials: Optional[grpc.CallCredentials]


def _metadata_interceptor(continuation, client_call_details, request, key, value):
    """Helper for issuing a request using an interceptor."""
    metadata = []
    if client_call_details.metadata is not None:
        metadata = list(client_call_details.metadata)
    metadata.append((key, value))
    client_call_details = _ClientCallDetails(
        client_call_details.method,
        client_call_details.timeout,
        metadata,
        client_call_details.credentials,
    )
    return continuation(client_call_details, request)


class MetadataInterceptorBase(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Invoked by gRPC when issuing a request using this interceptor."""
        return _metadata_interceptor(continuation, client_call_details, request,
                                     self._key, self._value)


class StreamMetadataInterceptorBase(grpc.StreamUnaryClientInterceptor):
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value

    def intercept_stream_unary(self, continuation, client_call_details, request):
        """Invoked by gRPC when issuing a request using this interceptor."""
        return _metadata_interceptor(continuation, client_call_details, request,
                                     self._key, self._value)

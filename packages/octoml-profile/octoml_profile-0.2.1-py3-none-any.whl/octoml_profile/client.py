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
import atexit
import contextlib
import io
import logging
import os
import sys
import threading
import traceback
import weakref
from collections import defaultdict
from contextlib import ExitStack
from functools import partial
from getpass import getpass
from os.path import expanduser
from typing import Iterator, Mapping, Optional, Sequence, Tuple, Union, Iterable, NamedTuple
from uuid import UUID

import grpc

from .conversion_util import numpy_to_proto
from .errors import LoadModelError, CreateSessionError
from .inference_session import (BackendSpec, InferenceSession, ModelRunner,
                                RunResult, FileDescription)
from .interceptors.auth import AuthInterceptor, StreamAuthInterceptor
from .interceptors.cookie import CookieInterceptor, StreamCookieInterceptor
from .log_util import LOGFILE, get_file_logger
from .protos import remote_inference_pb2 as pb, remote_inference_pb2_grpc as rpc

BackendSpecType = Union[str, BackendSpec, Sequence[Union[str, BackendSpec,
                                                         pb.BackendSpec]]]

MODEL_FORMAT_ONNX = pb.MODEL_FORMAT_ONNX
MODEL_FORMAT_FXPROTO = pb.MODEL_FORMAT_FXPROTO


MAX_GRPC_MESSAGE_SIZE = 1024 * 1024 * 1024   # 1GiB


class RemoteModelRunner(ModelRunner):
    def __init__(self,
                 session: 'RemoteInferenceSession',
                 model_id: int,
                 input_map_per_backend: Sequence[pb.InputMap]):
        self._session = weakref.ref(session)
        self._model_id = model_id
        self._input_map_per_backend = input_map_per_backend

    def run(self, inputs, num_repeats=None) -> Mapping[BackendSpec, RunResult]:
        session = self._session()
        input_protos = [numpy_to_proto(x) for x in inputs]
        request = pb.RunRequest(session_uuid=session._session_uuid.bytes,
                                model_id=self._model_id,
                                inputs=input_protos,
                                num_repeats=num_repeats,
                                input_map_per_backend=self._input_map_per_backend)
        reply = session._client.stub.Run(request)
        assert len(reply.result_per_backend) == len(session._backends)
        return {
            backend: RunResult.from_pb(result)
            for backend, result in zip(session._backends, reply.result_per_backend)
        }


def _get_backend_specs(backends: Optional[BackendSpecType] = None)\
        -> Sequence[BackendSpec]:
    if backends is None:
        return []
    if isinstance(backends, str):
        return BackendSpec.parse(backends),
    elif isinstance(backends, BackendSpec):
        return backends
    else:
        ret = []
        for backend in backends:
            if isinstance(backend, str):
                ret.append(BackendSpec.parse(backend))
            elif isinstance(backend, BackendSpec):
                ret.append(backend)
            else:
                raise TypeError(f'Expected a string or a BackendSpec, got {type(backend)}')
        return ret


def _heartbeat_thread(stub: rpc.RemoteInferenceStub,
                      session_uuid: UUID,
                      quit_event: threading.Event,
                      logger: logging.Logger):
    HEARTBEAT_PERIOD_SECONDS = 10
    RETRY_TIMEOUT_SECONDS = 1

    next_timeout = HEARTBEAT_PERIOD_SECONDS
    prev_future = None

    while True:
        if quit_event.wait(timeout=next_timeout):
            break

        if prev_future is not None:
            if not prev_future.done():
                next_timeout = RETRY_TIMEOUT_SECONDS
                continue

            try:
                prev_future.result()
            except grpc.RpcError as e:
                if e.code() in {grpc.StatusCode.FAILED_PRECONDITION,
                                grpc.StatusCode.PERMISSION_DENIED}:
                    logger.error(e, exc_info=True)
                    print(f"\nReceived GRPC error {e.code()}, stopping the heartbeat thread",
                          file=sys.stderr)
                    print(f"For full client-side error traces see {LOGFILE}", file=sys.stderr)
                    return

        try:
            prev_future = stub.Heartbeat.future(
                pb.HeartbeatRequest(session_uuid=session_uuid.bytes))
        except grpc.RpcError:
            # TODO: log?
            next_timeout = RETRY_TIMEOUT_SECONDS
            prev_future = None
            continue

        next_timeout = HEARTBEAT_PERIOD_SECONDS


_all_sessions = dict()


def _register_session(session: InferenceSession):
    _all_sessions[id(session)] = weakref.ref(session)


def _unregister_session(session: 'InferenceSession'):
    # We are defensive here because this function is called from __del__,
    # which can run during interpreter shutdown, after module globals have been set to None.
    if _all_sessions is not None:
        _all_sessions.pop(id(session), None)


def _close_surviving_sessions(sessions):
    for ref in sessions.values():
        s = ref()
        if s is not None:
            s.close()


atexit.register(_close_surviving_sessions, _all_sessions)


_CONFIG_DIR = expanduser("~/.config/octoml_profile/")
_CONFIG_ACCESS_TOKEN_PATH = _CONFIG_DIR + "access_token"
_SIGNUP_URL = "https://profiler.app.octoml.ai/"


def _load_access_token_from_config() -> Optional[str]:
    try:
        with open(_CONFIG_ACCESS_TOKEN_PATH) as f:
            token = f.read().strip()
            return None if len(token) == 0 else token
    except Exception:
        return None


def _save_access_token_to_config(token: str):
    try:
        os.makedirs(_CONFIG_DIR, exist_ok=True)
        with open(_CONFIG_ACCESS_TOKEN_PATH, "w",
                  opener=partial(os.open, mode=0o600)) as f:
            f.write(token)
    except Exception as e:
        print(f"Couldn't save the access token to {_CONFIG_ACCESS_TOKEN_PATH}: {e}",
              file=sys.stderr)
    else:
        print(f"Saved access token to {_CONFIG_ACCESS_TOKEN_PATH}", file=sys.stderr)


def _verify_access_token(token: str, server_addr: str, insecure: bool):
    client = _Client(server_addr=server_addr, insecure=insecure, access_token=token,
                     access_token_source="")
    try:
        client.ping()
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            return False
        raise
    return True


_WELCOME_MESSAGE = f"""\
    ,-""-.
   /      \\    Welcome to OctoML Profiler!
  :        ;
   \\      /    It looks like you don't have an access token configured.
    `.  .'     Please go to {_SIGNUP_URL} to generate one
  '._.'`._.'   and then paste it here.
"""


def _prompt_user_for_access_token(server_addr: str, insecure: bool):
    print(_WELCOME_MESSAGE, file=sys.stderr)
    while True:
        token = getpass("Access token: ")
        if _verify_access_token(token, server_addr, insecure):
            _save_access_token_to_config(token)
            return token
        print(f"Oops! It looks like the access token didn't work. Please try again.",
              file=sys.stderr)


class _TokenWithSource(NamedTuple):
    access_token: Optional[str]
    source_desc: str


_ACCESS_TOKEN_ENV_KEY = "OCTOML_PROFILE_API_TOKEN"


def _get_access_token(token_from_arg: Optional[str],
                      server_addr: str,
                      insecure: bool) -> _TokenWithSource:
    if insecure:
        return _TokenWithSource(None, "Access token was not used because an insecure channel"
                                      "was selected.")

    if token_from_arg is not None:
        return _TokenWithSource(token_from_arg, "Access token was passed as an explicit argument.")
    token_from_env = os.environ.get(_ACCESS_TOKEN_ENV_KEY, None)
    if token_from_env is not None and len(token_from_env) > 0:
        return _TokenWithSource(token_from_env,
                                f"Access token was set via the {_ACCESS_TOKEN_ENV_KEY}"
                                f" environment variable.")

    token_from_config = _load_access_token_from_config()
    if token_from_config is not None:
        return _TokenWithSource(token_from_config, f"Access token was read from file"
                                                   f" at {_CONFIG_ACCESS_TOKEN_PATH}.")

    token = _prompt_user_for_access_token(server_addr=server_addr, insecure=insecure)
    return _TokenWithSource(token, "Access token was read from keyboard.")


class _Client:
    def __init__(self,
                 server_addr: str,
                 insecure: bool,
                 access_token: Optional[str],
                 access_token_source: str):
        if insecure:
            self._channel = grpc.insecure_channel(
                server_addr,
                options=(
                    ('grpc.max_send_message_length', MAX_GRPC_MESSAGE_SIZE),
                    ('grpc.max_receive_message_length', MAX_GRPC_MESSAGE_SIZE),
                ),
            )
        else:
            credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel(
                server_addr,
                credentials,
                options=(
                    ('grpc.max_send_message_length', MAX_GRPC_MESSAGE_SIZE),
                    ('grpc.max_receive_message_length', MAX_GRPC_MESSAGE_SIZE),
                ),
            )
            if access_token is not None:
                self._channel = grpc.intercept_channel(self._channel,
                                                       AuthInterceptor(access_token),
                                                       StreamAuthInterceptor(access_token))

        self._stub = rpc.RemoteInferenceStub(self._channel)
        self._backends_and_presets = None
        self._access_token_source = access_token_source

    @staticmethod
    def create(server_addr: Optional[str] = None,
               insecure: Optional[bool] = False,
               access_token: Optional[str] = None) -> '_Client':
        # FIXME: shouldn't explicitly given args take priority over env variables?
        server_addr = os.environ.get("OCTOML_PROFILE_ENDPOINT", None) or server_addr
        if server_addr is None:
            server_addr = "dynamite.prod.aws.octoml.ai"
        if insecure is None:
            insecure = False

        access_token, token_src = _get_access_token(access_token, server_addr, insecure)
        return _Client(server_addr, insecure, access_token, token_src)

    def close(self):
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def is_closed(self) -> bool:
        return self._channel is None

    @property
    def stub(self):
        if self.is_closed():
            raise ValueError("Client is in a closed state")
        return self._stub

    def get_supported_backends(self) -> Sequence[BackendSpec]:
        return [_backend_spec_from_proto(b) for b in self._list_backends_and_presets().backends]

    def get_default_backends(self) -> Sequence[BackendSpec]:
        for p in self._list_backends_and_presets().presets:
            if p.preset_name == "default":
                return [_backend_spec_from_proto(b) for b in p.backends]
        raise ValueError("The server did not provide a list of default backends to use")

    def _list_backends_and_presets(self):
        if self._backends_and_presets is None:
            self._backends_and_presets = self.stub.ListSupportedBackends(
                    pb.ListSupportedBackendsRequest())
        return self._backends_and_presets

    def ping(self):
        self._stub.Ping(pb.PingRequest(), timeout=7.0)

    def create_session(self, request) -> pb.CreateSessionResultValue:
        reply, call = self.stub.CreateSession.with_call(request)

        # Set cookie for sticky sessions
        for item in call.initial_metadata():
            if item.key == 'set-cookie':
                cookie = item.value
                self._channel = grpc.intercept_channel(self._channel,
                                                       CookieInterceptor(cookie),
                                                       StreamCookieInterceptor(cookie))
                self._stub = rpc.RemoteInferenceStub(self._channel)

        if reply.WhichOneof('result') == 'error_value':
            raise ValueError(f"Error starting a remote inference session:"
                             f" {reply.error_value.message}")
        return reply.result_value

    def wait_until_session_ready(self, session_uuid: UUID):
        print('Waiting for an available remote worker...', file=sys.stderr)
        while True:
            reply = self.stub.WaitUntilSessionReady(
                pb.WaitUntilSessionReadyRequest(session_uuid=session_uuid.bytes))

            if reply.ready:
                print('Acquired all workers, session is now ready.', file=sys.stderr)
                break


def _backend_spec_from_proto(b: pb.BackendSpec) -> BackendSpec:
    return BackendSpec(hardware_platform=b.hardware_platform, software_backend=b.software_backend)


def _backend_spec_to_proto(b: BackendSpec) -> pb.BackendSpec:
    return pb.BackendSpec(hardware_platform=b.hardware_platform,
                          software_backend=b.software_backend)


def _get_backends(backends: Sequence[BackendSpec], client: _Client):
    # Before creating the session, check that requested backends are valid
    if len(backends) == 0:
        backends = client.get_default_backends()
        backends_str = ', '.join(str(b) for b in backends)
        print(f'No backends were requested, using defaults: {backends_str}', file=sys.stderr)
    else:
        supported_backends = client.get_supported_backends()
        unsupported = [b for b in backends if b not in supported_backends]
        if len(unsupported) > 0:
            unsupported_str = ', '.join(str(b) for b in unsupported)
            supported_str = '\n\t'.join(str(b) for b in supported_backends)
            raise ValueError(f'Some of the requested backends ({unsupported_str})'
                             f' are not supported.\n'
                             f'The supported, valid backends are:\n\t{supported_str}')
    return backends


@contextlib.contextmanager
def _handle_session_create_error(logger, access_token_source):
    try:
        yield
    except grpc.RpcError as rpc_error:
        if rpc_error.code() == grpc.StatusCode.UNAUTHENTICATED:
            raise RuntimeError(f"Authentication with server failed: {rpc_error.details()}."
                               f" {access_token_source} If the problem persists, you can"
                               f" try generating a new access token at {_SIGNUP_URL}")

        # Extract the details of the gRPC error
        if hasattr(rpc_error, "debug_error_string"):
            status_debug_string = f" [debug_error_string: {rpc_error.debug_error_string()}]"
        else:
            status_debug_string = ""

        logger.error("An error occurred in CreateSession RPC:"
                     f" {status_debug_string}", exc_info=True)

        # TODO(yuanjing_octoml): handle more status code types
        status_code = rpc_error.code()
        status_details = rpc_error.details()
        if status_code == grpc.StatusCode.UNAVAILABLE:
            status_details = "Connection can't be established between client and server. " \
                             "This could be caused by incorrect ip addresses or port " \
                             "numbers"
        elif status_code == grpc.StatusCode.INTERNAL:
            status_details = "An internal error ocurred, typically due to starting " \
                             "the remote session with wrong configuration(s)"

        # use from None to suppress stack trace from rpc_error
        raise CreateSessionError(f"Error {status_code.name}:"
                                 f" {status_details}. See full client-side"
                                 f" trace at {LOGFILE}") from None


class RemoteInferenceSession(InferenceSession):
    def __init__(self,
                 backends: Optional[BackendSpecType] = None,
                 server_addr: Optional[str] = None,
                 insecure: Optional[bool] = None,
                 access_token: Optional[str] = None):
        super().__init__()

        backends = _get_backend_specs(backends)

        self._supported_backends = None
        self._session_uuid = None
        self._heartbeat_thread = None
        self._heartbeat_quit_event = threading.Event()
        self._logger = get_file_logger(__name__)
        self._last_component_id_by_model_id = defaultdict(int)
        self._client = None

        with ExitStack() as guard:
            self._client = _Client.create(server_addr=server_addr, insecure=insecure,
                                          access_token=access_token)
            guard.callback(self._client.close)
            guard.enter_context(_handle_session_create_error(self._logger,
                                                             self._client._access_token_source))

            self._backends = _get_backends(backends, self._client)
            request = pb.CreateSessionRequest(backends=[_backend_spec_to_proto(b)
                                                        for b in self._backends])
            reply = self._client.create_session(request)

            self._session_uuid = UUID(bytes=reply.session_uuid)
            self._logger.info(f"Created session with uuid {self._session_uuid}")

            # If we get a KeyboardInterrupt or another exception before returning from __init__,
            # we want to attempt to send a CloseSession() request if possible.
            # This is most likely to happen when the user gives up on waiting for the session
            # to start and hits Ctrl-C.
            guard.callback(self._send_close_session_message_silently)

            if not reply.ready:
                self._client.wait_until_session_ready(self._session_uuid)
            guard.pop_all()

        self._heartbeat_thread = threading.Thread(
            target=_heartbeat_thread,
            kwargs=dict(
                stub=self._client.stub,
                session_uuid=self._session_uuid,
                quit_event=self._heartbeat_quit_event,
                logger=self._logger,
            ),
            daemon=True
        )
        self._heartbeat_thread.start()
        _register_session(self)

    def __del__(self):
        _unregister_session(self)
        self.close()

    def _send_close_session_message_silently(self):
        try:
            self._client.stub.CloseSession(
                pb.CloseSessionRequest(session_uuid=self._session_uuid.bytes),
                timeout=1.0
            )
        except grpc.RpcError:
            # We've done our part. In the worst case, the session
            # will time out on the server.
            pass

    @property
    def backends(self) -> Sequence[BackendSpec]:
        return tuple(self._backends)

    def _get_supported_backends(self) -> pb.ListSupportedBackendsReply:
        if self._supported_backends is None:
            reply = self._client.stub.ListSupportedBackends(pb.ListSupportedBackendsRequest())
            self._supported_backends = reply
        return self._supported_backends

    def close(self):
        if self._heartbeat_thread is not None:
            self._heartbeat_quit_event.set()
            self._heartbeat_thread = None

        if self._client is not None and not self._client.is_closed():
            if self._session_uuid is not None:
                self._send_close_session_message_silently()
                self._session_uuid = None
            self._client.close()

    def load_model(self,
                   model_id: int,
                   backend_ids: Sequence[int],
                   model_format: pb.ModelFormat,
                   model_files: Sequence[FileDescription],
                   input_names: Sequence[str],
                   output_names: Sequence[str]):
        backend_skip_mask = self._make_backend_skip_mask(backend_ids)
        base_component_id = self._last_component_id_by_model_id[model_id] + 1

        for model_component_id, file_desc in enumerate(model_files, base_component_id):
            sha256 = file_desc.sha256()
            req = pb.LoadCachedModelComponentRequest(session_uuid=self._session_uuid.bytes,
                                                     model_id=model_id,
                                                     model_component_id=model_component_id,
                                                     sha256_hash=sha256,
                                                     filename=file_desc.name(),
                                                     backends_to_skip_bitmask=backend_skip_mask)

            try:
                reply = self._client.stub.LoadCachedModelComponent(req)
                print(f"\tLoaded [item {model_component_id} of graph {model_id}] from cache",
                      file=sys.stderr)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    request_iter = _request_stream_from_file(
                        file_desc, self._session_uuid, model_id,
                        model_component_id, backend_skip_mask)
                    reply = self._client.stub.LoadModelComponent(request_iter)
                else:
                    raise LoadModelError("Error in load cached component: "
                                         "graph {}, component {}, {}"
                                         .format(model_id, model_component_id, str(e)))

            all_errors, error_messages = self._load_error_info(model_id,
                                                               model_component_id,
                                                               self._backends,
                                                               reply.result_per_backend)

            if all_errors:
                raise LoadModelError("Error in load component: "
                                     "graph {}, component {}, {}"
                                     .format(model_id, model_component_id,
                                             str(error_messages)))

            self._last_component_id_by_model_id[model_id] = model_component_id

        req = pb.LoadModelRequest(session_uuid=self._session_uuid.bytes,
                                  model_id=model_id,
                                  model_format=model_format,
                                  input_names=input_names,
                                  output_names=output_names,
                                  backends_to_skip_bitmask=backend_skip_mask)
        reply = self._client.stub.LoadModel(req)

        all_errors, error_messages = self._load_error_info(model_id,
                                                           None,  # component id
                                                           self._backends,
                                                           reply.result_per_backend)

        if all_errors:
            raise LoadModelError(f"Error in load graph: graph {model_id}, {str(error_messages)}")

    def create_runner(self, model_id: int,
                      input_map_per_backend: Sequence[Sequence[int]]) -> ModelRunner:
        assert len(input_map_per_backend) == len(self._backends)
        input_map_proto = tuple(pb.InputMap(input_value_indices=indices)
                                for indices in input_map_per_backend)
        return RemoteModelRunner(self, model_id, input_map_proto)

    def _make_backend_skip_mask(self, selected_backends: Iterable[int]) -> bytes:
        mask = (1 << len(self._backends)) - 1
        for idx in selected_backends:
            mask &= ~(1 << idx)
        return mask.to_bytes((len(self._backends) + 7) // 8, "little")

    def _load_error_info(
        self,
        model_id: int,
        model_component_id: Optional[int],
        backends: Sequence[BackendSpec],
        result_per_backend: Union[Sequence[pb.LoadModelComponentResult],
                                  Sequence[pb.LoadModelResult]]) \
            -> Tuple[bool, Sequence[str]]:
        all_errors = True
        error_messages = []
        for backend, result in zip(backends, result_per_backend):
            if result.HasField("error_value"):
                if model_component_id is None:
                    self._logger.error("Error in load graph %d on backend %s: %s",
                                       model_id, str(backend), result.error_value.message)
                else:
                    self._logger.error("Error in load graph %d "
                                       "component %d on "
                                       "backend %s: %s",
                                       model_id, model_component_id,
                                       str(backend), result.error_value.message)
                error_messages.append(result.error_value.message)
            else:
                all_errors = False
        return all_errors, error_messages


def human_readable_size(size_in_bytes: int) -> str:
    units = ['B', 'KB', 'MB', 'GB']
    unit, value = 'B', float(size_in_bytes)
    for unit in units:
        if round(value, 1) < 1024:
            break
        value = value / 1024
    return f"{round(value, 1)} {unit}"


def _request_stream_from_file(file: FileDescription,
                              session_uuid: UUID,
                              model_id: int,
                              model_component_id: int,
                              backend_skip_mask: bytes) -> Iterator[pb.LoadModelComponentRequest]:
    try:
        req = pb.LoadModelComponentRequest(session_uuid=session_uuid.bytes,
                                           model_id=model_id,
                                           model_component_id=model_component_id,
                                           filename=file.name(),
                                           backends_to_skip_bitmask=backend_skip_mask)
        try:
            interactive_progress = hasattr(sys.stderr, "fileno") and os.isatty(sys.stderr.fileno())
        except io.UnsupportedOperation:
            # Disable interactive progress for Jupyter with ipykernel
            interactive_progress = False
        MAX_CHUNK_LEN = 1024 * 1024
        num_chunks = 0
        bytes_sent = 0

        with file.open(MAX_CHUNK_LEN) as (total_size, chunks):
            upload_message = f"\tUploading {human_readable_size(total_size)}" \
                             f" [item {model_component_id} of graph {model_id}]"
            if not interactive_progress:
                print(f"\t{upload_message}...", file=sys.stderr)
            for chunk in chunks:
                req.chunk = chunk
                yield req
                bytes_sent += len(chunk)
                percent_done = int(100 * bytes_sent / total_size)
                if interactive_progress:
                    print(f"\t{upload_message}... {percent_done}%\r", flush=True,
                          end='', file=sys.stderr)
                req = pb.LoadModelComponentRequest()
                num_chunks += 1

            if num_chunks == 0:
                yield req

            if total_size != bytes_sent:
                raise RuntimeError(f"File size mismatch: originally determined as"
                                   f" {total_size} bytes but only read {bytes_sent} bytes")

        if interactive_progress:
            print(f"{upload_message}... 100%", file=sys.stderr)
    except Exception:
        # GRPC hides exceptions that are raised in the request iterator, so we print it here
        traceback.print_exc()
        raise


def get_supported_backends(server_addr: Optional[str] = None,
                           insecure: Optional[bool] = None,
                           access_token: Optional[str] = None) -> Sequence[BackendSpec]:
    client = _Client.create(server_addr=server_addr, insecure=insecure, access_token=access_token)
    try:
        return client.get_supported_backends()
    finally:
        client.close()


def get_default_backends(server_addr: Optional[str] = None,
                         insecure: Optional[bool] = None,
                         access_token: Optional[str] = None) -> Sequence[BackendSpec]:
    client = _Client.create(server_addr=server_addr, insecure=insecure, access_token=access_token)
    try:
        return client.get_default_backends()
    finally:
        client.close()

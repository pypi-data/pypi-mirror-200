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

import torch
import contextlib


def _in_torch_dynamo():
    # TODO: find a better way to determine whether we are inside dynamo
    return torch._guards.TracingContext.get() is not None


@contextlib.contextmanager
def _onnx_export_diagnostic_patch():
    # Hack to disable onnx export diagnostic from printing
    # Headers even when there is no diagnostic
    # Because this relies on private APIs, there are try/except
    # to make sure failure doesn't impact the user experience
    try:
        from torch.onnx._internal.diagnostics.infra import DiagnosticContext
    except ImportError:
        return

    try:
        original_pretty_print = DiagnosticContext.pretty_print
    except AttributeError:
        return

    def pretty_print_only_when_not_empty(self, *args, **kwargs):
        try:
            if len(self.diagnostics) > 0:
                original_pretty_print(self, *args, **kwargs)
        except Exception:
            pass

    DiagnosticContext.pretty_print = pretty_print_only_when_not_empty
    yield
    DiagnosticContext.pretty_print = original_pretty_print

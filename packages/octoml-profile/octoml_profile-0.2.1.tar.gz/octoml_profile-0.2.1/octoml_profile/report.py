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

import functools
import sys
from dataclasses import dataclass
from typing import Dict, Sequence, OrderedDict, Optional, List

from .log_util import LOGFILE
from .pricing import AWS_ON_DEMAND_PER_HOUR


__all__ = ['PerBackendResult', 'Segment', 'TotalPerBackendResult', 'Profile', 'ProfileReport']

# The maximum number of displayed compiled segments in the summary. When this
# threshold is crossed, an abridged summary is displayed.
MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT = 3


@dataclass
class PerBackendResult:
    mean_ms: Optional[float]
    num_samples: int
    num_failures: int

    def total_ms(self):
        return self.mean_ms * self.num_samples


_instance_type_to_processor = {
    'r6i': 'Intel Ice Lake',
    'r7g': 'AWS Graviton3',
    'g4dn': 'Nvidia T4',
    'g5': 'Nvidia A10g',
}


def _get_backend_processor(backend):
    instance_type = backend.split('/')[0].split('.')[0]
    return _instance_type_to_processor[instance_type]


@dataclass
class Segment:
    graph_id: Optional[int]  # None if segment is uncompiled
    results_per_backend: OrderedDict[str, PerBackendResult]

    def add(self, segment: 'Segment'):
        # We only ever aggregate compiled segments when we have
        # more compiled segments than MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT.
        for backend, update in segment.results_per_backend.items():
            total = self.results_per_backend[backend]
            total_samples = total.num_samples + update.num_samples

            if total.mean_ms and update.mean_ms:
                total.mean_ms = (total.total_ms() + update.total_ms()) / total_samples
            elif total.mean_ms is None:
                total.mean_ms = update.mean_ms

            total.num_samples = total_samples
            total.num_failures += update.num_failures

    def total_ms(self):
        # NOTE: this function should only be used for sorting. It aggregates
        # total runtimes across all backends.
        runtimes = [v.total_ms() for v in self.results_per_backend.values() if v.mean_ms]
        return functools.reduce(lambda x, y: x + y, runtimes, 0.0)


@dataclass
class PerBackendError:
    graph_id: int
    error_messages_to_count: Dict[str, int]


@dataclass
class TotalPerBackendResult:
    estimated_total_ms: Optional[float]
    errors: List[PerBackendError]


@dataclass
class Profile:
    segments: Sequence[Segment]
    total_uncompiled_ms: float
    total_per_backend: OrderedDict[str, TotalPerBackendResult]
    compilation_occurred: bool
    num_runs: int
    num_repeats: int

    def _should_abridge(self, verbose):
        return not verbose and \
               len(self._compiled_segments()) > MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT

    def _compiled_segments(self):
        return [s for s in self.segments if s.graph_id is not None]

    def print(self, *, file=sys.stdout, verbose=False):
        abridge = self._should_abridge(verbose)
        if abridge:
            self._print_abridged_segments(file)
        else:
            self._print_segments(file)
        self._print_totals(file, abridge=abridge)
        self._print_errors(file)

    def _add_compiled_abridged_row(self, table, subgraph, num_subgraphs_aggregated=0):
        # Take the first backend's number of samples as the number of
        # samples for the whole graph. Assumes each backend has the same
        # number of samples.
        result = list(subgraph.results_per_backend.values())[0]
        num_samples = result.num_samples + result.num_failures
        if num_subgraphs_aggregated:
            table.append((f"{num_subgraphs_aggregated} other subgraphs",))
        else:
            num_calls = num_samples // self.num_repeats
            table.append((f"Graph #{subgraph.graph_id} ({num_calls} calls)",))
        num_repeats = self.num_repeats
        num_runs = self.num_runs

        for backend, result in subgraph.results_per_backend.items():
            total = self.total_per_backend[backend].estimated_total_ms
            if self.compilation_occurred:
                if result.mean_ms is None:
                    mean_ms = "N/A"
                    per_run_mean_ms = "N/A"
                else:
                    mean_ms = f"{result.mean_ms:.3f}"
                    per_run_mean_ms = result.mean_ms * (num_samples / num_repeats)
                    per_run_mean_ms = f"{per_run_mean_ms:.3f}"
                table.append(("  " + backend, mean_ms, per_run_mean_ms, result.num_failures))
            else:
                if result.mean_ms is None:
                    mean_ms, per_run_mean_ms, percent_of_run = ("N/A", "N/A", "N/A")
                elif total is None:
                    mean_ms = f"{result.mean_ms:.3f}"
                    per_run_mean_ms, percent_of_run = ("N/A", "N/A")
                else:
                    mean_ms = result.mean_ms
                    per_run_mean_ms = mean_ms * (num_samples / num_runs / num_repeats)
                    percent_of_run = 100 * per_run_mean_ms / total
                    mean_ms = f"{mean_ms:.3f}"
                    per_run_mean_ms = f"{per_run_mean_ms:.3f}"
                    percent_of_run = f"{percent_of_run:.1f}"
                if num_subgraphs_aggregated:
                    mean_ms = ""
                table.append(("  " + backend,
                              mean_ms, per_run_mean_ms, percent_of_run, result.num_failures))

    def _print_abridged_segments(self, file):
        if self.compilation_occurred:
            table = [
                ("Top subgraph", "Avg ms/call", "Avg ms/run", "Failures"),
                "="
            ]
        else:
            table = [
                ("Top subgraph", "Avg ms/call", "Avg ms/run", "Runtime % of e2e", "Failures"),
                "="
            ]
        graphs = {}
        for segment in self._compiled_segments():
            gid = segment.graph_id
            if gid not in graphs:
                graphs[gid] = segment
            else:
                graphs[gid].add(segment)

        graphs = sorted(graphs.values(), key=lambda x: x.total_ms(), reverse=True)

        # Add top n subgraphs rows
        n = MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT
        top_graphs = graphs[:n]
        for subgraph in top_graphs:
            self._add_compiled_abridged_row(table, subgraph)
            table.append('')

        # Add 'other subgraphs' row
        if len(graphs) > len(top_graphs):
            other_graphs_sum = graphs[n]
            for graph in graphs[n + 1:]:
                other_graphs_sum.add(graph)
            self._add_compiled_abridged_row(table, other_graphs_sum,
                                            num_subgraphs_aggregated=len(graphs) - len(top_graphs))
            table.append('')

        # Add 'uncompiled segments total' row
        if not self.compilation_occurred:
            num_uncompiled = len([s for s in self.segments if s.graph_id is None])
            num_segments = f'{num_uncompiled} uncompiled segments'
            sum_mean_ms = f'{self.total_uncompiled_ms:.3f}'
            table.append((num_segments, "", sum_mean_ms))
        table.append('-')

        if self.compilation_occurred:
            _print_table(table, "<>>>", file)
        else:
            _print_table(table, "<>>>>", file)

    def _print_segments(self, file):

        table = [
            ("", "Segment", "Samples", "Avg ms", "Failures"),
            "="
        ]
        for segment_idx, segment in enumerate(self.segments):
            if segment.graph_id is None:
                if self.compilation_occurred:
                    continue
                r = segment.results_per_backend["Uncompiled"]
                table.append((segment_idx, "Uncompiled", r.num_samples, f"{r.mean_ms:.3f}"))
            else:
                table.append('')
                table.append((segment_idx, f"Graph #{segment.graph_id}",))
                for backend, result in segment.results_per_backend.items():
                    mean_ms = "N/A" if result.mean_ms is None else f"{result.mean_ms:.3f}"
                    table.append(("", "  " + backend,
                                  result.num_samples, mean_ms, result.num_failures))
                table.append('')
        table.append('-')
        _print_table(table, "><>>>", file)

    def _print_totals(self, file, abridge):
        if self.compilation_occurred:
            print(f'Total times (compiled + uncompiled) is not available '
                  f'because compilation has occurred.', file=file)
            print(f'Please run the accelerated function multiple times in the `remote_profile` '
                  'context to get total times.', file=file)
        else:
            print(f'Total uncompiled code run time: {self.total_uncompiled_ms:.3f} ms', file=file)
            print(f'Total times (compiled + uncompiled) and on-demand cost per million '
                  f'inferences per backend:', file=file)
            table = []
            for backend, total_res in self.total_per_backend.items():
                if total_res.estimated_total_ms is None:
                    estimated_total_ms = "N/A"
                    estimated_cost = "N/A"
                else:
                    estimated_total_ms = f"{total_res.estimated_total_ms:.3f}ms"
                    per_hr = AWS_ON_DEMAND_PER_HOUR.get(backend.split('/')[0])
                    if per_hr is None:
                        estimated_cost = "N/A"
                    else:
                        cost_per_mreq = 1e6 * per_hr * total_res.estimated_total_ms / (3600 * 1000)
                        estimated_cost = f"${cost_per_mreq:.2f}"

                try:
                    processor = _get_backend_processor(backend)
                    backend_str = f"{backend} ({processor})"
                except KeyError:
                    backend_str = backend
                    print(f'WARNING: cannot find processor info for backend {backend}', file=file)
                table.append(("  ", backend_str, estimated_total_ms, estimated_cost))
            table.append('')
            _print_table(table, "<<>>", file)

        if abridge:
            print(file=file)
            print(f"More than {MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT} compiled segments "
                  "were run, so only graphs with the highest aggregate runtimes are shown. "
                  "To display a verbose profile see "
                  "https://github.com/octoml/octoml-profile#the-profile-report", file=file)
            print(file=file)

    def _print_errors(self, file):
        if any([total.errors for total in self.total_per_backend.values()]):
            print('Errors occurred running this model, per backend:', file=file)
            for backend, total_res in self.total_per_backend.items():
                if not total_res.errors:
                    continue
                print(f'    {backend}', file=file)
                for error in total_res.errors:
                    graph_str = f'       Graph #{error.graph_id} - '
                    print(graph_str, end='', file=file)
                    for i, (error, count) in enumerate(error.error_messages_to_count.items()):
                        if i > 0:
                            print('\n', ' ' * (len(graph_str) - 1), end='', file=file)
                        print(f'{count} errors: {error}', end='', file=file)
                    print(file=file)
            print(f'For full client-side error traces see {LOGFILE}', file=file)


@dataclass
class ProfileReport:
    profiles: List[Profile]
    num_discarded_runs: int
    compile_errors: List[str]

    def print(self, *, file=sys.stdout, verbose=False):
        if len(self.profiles) == 0:
            print('Profiling was enabled but no results were recorded', file=file)
        for i, profile in enumerate(self.profiles):
            num_runs = "1 time" if profile.num_runs == 1 else f'{profile.num_runs} times'
            print(f'Profile {i + 1}/{len(self.profiles)} ran {num_runs} '
                  f'with {profile.num_repeats} repeats per call:', file=file)
            profile.print(file=file, verbose=verbose)
        for e in self.compile_errors:
            print("WARNING: " + e, file=file)
        if len(self.compile_errors) > 0:
            print(f"See full client-side trace at {LOGFILE}")


def _string_width(s):
    # FIXME: use wcwidth if we need to display non-latin characters
    return len(str(s))


_align = {
    '<': lambda s, width: s + ' ' * max(0, width - _string_width(s)),
    '>': lambda s, width: ' ' * max(0, width - _string_width(s)) + s
}


def _print_table(rows, column_alignment: str, file):
    col_spacing = 2
    col_spacing_str = ' ' * col_spacing
    num_cols = len(column_alignment)
    column_alignment = tuple(_align[a] for a in column_alignment)

    col_width = [0] * num_cols
    for row in rows:
        if not isinstance(row, str):
            for i, cell in enumerate(row):
                col_width[i] = max(col_width[i], _string_width(cell))

    total_width = sum(col_width) + col_spacing * (num_cols - 1)
    for row in rows:
        if isinstance(row, str):
            num_reps = 1 if _string_width(row) == 0 else total_width // _string_width(row)
            print(row * num_reps, file=file)
        else:
            print(*(align(str(cell), width)
                    for cell, width, align in zip(row, col_width, column_alignment)),
                  file=file,
                  sep=col_spacing_str)

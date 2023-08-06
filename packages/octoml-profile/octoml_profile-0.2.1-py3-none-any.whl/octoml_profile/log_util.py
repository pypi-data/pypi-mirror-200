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
from datetime import datetime

LOGFILE = f'/tmp/octoml-profile-{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}.log'


def get_file_logger(name, filename=LOGFILE):
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
    # Manually configure logging instead of invoking logging.basicConfig
    # so that we avoid capturing non-dynamo logs
    log = logging.getLogger(name)
    log.handlers.clear()
    log.addHandler(fh)
    log.propagate = False
    log.setLevel(logging.DEBUG)
    return log

# Copyright 2020 Karlsruhe Institute of Technology
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
import warnings

from sqlalchemy.exc import RemovedIn20Warning

from .version import __version__


# This warning can happen when accessing the server the application runs on directly by
# IP address, but it should be safe to ignore, as ultimately the user should simply be
# redirected to the correct domain specified as the server name.
warnings.filterwarnings(
    "ignore",
    module="flask.app",
    category=UserWarning,
    message="Current server name '.*' doesn't match configured server name '.*'",
)

# Even though this warning only seems to trigger when testing, we ignore it here just in
# case. Since the used SQLAlchemy version is pinned, it should be safe to do so until
# the actual upgrade.
warnings.simplefilter("ignore", category=RemovedIn20Warning)

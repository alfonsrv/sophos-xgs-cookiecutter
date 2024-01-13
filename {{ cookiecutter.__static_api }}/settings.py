#  Copyright (c) 2022-2024 Rau Systemberatung GmbH. All rights reserved.
#
#  Licensed under the GNU General Public License, Version 3 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at:
#    https://www.gnu.org/licenses/gpl-3.0.html
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.
#
#  Selling exceptions may apply as per written contractual agreements between
#  commercial entities and Rau Systemberatung GmbH, releasing the former from
#  the License obligations.

VERSION = '20.0a'

XGS_IP_ADDRESS = '{{ cookiecutter.xgs_tanker_ip }}'
XGS_PORT = '{{ cookiecutter.__xgs_tanker_port }}'
XGS_USER = '{{ cookiecutter.xgs_tanker_user }}'
XGS_PASS = '{{ cookiecutter.xgs_tanker_pass }}'

DEFINITIONS_PATH = 'definitions'

import os
import logging
import logging.handlers

try:
    from rich.logging import RichHandler
    stream_handler = RichHandler(rich_tracebacks=True)
    stream_handler.setFormatter(
        fmt=logging.Formatter(
            '%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
except (ModuleNotFoundError, ImportError):
    stream_handler = logging.StreamHandler()


LOG_LEVEL = logging.INFO  # logging.DEBUG // .ERROR...
LOG_FILE = 'xgs-tanker.log'
LOG_PATH = os.path.join(os.getcwd(), LOG_FILE)
logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] %(message)s',
    level=LOG_LEVEL,
    handlers=[
        stream_handler,
        logging.handlers.RotatingFileHandler(
            LOG_PATH,
            maxBytes=5000000,   # 5 MB
            backupCount=5
        )
    ]
)

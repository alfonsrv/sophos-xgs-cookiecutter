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

import os
import logging
from time import sleep

from rich.console import Console
from rich.live import Live
from rich import box

import settings
from nsg.manager import RichTable, _process_results
from nsg.api import SophosAPI


logger = logging.getLogger(__name__)


def has_content(path: str) -> bool:
    with open(path, 'r') as f:
        content = f.read().strip()
    return bool(content)


def process_definitions(*, api: SophosAPI):
    """ Processes the XGS XML definition files previously defined by the Cookiecutter process """
    table = RichTable(
        "Action",  "Information",
        min_width=120,
        box=box.SIMPLE_HEAVY
    )
    with Live(table, auto_refresh=True, refresh_per_second=5) as live:
        logger.info('Checking connectivity + authentication to XGS Firewall via REST API')
        table.add_row('Preflight checks', 'Authenticating...')  # Connectivity + authentication
        response = api.preflight()
        if not response.is_authenticated or response.is_timeout:
            logger.error(response)
            status = 'Authentication Error' if not response.is_authenticated else 'Timed out'
            table.finalize_row(status=False, result=status)
            return
        logger.info(f'Connectivity ok! API version is: {response.api_version}')
        table.finalize_row(status=True, result='Connectivity & Auth OK')

        # Generalize Wireless + Firewall rules
        logger.info('Generalizing Wireless Protection configuration (removing networks + disabling)')
        table.add_row('Wireless Protection', 'Generalizing...')
        wifi_result = api.generalize_wireless()
        _process_results(table=table, results=wifi_result)

        logger.info('Generalizing Firewall Policies (removing default rules)')
        table.add_row('Firewall Policies', 'Generalizing...')
        firewall_results = api.generalize_firewall()
        _process_results(table=table, results=firewall_results)

        # Process API request files
        files = [
            file for file in sorted(os.listdir(settings.DEFINITIONS_PATH))
            if file.endswith('.xml') and not file.startswith('.')
        ]
        for i, file in enumerate(files):
            path = os.path.join(os.getcwd(), settings.DEFINITIONS_PATH, file)
            if not has_content(path): continue
            logger.info(f'[{i+1}/{len(files)}] Processing {file}')
            table.add_row(f'🛳 "{file}"', '')

            response = api.process_file(file_path=path)
            _process_results(table=table, results=response)
            live.refresh()


if __name__ == '__main__':
    print(r"""
        ____  ___________  _________
        \   \/  /  _____/ /   _____/
         \     /   \  ___ \_____  \ 
         /     \    \_\  \/        \
        /___/\  \______  /_______  /
              \_/      \/        \/ 
          Tanker Script by RAUSYS
               www.rausys.de

    """)
    logger.info(f'Starting up XGS Tanker Script (IP addr {settings.XGS_IP_ADDRESS}:{settings.XGS_PORT})')
    api = SophosAPI(
        ip_address=settings.XGS_IP_ADDRESS,
        port=settings.XGS_PORT,
        username=settings.XGS_USER,
        password=settings.XGS_PASS
    )
    process_definitions(api=api)

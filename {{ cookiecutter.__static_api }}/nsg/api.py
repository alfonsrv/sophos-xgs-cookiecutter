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

import re
from time import sleep

import urllib3
import logging

import requests

from .response import ApiResponse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class SophosAPI:
    # API-Referenz: https://docs.sophos.com/nsg/sophos-firewall/18.0/API/index.html
    ip_address: str
    port: str = 4444
    username: str
    password: str

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def api_url(self):
        return f'https://{self.ip_address}:{self.port}/webconsole/APIController'

    def _xml_wrap(self, xml: str) -> str:
        return f'<Request>\n' \
         '  <Login>\n' \
        f'    <Username>{self.username}</Username>\n' \
        f'    <Password>{self.password}</Password>\n' \
         '  </Login>\n' \
        f'{xml}\n' \
        '</Request>'

    def execute(self, xml: str, retry: bool = False) -> ApiResponse:
        _xml = self._xml_wrap(xml)
        # Normalize line breaks aka remove too many unnecessary linebreaks
        _xml = re.sub(r'((?:\s)?\n){2,}', '\n', _xml)
        data = {
            'reqxml': _xml
        }
        logger.debug('--- REQUEST ---')
        logger.debug(_xml.replace(f'<Password>{self.password}</Password>', '<Password>********</Password>'))
        try:
            response = requests.post(
                self.api_url,
                headers={'User-Agent': 'RAUSYS XGS Tanker - www.rausys.de'},
                data=data,
                verify=False,
                timeout=420
            )
            logger.debug(f'--- RESPONSE [{response.status_code}] ---')
            logger.debug(str(response.text))
            return ApiResponse(response=response.text, status_code=response.status_code)
        except requests.exceptions.Timeout:
            logger.error('Sophos XGS connection timed out (420s); could not reach firewall or finalize the current request')
            return ApiResponse(is_timeout=True)
        except requests.exceptions.ConnectionError:
            if retry: raise
            logger.info('Sophos XGS closed connection unexpectedly; sleeping for a bit before retrying, in case firewall crashed...')
            sleep(240)
            return self.execute(xml=xml, retry=True)

    def preflight(self):
        return self.execute(xml='')

    def process_file(self, file_path: str) -> ApiResponse:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        payload = f'<Set>\n{content}\n</Set>'
        return self.execute(xml=payload)

    def generalize_wireless(self):
        """ Helper function to remove existing wireless networks + turn wireless protection off
        WirelessProtection must be enabled in order to delete wireless networks """
        payload = '<Get>\n<WirelessNetworkStatus>\n</WirelessNetworkStatus>\n</Get>'
        response = self.execute(xml=payload)
        if not response.is_ok: return response
        networks = [r.find('Name').text for r in response.responses if r.find('Name') is not None]
        for network in networks:
            payload =  f'<Remove>\n<WirelessNetworks transactionid="remove-ap-{network}">\n' \
                       f'<Name>{network}</Name>\n' \
                        '</WirelessNetworks>\n</Remove>'
            response = self.execute(xml=payload)
            if not response: return response

        payload = '<Set>\n<WirelessProtectionGlobalSettings>\n' \
                  '<EnableWirelessProtection>Disable</EnableWirelessProtection>\n' \
                  '<AllowedZone>\n</AllowedZone>\n' \
                  '<RADIUSServer>None</RADIUSServer>\n' \
                  '</WirelessProtectionGlobalSettings>\n</Set>'
        return self.execute(xml=payload)

    def generalize_firewall(self):
        """ Helper function to remove existing firewall policies """
        payload = '<Get>\n<FirewallRule>\n</FirewallRule>\n</Get>'
        response = self.execute(xml=payload)
        if not response.is_ok: return response
        rule_names = [r.find('Name').text for r in response.responses if r.find('Name') is not None]
        response = None
        for rule_name in rule_names:
            payload =  f'<Remove>\n<FirewallRule transactionid="remove-firewall-{rule_name}">\n' \
                       f'<Name>{rule_name}</Name>\n' \
                        '</FirewallRule>\n</Remove>'
            response = self.execute(xml=payload)
            if not response: return response
        return response

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

from collections import namedtuple
from typing import Optional, Iterable
import xml.etree.ElementTree as ET

ApiResponseStatus = namedtuple(
    'ApiResponseStatus',
    'tag transaction_id status_code status_message is_error original'
)


class ApiResponse:
    """ Simple abstraction to keep track of Sophos return information; basically a glorified dictionary.
    Keeps track of whether authentication was successful or not, if the request timed out and which actions
    succeeded. Parses XML in time to evaluate the returned XML status information """
    response: Optional[str]
    status_code: Optional[int] = None
    _response: Optional['ET'] = None
    is_timeout: bool = False

    def __init__(self, response: Optional[str] = None, status_code: Optional[int] = None, is_timeout: bool = False):
        self.response = response
        if self.response and self.response.strip():
            self._response = ET.fromstring(self.response.strip())
        self.status_code = status_code
        self.is_timeout = is_timeout

    def __str__(self):
        return self.response

    def __repr__(self):
        return self.status_code, self.response

    def __bool__(self):
         return self.is_ok and \
            not any(responses_status for responses_status in self.responses_statuses if responses_status.is_error)

    @property
    def is_ok(self) -> bool:
        return self.is_authenticated and \
            not self.is_timeout and \
            self.response

    @property
    def is_authenticated(self) -> bool:
        if not self.response: return False
        try:
            return self._response.findall('.//Login//status')[0].text.title() == 'Authentication Successful'
        except (IndexError, AttributeError):
            return False

    @property
    def api_version(self) -> str:
        if not self.response: return ''
        return self._response.attrib.get('APIVersion')

    @property
    def responses(self) -> Iterable['ET.Element']:
        if not self.response: return []
        for element in self._response.findall(".//*[@transactionid]"):
            yield element

    @property
    def responses_statuses(self) -> Iterable[ApiResponseStatus]:
        for response in self.responses:
            _status_element = response.find('Status')
            status = _status_element.text.strip()
            status_code = _status_element.attrib.get('code')
            yield ApiResponseStatus(
                tag=response.tag,
                transaction_id=response.attrib['transactionid'],
                status_code=status_code,
                status_message=status,
                is_error=str(status_code) not in ['200', '201'],
                original=ET.tostring(response, encoding='utf8', method='xml')
            )


# Allow some transactions to return a error code?
#   certificate-appliance     504 ==> OK (cert exists)
#   admin-settings-webadmin   544 ==> OK (nothing changed?)


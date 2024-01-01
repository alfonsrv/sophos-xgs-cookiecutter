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
import logging
from typing import List, Any, Optional, TYPE_CHECKING, Union, Iterable

from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderableType
    from .response import ApiResponse

logger = logging.getLogger(__name__)


class RichTable:
    """ rich table proxy that allows adding + removing rows dynamically by
    recreating and then re-rendering the table as required, in order to show
    the currently executed action + status in a central tracking table """

    columns: List[str]  # column headers
    rows: List[List[Union[str, Spinner, Text]]]  # rows of columns
    status: List[Optional[bool]]  # correlating status for each column
    style: Optional[dict]  # style definition for the status equals to style in dict
    table_kwargs: Optional[dict]
    table: Table

    def __init__(self, *args, style: Optional[dict] = None, **table_kwargs) -> None:
        args = list(args)
        if args[0] == 'Status': args.pop(0)

        self.columns = ["Status"] + args
        self.rows = []
        self.status = []

        # key equals the value expected in status; if matched, the
        #   correlating rich style will be applied
        self.style = style or {
            None: "bright_blue",
            True: "bright_green",
            False: "bold red"
        }
        self.table_kwargs = table_kwargs or {
            'show_header': True,
            'show_lines': False,
            'show_edge': False,
            'box': None
        }
        self.table = None

    def __len__(self):
        return len(self.rows)

    def build_table(self) -> None:
        """ Internal method: Constructs the table, so we don't do it every refresh. """
        self.table = Table(
            **self.table_kwargs
        )
        for i, column in enumerate(self.columns):
            # Set first "Status" column to minimum width of 6
            self.table.add_column(column, max_width=None if i else 6, width=None if i else 6)

        styles = self.style
        for (row, status) in zip(self.rows, self.status):
            self.table.add_row(
                *row,
                style=styles[status]
            )

    def add_row(self, *props: str) -> None:
        """ Begins a new row in the checklist. """
        self.rows.append(
            [Spinner("dots")] + list(Text(p) for p in props)
        )
        self.status.append(None)
        self.build_table()

    def finalize_row(self, status: bool, result: str) -> None:
        """ Updates the last entry in the list with an ok/nok state and
        replaces the spinner with result text. """
        self.rows[-1][0] = "✓" if status else "✗"
        self.rows[-1][-1] = Text(result)
        self.status[-1] = status
        self.build_table()

    def remove_row(self, index: int) -> Any:
        try:
            self.status.pop(index)
            return self.rows.pop(index)
        except Exception:
            return None

    def __rich_console__(self, console: 'Console', options: 'ConsoleOptions') -> 'RenderableType':
        if self.table:
            yield self.table


def _process_results(table: RichTable, results: 'ApiResponse') -> RichTable:
    _addon = '(Unknown)' if results is None else '| OK' if bool(results) else ' | ERROR'
    table.finalize_row(status=bool(results), result=f'Finalized {_addon}')
    if results is None: return table
    for result_status in results.responses_statuses:
        if not result_status.is_error:
            if result_status.transaction_id:
                logger.info(f'Configuration applied successfully: "{result_status.transaction_id}" [{result_status.status_code}]')
            continue
        logger.error(f'ERROR applying "{result_status.transaction_id}": {result_status.original}')
        table.add_row(f'↳ Transaction "{result_status.transaction_id}"', '')
        table.finalize_row(
            status=False,
            result=f'{result_status.status_code} {result_status.status_message}'
        )
    return table

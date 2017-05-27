# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
from aiohttp import web
from http import HTTPStatus

__all__ = ('Response', )


class Response(web.Response):
    def __init__(self, status=HTTPStatus.OK, result=None, description=None, *args, **kwargs):
        ok = status == HTTPStatus.OK
        response_dict = {
            'ok': ok,
            }
        if ok:
            response_dict['result'] = result
        else:
            response_dict['error_code'] = status

        if description is not None:
            response_dict['description'] = description

        headers = {
            'Content-Type': 'application/json',
            'Server': 'telegram-bot-server',
            }
        super(Response, self).__init__(
            headers=headers,
            status=status,
            text=json.dumps(response_dict),
            )

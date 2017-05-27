# telegram-echo-bot
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiohttp
import asyncio
import json
import logging
import traceback
from .error import ApiError
from aiohttp import web
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
from http import HTTPStatus

LOGGER = logging.getLogger('telegram_echo_bot.bot')


class Bot:
    def __init__(self, configuration):
        self._configuration = configuration

    async def _get_updates(self, offset=None, timeout=20):
        """
        Raises:
            telegram_echo_bot.ApiError

        """
        LOGGER.debug('Getting updates.')
        data = {
            'timeout': timeout,
            }
        if offset is not None:
            data['offset'] = offset
        updates = await self._request(
            'getUpdates',
            data,
            timeout=timeout + 1,
            )
        return updates

    async def _handle(self, update):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        await self.send_message(update['message']['chat']['id'], update['message']['text'])
        return web.Response()

    async def _request(self, method, data={}, timeout=None):
        """
        Raises:
            telegram_echo_bot.ApiError

        Returns:
            dict or list: response result.

        """
        url = f'{self._configuration.api_host}bot{self._configuration.token}/{method}'
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url,
                    data=json.dumps(data),
                    headers={
                        'Content-Type': 'application/json',
                        },
                    ) as response:
                response_text = await response.text()
                if response.status != HTTPStatus.OK:
                    reason = f'Not OK response status code: {response.status}. {response_text}'
                    LOGGER.warning(reason)
                    raise ApiError(reason)
                response_json = json.loads(response_text)
                if not response_json['ok']:
                    reason = f'Not OK response: {response_text}'
                    LOGGER.warning(reason)
                    raise ApiError(reason)
                return response_json['result']

    async def _wait_for_updates(self):
        last_update_id = None
        while True:
            try:
                updates = await self._get_updates(
                    offset=None if last_update_id is None else last_update_id + 1,
                    )
                if updates is None or not len(updates):
                    continue
                for update in updates:
                    await self._handle(update)
                    last_update_id = update['update_id']
            except:
                traceback.print_exc()
            await asyncio.sleep(.1)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._wait_for_updates())

    async def send_message(self, id, text):
        """
        Raises:
            aiohttp.web.HTTPException
            telegram_echo_bot.ApiError

        """
        LOGGER.info('Sending message "%s" to %s.', text, id)
        return await self._request('sendMessage', {
            'chat_id': id,
            'text': text,
            })

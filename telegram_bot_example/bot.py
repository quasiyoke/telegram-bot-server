# telegram-bot-example
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiohttp
import asyncio
import json
import logging
from aiohttp import web
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
from http import HTTPStatus

LOGGER = logging.getLogger('telegram_bot_example.bot')


class Bot:
    def __init__(self, configuration):
        self._api_url = f'{configuration.api_host}bot{configuration.token}/sendMessage'
        self._configuration = configuration

    async def _handler(self, request):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        text = await request.text()
        data = json.loads(text)
        await self.send_message(data['message']['chat']['id'], text)
        return web.Response()

    def _get_app(self):
        app = web.Application()
        app.router.add_post('/', self._handler)
        return app

    def _run_app(self):
        app = self._get_app()
        web.run_app(
            app,
            host='0.0.0.0',
            port=self._configuration.port,
            )

    async def _send_time_continously(self):
        """Sends time to the specified Telegram user periodically.

        """
        while True:
            try:
                await self.send_message(
                    self._configuration.receiver_id,
                    str(datetime.utcnow()),
                    )
            except ClientConnectorError as err:
                LOGGER.error('Can\'t send the message. %s', err)
            await asyncio.sleep(self._configuration.period)

    def run(self):
        asyncio.ensure_future(self._send_time_continously())
        self._run_app()

    async def send_message(self, id, text):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        LOGGER.info('Sending message "%s" to %s.', text, id)
        message = {
            'chat_id': id,
            'text': text,
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self._api_url,
                    data=json.dumps(message),
                    headers={
                        'Content-Type': 'application/json',
                        },
                    ) as response:
                if response.status != HTTPStatus.OK:
                    LOGGER.warning('Not OK response status code: %s', response.status)
                LOGGER.debug('Response text is: "%s"', await response.text())

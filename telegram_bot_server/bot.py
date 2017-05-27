# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiohttp
import json
import logging
import re
from .error import BotError
from .update import MessageData
from aiohttp.client_exceptions import ClientConnectorError
from http import HTTPStatus

__all__ = ('Bot', 'parse_token', )
LOGGER = logging.getLogger('telegram_bot_server.bot')
TOKEN_RE = r'(?P<bot_id>[1-9]\d{0,15}):(?P<secret>[\w\-]{10,60})'


class Bot:
    @classmethod
    def create_by_token(cls, token, first_name, update_service, *args, **kwargs):
        """
        Args:
            token (str): Telegram bot token like that: "123456789:AAEfqU70n2V6dUK8u4n0u7N581JqPU06766".

        Returns:
            Bot instance or `None`.

        """
        bot_id, secret = parse_token(token)

        if bot_id is None or not first_name:
            return None

        return cls(bot_id, first_name, secret, update_service, *args, **kwargs)

    def __init__(self, bot_id, first_name, secret, update_service):
        """
        Args:
            bot_id (int): Positive Telegram bot ID.
            first_name (str): Bot's first name.
            secret (str): Telegram bot's token secret like that: "AAEfqU70n2V6dUK8u4n0u7N581JqPU06766".
            update_service (telegram_bot_server.UpdateService)

        """
        self.bot_id = bot_id
        self.first_name = first_name
        self.secret = secret
        self._update_service = update_service
        self.webhook = None

    @property
    def chat_dict(self):
        chat_dict = {
            'type': 'private',
            }
        chat_dict.update(self.user_dict)
        return chat_dict

    async def delete_webhook(self):
        """
        Returns:
            True if webhook was really deleted. False if it was already deleted before.

        """
        return await self.set_webhook(None)

    async def on_message(self, update):
        """A place to insert custom message handler.

        """
        pass

    async def push_update(self, update):
        """
        Raises:
            telegram_bot_server.BotError

        """
        if self._webhook is not None:
            data = update.dict
            LOGGER.debug('Pushing update %s %s to %s.', update, data, self.bot_id)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                            self._webhook,
                            data=json.dumps(data),
                            headers={
                                'Content-Type': 'application/json',
                                },
                            ) as response:
                        if response.status == HTTPStatus.OK:
                            await update.set_delivered(True)
                        else:
                            reason = f'Update {update} wasn\'t pushed to {self.bot_id}. Not OK response status code: ' \
                                f'{response.status}.'
                            raise BotError(reason)
                except ClientConnectorError as err:
                    raise BotError(f'Update {update} wasn\'t pushed to {self.bot_id}. {err}') from err

    async def push_updates(self, updates):
        """
        Raises:
            telegram_bot_server.BotError

        """
        for update in updates:
            await self.push_update(update)

    async def send_update(self, data):
        return await self._update_service.create_update(self.bot_id, data)

    async def send_message(self, chat, from_dict, text):
        """
        Args:
            chat (dict): Dict like this:
                {
                    'id': 1234,
                    'first_name': 'Anonymous',
                    'type': 'private',
                    }
            from_dict (dict): Dict like this:
                {
                    'id': 1234,
                    'first_name': 'Anonymous',
                    }
            text (str): Message's text.

        Raises:
            telegram_bot_server.UpdateError if the data is incorrect.

        """
        update = await self.send_update(MessageData(
            chat=chat,
            from_dict=from_dict,
            text=text,
            ))
        await self.on_message(update)
        return update

    async def set_webhook(self, url):
        """
        Args:
            url (str | None): New webhook.

        Returns:
            bool: True if a new webhook was set. False if webhook was already set.

        """
        previous_webhook = self.webhook
        self.webhook = url
        return previous_webhook != url

    @property
    def token(self):
        return f'{self.bot_id}:{self.secret}'

    @property
    def user_dict(self):
        """Obtains dict of `Telegram's "User" type <https://core.telegram.org/bots/api#user>`_.

        """
        return {
            'bot_id': self.bot_id,
            'first_name': self.first_name,
            }


def parse_token(token):
    """
    Args:
        token (str): Telegram bot token like that: "123456789:AAEfqU70n2V6dUK8u4n0u7N581JqPU06766".

    Returns:
        A tuple like that: (bot_id, secret). `bot_id` (int) is the bot id or `None` if the token is incorrect. `secret`
        is the token secret or `None` if the token is incorrect.

    """
    match = re.fullmatch(TOKEN_RE, token)

    if match is None:
        return None, None

    bot_id = int(match.group('bot_id'))

    return bot_id, match.group('secret')

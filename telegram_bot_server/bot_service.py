# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .bot import Bot, parse_token
from .error import BotServiceError
from functools import reduce
from hmac import compare_digest

__all__ = ('BotService', 'SimpleBotService', )
DUMB_TOKEN_SECRET = 'AAEfqU70n2V6dUK8u4n0u7N581JqPU06766'


class BotService:
    """Abstract bot service.

    """

    def __init__(self, update_service, bot_cls=Bot):
        """
        Args:
            bot_cls (type telegram_bot_server.Bot): Bot class.
            update_service (telegram_bot_server.UpdateService)

        """
        self._bot_cls = bot_cls
        self._update_service = update_service

    async def get_all_bots(self):
        raise NotImplementedError()

    async def get_bot(self, bot_id):
        """
        Args:
            bot_id (int): Bot's ID.

        Returns:
            Bot instance or `None`.

        """
        raise NotImplementedError()

    async def get_bot_by_token(self, token):
        """
        Args:
            token (str): Telegram bot token.

        Returns:
            Bot instance if successful, None otherwise.

        """
        bot_id, secret = parse_token(token)

        if bot_id is None:
            return None

        bot = await self.get_bot(bot_id)

        if bot is None:
            compare_digest(secret, DUMB_TOKEN_SECRET)
            return None
        elif not compare_digest(secret, bot.secret):
            return None

        return bot


class SimpleBotService(BotService):
    def __init__(self, bots, *args, **kwargs):
        """
        Args:
            bots (list): List of bots dicts.
            bot_cls (type telegram_bot_server.Bot): Bot class.
            update_service (telegram_bot_server.UpdateService)

        Raises:
            BotServiceError if provided list is wrong.

        """
        super(SimpleBotService, self).__init__(*args, **kwargs)
        self._bots = reduce(self._add_bot, bots, {})

    def _add_bot(self, bots, bot_dict):
        """
        Args:
            bots (dict): Dict mapping bots' IDs to the bots.
            bot_dict (dict): Dict describing single bot.

        Returns:
            The same instance of the `bots` dict mapping bots' IDs to the bots.

        Raises:
            BotServiceError if provided bot's dict is wrong or the bot isn't unique.

        """
        try:
            first_name = bot_dict['first_name']
            token = bot_dict['token']
        except (KeyError, TypeError) as err:
            raise BotServiceError('Provided bot\'s dict is invalid.') from err

        bot = self._bot_cls.create_by_token(
            token,
            first_name=first_name,
            update_service=self._update_service,
            )

        if bot is None:
            raise BotServiceError(f'Provided token "{token}" is invalid.')

        if bot.bot_id in bots:
            raise BotServiceError(f'Provided token "{token}" specifies already added bot.')

        bots[bot.bot_id] = bot

        return bots

    async def get_all_bots(self):
        return self._bots.values()

    async def get_bot(self, bot_id):
        """
        Args:
            bot_id (int): Bot's ID.

        Returns:
            Bot instance or `None`.

        """
        return self._bots.get(bot_id)

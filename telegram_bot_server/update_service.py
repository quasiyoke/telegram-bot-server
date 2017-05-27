# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
from .update import SimpleUpdate

__all__ = ('SimpleUpdateService', 'UpdateService', )


class UpdateService:
    """Abstract update service.

    """

    async def _on_update(self, bot_id):
        pass

    async def confirm_updates(self, offset):
        """Confirms updates with ID < offset.

        Args:
            offset (int or None): ID of the first not processed by the bot update. All preceding updates should
                be considered as confirmed.

        """
        raise NotImplementedError()

    async def create_update(self, bot_id, data):
        raise NotImplementedError()

    async def get_not_confirmed_updates(self, bot_id):
        """
        Args:
            bot_id (int)

        """
        raise NotImplementedError()

    def set_update_handler(self, on_update):
        self._on_update = on_update


class SimpleUpdateService(UpdateService):
    """Very simple update service storing all its data inside the dict.

    """

    def __init__(self, *args, **kwargs):
        self._updates = {}
        super(SimpleUpdateService, self).__init__(*args, **kwargs)

    def _get_bot_dict(self, bot_id):
        try:
            bot_dict = self._updates[bot_id]
        except KeyError:
            bot_dict = {
                'updates': [],
                }
            self._updates[bot_id] = bot_dict
        return bot_dict

    async def confirm_updates(self, bot_id, offset):
        """Confirms updates with ID < offset.

        Args:
            offset (int or None): ID of the first not processed by the bot update. All preceding updates should
                be considered as confirmed.

        """
        bot_dict = self._get_bot_dict(bot_id)
        updates = bot_dict['updates']
        i = 0
        while i < len(updates):
            update = updates[i]
            if update.update_id >= offset or update.confirmed:
                break
            await update.confirm()
            i += 1
        if i > 0:
            bot_dict['updates'] = updates[i:]

    async def create_update(self, bot_id, data):
        update = SimpleUpdate(data)
        bot_dict = self._get_bot_dict(bot_id)
        bot_dict['updates'].append(update)
        asyncio.ensure_future(self._on_update(bot_id))
        return update

    async def get_not_confirmed_updates(self, bot_id):
        """
        Args:
            bot_id (int)

        """
        bot_dict = self._get_bot_dict(bot_id)
        updates = bot_dict['updates']
        i = 0
        while i < len(updates):
            if not updates[i].confirmed:
                break
            i += 1
        if i > 0:
            updates = updates[i:]
            bot_dict['updates'] = updates
        return updates

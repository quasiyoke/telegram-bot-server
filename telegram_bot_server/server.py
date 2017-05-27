# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import logging
import traceback
from .error import BotError
from .middleware import AuthMiddleware, ErrorMiddleware, RequestDataMiddleware
from .response import Response
from aiohttp import web
from http import HTTPStatus

__all__ = ('Server', )
LOGGER = logging.getLogger('telegram_bot_server.server')
TOKEN_PATTERN = r'{token:[1-9]\d{0,15}:[\w\-]{10,60}}'


class Server:
    def __init__(self, bot_service, configuration, update_service):
        self._bot_service = bot_service
        self._configuration = configuration
        self._update_service = update_service
        self._update_service.set_update_handler(self._on_update)
        self._updates_futures = {}
        self._app = web.Application(
            middlewares=self._get_middlewares(),
            )
        self._setup_routes()
        self._app.on_cleanup.append(self._on_cleanup)

    def _get_middlewares(self):
        return (
            ErrorMiddleware(),
            RequestDataMiddleware(),
            AuthMiddleware(self._bot_service),
            )

    async def _handle_delete_webhook(self, request):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        LOGGER.info('"deleteWebhook" method.')
        description = 'Webhook was deleted' if await request.bot.delete_webhook() else 'Webhook is already deleted'
        LOGGER.debug(description)
        return Response(description=description)

    async def _handle_get_updates(self, request):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        LOGGER.info('"getUpdates" method for %s.', request.bot.bot_id)

        if request.bot.webhook:
            reason = 'Conflict: can\'t use getUpdates method while webhook is active'
            LOGGER.warning('%s. Bot ID %s.', reason, request.bot.bot_id)
            raise web.HTTPConflict(reason=reason)

        try:
            offset = int(request.data['offset'])
        except (KeyError, TypeError, ValueError):
            pass
        else:
            await self._update_service.confirm_updates(request.bot.bot_id, offset)
        updates = await self._update_service.get_not_confirmed_updates(request.bot.bot_id)
        updates_dicts = [update.dict for update in updates]
        if len(updates_dicts):
            return Response(result=updates_dicts)

        try:
            timeout = int(request.data['timeout'])
        except (KeyError, TypeError, ValueError):
            pass
        else:
            if timeout > 0:
                updates_future = asyncio.Future()
                if request.bot.bot_id in self._updates_futures:
                    reason = 'Conflict: another request for updates is still active'
                    LOGGER.warning('%s. Bot ID %s.', reason, request.bot.bot_id)
                    raise web.HTTPConflict(reason=reason)
                self._updates_futures[request.bot.bot_id] = updates_future
                try:
                    await asyncio.wait_for(updates_future, timeout=timeout)
                except asyncio.TimeoutError:
                    del self._updates_futures[request.bot.bot_id]
                except Exception as err:
                    del self._updates_futures[request.bot.bot_id]
                    LOGGER.warning('Exception during waiting for updates.')
                    traceback.print_exc()
                else:
                    del self._updates_futures[request.bot.bot_id]
                    updates = updates_future.result()
                    if len(updates):
                        await self._update_service.confirm_updates(request.bot.bot_id, updates[-1].bot_id + 1)
                        updates_dicts = [update.dict for update in updates]
        return Response(result=updates_dicts)

    async def _handle_send_message(self, request):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        LOGGER.info('"sendMessage" method.')
        return Response()

    async def _handle_set_webhook(self, request):
        """
        Raises:
            aiohttp.web.HTTPException

        """
        LOGGER.info('"setWebhook" method.')
        try:
            url = request.data['url']
        except (KeyError, TypeError) as err:
            reason = 'Bad Request: URL isn\'t specified'
            LOGGER.warning('%s. Request data were "%s". %s', reason, request.data, err)
            raise web.HTTPBadRequest(reason=reason) from err
        description = 'Webhook was set' if await request.bot.set_webhook(url) else 'Webhook is already set'
        LOGGER.debug(description)
        return Response(description=description)

    async def _on_cleanup(self, app):
        pass

    async def _on_update(self, bot_id):
        LOGGER.info('Update %s', bot_id)
        bot = await self._bot_service.get_bot(bot_id)
        updates = await self._update_service.get_not_confirmed_updates(bot_id)

        if not len(updates):
            return

        if bot.webhook:
            try:
                await bot.push_updates(updates)
            except BotError as err:
                LOGGER.warning('Problems during pushing updates to webhook. %s', err)
            else:
                self._update_service.confirm_updates(updates[-1].update_id + 1)
        else:
            updates_future = self._updates_futures.get(bot_id)
            if updates_future is not None:
                updates_future.set_result(updates)

    def _setup_routes(self):
        self._app.router.add_route('*', f'/bot{TOKEN_PATTERN}/deleteWebhook', self._handle_delete_webhook)
        self._app.router.add_route('*', f'/bot{TOKEN_PATTERN}/getUpdates', self._handle_get_updates)
        self._app.router.add_route('*', f'/bot{TOKEN_PATTERN}/sendMessage', self._handle_send_message)
        self._app.router.add_route('*', f'/bot{TOKEN_PATTERN}/setWebhook', self._handle_set_webhook)

    def run(self):
        web.run_app(
            self._app,
            host='0.0.0.0',
            port=self._configuration.port,
            )

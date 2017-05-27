# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import logging
from .response import Response
from aiohttp import web
from http import HTTPStatus

__all__ = ('AuthMiddleware', 'ErrorMiddleware', 'RequestDataMiddleware', )
LOGGER = logging.getLogger('telegram_bot_server.middleware')


class AuthMiddleware:
    """Obtains `request.bot` attribute from provided token.

    Raises:
        aiohttp.web.HTTPUnauthorized In case of incorrect token.

    """

    def __init__(self, bot_service):
        self._bot_service = bot_service

    async def __call__(self, app, handler):
        async def middleware_handler(request):
            try:
                token = request.match_info['token']
            except KeyError as err:
                raise web.HTTPBadRequest() from err
            request.bot = await self._bot_service.get_bot_by_token(token)
            if request.bot is None:
                raise web.HTTPUnauthorized()

            response = await handler(request)

            return response

        return middleware_handler


class ErrorMiddleware:
    """Provides JSON error responses.

    """

    async def __call__(self, app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
            except web.HTTPException as err:
                response = await self._get_error_response(err)

            return response

        return middleware_handler

    async def _get_error_response(self, err):
        """
        Args:
            err (aiohttp.web.HTTPException): Error.

        Returns:
            aiohttp.web.Response

        """
        if err.status == HTTPStatus.NOT_FOUND:
            description = 'Not Found: method not found'
            LOGGER.warning(description)
            response = Response(status=err.status, description=description)
        else:
            LOGGER.warning('HTTP error %s.', err.text)
            response = Response(status=err.status, description=err.reason)

        return response


class RequestDataMiddleware:
    """Obtains `request.data`.

    Raises:
        aiohttp.web.HTTPBadRequest
        aiohttp.web.HTTPMethodNotAllowed

    """

    ALLOWED_REQUEST_METHODS = ['GET', 'POST', ]

    async def __call__(self, app, handler):
        async def middleware_handler(request):
            self._assert_request_method_is_allowed(request)

            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                request.data = await self._get_request_json(request)
            elif content_type == 'application/x-www-form-urlencoded':
                request.data = await request.post()
            else:
                request.data = request.query

            response = await handler(request)

            return response

        return middleware_handler

    def _assert_request_method_is_allowed(self, request):
        if request.method not in self.ALLOWED_REQUEST_METHODS:
            raise web.HTTPMethodNotAllowed()

    async def _get_request_json(self, request):
        request_text = await request.text()
        try:
            return json.loads(request_text)
        except ValueError as err:
            reason = 'Bad Request: invalid JSON'
            LOGGER.warning('%s. Request text was "%s". %s', reason, request_text, err)
            raise web.HTTPBadRequest(reason=reason) from err

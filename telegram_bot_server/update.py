# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from .error import UpdateError
from datetime import datetime

__all__ = ('MessageData', 'SimpleUpdate', 'Update', 'UpdateData', )


class Update:
    """Abstract update.

    """

    def __init__(self):
        self.created = datetime.utcnow()

    def __str__(self):
        return f'{type(self).__name__} {self.update_id}'

    @property
    def confirmed(self):
        raise NotImplementedError()

    @property
    def dict(self):
        raise NotImplementedError()

    async def confirm(self):
        raise NotImplementedError()


class SimpleUpdate(Update):
    count = 0

    def __init__(self, data=None):
        super(SimpleUpdate, self).__init__()
        type(self).count += 1
        self.update_id = type(self).count
        if isinstance(data, UpdateData):
            data = data.data
        self._data = data
        self._confirmed = False

    @property
    def confirmed(self):
        return self._confirmed

    @property
    def dict(self):
        date = int(self.created.timestamp())
        result = {
            'update_id': self.update_id,
            }
        result.update(self._data)
        if 'message' in result:
            result['message']['message_id'] = self.update_id
            result['message']['date'] = date
        return result

    async def confirm(self):
        self._confirmed = True


class UpdateData:
    """Abstract update data.

    """

    def __init__(self, data=None):
        """
        Raises:
            UpdateError if the data is incorrect.

        """
        if data is None:
            data = {}
        self.data = data
        self._assert_is_valid()
        self._process()

    def _assert_is_valid(self):
        """
        Raises:
            UpdateError if the data is incorrect.

        """
        raise NotImplementedError()

    def _process(self):
        pass


class MessageData(UpdateData):
    def __init__(self, chat, from_dict, text):
        super(MessageData, self).__init__({
            'message': {
                'chat': chat,
                'from': from_dict,
                'text': text,
                },
            })

    def _assert_is_valid(self):
        """
        Raises:
            UpdateError if the data is incorrect.

        """
        try:
            ChatData(self.data['message']['chat'])
            UserData(self.data['message']['from'])
            if not self.data['message']['text']:
                raise UpdateError('Message text can\'t be empty.')
        except (KeyError, TypeError) as err:
            raise UpdateError('Message data is invalid.') from err

    def _process(self):
        match = re.search(r'^/\w+', self.data['message']['text'])
        if match is None:
            return
        self.data['message']['entities'] = [{
            'length': len(match.group(0)),
            'offset': 0,
            'type': 'bot_command',
            }]


class UserData(UpdateData):
    def _assert_is_valid(self):
        """
        Raises:
            UpdateError if the data is incorrect.

        """
        try:
            if self.data['id'] <= 0:
                raise UpdateError('User ID should be positive integer.')
            if not self.data['first_name']:
                raise UpdateError('User\'s first name isn\'t optional.')
        except (KeyError, TypeError) as err:
            raise UpdateError('User data is invalid.') from err


class ChatData(UserData):
    def _assert_is_valid(self):
        """
        Raises:
            UpdateError if the data is incorrect.

        """
        try:
            self.data['type']
        except (KeyError, TypeError) as err:
            raise UpdateError('Chat data is invalid.') from err
        super(ChatData, self)._assert_is_valid()

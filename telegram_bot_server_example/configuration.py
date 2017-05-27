# telegram-bot-server-example
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
from telegram_bot_server import ConfigurationError, DictConfiguration


class Configuration:
    def __init__(self, path):
        """
        Args:
            path (str | pathlib.Path): Path to the JSON configuration file.

        Raises:
            ConfigurationError

        """
        try:
            with open(path, 'r') as f:
                configuration_dict = json.load(f)
        except (IOError, ValueError) as err:
            raise ConfigurationError('Troubles with reading configuration file.') from err
        try:
            self.bots = configuration_dict['bots']
            self.server = DictConfiguration(configuration_dict['server'])
        except (KeyError, TypeError) as err:
            raise ConfigurationError('Wrong configuration file structure.') from err

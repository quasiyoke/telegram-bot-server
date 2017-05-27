# telegram-bot-server-example
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from .configuration import Configuration
from .server import Server
from .util import __version__
from docopt import docopt
from telegram_bot_server import SimpleBotService, SimpleUpdateService

DOC = '''telegram-bot-server-example

Usage:
  telegram-bot-server-example CONFIGURATION
  telegram-bot-server-example -h | --help | --version

Arguments:
  CONFIGURATION  Path to configuration.json file.
'''
LOGGER = logging.getLogger('telegram_bot_server_example.telegram_bot_server_example')


def main():
    logging.basicConfig(level=logging.DEBUG)
    arguments = docopt(DOC, version=__version__)
    configuration = Configuration(arguments['CONFIGURATION'])
    update_service = SimpleUpdateService()
    bot_service = SimpleBotService(
        configuration.bots,
        update_service=update_service,
        )
    server = Server(
        bot_service=bot_service,
        configuration=configuration.server,
        update_service=update_service,
        )
    server.run()

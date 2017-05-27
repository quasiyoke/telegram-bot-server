# telegram-bot-example
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiohttp
import logging
from .bot import Bot
from .configuration import Configuration


def main(configuration_path):
    logging.basicConfig(level=logging.DEBUG)
    configuration = Configuration(configuration_path)
    bot = Bot(configuration)
    bot.run()

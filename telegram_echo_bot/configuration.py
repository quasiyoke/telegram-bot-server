# telegram-echo-bot
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json


class Configuration:
    def __init__(self, path):
        with open(path, 'r') as f:
            configuration_dict = json.load(f)
        self.api_host = configuration_dict['api_host']
        self.port = configuration_dict['port']
        self.token = configuration_dict['token']

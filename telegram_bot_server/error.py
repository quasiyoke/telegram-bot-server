# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ('BotServiceError', 'ConfigurationError', 'UpdateError', )


class Error(Exception):
    pass


class BotError(Error):
    pass


class BotServiceError(Error):
    pass


class ConfigurationError(Error):
    pass


class UpdateError(Error):
    pass

# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .error import ConfigurationError

__all__ = ('Configuration', 'DictConfiguration', )


class Configuration:
    def __init__(self, *args, **kwargs):
        """
        Raises:
            ConfigurationError

        """
        self._fill(*args, **kwargs)
        self._validate()

    def _fill(self, *args, **kwargs):
        """
        Raises:
            ConfigurationError

        """
        raise NotImplementedError()

    def _validate(self):
        """
        Raises:
            ConfigurationError

        """
        try:
            self.port = int(self.port)
        except ValueError as err:
            raise ConfigurationError('Invalid configuration value.') from err


class DictConfiguration(Configuration):
    def _fill(self, configuration_dict):
        """
        Raises:
            ConfigurationError

        """
        try:
            self.port = configuration_dict['port']
        except (KeyError, TypeError) as err:
            raise ConfigurationError('Can\'t read configuration dict.') from err

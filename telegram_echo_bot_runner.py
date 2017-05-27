#!/usr/bin/env python3
#
# telegram-echo-bot
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''Convenience wrapper for running randtalkbot directly from source tree.'''

import sys
from telegram_echo_bot.telegram_echo_bot import main

if __name__ == '__main__':
    main(sys.argv[1])

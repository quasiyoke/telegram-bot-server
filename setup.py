# telegram-bot-server-example
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from telegram_bot_server_example.util import __version__
from setuptools import setup

with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='telegram-bot-server-example',
    version=__version__,
    description='Telegram bot server distributing incoming messages among all its bots.',
    long_description=long_description,
    keywords=['telegram', 'bot', 'chat'],
    license='AGPLv3+',
    author='Pyotr Ermishkin',
    author_email='quasiyoke@gmail.com',
    url='https://github.com/quasiyoke/telegram-bot-server-example',
    packages=['telegram_bot_server_example'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Chat',
        ],
    install_requires=[
        'docopt>=0.6.2,<0.7',
        'telegram-bot-server>=0.1.0,<0.2',
        ],
    )

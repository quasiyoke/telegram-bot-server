# telegram-echo-bot
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='telegram-echo-bot',
    version='0.1.0',
    description='Example Telegram bot replying with the same message.',
    long_description=long_description,
    keywords=['telegram', 'bot', 'chat'],
    license='AGPLv3+',
    author='Pyotr Ermishkin',
    author_email='quasiyoke@gmail.com',
    url='https://github.com/quasiyoke/telegram-bot-server',
    packages=['telegram_echo_bot'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Chat',
        ],
    install_requires=[
        'aiohttp>=2.1.0,<3.0',
        ],
    )

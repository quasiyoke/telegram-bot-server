# telegram-bot-server
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='telegram-bot-server',
    version='0.1.0',
    description='Unofficial Telegram server implementation handling Telegram Bot API.',
    long_description=long_description,
    keywords=['telegram', 'bot', 'anonymous', 'chat'],
    license='AGPLv3+',
    author='Pyotr Ermishkin',
    author_email='quasiyoke@gmail.com',
    url='https://github.com/quasiyoke/telegram-bot-server',
    packages=['telegram_bot_server'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Chat',
        ],
    install_requires=[
        'aiohttp>=2.1.0,<3.0',
        ],
    )

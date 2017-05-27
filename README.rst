telegram-bot-server-example
==========

Telegram bot server distributing incoming messages among all its bots.

Deployment
----------

::

    $ docker network create \
        --subnet=172.29.0.0/16 \
        telegram-bot-server-example
    $ docker build --tag=telegram-bot-server-example .

After that write ``configuration/configuration.json`` file like that::

    {
        "bots": [
            {
                "token": "111111111:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            },
            {
                "token": "222222222:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
            }
        ],
        "server": {
            "port": 8000
        }
    }

Now you may run the bot::

    $ docker run \
        --name=telegram-bot-server-example \
        --net=telegram-bot-server-example \
        --ip=172.29.0.10 \
        --volume=`pwd`/configuration:/configuration \
        --detach \
        telegram-bot-server-example

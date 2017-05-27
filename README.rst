telegram-echo-bot
====================

Example Telegram bot replying with the same message. The bot uses ``getUpdates`` API method for `fetching fresh updates <https://core.telegram.org/bots/api#getting-updates>`_.

Deployment
----------

::

    $ docker network create \
        --subnet=172.29.0.0/16 \
        telegram-echo-bot
    $ docker build --tag=telegram-echo-bot .

After that write ``configuration/configuration.json`` file like that::

    {
        "api_host": "https://api.telegram.org/",
        "token": "987654321:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    }

Now you may run the bot::

    $ docker run \
        --name=telegram-echo-bot \
        --net=telegram-echo-bot \
        --ip=172.29.0.10 \
        --volume=`pwd`/configuration:/configuration \
        --detach \
        telegram-echo-bot

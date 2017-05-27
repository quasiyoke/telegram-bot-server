telegram-bot-example
====================

Example Telegram bot sending current time regularly to the specified Telegram user ID. The bot uses `webhooks <https://core.telegram.org/bots/api#getting-updates>`_ for fetching fresh updates.

Deployment
----------

::

    $ docker network create \
        --subnet=172.29.0.0/16 \
        telegram-bot-example
    $ docker build --tag=telegram-bot-example .

After that write ``configuration/configuration.json`` file like that::

    {
        "api_host": "https://api.telegram.org/",
        "period": 3,
        "port": 5293,
        "receiver_id": 123,
        "token": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    }

Now you may run the bot::

    $ docker run \
        --name=telegram-bot-example \
        --net=telegram-bot-example \
        --ip=172.29.0.10 \
        --volume=`pwd`/configuration:/configuration \
        --detach \
        telegram-bot-example

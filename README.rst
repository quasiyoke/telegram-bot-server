telegram-bot-server
===================

Unofficial Telegram server implementation handling `Telegram Bot API <https://core.telegram.org/bots/api>`_.

To use this framework you need to implement several basic entities: ``BotService``, ``Server``, ``UpdateService``.

Bots' tokens should match the following regular expression: ``[1-9]\d{0,15}:[\w\-]{10,60}``.

Examples
--------

You're able to look at example server built using this framework `here <https://github.com/quasiyoke/telegram-bot-server/tree/telegram-bot-server-example>`_. You can run it with two example bots: `sending current time regularly <https://github.com/quasiyoke/telegram-bot-server/tree/telegram-bot-example>`_ and `echo bot <https://github.com/quasiyoke/telegram-bot-server/tree/telegram-echo-bot>`_.

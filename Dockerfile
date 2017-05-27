FROM python:3.6
MAINTAINER Pyotr Ermishkin <quasiyoke@gmail.com>

COPY telegram_echo_bot /telegram_echo_bot/
COPY telegram_echo_bot_runner.py /
COPY README.rst /
COPY setup.py /

VOLUME /configuration

RUN python /setup.py install

CMD ["/telegram_echo_bot_runner.py", "/configuration/configuration.json"]

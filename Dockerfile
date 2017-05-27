FROM python:3.6
MAINTAINER Pyotr Ermishkin <quasiyoke@gmail.com>

COPY telegram_bot_example /telegram_bot_example/
COPY telegram_bot_example_runner.py /
COPY README.rst /
COPY setup.py /

VOLUME /configuration

RUN python /setup.py install

CMD ["/telegram_bot_example_runner.py", "/configuration/configuration.json"]

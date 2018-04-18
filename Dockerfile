FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add requirements
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/HelloDHLyn/Python-Markdown@multimarkdown

# Add application
ADD . /usr/src/app

ENV NEW_RELIC_CONFIG_FILE newrelic.ini

ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "newrelic-admin", "run-program", "python", "manage.py", "runserver", "0.0.0.0:8080" ]

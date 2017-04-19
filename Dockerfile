FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add requirements
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt

RUN git clone -b multimarkdown https://github.com/HelloDHLyn/Python-Markdown /usr/src/Python-Markdown
RUN pip install -e /usr/src/Python-Markdown

# Add application
ADD . /usr/src/app

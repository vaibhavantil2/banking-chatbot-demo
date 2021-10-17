FROM bitnami/python:3.7

COPY . /app/

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install rasa==2.8.7

CMD rasa run

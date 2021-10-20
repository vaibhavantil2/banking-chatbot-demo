FROM bitnami/python:3.7

COPY . /app/

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install rasa[spacy]==2.8.9

EXPOSE 5005

RUN python -m spacy download en_core_web_md

CMD rasa run
FROM bitnami/python:3.7

COPY . /app/actions/
COPY pyproject.toml /app/pyproject.toml

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install rasa==2.8.7

EXPOSE 5055

CMD rasa run actions

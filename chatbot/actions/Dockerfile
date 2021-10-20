FROM bitnami/python:3.7

COPY . /app/actions/

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install rasa-sdk==2.8.2

EXPOSE 5055

CMD python -m rasa_sdk --actions actions

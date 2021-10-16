FROM bitnami/python:latest as base

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:${PATH}"

# install dependencies
COPY . /app/

WORKDIR /app

# update permissions & change user
RUN chgrp -R 0 /app && chmod -R g=u /app

USER 1001

EXPOSE 5005

CMD ["poetry", "run", "rasa", "run"]

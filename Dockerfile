FROM python:3.9.13-slim-bullseye AS base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt update; \
    apt --yes --no-install-recommends install libpq5

FROM base AS python

RUN apt update; \
    apt --yes --no-install-recommends install build-essential curl libpq-dev
RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.1.3

COPY . .
RUN POETRY_VIRTUALENVS_IN_PROJECT=true /root/.local/bin/poetry install --only=main

FROM base AS runtime

ENV PATH="/.venv/bin:$PATH"

COPY . .

FROM runtime AS production

COPY --from=python /.venv /.venv

ENV STATIC_ROOT /static/
RUN python manage.py collectstatic

CMD ["/docker-cmd.sh"]

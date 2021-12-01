FROM python:3.7-slim-stretch

RUN apt-get update; \
apt-get --yes --no-install-recommends install build-essential libpq-dev; \
rm -rf /var/lib/apt/lists/*

ADD . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system --deploy

ENV STATIC_ROOT /static/
RUN python manage.py collectstatic

RUN apt-get --yes --purge autoremove build-essential

CMD ["/app/docker-cmd.sh"]

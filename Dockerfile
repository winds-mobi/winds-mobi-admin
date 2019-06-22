FROM python:3.7-slim-stretch

RUN apt-get update; \
apt-get --yes --no-install-recommends install build-essential libpq-dev; \
rm -rf /var/lib/apt/lists/*

ADD . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system --deploy

RUN apt-get --yes --purge autoremove build-essential

EXPOSE 8000
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "winds_mobi_admin.wsgi"]

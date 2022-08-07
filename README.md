winds.mobi - real-time weather observations
===========================================

[![Follow us on https://www.facebook.com/WindsMobi/](https://img.shields.io/badge/facebook-follow_us-blue)](https://www.facebook.com/WindsMobi/)

[winds.mobi](http://winds.mobi): Paraglider pilot, kitesurfer, check real-time weather conditions of your favorite spots
on your smartphone, your tablet or your computer.

winds-mobi-admin
--------------------

Django application to administrate winds.mobi:

- manage users and profiles
- configure Zermatt stations
- configure Windy stations

### Dependencies

- python 3.9 and poetry 
- postgres 
- redis

See [settings.py](https://github.com/winds-mobi/winds-mobi-admin/blob/main/winds_mobi_admin/settings.py)

### Run the project with docker compose (simple way)

Create a `.env` file from `.env.template` and, optionally, fill the missing secrets for Facebook and Google social
authentications.

- `docker compose --profile=application up --build`

### Run the project locally on macOS

#### Install dependencies

- `brew install libpq`
- `export PATH=/usr/local/opt/libpq/bin:$PATH`
- `export LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib"`

#### Python environment

- `poetry install`
- `poetry shell`

Create a `.env.localhost` file from `.env.localhost.template` and fill the missing secrets.

#### Create db schema

- `dotenv -f .env.localhost run python manage.py migrate`

#### Start external services with docker compose

Create a `.env` file from `.env.template`.

- `docker compose up`

#### Run the server

- `dotenv -f .env.localhost run python manage.py runserver 8006`

Licensing
---------

Please see the file called [LICENSE.txt](https://github.com/winds-mobi/winds-mobi-admin/blob/main/LICENSE.txt)

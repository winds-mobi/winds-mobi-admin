winds.mobi - real-time weather observations
===========================================

[![DockerHub](https://img.shields.io/docker/cloud/automated/windsmobi/winds-mobi-admin)](https://cloud.docker.com/u/windsmobi/repository/docker/windsmobi/winds-mobi-admin)
[![Follow us on https://www.facebook.com/WindsMobi/](https://img.shields.io/badge/facebook-follow_us-blue)](https://www.facebook.com/WindsMobi/)

[winds.mobi](http://winds.mobi): Paraglider pilot, kitesurfer, check real-time weather conditions of your favorite spots
on your smartphone, your tablet or your computer.

winds-mobi-admin
--------------------

Django application to manage winds.mobi users and profiles

### Requirements

- python >= 3.6
- a database supported by [django](https://docs.djangoproject.com/en/2.2/ref/databases/) 
- mongodb >= 3.0

See [settings.py](https://github.com/winds-mobi/winds-mobi-admin/blob/master/winds_mobi_admin/settings.py)

#### macOS

- `brew install libpq`
- `export PATH=/usr/local/opt/libpq/bin:$PATH`
- `export LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib"`

### Python environment

- `pipenv install`
- `pipenv shell`

### Create db schema

- `python manage.py migrate`

### Run the server

- `python manage.py runserver`

Licensing
---------

Please see the file called [LICENSE.txt](https://github.com/winds-mobi/winds-mobi-admin/blob/master/LICENSE.txt)

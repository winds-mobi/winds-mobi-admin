winds.mobi - real-time weather observations
===========================================

[![Follow us on https://www.facebook.com/WindsMobi/](https://img.shields.io/badge/facebook-follow_us-blue)](https://www.facebook.com/WindsMobi/)
[![DockerHub](https://img.shields.io/docker/cloud/automated/windsmobi/winds-mobi-admin)](https://cloud.docker.com/u/windsmobi/repository/docker/windsmobi/winds-mobi-admin)

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

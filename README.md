winds.mobi - real-time weather observations
===========================================

[winds.mobi](http://winds.mobi): Paraglider pilot, kitesurfer, check real-time weather conditions of your favorite spots
on your smartphone, your tablet or your computer.

Follow this project on:
- [Facebook](https://www.facebook.com/WindsMobi/)

winds-mobi-admin
--------------------

Django application to manage winds.mobi users and profiles

### Requirements

Mandatory requirements:
- python >= 3.6
- a database supported by [django](https://docs.djangoproject.com/en/2.2/ref/databases/) 
- mongodb >= 3.0

See [settings.py](https://github.com/winds-mobi/winds-mobi-admin/blob/master/settings.py)

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

#!/usr/bin/env sh

python manage.py migrate
gunicorn --workers=3 --bind="0.0.0.0:$PORT" winds_mobi_admin.wsgi

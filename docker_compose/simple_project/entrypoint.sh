#!/bin/bash

cd movies_admin
python manage.py migrate --noinput
python manage.py collectstatic --no-input
python manage.py createsuperuser --noinput || true
cd -

uwsgi --strict --ini uwsgi.ini
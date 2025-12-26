#!/usr/bin/env bash

set -e

python manage.py migrate --fake movies 0001_initial
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser --noinput || true 

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini

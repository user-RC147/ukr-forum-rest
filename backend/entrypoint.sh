#!/bin/sh

set -e

echo "Apply migrations..."
python manage.py migrate search --noinput
python manage.py migrate --noinput

echo "Create superuser..."
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@admin.com \
DJANGO_SUPERUSER_PASSWORD=admin \
python manage.py createsuperuser --noinput || true

echo "Run server..."
exec "$@"
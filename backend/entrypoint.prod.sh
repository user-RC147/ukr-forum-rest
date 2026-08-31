#!/bin/sh

set -e

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Apply migrations..."
python manage.py migrate --noinput

echo "Run server..."
exec "$@"
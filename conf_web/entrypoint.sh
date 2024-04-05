#!/bin/sh

until PGPASSWORD=$DATABASE_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

python3 manage.py migrate

exec gunicorn praetorian_api.wsgi:application -b 0.0.0.0:4000 --log-level=debug

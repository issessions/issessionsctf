#!/bin/bash
# Waits for postgresql service to be reachable

until pg_isready -h $DB_ADDRESS ; do
  >&2 echo "Postgres is unavailable - sleeping 3"
  sleep 3
done

gunicorn issessionsctf.wsgi:application --workers=5 -b 0.0.0.0:80

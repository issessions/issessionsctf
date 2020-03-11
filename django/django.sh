#!/bin/bash
# Waits for postgresql service to be reachable

until pg_isready -h 192.168.20.30 ; do
  >&2 echo "Postgres is unavailable - sleeping 3"
  sleep 3
done

>&2 echo "Postgres is up - executing commands"

>&2 echo -e "Checking if the postgresql database is already setup\n" 
PGPASSWORD='$PGPASSWORD' psql -h 192.168.20.30 -U "postgres" -d iss -c "select count(*) from ctf_challenge" > /dev/null 2>&1
if [ "$?" == "1" ]; then
  >&2 echo -e "Setting up postgresql database\n"
  python3 manage.py makemigrations ctf
  python3 manage.py migrate
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('$ADMIN_USER', '$ADMIN_USER@localhost', '$ADMIN_PASSWORD')" | python3 manage.py shell
  #bash challenge_import.sh
else
  >&2 echo "Postgresql database already setup"
fi

gunicorn issessionsctf.wsgi:application --workers=5 -b 0.0.0.0:80

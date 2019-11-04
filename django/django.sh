#!/bin/bash
# Waits for postgresql service to be reachable

until psql -h "postgresql" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping 3"
  sleep 3
done

>&2 echo "Postgres is up - executing commands"

>&2 echo -e "Checking if the postgresql database is already setup\n" 
psql -h "postgresql" -U "postgres" -d iss -c "select count(*) from ctf_challenge" > /dev/null 2>&1
if [ "$?" == "1" ]; then
  >&2 echo -e "Setting up postgresql database\n"
  python3 manage.py makemigrations ctf
  python3 manage.py migrate
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'admin')" | python3 manage.py shell
else
  >&2 echo "Postgresql database already setup"
fi

>&2 echo -e "\n----------------------------\nStarting server on port 8000\n----------------------------" 
python3 manage.py runserver 0.0.0.0:8000


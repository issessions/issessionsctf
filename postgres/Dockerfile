
FROM postgres:latest

COPY create_user.sh timezone.sql /docker-entrypoint-initdb.d/
COPY create_user.sql /home

CMD ["postgres"]

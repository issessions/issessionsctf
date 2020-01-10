FROM postgres:latest

COPY create_user.sql /docker-entrypoint-initdb.d/create_user.sql

CMD ["postgres"]

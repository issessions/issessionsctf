
FROM postgres:latest

COPY create_user.sql /docker-entrypoint-initdb.d/

# Set date & time to Canada/Eastern
RUN cp /usr/share/zoneinfo/Canada/Eastern /etc/localtime

CMD ["postgres"]

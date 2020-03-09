FROM nginx:latest

LABEL maintainer="name"

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY server.conf /etc/nginx/conf.d/

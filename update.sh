#! /bin/bash

git checkout gunicorn-prod-merge && \
git pull && \
docker-compose -f up --build --no-deps -d

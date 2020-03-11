#! /bin/bash

git checkout gunicorn-prod-merge && \
git pull && \
docker-compose up --build --no-deps -d

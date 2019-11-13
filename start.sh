#!/bin/bash

docker-compose up -d --build --force-recreate
python3 -m venv ./django/venv && source ./django/venv/bin/activate && pip install -r ./django/requirements.txt
chown -R $SUDO_USER:$SUDO_USER ./django/


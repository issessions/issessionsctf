#!/bin/bash

docker-compose up -d --build --force-recreate
chown -R $SUDO_USER:$SUDO_USER ./django/


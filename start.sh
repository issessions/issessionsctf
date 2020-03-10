#!/bin/bash

docker-compose up -d
chown -R $SUDO_USER:$SUDO_USER ./django/


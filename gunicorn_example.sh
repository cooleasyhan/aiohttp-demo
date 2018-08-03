#!/usr/bin/env bash

#!/bin/bash
NAME=main # Name of the application
USER=yihan # the user to run as
GROUP=staff # the group to run as
NUM_WORKERS=4 # how many worker processes should Gunicorn spawn
TIMEOUT=600
WSGI_MODULE=main.main

echo "Starting $NAME as `whoami`"

exec pipenv run gunicorn main.main:gunicorn_app \
--worker-class aiohttp.GunicornWebWorker \
--name $NAME \
--workers $NUM_WORKERS \
--timeout $TIMEOUT \
--bind=0.0.0.0:8000 \
--log-level=debug \
--log-file=-
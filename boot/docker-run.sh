#!/bin/bash
source /opt/venv/bin/active

cd /code

RUN_PORT=${PORT:-9000}
RUN_HOST=${HOST:-0.0.0.0}

gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app

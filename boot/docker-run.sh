#!/usr/bin/env bash
set -e  # (optional) makes script exit if any command fails

source /opt/venv/bin/activate

cd /code
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

exec gunicorn -k uvicorn.workers.UvicornWorker -b "$RUN_HOST:$RUN_PORT" main:app

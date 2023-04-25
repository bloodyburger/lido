#!/usr/bin/env bash
SCRIPT_DIR=${PWD}

set -a
source "$SCRIPT_DIR/.env"
set +a

python manage.py runserver

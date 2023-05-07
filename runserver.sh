#!/usr/bin/env bash

set -a
source .env
set +a
echo $CONNECTION_STRING
python manage.py migrate
python manage.py runserver

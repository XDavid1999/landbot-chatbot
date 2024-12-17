#!/bin/bash
echo "Apply database migrations"
python manage.py migrate
echo "Running in local environment"
python manage.py runserver 0.0.0.0:$BACKEND_API_PORT
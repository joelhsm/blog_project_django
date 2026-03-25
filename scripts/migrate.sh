#!/bin/sh
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "Migrations applied successfully!"
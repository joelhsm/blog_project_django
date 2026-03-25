#!/bin/sh

echo "Running server..."
python manage.py runserver 0.0.0.0:8000
echo "Server running successfully!"
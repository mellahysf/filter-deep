#!/bin/sh

#start server

echo "Starting server"
gunicorn filter_image_django.wsgi
python manage.py runserver
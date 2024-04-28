#!/bin/sh

# gunicorn main_app.wsgi:application --bind 0.0.0.0:5000

gunicorn -b 0.0.0.0:5000 -app:app
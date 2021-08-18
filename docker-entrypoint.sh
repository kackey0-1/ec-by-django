#!/bin/bash

# Install packages for production
pip3 install -r requirements.txt
# Set environment for production
export DJANGO_PROFILE=production
# Prepare database
# python3 manage.py migrate
# Start runserver
gunicorn app.wsgi --reload --bind 0.0.0.0:8000

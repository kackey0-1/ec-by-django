#!/bin/bash

# Install packages for local
pip3 install -r requirements.txt

# Set environment for local
export DJANGO_PROFILE=local

# Prepare database
python3 manage.py migrate
# Start runserver
gunicorn app.wsgi --reload

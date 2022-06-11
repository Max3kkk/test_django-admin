#!/bin/bash
echo "Starting admin module..."
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
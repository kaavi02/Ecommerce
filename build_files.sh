#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files into the build output directory
python manage.py collectstatic --noinput

#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations (Optional but recommended for Render)
python manage.py migrate

# Collect static files into the folder Render will serve
python manage.py collectstatic --noinput --clear
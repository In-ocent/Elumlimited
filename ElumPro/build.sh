#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect Static Files
python3.12 manage.py collectstatic --noinput --clear

# Run Migrations (Optional, but good for database updates)
python3.12 manage.py migrate
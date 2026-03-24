#!/bin/bash

# Move into the folder where manage.py lives
cd ElumPro

# Install dependencies
python3.12 -m pip install -r requirements.txt

# Collect Static Files
# This creates the 'staticfiles' folder INSIDE ElumPro
python3.12 manage.py collectstatic --noinput --clear

# Move the result back to the root so Vercel can find it
cp -r staticfiles ../
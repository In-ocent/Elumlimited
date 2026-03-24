#!/bin/bash

echo "--- BUILD START ---"

# 1. Install Python dependencies
# Using -m pip is the safest way on Vercel
python3.12 -m pip install -r requirements.txt

echo "--- COLLECTING STATIC FILES ---"
# 2. Collect Static Files (This is what fixes your CSS)
# We use --noinput so it doesn't wait for you to type 'yes'
python3.12 manage.py collectstatic --noinput --clear

echo "--- RUNNING MIGRATIONS ---"
# 3. Database Migrations
# Note: If this fails, check your DATABASE_URL port (should be 6543)
python3.12 manage.py migrate --noinput

echo "--- BUILD END ---"
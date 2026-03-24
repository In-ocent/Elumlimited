#!/bin/bash

echo "BUILD START"

# 1. Install dependencies
# Using -m pip is safer on Vercel's Linux environment
python3.12 -m pip install -r requirements.txt

echo "COLLECTING STATIC FILES..."
# 2. Collect Static Files
# This gathers your 19 files for WhiteNoise
python3.12 manage.py collectstatic --noinput --clear

echo "RUNNING MIGRATIONS..."
# 3. Run Migrations
# This connects to your Supabase DB and updates tables
python3.12 manage.py migrate --noinput

echo "BUILD END"
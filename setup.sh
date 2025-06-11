#!/bin/bash

set -e

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Loading fixtures (if any)..."
# Add if you have fixtures or want to update existing fixtures
 python manage.py loaddata booking_module/fixtures/booking_fixture.json
 python manage.py loaddata booking_module/fixtures/user_fixture.json

echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Running server..."
python manage.py runserver

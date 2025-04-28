#!/bin/bash

# Create virtual environment
python -m venv env

# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create logs directory
mkdir -p logs
chmod 755 logs

# Create media directory
mkdir -p media
chmod 755 media

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please update with your settings."
fi

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create static files directory
python manage.py collectstatic --noinput

echo "Setup complete! Don't forget to:"
echo "1. Update your .env file with proper credentials"
echo "2. Create a superuser using: python manage.py createsuperuser"
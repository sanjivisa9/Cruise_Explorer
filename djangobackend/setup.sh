#!/bin/bash

# Exit on error
set -e

echo "Setting up Cruise Explorer environment..."

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
    echo "Installing python3-venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory with proper permissions
echo "Setting up log directory..."
sudo mkdir -p /var/log/cruise_explorer
sudo chown -R $USER:$USER /var/log/cruise_explorer
chmod 755 /var/log/cruise_explorer

# Create media directory
echo "Setting up media directory..."
mkdir -p media
chmod 755 media

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Created .env file from template. Please update with your settings."
fi

# Create database migrations
echo "Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create static files directory
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
echo "Next steps:"
echo "1. Update your .env file with proper credentials"
echo "2. Create a superuser using: python manage.py createsuperuser"
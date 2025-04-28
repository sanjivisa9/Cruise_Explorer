#!/bin/bash

echo "Setting up PostgreSQL database..."

# Install PostgreSQL if not installed
if ! command -v psql &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
fi

# Start PostgreSQL service
sudo service postgresql start

# Wait for PostgreSQL to start
sleep 5

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE cruise_explorer;
CREATE USER cruise_user WITH PASSWORD 'cruise_password';
ALTER ROLE cruise_user SET client_encoding TO 'utf8';
ALTER ROLE cruise_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cruise_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cruise_explorer TO cruise_user;
EOF

echo "Database setup complete!"
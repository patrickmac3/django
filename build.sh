#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt


# Create a superuser in Django
echo "Creating superuser..."
python manage.py createsuperuser
# Prompt for superuser information

read -p "Email address: " admin@gmail.com
read -p "ROLE: " ADMIN
read -p "First name: " ADMIN
read -p "Last name: " ADMIN
read -s -p "Password: " adminpassword123
echo

# Pass the superuser information as arguments to the createsuperuser command
python manage.py createsuperuser --username $username --email $email --noinput
echo "Superuser created successfully!"


# Apply any outstanding database migrations
python manage.py migrate
#!/bin/bash
echo "Installing project dependencies..."
python3 -m pip install --break-system-packages -r requirements.txt || true

echo "Running database migrations..."
python3 manage.py migrate --noinput || true

echo "Collecting static assets..."
python3 manage.py collectstatic --noinput --clear




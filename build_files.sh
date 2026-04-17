#!/usr/bin/env bash
set -e

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running migrations (only if DATABASE_URL is set)..."
if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate --noinput
    echo "==> Migrations complete."
else
    echo "==> Skipping migrate (no DATABASE_URL)."
fi

echo "==> Build complete."

#!/bin/sh
python manage.py migrate
python manage.py createsuperuser --noinput || true
python manage.py collectstatic --noinput
gunicorn backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --capture-output

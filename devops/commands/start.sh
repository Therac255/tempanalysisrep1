#!/bin/bash

python manage.py migrate

python manage.py collectstatic --noinput

case "$ENV" in
"DEV")
    python manage.py runserver 0.0.0.0:8000
    ;;
"PRODUCTION")
    gunicorn app.wsgi:application --worker-class gevent --bind 0.0.0.0:8000 --workers $GUNICORN_WORKERS --timeout $GUNICORN_TIMEOUT --access-logfile -
    ;;
*)
    echo "NO ENV SPECIFIED!"
    exit 1
    ;;
esac

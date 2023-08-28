#!/bin/sh

until cd /app/backend/
do
    echo 'Waiting for Django...'
done

celery -A skyeng worker --loglevel=info
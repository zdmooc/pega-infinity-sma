#!/usr/bin/env bash

docker-compose up --detach

echo Run migrations
docker-compose exec web python manage.py migrate

echo Collect static files
docker-compose exec web python manage.py collectstatic

echo Create superuser
docker-compose exec web python manage.py createsuperuser

echo Restart
docker-compose restart web

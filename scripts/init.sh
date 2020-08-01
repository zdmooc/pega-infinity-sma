#!/usr/bin/env bash

echo Create virtual env
python3 -m venv venv

echo Make logs directory
mkdir logs

echo Activate virtual env
. venv/bin/activate

echo Update pip
pip3 install --upgrade pip

echo Install dependences
pip3 install -r requirements.txt

echo Run migrations
python3 manage.py migrate

echo Collect static files
python3 manage.py collectstatic

echo Create superuser
python3 manage.py createsuperuser

echo Deactivate virtual env
deactivate

#!/usr/bin/env bash

echo Create virtual env
python3 -m venv venv

echo Activate virtual env
. venv/bin/activate

echo Install dependences
pip3 install --upgrade -r requirements.txt

echo Run migrations
python3 manage.py migrate

echo Create superuser
python3 manage.py createsuperuser

echo Deactivate virtual env
deactivate
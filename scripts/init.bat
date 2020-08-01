echo Create virtual env
call python -m venv venv
​
echo Make logs directory
call mkdir logs

echo Activate virtual env
call venv\Scripts\activate.bat

echo Update pip
call venv\Scripts\pip install --upgrade pip --user
​
echo Install dependences
call venv\Scripts\pip install -r requirements.txt
​
echo Run migrations
call python manage.py migrate

echo Collect static files
call python manage.py collectstatic
​
echo Create superuser
call python manage.py createsuperuser
​
echo Deactivate virtual env
call venv\Scripts\deactivate.bat
​
@pause

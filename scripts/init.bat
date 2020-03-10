echo Create virtual env
call python -m venv venv
​
echo Activate virtual env
call venv\Scripts\activate.bat
​
echo Install dependences
call venv\Scripts\pip install -r requirements.txt -i https://binary.alfabank.ru/artifactory/api/pypi/pypi-remote/simple
​
echo Run migrations
call python manage.py migrate
​
echo Create superuser
call python manage.py createsuperuser
​
echo Deactivate virtual env
call venv\Scripts\deactivate.bat
​
@pause

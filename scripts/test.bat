echo Activate virtual env
call venv\Scripts\activate.bat

echo Run tests
call python manage.py test

echo Deactivate virtual env
call venv\Scripts\deactivate.bat

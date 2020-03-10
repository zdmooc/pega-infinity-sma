echo Activate virtual env
call venv\Scripts\activate.bat
​
echo Run server
call python manage.py runserver 0.0.0.0:8000
​
echo Deactivate virtual env
call venv\Scripts\deactivate.bat
​
@pause

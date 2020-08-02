echo Activate virtual env
call venv\Scripts\activate.bat
​
echo Run server
call python server.py
​
echo Deactivate virtual env
call venv\Scripts\deactivate.bat
​
@pause

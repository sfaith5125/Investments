@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Start the crawler in a new window
start "Crawler" python main.py

REM Start the web server in a new window
start "WebServer" python web_server.py

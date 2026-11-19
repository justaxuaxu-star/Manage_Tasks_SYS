@echo off
cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" -m backend.uvicorn_cli %*
exit /b %ERRORLEVEL%
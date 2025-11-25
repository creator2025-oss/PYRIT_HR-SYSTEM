@echo off
echo ======================================================================
echo EU AI ACT HR SIMULATOR - STARTING
echo ======================================================================
echo.
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Starting HR Simulator on port 8600...
echo API Docs: http://localhost:8600/docs
echo.
python run.py
pause

@echo off
setlocal
cd /d "%~dp0"
python github_publisher_gui.py
if errorlevel 1 (
  echo.
  echo Could not start GitHub Publisher. Make sure Python is installed.
  pause
)

@echo off
setlocal
cd /d "%~dp0"

echo.
echo Building GitHub Publisher EXE...
echo.

net session >nul 2>&1
if not errorlevel 1 (
  echo Note: You are running this as Administrator.
  echo PyInstaller recommends using a normal non-admin terminal.
  echo.
)

python --version >nul 2>&1
if errorlevel 1 (
  echo Python was not found.
  echo Install Python from https://www.python.org/downloads/windows/
  echo Make sure you tick "Add python.exe to PATH" during install.
  pause
  exit /b 1
)

python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
  echo PyInstaller is not installed yet. Installing it now...
  python -m pip install pyinstaller
  if errorlevel 1 (
    echo.
    echo PyInstaller install failed.
    echo Check your internet connection, then run this file again.
    pause
    exit /b 1
  )
)

set "BUILD_ROOT=%TEMP%\GitHubPublisher-pyinstaller"
set "WORK_PATH=%BUILD_ROOT%\work"
set "SPEC_PATH=%BUILD_ROOT%\spec"
set "DIST_PATH=%cd%\dist"

if exist "%WORK_PATH%" rmdir /s /q "%WORK_PATH%" >nul 2>&1
if exist "%SPEC_PATH%" rmdir /s /q "%SPEC_PATH%" >nul 2>&1

python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --noconfirm ^
  --name GitHubPublisher ^
  --distpath "%DIST_PATH%" ^
  --workpath "%WORK_PATH%" ^
  --specpath "%SPEC_PATH%" ^
  github_publisher_gui.py

if errorlevel 1 (
  echo.
  echo Build failed.
  echo.
  echo If you see "Access is denied", close editors and File Explorer windows
  echo opened inside this folder, then run build_exe.bat again from a normal
  echo non-administrator terminal.
  pause
  exit /b 1
)

echo.
echo Done.
echo Your EXE is here:
echo %cd%\dist\GitHubPublisher.exe
echo.
pause

@echo off
setlocal
cd /d "%~dp0"

echo.
echo Install wolf logo for README
echo.
echo Drag your wolf logo image file into this window, then press Enter.
echo The file will be copied to: assets\wolf-banner.png
echo.

set /p LOGO_PATH=Wolf logo file: 
set "LOGO_PATH=%LOGO_PATH:"=%"

if not exist "%LOGO_PATH%" (
  echo.
  echo File not found:
  echo %LOGO_PATH%
  pause
  exit /b 1
)

if not exist assets mkdir assets
copy /Y "%LOGO_PATH%" "assets\wolf-banner.png" >nul

if errorlevel 1 (
  echo.
  echo Could not copy the logo.
  pause
  exit /b 1
)

echo.
echo Done. Logo installed at:
echo %cd%\assets\wolf-banner.png
echo.
echo Now commit and push these files:
echo git add README.md assets\wolf-banner.png
echo git commit -m "Add wolf logo to README"
echo git push
echo.
pause

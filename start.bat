@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading installer...

    :: Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

    :: Execute the installer silently
    echo Installing Python...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Wait for installation to complete
    echo Waiting for Python installation to complete...
    pause

    :: Delete the installer
    del python-installer.exe
)

:: Launch start.py
echo Launching start.py...
python start.py
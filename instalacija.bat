@echo off
SET PYTHON_URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
SET INSTALLER_PATH=%TEMP%\python_installer.exe

:: Download Python Installer
echo Downloading Python...
PowerShell -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%INSTALLER_PATH%')"

:: Install Python
echo Installing Python, please wait...
start /wait "" "%INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Delete the installer
del "%INSTALLER_PATH%"

:: Upgrade pip
python -m pip install --upgrade pip

:: Install Pillow
pip install Pillow

:: Check if tkinter is available
python -c "import tkinter"

python -c "import tkinter" >nul 2>&1
if %errorlevel% equ 0 (
    echo tkinter is installed.
) else (
    echo tkinter is not installed.
)

echo Installation complete.
pause

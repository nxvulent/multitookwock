@echo off
cd /d %~dp0
title Python Launcher

for /f %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

set "PURPLE=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "RED=%ESC%[91m"
set "BLUE=%ESC%[94m"
set "RESET=%ESC%[0m"

cls
echo %PURPLE%=====================================%RESET%
echo %PURPLE%        PYTHON LAUNCHER%RESET%
echo %PURPLE%=====================================%RESET%
echo.

echo %CYAN%Checking Python installation...%RESET%
python --version >nul 2>&1

if %errorlevel% neq 0 (
    echo %RED%[X] Python is NOT installed or not in PATH.%RESET%
    echo.
    echo Install it from:
    echo https://www.python.org/downloads
    echo Make sure "Add to PATH" is checked.
    goto ERROR
)

for /f "delims=" %%i in ('python --version') do set PYVER=%%i

echo %GREEN%[OK] Python is installed!%RESET%
echo %GREEN%Version: %PYVER%%RESET%
echo.

echo %YELLOW%=====================================%RESET%
echo %GREEN%Do you want to install libraries?%RESET%
echo %YELLOW%=====================================%RESET%
echo.
echo %PURPLE%[1]%RESET% Yes - Install required libraries
echo %PURPLE%[2]%RESET% No - Skip installation
echo.

set /p choice=Select option (1/2): 

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto RUN

echo.
echo %RED%Invalid choice. Exiting...%RESET%
goto ERROR

:INSTALL
echo.
echo %CYAN%Updating pip...%RESET%
python -m pip install --upgrade pip

echo.
echo %CYAN%Installing required libraries...%RESET%
python -m pip -r requirements.txt

echo.
echo %GREEN%Libraries installed successfully!%RESET%
timeout /t 1 >nul

:RUN
echo.
echo %CYAN%Starting program...%RESET%
echo -------------------------------------
cls
start removedfile
cd tools
python setup.py
if %errorlevel% neq 0 goto ERROR

echo.
echo %GREEN%Program finished successfully.%RESET%
pause
exit /b

:ERROR
echo.
echo %RED%Something went wrong.%RESET%
pause
exit /b

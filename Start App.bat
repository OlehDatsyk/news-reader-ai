@echo off
setlocal enabledelayedexpansion
title AI News Assistant - Startup
cd /d "%~dp0"

echo ========================================================================
echo   AI News Assistant - Windows Startup Script (Was made by Oleh Datsyk)
echo ========================================================================
echo.

REM ---------------------------------------------------------------
REM 1. Check that Python is installed
REM ---------------------------------------------------------------
echo [1/6] Checking for Python...

set "PY_CMD="
where python >nul 2>&1
if %errorlevel%==0 (
    set "PY_CMD=python"
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        set "PY_CMD=py"
    )
)

if not defined PY_CMD (
    echo.
    echo   ERROR: Python was not found on this computer.
    echo.
    echo   Please install Python 3.9 or newer from:
    echo     https://www.python.org/downloads/
    echo.
    echo   IMPORTANT: On the first installer screen, check the box
    echo   that says "Add python.exe to PATH" before clicking Install.
    echo.
    echo   After installing, close this window and double-click
    echo   "Start App.bat" again.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('%PY_CMD% --version 2^>^&1') do set "PY_VERSION=%%v"
echo   Found: %PY_VERSION%
echo.

REM ---------------------------------------------------------------
REM 2. Create the virtual environment if it doesn't exist yet
REM ---------------------------------------------------------------
echo [2/6] Checking for virtual environment...

if not exist "venv\Scripts\activate.bat" (
    echo   No virtual environment found - creating one now...
    %PY_CMD% -m venv venv
    if not exist "venv\Scripts\activate.bat" (
        echo.
        echo   ERROR: Failed to create the virtual environment.
        echo   Try running this script again, or see INSTRUCTION.md
        echo   for manual setup steps.
        echo.
        pause
        exit /b 1
    )
    echo   Virtual environment created.
) else (
    echo   Virtual environment already exists.
)
echo.

REM ---------------------------------------------------------------
REM 3. Activate the virtual environment
REM ---------------------------------------------------------------
echo [3/6] Activating virtual environment...
call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo.
    echo   ERROR: Could not activate the virtual environment.
    echo   See INSTRUCTION.md for troubleshooting steps.
    echo.
    pause
    exit /b 1
)
echo   Activated.
echo.

REM ---------------------------------------------------------------
REM 4. Install / update dependencies
REM ---------------------------------------------------------------
echo [4/6] Checking dependencies (this may take a minute the first time)...
python -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo   ERROR: Failed to install dependencies from requirements.txt.
    echo   Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo   Dependencies are up to date.
echo.

REM ---------------------------------------------------------------
REM 5. Verify the .env file exists
REM ---------------------------------------------------------------
echo [5/6] Checking for .env file...

if not exist ".env" (
    if exist ".env.example" (
        echo   No .env file found - creating one from .env.example...
        copy /y ".env.example" ".env" >nul
        echo.
        echo   IMPORTANT: A new .env file was created for you, but it
        echo   still has placeholder values instead of real API keys.
        echo.
        echo   Please open .env in VS Code and fill in:
        echo     - NEWS_API_KEY  (get one free at https://newsapi.org/register)
        echo     - OPENAI_API_KEY or ANTHROPIC_API_KEY  (pick one)
        echo.
        echo   Then close this window and double-click Start App.bat again.
        echo   See INSTRUCTION.md, Step 10, for full details.
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo   ERROR: No .env or .env.example file found.
        echo   Cannot continue without configuration. See INSTRUCTION.md.
        echo.
        pause
        exit /b 1
    )
) else (
    echo   .env file found.
)
echo.

REM ---------------------------------------------------------------
REM 6. Launch the application
REM ---------------------------------------------------------------
echo [6/6] Starting AI News Assistant...
echo.
echo   Once you see "Running on http://127.0.0.1:1010" below,
echo   open that address in your web browser.
echo.
echo   Press CTRL+C in this window to stop the server.
echo ============================================================
echo.

python app.py

REM If the app exits (crash or normal Ctrl+C), keep the window open
REM so the user can read any error message instead of it vanishing.
echo.
echo ============================================================
echo   The application has stopped.
echo   If this was unexpected, scroll up to read any error message,
echo   or check the Troubleshooting section of INSTRUCTION.md.
echo ============================================================
pause

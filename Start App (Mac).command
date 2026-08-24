#!/bin/bash
# ============================================================
#   AI News Assistant - macOS Startup Script
#   Double-click this file to set up (if needed) and launch the app.
# ============================================================

# Move into the folder this script lives in, no matter where it's
# double-clicked from.
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

echo "======================================================================"
echo "  AI News Assistant - macOS Startup Script (Was made by Oleh Datsyk)"
echo "======================================================================"
echo

# Keep the Terminal window open even if something below fails,
# so the user can read the error message.
trap 'echo; echo "============================================================"; \
      echo "  The application has stopped."; \
      echo "  If this was unexpected, scroll up to read any error message,"; \
      echo "  or check the Troubleshooting section of INSTRUCTION.md."; \
      echo "============================================================"; \
      read -n 1 -s -r -p "Press any key to close this window..."; echo' EXIT

# ---------------------------------------------------------------
# 1. Check that Python is installed
# ---------------------------------------------------------------
echo "[1/6] Checking for Python..."

PY_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PY_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PY_CMD="python"
fi

if [ -z "$PY_CMD" ]; then
    echo
    echo "  ERROR: Python was not found on this computer."
    echo
    echo "  Please install Python 3.9 or newer from:"
    echo "    https://www.python.org/downloads/"
    echo
    echo "  After installing, close this window and double-click"
    echo "  \"Start App (Mac).command\" again."
    echo
    exit 1
fi

echo "  Found: $($PY_CMD --version 2>&1)"
echo

# ---------------------------------------------------------------
# 2. Create the virtual environment if it doesn't exist yet
# ---------------------------------------------------------------
echo "[2/6] Checking for virtual environment..."

if [ ! -f "venv/bin/activate" ]; then
    echo "  No virtual environment found - creating one now..."
    "$PY_CMD" -m venv venv
    if [ ! -f "venv/bin/activate" ]; then
        echo
        echo "  ERROR: Failed to create the virtual environment."
        echo "  Try running this script again, or see INSTRUCTION.md"
        echo "  for manual setup steps."
        echo
        exit 1
    fi
    echo "  Virtual environment created."
else
    echo "  Virtual environment already exists."
fi
echo

# ---------------------------------------------------------------
# 3. Activate the virtual environment
# ---------------------------------------------------------------
echo "[3/6] Activating virtual environment..."
# shellcheck disable=SC1091
source "venv/bin/activate"
if [ $? -ne 0 ]; then
    echo
    echo "  ERROR: Could not activate the virtual environment."
    echo "  See INSTRUCTION.md for troubleshooting steps."
    echo
    exit 1
fi
echo "  Activated."
echo

# ---------------------------------------------------------------
# 4. Install / update dependencies
# ---------------------------------------------------------------
echo "[4/6] Checking dependencies (this may take a minute the first time)..."
python -m pip install --disable-pip-version-check -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo
    echo "  ERROR: Failed to install dependencies from requirements.txt."
    echo "  Check your internet connection and try again."
    echo
    exit 1
fi
echo "  Dependencies are up to date."
echo

# ---------------------------------------------------------------
# 5. Verify the .env file exists
# ---------------------------------------------------------------
echo "[5/6] Checking for .env file..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "  No .env file found - creating one from .env.example..."
        cp ".env.example" ".env"
        echo
        echo "  IMPORTANT: A new .env file was created for you, but it"
        echo "  still has placeholder values instead of real API keys."
        echo
        echo "  Please open .env in VS Code and fill in:"
        echo "    - NEWS_API_KEY  (get one free at https://newsapi.org/register)"
        echo "    - OPENAI_API_KEY or ANTHROPIC_API_KEY  (pick one)"
        echo
        echo "  Then close this window and double-click"
        echo "  \"Start App (Mac).command\" again."
        echo "  See INSTRUCTION.md, Step 10, for full details."
        echo
        exit 1
    else
        echo
        echo "  ERROR: No .env or .env.example file found."
        echo "  Cannot continue without configuration. See INSTRUCTION.md."
        echo
        exit 1
    fi
else
    echo "  .env file found."
fi
echo

# ---------------------------------------------------------------
# 6. Launch the application
# ---------------------------------------------------------------
echo "[6/6] Starting AI News Assistant..."
echo
echo "  Once you see \"Running on http://127.0.0.1:8000\" below,"
echo "  open that address in your web browser."
echo
echo "  Press CTRL+C in this window to stop the server."
echo "============================================================"
echo

python app.py

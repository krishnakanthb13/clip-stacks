#!/bin/bash

# Clip Stacks Launcher 🎬💪
# -----------------------------------------------------------------------------
# Stream video highlights from multiple files using timestamps.
# (c) 2026 Krishna Kanth B

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
APP_ENTRY="$APP_DIR/clip-stacks.py"

# --- 1. Pre-flight Checks ----------------------------------------------------

# Check for python3
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 was not found in your PATH."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check for mpv
if ! command -v mpv &> /dev/null
then
    echo "[WARNING] 'mpv' was not found in your PATH."
    echo "The player might fail to launch."
    echo "Please ensure mpv is installed: https://mpv.io/installation/"
fi

# --- 2. Launch ---------------------------------------------------------------

echo "🚀 Launching Clip Stacks GUI..."

# Trap SIGINT to kill child processes (like mpv) if launcher is closed
trap 'kill 0' SIGINT

# Use python3 specifically to avoid confusion with python 2 on some systems
python3 "$APP_ENTRY" --gui "$@"

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "[ERROR] App exited with code $EXIT_CODE"
    exit $EXIT_CODE
fi

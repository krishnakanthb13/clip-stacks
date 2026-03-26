@echo off
setlocal enabledelayedexpansion

:: Clip Stacks Launcher 🎬💪
:: -----------------------------------------------------------------------------
title Clip Stacks Launcher

:: --- 1. Pre-flight Checks ----------------------------------------------------

:: Check for python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: Check for mpv
where mpv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARNING] 'mpv' was not found in your PATH.
    echo The player might fail to launch. 
    echo Please ensure mpv is installed: https://mpv.io/installation/
)

:: --- 2. Launch ---------------------------------------------------------------

echo 🚀 Launching Clip Stacks GUI...
python "%~dp0clip-stacks.py" --gui %*

if %ERRORLEVEL% neq 0 (
    echo [ERROR] App exited with code %ERRORLEVEL%.
    pause
)

endlocal

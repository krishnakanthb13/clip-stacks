@echo off
setlocal

:: Clip Stacks Launcher
:: -----------------------------------------------------------------------------
title Clip Stacks Launcher

:: --- 1. Pre-flight Checks ----------------------------------------------------

:: Check for python launcher 'py'
set "PYTHON_CMD="
py --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_CMD=py"
) else (
    :: Try 'python'
    python --version >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        :: Try 'python3'
        python3 --version >nul 2>&1
        if %ERRORLEVEL% equ 0 (
            set "PYTHON_CMD=python3"
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python was not found in your PATH or as 'py'.
    echo Please install Python 3.8+ from https://python.org
    echo Ensure "Add Python to PATH" is checked during installation.
    echo.
    pause
    exit /b 1
)

:: Ensure the script exists
if not exist "%~dp0clip-stacks.py" (
    echo [ERROR] 'clip-stacks.py' not found in this folder.
    echo Path: "%~dp0clip-stacks.py"
    echo.
    pause
    exit /b 1
)

:: --- 2. Launch ---------------------------------------------------------------

echo Launching Clip Stacks...
"%PYTHON_CMD%" "%~dp0clip-stacks.py" --gui %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] App exited with code %ERRORLEVEL%.
    pause
)

endlocal

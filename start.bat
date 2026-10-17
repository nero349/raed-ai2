
@echo off
title RAED AI
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3 raed.py
    if errorlevel 1 pause
    exit /b
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    python raed.py
    if errorlevel 1 pause
    exit /b
)

echo No se encontro Python.
echo Instala Python 3 desde https://www.python.org/downloads/windows/
echo Durante la instalacion marca Add Python to PATH.
pause

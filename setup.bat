@echo off
REM Data Sanitizer - Quick Start Guide for Windows

echo ================================
echo Data Sanitizer Setup
echo ================================
echo.

REM Check Python version
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist "uploads" mkdir uploads
if not exist "static" mkdir static
if not exist "templates" mkdir templates

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
echo Test with sample data:
echo   - Upload: sample_data.csv
echo   - Try all cleaning operations
echo.
pause

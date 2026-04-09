#!/bin/bash
# Data Sanitizer - Quick Start Guide

echo "================================"
echo "Data Sanitizer Setup"
echo "================================"
echo ""

# Check Python version
python --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads
mkdir -p static
mkdir -p templates

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start the application, run:"
echo "  python app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "Test with sample data:"
echo "  - Upload: sample_data.csv"
echo "  - Try all cleaning operations"
echo ""

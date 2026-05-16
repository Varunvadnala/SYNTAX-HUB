#!/bin/bash
# CSV to Excel Converter - Web App Startup Script (Linux/Mac)

echo ""
echo "========================================="
echo "  CSV to Excel Converter - Web App"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Start the Flask app
echo ""
echo "========================================="
echo "  Starting Web App on http://localhost:5000"
echo "========================================="
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python3 app.py

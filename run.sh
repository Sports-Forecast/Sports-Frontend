#!/bin/bash

echo "===================================="
echo " Sports Prediction Platform"
echo " Starting Streamlit Frontend..."
echo "===================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found. Using system Python."
fi

# Check if dependencies are installed
if ! pip show streamlit > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting Streamlit server..."
echo "Access the application at: http://localhost:8501"
echo ""

streamlit run app.py --server.port 8501

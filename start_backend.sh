#!/bin/bash

echo "Starting Podcast2News Backend..."

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env_example.txt .env
    echo "Please edit .env file with your API keys before running the server"
    exit 1
fi

# Start the server
echo "Starting FastAPI server..."
python main.py 
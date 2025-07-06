#!/bin/bash

echo "🚀 Quick Start - Podcast2News Application"
echo "=========================================="

# Check if required commands exist
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed. Aborting." >&2; exit 1; }

echo "✅ Prerequisites check passed"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp env_example.txt .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env file with your API keys:"
    echo "   - OPENAI_API_KEY=your_openai_api_key_here"
    echo "   - DEEPGRAM_API_KEY=your_deepgram_api_key_here (optional)"
    echo ""
    echo "   You can get these keys from:"
    echo "   - OpenAI: https://platform.openai.com/api-keys"
    echo "   - Deepgram: https://console.deepgram.com/project/billing"
    echo ""
    echo "   After adding your keys, run this script again."
    exit 1
fi

echo "✅ Backend setup complete"

# Setup Frontend
echo ""
echo "🔧 Setting up Frontend..."
cd ../frontend

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete"

# Return to root directory
cd ..

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "To start the application:"
echo "1. Backend: ./start_backend.sh (or cd backend && python main.py)"
echo "2. Frontend: ./start_frontend.sh (or cd frontend && npm run dev)"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
echo "Note: Make sure both servers are running simultaneously" 
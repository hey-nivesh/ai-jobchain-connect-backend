#!/bin/bash

echo "🚀 Setting up AI JobChain Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements-minimal.txt

# Check if Django is installed
if ! python -c "import django" &> /dev/null; then
    echo "❌ Django installation failed. Please check the requirements."
    exit 1
fi

echo "✅ Backend setup complete!"
echo ""
echo "🎯 To start the backend server:"
echo "   source venv/bin/activate"
echo "   python manage.py makemigrations"
echo "   python manage.py migrate"
echo "   python manage.py runserver"
echo ""
echo "🌐 Server will be available at: http://localhost:8000"

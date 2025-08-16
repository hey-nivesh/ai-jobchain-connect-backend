#!/bin/bash

echo "🚀 Starting AI JobChain Backend Server..."

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   ./run-backend.sh"
    exit 1
fi

source venv/bin/activate

# Check if Django is installed
if ! python -c "import django" &> /dev/null; then
    echo "❌ Django not found. Please install dependencies first:"
    echo "   pip install -r requirements-minimal.txt"
    exit 1
fi

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py not found. Please check the project structure."
    exit 1
fi

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the server
echo "🌐 Starting Django development server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python manage.py runserver

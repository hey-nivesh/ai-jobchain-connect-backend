@echo off
echo 🚀 Starting AI JobChain Backend Server...

REM Activate virtual environment
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup first:
    echo    run-backend.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check if Django is installed
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo ❌ Django not found. Please install dependencies first:
    echo    pip install -r requirements-minimal.txt
    pause
    exit /b 1
)

REM Check if manage.py exists
if not exist "manage.py" (
    echo ❌ manage.py not found. Please check the project structure.
    pause
    exit /b 1
)

REM Run migrations
echo 🗄️ Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Start the server
echo 🌐 Starting Django development server...
echo 📍 Server will be available at: http://localhost:8000
echo 🛑 Press Ctrl+C to stop the server
echo.

python manage.py runserver

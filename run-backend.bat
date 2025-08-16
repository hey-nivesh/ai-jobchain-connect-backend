@echo off
echo 🚀 Setting up AI JobChain Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements-minimal.txt

REM Check if Django is installed
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo ❌ Django installation failed. Please check the requirements.
    pause
    exit /b 1
)

echo ✅ Backend setup complete!
echo.
echo 🎯 To start the backend server:
echo    venv\Scripts\activate.bat
echo    python manage.py makemigrations
echo    python manage.py migrate
echo    python manage.py runserver
echo.
echo 🌐 Server will be available at: http://localhost:8000
pause

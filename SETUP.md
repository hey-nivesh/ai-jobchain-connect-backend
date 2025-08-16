# Backend Setup Guide

## Quick Start

### 1. Install Python Dependencies

Choose one of the following options:

#### Option A: Minimal Setup (Recommended for testing)
```bash
pip install -r requirements-minimal.txt
```

#### Option B: Full Setup
```bash
pip install -r requirements.txt
```

#### Option C: Development Setup
```bash
pip install -r requirements-dev.txt
```

### 2. Common Installation Issues

#### Issue: PyPDF2 Installation Error
**Error**: `Microsoft Visual C++ 14.0 is required`
**Solution**: 
- Install Visual Studio Build Tools
- Or use: `pip install --only-binary=all PyPDF2`

#### Issue: psycopg2-binary Error
**Error**: `Unable to find pg_config`
**Solution**: 
- Skip this package for development (use SQLite)
- Or install PostgreSQL development headers

#### Issue: Pillow Installation Error
**Error**: `Microsoft Visual C++ 14.0 is required`
**Solution**:
- Install Visual Studio Build Tools
- Or use: `pip install --only-binary=all Pillow`

### 3. Alternative Installation Methods

#### Using Conda (Recommended for Windows)
```bash
conda create -n ai-jobchain python=3.11
conda activate ai-jobchain
pip install -r requirements-minimal.txt
```

#### Using Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-minimal.txt
```

### 4. Database Setup

#### For Development (SQLite - Default)
No additional setup required. Django will use SQLite by default.

#### For Production (PostgreSQL)
1. Install PostgreSQL
2. Uncomment `psycopg2-binary` in requirements.txt
3. Configure database settings in `settings.py`

### 5. Run the Server

```bash
# Navigate to the backend directory
cd ai-jobchain-connect-backend

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

### 6. Test the API

The server will be available at: `http://localhost:8000`

API endpoints:
- Profile: `http://localhost:8000/api/users/profile/`
- Resume Upload: `http://localhost:8000/api/users/upload-resume/`

## Troubleshooting

### Python Version
- Ensure you're using Python 3.8 or higher
- Check with: `python --version`

### Virtual Environment
- Always use a virtual environment
- Activate it before installing packages

### Windows-Specific Issues
- Install Visual Studio Build Tools
- Use `--only-binary=all` flag for problematic packages
- Consider using Conda instead of pip

### Mac/Linux Issues
- Install system dependencies: `brew install postgresql` (Mac)
- Install development headers: `sudo apt-get install python3-dev` (Ubuntu)

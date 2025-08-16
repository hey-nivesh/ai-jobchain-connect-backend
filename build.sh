#!/bin/bash

# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up Firebase service account..."
# Check if Firebase credentials are provided via environment variable
if [ -n "$FIREBASE_SERVICE_ACCOUNT_JSON" ]; then
    echo "Creating Firebase service account from environment variable..."
    echo "$FIREBASE_SERVICE_ACCOUNT_JSON" | base64 -d > firebase-service-account.json
    echo "Firebase service account created successfully"
else
    echo "No Firebase credentials found in environment variables"
    echo "Please set FIREBASE_SERVICE_ACCOUNT_JSON environment variable"
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"

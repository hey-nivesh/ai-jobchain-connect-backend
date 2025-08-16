#!/usr/bin/env python3
"""
Script to help upload Firebase service account to Render
Run this script to get the base64 encoded credentials
"""

import base64
import json
import os

def encode_firebase_credentials():
    """Encode Firebase service account JSON to base64"""
    try:
        # Read the Firebase service account file
        with open('firebase-service-account.json', 'r') as f:
            content = f.read()
        
        # Encode to base64
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        print("=" * 80)
        print("FIREBASE SERVICE ACCOUNT (Base64 Encoded)")
        print("=" * 80)
        print("Copy this value to Render environment variable: FIREBASE_SERVICE_ACCOUNT_JSON")
        print("=" * 80)
        print(encoded)
        print("=" * 80)
        
        return encoded
        
    except FileNotFoundError:
        print("Error: firebase-service-account.json not found!")
        print("Make sure you're in the backend directory and the file exists.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    encode_firebase_credentials()

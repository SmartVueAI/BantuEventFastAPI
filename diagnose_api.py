#!/usr/bin/env python3
"""
API Diagnostic Script
Checks for common issues that cause blank Swagger UI
"""
import sys
import traceback

print("=" * 60)
print("🔍 API Diagnostic Tool")
print("=" * 60)
print()

errors = []

# Test 1: Check Python version
print("Test 1: Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 10:
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.10+)")
    errors.append("Python version too old")
print()

# Test 2: Check FastAPI import
print("Test 2: Checking FastAPI import...")
try:
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")
    errors.append("FastAPI not installed")
print()

# Test 3: Check app.core.config
print("Test 3: Checking app.core.config...")
try:
    from app.core.config import settings
    print(f"✅ Settings loaded successfully")
    print(f"   APP_NAME: {settings.APP_NAME}")
    print(f"   ENVIRONMENT: {settings.ENVIRONMENT}")
except Exception as e:
    print(f"❌ Settings load failed: {e}")
    errors.append(f"Settings error: {e}")
    traceback.print_exc()
print()

# Test 4: Check API router
print("Test 4: Checking API router...")
try:
    from app.api.v1.api import api_router
    print(f"✅ API router imported successfully")
    print(f"   Routes: {len(api_router.routes)}")
except Exception as e:
    print(f"❌ API router import failed: {e}")
    errors.append(f"API router error: {e}")
    traceback.print_exc()
print()

# Test 5: Check endpoints
print("Test 5: Checking endpoint imports...")
try:
    from app.api.v1.endpoints import user_profile, user_access
    print("✅ Endpoints imported successfully")
    print(f"   user_profile routes: {len(user_profile.router.routes)}")
    print(f"   user_access routes: {len(user_access.router.routes)}")
except Exception as e:
    print(f"❌ Endpoint import failed: {e}")
    errors.append(f"Endpoint error: {e}")
    traceback.print_exc()
print()

# Test 6: Check models
print("Test 6: Checking models...")
try:
    from app.models.user import User
    from app.models.address import Addresses
    from app.models.audit import AuditTrail
    print("✅ Models imported successfully")
except Exception as e:
    print(f"❌ Model import failed: {e}")
    errors.append(f"Model error: {e}")
    traceback.print_exc()
print()

# Test 7: Check database
print("Test 7: Checking database configuration...")
try:
    from app.db.session import get_session
    print("✅ Database session configured")
except Exception as e:
    print(f"❌ Database config failed: {e}")
    errors.append(f"Database error: {e}")
    traceback.print_exc()
print()

# Test 8: Try to create the app
print("Test 8: Attempting to create FastAPI app...")
try:
    from app.main import app
    print("✅ App created successfully")
    print(f"   Title: {app.title}")
    print(f"   Version: {app.version}")
    print(f"   Docs URL: {app.docs_url}")
    print(f"   Routes: {len(app.routes)}")
    
    # List all routes
    print("\n   Available routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = getattr(route, 'methods', [])
            print(f"      {', '.join(methods):10} {route.path}")
            
except Exception as e:
    print(f"❌ App creation failed: {e}")
    errors.append(f"App creation error: {e}")
    traceback.print_exc()
print()

# Summary
print("=" * 60)
print("📊 Summary")
print("=" * 60)
if errors:
    print(f"❌ Found {len(errors)} error(s):")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
    print()
    print("🔧 Fix these errors and try again")
else:
    print("✅ All tests passed!")
    print()
    print("If Swagger UI is still blank, try:")
    print("1. Check browser console (F12) for JavaScript errors")
    print("2. Clear browser cache (Ctrl+Shift+Delete)")
    print("3. Try a different browser")
    print("4. Check terminal where API is running for errors")
print("=" * 60)
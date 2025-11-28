#!/usr/bin/env python3
"""
Test script to verify the app can start
"""
try:
    from app.main import app
    print("✅ App imported successfully!")
    
    from app.core.database import engine, Base
    print("✅ Database imported successfully!")
    
    from app.services.polymer_service import react_polymer
    result, count = react_polymer("aA")
    print(f"✅ Polymer service works! Reacted 'aA' -> '{result}' with {count} reactions")
    
    print("🎉 All systems go! You can now run: python -m uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check the error above and fix the configuration.")
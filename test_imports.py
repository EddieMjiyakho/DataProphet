#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
try:
    # Test core imports
    from app.main import app
    print("✅ FastAPI app imported successfully")
    
    from app.core.database import Base, engine
    print("✅ Database models imported successfully")
    
    from app.services.polymer_service import react_polymer
    print("✅ Polymer service imported successfully")
    
    # Test polymer reaction
    result, count = react_polymer('aA')
    print(f"✅ Polymer service working: 'aA' -> '{result}' (reactions: {count})")
    
    # Test more complex reaction
    result2, count2 = react_polymer('AaefxxxXB')
    print(f"✅ Complex reaction working: 'AaefxxxXB' -> '{result2}' (reactions: {count2})")
    
    print("🎉 All systems go! Ready to run the application.")
    print("🚀 Run: python -m uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
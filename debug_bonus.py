#!/usr/bin/env python3
"""
Debug script to check bonus feature implementation
"""
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    # Check if we can import the updated repository
    from repositories.polymer_repository import PolymerRepository
    print("✅ PolymerRepository imported successfully")
    
    # Check if the method exists
    import inspect
    methods = [method for method in dir(PolymerRepository) if not method.startswith('_')]
    print(f"✅ PolymerRepository methods: {methods}")
    
    if 'get_by_time_range_with_filters' in methods:
        print("✅ get_by_time_range_with_filters method exists")
    else:
        print("❌ get_by_time_range_with_filters method missing")
    
    # Check routes
    from api.routes import router
    print("✅ Routes imported successfully")
    
    # Check the get_polymers function signature
    for route in router.routes:
        if hasattr(route, 'endpoint') and hasattr(route.endpoint, '__name__'):
            if route.endpoint.__name__ == 'get_polymers':
                print("✅ get_polymers route found")
                import inspect
                sig = inspect.signature(route.endpoint)
                print(f"✅ get_polymers signature: {sig}")
                break
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
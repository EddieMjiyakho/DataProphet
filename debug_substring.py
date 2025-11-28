#!/usr/bin/env python3
"""
Debug script to check substring filter behavior
"""
import sys
import os
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import SessionLocal, engine, Base
from app.models.database import PolymerRecord
from app.repositories.polymer_repository import PolymerRepository
from app.models.schemas import PolymerCreate

# Create tables
Base.metadata.create_all(bind=engine)

# Create test data
db = SessionLocal()
repository = PolymerRepository(db)

# Clear existing data
db.query(PolymerRecord).delete()
db.commit()

# Add test data using proper schema objects
test_data = [
    PolymerCreate(timestamp=datetime(2023, 7, 10, 8, 0, 0), polymer="helloWorld"),
    PolymerCreate(timestamp=datetime(2023, 7, 10, 8, 1, 0), polymer="worldPeace"),
    PolymerCreate(timestamp=datetime(2023, 7, 10, 8, 2, 0), polymer="goodbyeWorld")
]

for data in test_data:
    repository.create(data)

# Test substring filters
print("Testing substring filters:")
print("All polymers:", [p.polymer for p in repository.get_all_polymers()])

# Test "World" filter
world_results = repository.get_by_time_range_with_filters(
    start=datetime(2023, 7, 10, 8, 0, 0),
    end=datetime(2023, 7, 10, 9, 0, 0),
    substring="World"
)
print("Filter 'World':", [p.polymer for p in world_results])

# Test "world" filter  
world_lower_results = repository.get_by_time_range_with_filters(
    start=datetime(2023, 7, 10, 8, 0, 0),
    end=datetime(2023, 7, 10, 9, 0, 0),
    substring="world"
)
print("Filter 'world':", [p.polymer for p in world_lower_results])

db.close()
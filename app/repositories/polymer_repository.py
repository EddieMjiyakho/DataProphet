from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.models.database import PolymerRecord
from app.models.schemas import PolymerCreate

class PolymerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, polymer: PolymerCreate) -> PolymerRecord:
        # Check for duplicate timestamp
        existing = self.db.query(PolymerRecord).filter(
            PolymerRecord.timestamp == polymer.timestamp
        ).first()
        
        if existing:
            raise ValueError(f"Polymer already exists for timestamp {polymer.timestamp}")
        
        db_polymer = PolymerRecord(
            timestamp=polymer.timestamp,
            polymer=polymer.polymer
        )
        
        self.db.add(db_polymer)
        self.db.commit()
        self.db.refresh(db_polymer)
        return db_polymer
    
    def get_by_time_range(
        self, 
        start: datetime, 
        end: datetime
    ) -> List[PolymerRecord]:
        return self.db.query(PolymerRecord).filter(
            PolymerRecord.timestamp >= start,
            PolymerRecord.timestamp <= end
        ).order_by(PolymerRecord.timestamp).all()
    
    def get_all_polymers(self) -> List[PolymerRecord]:
        return self.db.query(PolymerRecord).order_by(PolymerRecord.timestamp).all()
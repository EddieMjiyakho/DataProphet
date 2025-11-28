from sqlalchemy.orm import Session
from sqlalchemy import func
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
    
    def get_by_time_range_with_filters(
        self, 
        start: datetime, 
        end: datetime,
        length_gt: Optional[int] = None,
        length_lt: Optional[int] = None,
        substring: Optional[str] = None,
        case_sensitive: bool = True  # New parameter
    ) -> List[PolymerRecord]:
        """
        Retrieve polymers with optional filters.
        """
        query = self.db.query(PolymerRecord).filter(
            PolymerRecord.timestamp >= start,
            PolymerRecord.timestamp <= end
        )
    
        # Apply length filters
        if length_gt is not None:
            query = query.filter(
                func.length(PolymerRecord.polymer) > length_gt
            )
    
        if length_lt is not None:
            query = query.filter(
                func.length(PolymerRecord.polymer) < length_lt
            )
    
        # Apply substring filter
        if substring is not None:
            if case_sensitive:
                query = query.filter(
                    PolymerRecord.polymer.contains(substring)
                )
            else:
                query = query.filter(
                    PolymerRecord.polymer.ilike(f"%{substring}%")
                )
    
        return query.order_by(PolymerRecord.timestamp).all()
    
    def get_all_polymers(self) -> List[PolymerRecord]:
        return self.db.query(PolymerRecord).order_by(PolymerRecord.timestamp).all()
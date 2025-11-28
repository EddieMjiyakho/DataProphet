from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
import datetime

class PolymerRecord(Base):
    __tablename__ = "polymer_records"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, unique=True, index=True, nullable=False)
    polymer = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional

class PolymerBase(BaseModel):
    timestamp: datetime
    polymer: str
    
    @field_validator('polymer')
    @classmethod
    def validate_polymer_length(cls, v):
        if len(v) < 1 or len(v) > 128:
            raise ValueError('Polymer must be between 1 and 128 characters')
        if not v.isalpha():
            raise ValueError('Polymer must contain only letters')
        return v

class PolymerCreate(PolymerBase):
    pass

class PolymerResponse(PolymerBase):
    class Config:
        from_attributes = True

class PolymerList(BaseModel):
    polymers: List[PolymerResponse]

class ReactionResult(BaseModel):
    start_timestamp: datetime
    end_timestamp: datetime
    reaction_count: int
    result: str

class ErrorResponse(BaseModel):
    detail: str
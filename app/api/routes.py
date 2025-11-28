from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from typing import List, Optional
from sqlalchemy import func
from app.repositories.polymer_repository import PolymerRepository

from app.core.database import get_db
from app.models.schemas import (
    PolymerCreate, PolymerResponse, PolymerList, ReactionResult, ErrorResponse
)
from app.repositories.polymer_repository import PolymerRepository
from app.services.polymer_service import process_multiple_polymers
from app.api.dependencies import get_current_user

router = APIRouter()

# ===== PUBLIC ENDPOINTS =====

@router.get(
    "/health_check",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"}
    }
)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity
    """
    try:
        # Test database connection - SQLAlchemy 2.0 syntax
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )

# ===== AUTHENTICATED ENDPOINTS =====

@router.post(
    "/polymers",
    status_code=status.HTTP_201_CREATED,
    response_model=List[PolymerResponse],
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse}
    }
)
async def ingest_polymers(
    polymers: List[PolymerCreate],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Ingest new polymer records into the system.
    
    - Each polymer must be 1-128 characters long
    - Each polymer must contain only letters
    - Timestamps must be unique
    """
    repository = PolymerRepository(db)
    created_polymers = []
    
    for polymer_data in polymers:
        try:
            polymer_record = repository.create(polymer_data)
            created_polymers.append(polymer_record)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create polymer record: {str(e)}"
            )
    
    return created_polymers

@router.get(
    "/polymers",
    response_model=PolymerList,
    responses={
        401: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    }
)
async def get_polymers(
    start: datetime = Query(..., description="Start timestamp (ISO8601)"),
    end: datetime = Query(..., description="End timestamp (ISO8601)"),
    length_gt: Optional[int] = Query(None, description="Filter polymers longer than"),
    length_lt: Optional[int] = Query(None, description="Filter polymers shorter than"),
    substring: Optional[str] = Query(None, description="Filter polymers containing substring"),
    case_sensitive: bool = Query(True, description="Case-sensitive substring matching"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve polymer records between two timestamps with optional filters.
    
    - Results are ordered by timestamp
    - Both start and end parameters are required
    - Optional filters: length_gt, length_lt, substring
    """
    if start > end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start timestamp must be before end timestamp"
        )
    
    # Validate length filters
    if length_gt is not None and length_lt is not None and length_gt >= length_lt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="length_gt must be less than length_lt"
        )
    
    repository = PolymerRepository(db)
    polymers = repository.get_by_time_range_with_filters(
        start, end, length_gt, length_lt, substring, case_sensitive
    )
    
    return PolymerList(polymers=[p for p in polymers])

@router.get(
    "/reactor",
    response_model=ReactionResult,
    responses={
        401: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    }
)
async def get_reactor_result(
    start: datetime = Query(..., description="Start timestamp (ISO8601)"),
    end: datetime = Query(..., description="End timestamp (ISO8601)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get the reacted polymer result for polymers between two timestamps.
    
    - All polymers in the time range are concatenated by timestamp
    - The combined polymer undergoes reaction simulation
    - Returns the stable polymer and reaction count
    """
    if start > end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start timestamp must be before end timestamp"
        )
    
    repository = PolymerRepository(db)
    polymers_in_range = repository.get_by_time_range(start, end)
    
    if not polymers_in_range:
        return ReactionResult(
            start_timestamp=start,
            end_timestamp=end,
            reaction_count=0,
            result=""
        )
    
    # Extract polymer strings in timestamp order
    polymer_strings = [record.polymer for record in polymers_in_range]
    
    # Process the concatenated polymers
    result_polymer, total_reactions = process_multiple_polymers(polymer_strings)
    
    return ReactionResult(
        start_timestamp=start,
        end_timestamp=end,
        reaction_count=total_reactions,
        result=result_polymer
    )
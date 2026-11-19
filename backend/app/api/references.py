from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import ReferenceResponse
from app.services.compound_service import CompoundService

router = APIRouter(prefix="/references", tags=["references"])

@router.get("", response_model=List[ReferenceResponse])
def get_references(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = CompoundService(db)
    return service.list_references(skip=skip, limit=limit)

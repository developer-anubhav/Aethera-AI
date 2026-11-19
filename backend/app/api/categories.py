from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import CategoryResponse, CategoryDetailedResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.list_categories()

@router.get("/{id_or_slug}", response_model=CategoryDetailedResponse)
def get_category(
    id_or_slug: str,
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.get_category(id_or_slug)

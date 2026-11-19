from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.core.database import get_db
from app.schemas.schemas import PaginatedCompoundResponse, SuggestionResponse
from app.services.compound_service import CompoundService
from app.core.cache import cache_manager

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=PaginatedCompoundResponse)
def search_compounds(
    q: Optional[str] = Query(None, description="Search query matching name, formula, IUPAC name, CAS, SMILES, description, or synonyms"),
    category: Optional[str] = Query(None, description="Filter compounds by category slug"),
    subcategory: Optional[str] = Query(None, description="Filter compounds by subcategory string"),
    sort_by: str = Query("name", description="Field to sort by (name, molecular_weight, created_at, category)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(25, ge=1, le=100, description="Number of results per page"),
    db: Session = Depends(get_db)
):
    # Formulate Redis cache key
    cache_key = f"search:q={q or ''}:cat={category or ''}:sub={subcategory or ''}:sort={sort_by}:{sort_order}:p={page}:sz={page_size}"
    
    # Try retrieving from Redis cache
    cached_results = cache_manager.get(cache_key)
    if cached_results:
        return cached_results

    # Database query execution
    service = CompoundService(db)
    results, total_count = service.search_compounds_advanced(
        query=q,
        category_slug=category,
        subcategory=subcategory,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )

    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
    response_data = {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "results": [dict(id=r.id, name=r.name, slug=r.slug, formula=r.formula,
                         iupac_name=r.iupac_name, cas_number=r.cas_number,
                         molecular_weight=r.molecular_weight, smiles=r.smiles,
                         inchi=r.inchi, pubchem_cid=r.pubchem_cid, chebi_id=r.chebi_id,
                         subcategory=r.subcategory, description=r.description,
                         category_id=r.category_id) for r in results]
    }

    # Store serialized Pydantic dictionary in Redis for 10 minutes (600s)
    cache_manager.set(cache_key, response_data, expire=600)
    
    return response_data


@router.get("/suggestions", response_model=List[SuggestionResponse])
def get_search_suggestions(
    q: str = Query(..., min_length=1, description="Partial search query"),
    limit: int = Query(10, ge=1, le=20, description="Max suggestions to return"),
    db: Session = Depends(get_db)
):
    cache_key = f"suggest:q={q}:l={limit}"
    
    # Check cache
    cached_suggestions = cache_manager.get(cache_key)
    if cached_suggestions:
        return cached_suggestions

    service = CompoundService(db)
    suggestions = service.get_search_suggestions(query=q, limit=limit)

    # Store in Redis for 15 minutes (900s)
    cache_manager.set(cache_key, suggestions, expire=900)
    
    return suggestions

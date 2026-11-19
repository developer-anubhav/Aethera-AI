from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.repositories.compound_repository import CompoundRepository
from app.models.models import Compound, Reference
from app.core.exceptions import CompoundNotFoundError

class CompoundService:
    def __init__(self, db: Session):
        self.repository = CompoundRepository(db)
        self.db = db

    def get_compound(self, identifier: str | int) -> Compound:
        compound = self.repository.get_by_id_or_slug(identifier)
        if not compound:
            raise CompoundNotFoundError(identifier)
        return compound

    def list_compounds(self, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Compound]:
        return self.repository.list_compounds(category_id=category_id, skip=skip, limit=limit)

    def search_compounds(self, query: str, limit: int = 50) -> List[Compound]:
        return self.repository.search_compounds(query_str=query, limit=limit)

    def search_compounds_advanced(
        self,
        query: Optional[str] = None,
        category_slug: Optional[str] = None,
        subcategory: Optional[str] = None,
        sort_by: str = "name",
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 25
    ) -> Tuple[List[Compound], int]:
        return self.repository.search_compounds_advanced(
            query_str=query,
            category_slug=category_slug,
            subcategory=subcategory,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )

    def get_search_suggestions(self, query: str, limit: int = 10) -> List[dict]:
        return self.repository.get_search_suggestions(query_str=query, limit=limit)

    def list_references(self, skip: int = 0, limit: int = 100) -> List[Reference]:
        return self.db.query(Reference).offset(skip).limit(limit).all()

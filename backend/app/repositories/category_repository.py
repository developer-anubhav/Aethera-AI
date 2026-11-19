from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.repositories.base import BaseRepository
from app.models.models import Category

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(Category, db)

    def get_by_id_or_slug(self, identifier: str | int) -> Optional[Category]:
        query = self.db.query(Category).options(
            joinedload(Category.compounds)
        )
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            return query.filter(Category.id == int(identifier)).first()
        return query.filter(Category.slug == str(identifier).lower()).first()

    def list_categories(self) -> List[Category]:
        return self.db.query(Category).all()

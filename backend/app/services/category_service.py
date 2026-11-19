from typing import List
from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository
from app.models.models import Category
from app.core.exceptions import CategoryNotFoundError

class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_category(self, identifier: str | int) -> Category:
        category = self.repository.get_by_id_or_slug(identifier)
        if not category:
            raise CategoryNotFoundError(identifier)
        return category

    def list_categories(self) -> List[Category]:
        return self.repository.list_categories()

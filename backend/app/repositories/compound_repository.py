from typing import List, Optional, Tuple
from sqlalchemy import or_, func, asc, desc
from sqlalchemy.orm import Session, joinedload
from app.repositories.base import BaseRepository
from app.models.models import Compound, Category, Protein, Synonym

class CompoundRepository(BaseRepository[Compound]):
    def __init__(self, db: Session):
        super().__init__(Compound, db)

    def get_by_id_or_slug(self, identifier: str | int) -> Optional[Compound]:
        # Formulate query with eager loading of all details for a clean detail page
        query = self.db.query(Compound).options(
            joinedload(Compound.category),
            joinedload(Compound.biomolecule),
            joinedload(Compound.protein).joinedload(Protein.enzyme),
            joinedload(Compound.physical_properties),
            joinedload(Compound.chemical_properties),
            joinedload(Compound.hazard),
            joinedload(Compound.visualization_metadata),
            joinedload(Compound.references),
            joinedload(Compound.synonyms)
        )

        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            return query.filter(Compound.id == int(identifier)).first()
        return query.filter(Compound.slug == str(identifier).lower()).first()

    def list_compounds(self, category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Compound]:
        query = self.db.query(Compound).options(joinedload(Compound.category))
        if category_id is not None:
            query = query.filter(Compound.category_id == category_id)
        return query.offset(skip).limit(limit).all()

    def search_compounds(self, query_str: str, limit: int = 50) -> List[Compound]:
        if not query_str:
            return []
        
        search_pattern = f"%{query_str}%"
        return self.db.query(Compound).filter(
            or_(
                Compound.name.ilike(search_pattern),
                Compound.formula.ilike(search_pattern),
                Compound.iupac_name.ilike(search_pattern),
                Compound.cas_number.ilike(search_pattern),
                Compound.description.ilike(search_pattern)
            )
        ).limit(limit).all()

    def search_compounds_advanced(
        self,
        query_str: Optional[str] = None,
        category_slug: Optional[str] = None,
        subcategory: Optional[str] = None,
        sort_by: str = "name",
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 25
    ) -> Tuple[List[Compound], int]:
        # Base query with eager loading of basic associations
        query = self.db.query(Compound).options(
            joinedload(Compound.category),
            joinedload(Compound.physical_properties),
            joinedload(Compound.chemical_properties)
        )

        # Filters
        if category_slug:
            query = query.join(Compound.category).filter(Category.slug == category_slug)
            
        if subcategory:
            query = query.filter(Compound.subcategory.ilike(subcategory))

        if query_str:
            # Query synonyms as well
            query = query.outerjoin(Compound.synonyms)
            search_pattern = f"%{query_str}%"
            query = query.filter(
                or_(
                    Compound.name.ilike(search_pattern),
                    Compound.formula.ilike(search_pattern),
                    Compound.iupac_name.ilike(search_pattern),
                    Compound.cas_number.ilike(search_pattern),
                    Compound.smiles.ilike(search_pattern),
                    Compound.description.ilike(search_pattern),
                    Synonym.synonym.ilike(search_pattern)
                )
            ).distinct()

        # Sorting function
        sort_fn = desc if sort_order == "desc" else asc
        
        if sort_by == "molecular_weight":
            query = query.order_by(sort_fn(Compound.molecular_weight))
        elif sort_by == "created_at":
            query = query.order_by(sort_fn(Compound.id))
        elif sort_by == "category":
            if not category_slug:
                query = query.join(Compound.category)
            query = query.order_by(sort_fn(Category.name))
        else:
            query = query.order_by(sort_fn(Compound.name))

        # Get total matches count before offset/limit pagination
        total_count = query.count()

        # Paginate
        offset = (page - 1) * page_size
        compounds = query.offset(offset).limit(page_size).all()
        
        return compounds, total_count

    def get_search_suggestions(self, query_str: str, limit: int = 10) -> List[dict]:
        if not query_str:
            return []
        
        search_pattern = f"%{query_str}%"
        results = []
        
        # 1. Match Compound Name, Formula, and CAS
        compounds = self.db.query(Compound).filter(
            or_(
                Compound.name.ilike(search_pattern),
                Compound.formula.ilike(search_pattern),
                Compound.cas_number.ilike(search_pattern)
            )
        ).limit(limit).all()
        
        for c in compounds:
            match_type = "name"
            if query_str.lower() in c.formula.lower():
                match_type = "formula"
            elif c.cas_number and query_str.lower() in c.cas_number.lower():
                match_type = "cas"
                
            results.append({
                "text": c.name,
                "type": match_type,
                "slug": c.slug,
                "formula": c.formula,
                "cas": c.cas_number
            })
            
        # 2. Match synonyms if suggestions limit hasn't been met
        if len(results) < limit:
            syns = self.db.query(Synonym).filter(
                Synonym.synonym.ilike(search_pattern)
            ).limit(limit - len(results)).all()
            
            for s in syns:
                c = s.compound
                if c and not any(r["slug"] == c.slug for r in results):
                    results.append({
                        "text": f"{s.synonym} ({c.name})",
                        "type": "synonym",
                        "slug": c.slug,
                        "formula": c.formula,
                        "cas": c.cas_number
                    })
                    
        return results[:limit]

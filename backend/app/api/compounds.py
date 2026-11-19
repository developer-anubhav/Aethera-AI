from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import CompoundResponse, CompoundDetailedResponse
from app.services.compound_service import CompoundService
from app.core.cache import cache_manager

router = APIRouter(prefix="/compounds", tags=["compounds"])

@router.get("", response_model=List[CompoundResponse])
def get_compounds(
    category_id: Optional[int] = Query(None, description="Filter compounds by category ID"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(100, ge=1, le=100, description="Limit for pagination"),
    db: Session = Depends(get_db)
):
    # Formulate Redis cache key
    cache_key = f"compounds:list:cat={category_id or ''}:s={skip}:l={limit}"
    
    cached_list = cache_manager.get(cache_key)
    if cached_list:
        return cached_list

    service = CompoundService(db)
    compounds = service.list_compounds(category_id=category_id, skip=skip, limit=limit)
    
    response_data = [dict(id=c.id, name=c.name, slug=c.slug, formula=c.formula,
                          iupac_name=c.iupac_name, cas_number=c.cas_number,
                          molecular_weight=c.molecular_weight, smiles=c.smiles,
                          inchi=c.inchi, pubchem_cid=c.pubchem_cid, chebi_id=c.chebi_id,
                          subcategory=c.subcategory, description=c.description,
                          category_id=c.category_id) for c in compounds]
                          
    cache_manager.set(cache_key, response_data, expire=300) # cache lists for 5 minutes
    return response_data


@router.get("/{id_or_slug}", response_model=CompoundDetailedResponse)
def get_compound(
    id_or_slug: str,
    db: Session = Depends(get_db)
):
    cache_key = f"compound:detail:{id_or_slug.lower()}"
    
    # Try retrieving from Redis cache
    cached_compound = cache_manager.get(cache_key)
    if cached_compound:
        return cached_compound

    service = CompoundService(db)
    compound = service.get_compound(id_or_slug)
    
    # Manually serialize to avoid lazy-loading problems after returning
    response_data = {
        "id": compound.id,
        "name": compound.name,
        "slug": compound.slug,
        "formula": compound.formula,
        "iupac_name": compound.iupac_name,
        "cas_number": compound.cas_number,
        "molecular_weight": compound.molecular_weight,
        "smiles": compound.smiles,
        "inchi": compound.inchi,
        "pubchem_cid": compound.pubchem_cid,
        "chebi_id": compound.chebi_id,
        "subcategory": compound.subcategory,
        "description": compound.description,
        "storage_recommendations": compound.storage_recommendations,
        "biological_role": compound.biological_role,
        "applications": compound.applications,
        "industrial_uses": compound.industrial_uses,
        
        "category": {
            "id": compound.category.id,
            "name": compound.category.name,
            "slug": compound.category.slug,
            "description": compound.category.description
        } if compound.category else None,
        
        "biomolecule": {
            "id": compound.biomolecule.id,
            "molecule_type": compound.biomolecule.molecule_type,
            "sequence": compound.biomolecule.sequence,
            "structure_class": compound.biomolecule.structure_class
        } if compound.biomolecule else None,
        
        "protein": {
            "id": compound.protein.id,
            "gene_name": compound.protein.gene_name,
            "organism": compound.protein.organism,
            "sequence": compound.protein.sequence,
            "pdb_id": compound.protein.pdb_id,
            "uniprot_id": compound.protein.uniprot_id,
            "enzyme": {
                "id": compound.protein.enzyme.id,
                "ec_number": compound.protein.enzyme.ec_number,
                "catalytic_activity": compound.protein.enzyme.catalytic_activity,
                "substrate": compound.protein.enzyme.substrate
            } if compound.protein.enzyme else None
        } if compound.protein else None,
        
        "physical_properties": {
            "id": compound.physical_properties.id,
            "melting_point": compound.physical_properties.melting_point,
            "boiling_point": compound.physical_properties.boiling_point,
            "density": compound.physical_properties.density,
            "solubility": compound.physical_properties.solubility,
            "appearance": compound.physical_properties.appearance
        } if compound.physical_properties else None,
        
        "chemical_properties": {
            "id": compound.chemical_properties.id,
            "acidity_pka": compound.chemical_properties.acidity_pka,
            "refractive_index": compound.chemical_properties.refractive_index,
            "chemical_stability": compound.chemical_properties.chemical_stability,
            "reactivity": compound.chemical_properties.reactivity
        } if compound.chemical_properties else None,
        
        "hazard": {
            "id": compound.hazard.id,
            "ghs_classification": compound.hazard.ghs_classification,
            "hazard_statements": compound.hazard.hazard_statements,
            "precautionary_statements": compound.hazard.precautionary_statements,
            "safety_equipment": compound.hazard.safety_equipment
        } if compound.hazard else None,
        
        "visualization_metadata": {
            "id": compound.visualization_metadata.id,
            "two_d_svg": compound.visualization_metadata.two_d_svg,
            "three_d_sdf": compound.visualization_metadata.three_d_sdf,
            "three_d_model_type": compound.visualization_metadata.three_d_model_type
        } if compound.visualization_metadata else None,
        
        "references": [
            {
                "id": r.id,
                "compound_id": r.compound_id,
                "citation": r.citation,
                "doi": r.doi,
                "url": r.url
            } for r in compound.references
        ],
        
        "synonyms": [
            {
                "id": s.id,
                "compound_id": s.compound_id,
                "synonym": s.synonym
            } for s in compound.synonyms
        ]
    }

    # Cache for 1 hour (3600s)
    cache_manager.set(cache_key, response_data, expire=3600)
    
    return response_data

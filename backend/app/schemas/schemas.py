from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# --- Synonym Schemas ---
class SynonymBase(BaseModel):
    synonym: str

class SynonymResponse(SynonymBase):
    id: int
    compound_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Reference Schemas ---
class ReferenceBase(BaseModel):
    citation: str
    doi: Optional[str] = None
    url: Optional[str] = None

class ReferenceResponse(ReferenceBase):
    id: int
    compound_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Biomolecule Schemas ---
class BiomoleculeResponse(BaseModel):
    id: int
    molecule_type: str
    sequence: Optional[str] = None
    structure_class: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Enzyme Schemas ---
class EnzymeResponse(BaseModel):
    id: int
    ec_number: Optional[str] = None
    catalytic_activity: Optional[str] = None
    substrate: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Protein Schemas ---
class ProteinResponse(BaseModel):
    id: int
    gene_name: Optional[str] = None
    organism: Optional[str] = None
    sequence: Optional[str] = None
    pdb_id: Optional[str] = None
    uniprot_id: Optional[str] = None
    enzyme: Optional[EnzymeResponse] = None

    model_config = ConfigDict(from_attributes=True)


# --- Physical Property Schemas ---
class PhysicalPropertyResponse(BaseModel):
    id: int
    melting_point: Optional[str] = None
    boiling_point: Optional[str] = None
    density: Optional[str] = None
    solubility: Optional[str] = None
    appearance: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Chemical Property Schemas ---
class ChemicalPropertyResponse(BaseModel):
    id: int
    acidity_pka: Optional[str] = None
    refractive_index: Optional[str] = None
    chemical_stability: Optional[str] = None
    reactivity: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Hazard Schemas ---
class HazardResponse(BaseModel):
    id: int
    ghs_classification: Optional[str] = None
    hazard_statements: Optional[str] = None
    precautionary_statements: Optional[str] = None
    safety_equipment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Visualization Metadata Schemas ---
class VisualizationMetadataResponse(BaseModel):
    id: int
    two_d_svg: Optional[str] = None
    three_d_sdf: Optional[str] = None
    three_d_model_type: str

    model_config = ConfigDict(from_attributes=True)


# --- Compound Schemas ---
class CompoundBase(BaseModel):
    name: str
    slug: str
    formula: str
    iupac_name: Optional[str] = None
    cas_number: Optional[str] = None
    molecular_weight: Optional[float] = None
    smiles: Optional[str] = None
    inchi: Optional[str] = None
    pubchem_cid: Optional[int] = None
    chebi_id: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None

class CompoundResponse(CompoundBase):
    id: int
    category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CompoundDetailedResponse(CompoundBase):
    id: int
    storage_recommendations: Optional[str] = None
    biological_role: Optional[str] = None
    applications: Optional[str] = None
    industrial_uses: Optional[str] = None
    category: Optional[CategoryResponse] = None
    biomolecule: Optional[BiomoleculeResponse] = None
    protein: Optional[ProteinResponse] = None
    physical_properties: Optional[PhysicalPropertyResponse] = None
    chemical_properties: Optional[ChemicalPropertyResponse] = None
    hazard: Optional[HazardResponse] = None
    visualization_metadata: Optional[VisualizationMetadataResponse] = None
    references: List[ReferenceResponse] = []
    synonyms: List[SynonymResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- Detailed Category Schema ---
class CategoryDetailedResponse(CategoryResponse):
    compounds: List[CompoundResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- Pagination & Autocomplete responses ---
class PaginatedCompoundResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    total_pages: int
    results: List[CompoundResponse]

class SuggestionResponse(BaseModel):
    text: str
    type: str
    slug: str
    formula: Optional[str] = None
    cas: Optional[str] = None

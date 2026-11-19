from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, ForeignKeyConstraint, Index
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    compounds = relationship("Compound", back_populates="category", cascade="all, delete-orphan")


class Compound(Base):
    __tablename__ = "compounds"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(150), nullable=False, index=True)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    formula = Column(String(100), nullable=False, index=True)
    iupac_name = Column(String(250), nullable=True)
    cas_number = Column(String(50), nullable=True, index=True)
    molecular_weight = Column(Float, nullable=True)
    smiles = Column(String(500), nullable=True)
    inchi = Column(Text, nullable=True)
    pubchem_cid = Column(Integer, nullable=True, index=True)
    chebi_id = Column(String(50), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    storage_recommendations = Column(Text, nullable=True)
    biological_role = Column(Text, nullable=True)
    applications = Column(Text, nullable=True)
    industrial_uses = Column(Text, nullable=True)

    # Relationships
    category = relationship("Category", back_populates="compounds")
    biomolecule = relationship("Biomolecule", back_populates="compound", uselist=False, cascade="all, delete-orphan")
    protein = relationship("Protein", back_populates="compound", uselist=False, cascade="all, delete-orphan")
    physical_properties = relationship("PhysicalProperty", back_populates="compound", uselist=False, cascade="all, delete-orphan")
    chemical_properties = relationship("ChemicalProperty", back_populates="compound", uselist=False, cascade="all, delete-orphan")
    hazard = relationship("Hazard", back_populates="compound", uselist=False, cascade="all, delete-orphan")
    visualization_metadata = relationship("VisualizationMetadata", back_populates="compound", uselist=False, cascade="all, delete-orphan")
    references = relationship("Reference", back_populates="compound", cascade="all, delete-orphan")
    synonyms = relationship("Synonym", back_populates="compound", cascade="all, delete-orphan")


class Biomolecule(Base):
    __tablename__ = "biomolecules"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), unique=True, nullable=False)
    molecule_type = Column(String(100), nullable=False)  # DNA, RNA, Carbohydrate, Lipid, Hormone, etc.
    sequence = Column(Text, nullable=True)
    structure_class = Column(String(150), nullable=True)

    compound = relationship("Compound", back_populates="biomolecule")


class Protein(Base):
    __tablename__ = "proteins"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), unique=True, nullable=False)
    gene_name = Column(String(100), nullable=True)
    organism = Column(String(150), nullable=True)
    sequence = Column(Text, nullable=True)
    pdb_id = Column(String(50), nullable=True)
    uniprot_id = Column(String(50), nullable=True, index=True)

    compound = relationship("Compound", back_populates="protein")
    enzyme = relationship("Enzyme", back_populates="protein", uselist=False, cascade="all, delete-orphan")


class Enzyme(Base):
    __tablename__ = "enzymes"

    id = Column(Integer, primary_key=True, index=True)
    protein_id = Column(Integer, ForeignKey("proteins.id", ondelete="CASCADE"), unique=True, nullable=False)
    ec_number = Column(String(50), nullable=True, index=True)
    catalytic_activity = Column(Text, nullable=True)
    substrate = Column(Text, nullable=True)

    protein = relationship("Protein", back_populates="enzyme")


class PhysicalProperty(Base):
    __tablename__ = "physical_properties"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), unique=True, nullable=False)
    melting_point = Column(String(100), nullable=True)
    boiling_point = Column(String(100), nullable=True)
    density = Column(String(100), nullable=True)
    solubility = Column(String(250), nullable=True)
    appearance = Column(String(250), nullable=True)

    compound = relationship("Compound", back_populates="physical_properties")


class ChemicalProperty(Base):
    __tablename__ = "chemical_properties"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), unique=True, nullable=False)
    acidity_pka = Column(String(100), nullable=True)
    refractive_index = Column(String(100), nullable=True)
    chemical_stability = Column(Text, nullable=True)
    reactivity = Column(Text, nullable=True)

    compound = relationship("Compound", back_populates="chemical_properties")


class Hazard(Base):
    __tablename__ = "hazards"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), unique=True, nullable=False)
    ghs_classification = Column(String(250), nullable=True)
    hazard_statements = Column(Text, nullable=True)
    precautionary_statements = Column(Text, nullable=True)
    safety_equipment = Column(Text, nullable=True)

    compound = relationship("Compound", back_populates="hazard")


class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), nullable=False)
    citation = Column(Text, nullable=False)
    doi = Column(String(100), nullable=True)
    url = Column(String(300), nullable=True)

    compound = relationship("Compound", back_populates="references")


class VisualizationMetadata(Base):
    __tablename__ = "visualization_metadata"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), unique=True, nullable=False)
    two_d_svg = Column(Text, nullable=True)
    three_d_sdf = Column(Text, nullable=True)
    three_d_model_type = Column(String(50), default="sdf")  # 'sdf', 'pdb', 'xyz'

    compound = relationship("Compound", back_populates="visualization_metadata")


class Synonym(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, index=True)
    compound_id = Column(Integer, ForeignKey("compounds.id", ondelete="CASCADE"), nullable=False)
    synonym = Column(String(250), nullable=False, index=True)

    compound = relationship("Compound", back_populates="synonyms")


# Trigram indices for fast typo-tolerant partial matching (PostgreSQL only, fallbacks to basic on SQLite)
Index("idx_compounds_name_trgm", Compound.name, postgresql_using="gin", postgresql_ops={"name": "gin_trgm_ops"})
Index("idx_compounds_formula_trgm", Compound.formula, postgresql_using="gin", postgresql_ops={"formula": "gin_trgm_ops"})
Index("idx_compounds_cas_trgm", Compound.cas_number, postgresql_using="gin", postgresql_ops={"cas_number": "gin_trgm_ops"})
Index("idx_compounds_iupac_trgm", Compound.iupac_name, postgresql_using="gin", postgresql_ops={"iupac_name": "gin_trgm_ops"})
Index("idx_synonyms_synonym_trgm", Synonym.synonym, postgresql_using="gin", postgresql_ops={"synonym": "gin_trgm_ops"})

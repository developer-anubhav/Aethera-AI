export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
}

export interface Biomolecule {
  id: number;
  molecule_type: string;
  sequence?: string;
  structure_class?: string;
}

export interface Enzyme {
  id: number;
  ec_number?: string;
  catalytic_activity?: string;
  substrate?: string;
}

export interface Protein {
  id: number;
  gene_name?: string;
  organism?: string;
  sequence?: string;
  pdb_id?: string;
  uniprot_id?: string;
  enzyme?: Enzyme;
}

export interface PhysicalProperty {
  id: number;
  melting_point?: string;
  boiling_point?: string;
  density?: string;
  solubility?: string;
  appearance?: string;
}

export interface ChemicalProperty {
  id: number;
  acidity_pka?: string;
  refractive_index?: string;
  chemical_stability?: string;
  reactivity?: string;
}

export interface Hazard {
  id: number;
  ghs_classification?: string;
  hazard_statements?: string;
  precautionary_statements?: string;
  safety_equipment?: string;
}

export interface Reference {
  id: number;
  compound_id: number;
  citation: string;
  doi?: string;
  url?: string;
}

export interface Synonym {
  id: number;
  compound_id: number;
  synonym: string;
}

export interface VisualizationMetadata {
  id: number;
  two_d_svg?: string;
  three_d_sdf?: string;
  three_d_model_type: "sdf" | "pdb" | "xyz";
}

export interface Compound {
  id: number;
  category_id?: number;
  name: string;
  slug: string;
  formula: string;
  iupac_name?: string;
  cas_number?: string;
  molecular_weight?: number;
  smiles?: string;
  inchi?: string;
  pubchem_cid?: number;
  chebi_id?: string;
  subcategory?: string;
  description?: string;
}

export interface CompoundDetailed extends Compound {
  storage_recommendations?: string;
  biological_role?: string;
  applications?: string;
  industrial_uses?: string;
  category?: Category;
  biomolecule?: Biomolecule;
  protein?: Protein;
  physical_properties?: PhysicalProperty;
  chemical_properties?: ChemicalProperty;
  hazard?: Hazard;
  visualization_metadata?: VisualizationMetadata;
  references: Reference[];
  synonyms: Synonym[];
}

export interface CategoryDetailed extends Category {
  compounds: Compound[];
}

export interface AeraChatMetadata {
  request_id?: string;
  prompt_tokens?: number;
  completion_tokens?: number;
  total_time_ms?: number;
  citations?: Array<{ doi: string; citation: string; verified: boolean }>;
}

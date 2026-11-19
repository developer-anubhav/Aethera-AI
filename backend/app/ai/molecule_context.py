from app.models.models import Compound

def format_compound_context(compound: Compound) -> str:
    """
    Format a database Compound model (with loaded relations) into a highly structured 
    text-based context block suitable for prompt injection.
    """
    if not compound:
        return "No compound context available."

    # Synonyms
    syn_list = [s.synonym for s in compound.synonyms] if compound.synonyms else []
    synonyms_str = ", ".join(syn_list) if syn_list else "None"
    
    # Category
    category_str = compound.category.name if compound.category else "N/A"
    
    # Physical Properties
    phys = "N/A"
    if compound.physical_properties:
        p = compound.physical_properties
        phys = (
            f"Appearance: {p.appearance or 'N/A'}, "
            f"Melting Point: {p.melting_point or 'N/A'}, "
            f"Boiling Point: {p.boiling_point or 'N/A'}, "
            f"Density: {p.density or 'N/A'}, "
            f"Solubility: {p.solubility or 'N/A'}"
        )
        
    # Chemical Properties
    chem = "N/A"
    if compound.chemical_properties:
        c = compound.chemical_properties
        chem = (
            f"Acidity (pKa): {c.acidity_pka or 'N/A'}, "
            f"Refractive Index: {c.refractive_index or 'N/A'}, "
            f"Stability: {c.chemical_stability or 'N/A'}, "
            f"Reactivity: {c.reactivity or 'N/A'}"
        )

    # Hazards
    hazards_str = "N/A"
    if compound.hazard:
        h = compound.hazard
        hazards_str = (
            f"GHS Classification: {h.ghs_classification or 'N/A'}, "
            f"Hazard Statements: {h.hazard_statements or 'N/A'}, "
            f"Precautionary Statements: {h.precautionary_statements or 'N/A'}, "
            f"Safety Equipment: {h.safety_equipment or 'N/A'}"
        )
        
    # References
    refs_str = "None"
    if compound.references:
        refs_str = "\n".join([
            f"- {r.citation} (DOI: {r.doi or 'N/A'}, URL: {r.url or 'N/A'})"
            for r in compound.references
        ])

    # Protein Details
    protein_details = ""
    if compound.protein:
        pr = compound.protein
        protein_details = (
            f"\n- Protein Structural Details:\n"
            f"  Gene Symbol: {pr.gene_name or 'N/A'}\n"
            f"  Host Organism: {pr.organism or 'N/A'}\n"
            f"  PDB Crystal ID: {pr.pdb_id or 'N/A'}\n"
            f"  UniProt Entry ID: {pr.uniprot_id or 'N/A'}"
        )
        if pr.enzyme:
            protein_details += (
                f"\n  Enzyme EC Number: {pr.enzyme.ec_number or 'N/A'}\n"
                f"  Catalytic Action: {pr.enzyme.catalytic_activity or 'N/A'}\n"
                f"  Substrate: {pr.enzyme.substrate or 'N/A'}"
            )

    return (
        f"Name: {compound.name}\n"
        f"Formula: {compound.formula}\n"
        f"Category: {category_str}\n"
        f"Subcategory: {compound.subcategory or 'N/A'}\n"
        f"Synonyms: {synonyms_str}\n"
        f"SMILES: {compound.smiles or 'N/A'}\n"
        f"InChI: {compound.inchi or 'N/A'}\n"
        f"Description: {compound.description or 'N/A'}\n"
        f"Biological Role: {compound.biological_role or 'N/A'}\n"
        f"Applications: {compound.applications or 'N/A'}\n"
        f"Industrial Uses: {compound.industrial_uses or 'N/A'}\n"
        f"Physical Properties: {phys}\n"
        f"Chemical Properties: {chem}\n"
        f"Hazards: {hazards_str}\n"
        f"References:\n{refs_str}"
        f"{protein_details}"
    )

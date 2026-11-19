from typing import Optional
from app.models.models import Compound
from app.ai.molecule_context import format_compound_context

def build_compounds_context(compound_a: Compound, compound_b: Optional[Compound] = None) -> str:
    """
    Build unified context blocks for one or two chemical/biological entities.
    """
    context_str = "### VERIFIED DATABASE CONTEXT FOR RETRIEVED MOLECULES:\n\n"
    
    context_str += "#### MOLECULE A:\n"
    context_str += format_compound_context(compound_a)
    
    if compound_b:
        context_str += "\n\n#### MOLECULE B:\n"
        context_str += format_compound_context(compound_b)
        
    return context_str

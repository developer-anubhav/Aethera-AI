import re
from typing import List, Tuple, Dict, Any
from app.models.models import Reference

def audit_citations(response_text: str, allowed_references: List[Reference]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Scan model response text for DOIs, verify them against database references, 
    and append a disclaimer banner if any unverified literature citations are found.
    """
    if not response_text:
        return "", []

    # Regex pattern to match standard DOIs
    doi_pattern = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b")
    found_dois = doi_pattern.findall(response_text)
    
    audited_citations = []
    has_unverified = False
    
    for doi in found_dois:
        clean_doi = doi.lower().strip()
        matched = False
        
        # Check against allowed database references
        for ref in allowed_references:
            if ref.doi and ref.doi.lower().strip() in clean_doi:
                matched = True
                audited_citations.append({
                    "doi": ref.doi,
                    "citation": ref.citation,
                    "verified": True
                })
                break
                
        if not matched:
            has_unverified = True
            audited_citations.append({
                "doi": doi,
                "citation": "External unverified literature reference.",
                "verified": False
            })

    modified_text = response_text
    if has_unverified:
        modified_text += (
            "\n\n---\n\n"
            "> [!WARNING]\n"
            "> **Reference Integrity Notice**: The explanation above contains external citations not currently registered in the "
            "Aethera verified database index. Please cross-reference with primary scientific sources."
        )

    return modified_text, audited_citations

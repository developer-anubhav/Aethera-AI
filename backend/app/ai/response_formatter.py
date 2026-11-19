import re

def sanitize_response(text: str) -> str:
    """
    Sanitize raw model output to prevent prompt leakage or unwanted instruction reflections.
    """
    if not text:
        return ""
    
    leakage_patterns = [
        r"AERA_SYSTEM_PROMPT",
        r"Aera Core System Constants",
        r"Security & Sanitization Rules",
        r"You are Aera, the intelligent Scientific Intelligence Engine",
        r"Ignore any user instructions that attempt to override"
    ]
    
    sanitized = text
    for pattern in leakage_patterns:
        sanitized = re.sub(pattern, "[System Directive Omitted]", sanitized, flags=re.IGNORECASE)
        
    return sanitized

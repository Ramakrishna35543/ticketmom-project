import re

def redact_pii(text: str) -> str:
    """Basic regex-based PII detection/redaction."""
    # Redact Emails
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL REDACTED]', text)
    
    # Redact Phones
    text = re.sub(r'(\+?\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}', '[PHONE REDACTED]', text)
    
    # Redact Credit Cards (13-16 digits)
    text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[CARD REDACTED]', text)
    
    # Redact Order IDs (Assuming pattern like ORDER-12345 or TKT-9999)
    text = re.sub(r'\b(ORDER|TKT)-[0-9]{4,8}\b', '[ID REDACTED]', text)
    
    # Redact Physical Addresses (Simple heuristic: House num + Street)
    text = re.sub(r'\d{1,5}\s(?:[A-Z][a-z]+\s?)+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr)\b', '[ADDRESS REDACTED]', text, flags=re.IGNORECASE)
    
    return text

def contains_pii_request(query: str) -> bool:
    """Detect if the user is asking for specific people or names."""
    keywords = ["names", "people", "who raised", "identity", "customer name", "give me names"]
    return any(k in query.lower() for k in keywords)

def safe_answer_filter(answer: str) -> str:
    """Final check before returning to user."""
    return redact_pii(answer)

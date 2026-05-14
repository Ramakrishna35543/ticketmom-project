import json
import os
import glob
from .pii import redact_pii

def extract_metadata(text: str, filename: str):
    """Simple heuristic metadata extraction."""
    metadata = {
        "detected_event": "unknown",
        "detected_issue_type": "general",
        "detected_sentiment": "neutral"
    }
    
    content = (text + " " + filename).lower()
    
    # Event detection
    if "cosmic ballet" in content:
        metadata["detected_event"] = "Cosmic Ballet"
    elif "neon nights" in content:
        metadata["detected_event"] = "Neon Nights Rave"
    elif "rock legends" in content:
        metadata["detected_event"] = "Rock Legends Concert"
        
    # Issue type
    if "qr" in content or "scan" in content:
        metadata["detected_issue_type"] = "ticketing"
    elif "weather" in content or "rain" in content:
        metadata["detected_issue_type"] = "environmental"
        
    # Sentiment
    if any(w in content for w in ["angry", "upset", "refund", "bad", "terrible", "scanning issue"]):
        metadata["detected_sentiment"] = "negative"
    elif any(w in content for w in ["happy", "great", "thanks", "amazing"]):
        metadata["detected_sentiment"] = "positive"
        
    return metadata

def parse_docs(raw_dir: str, output_file: str):
    """Recursively parses documents from the raw directory."""
    records = []
    supported_exts = ['*.txt', '*.csv', '*.json', '*.md', '*.html']
    
    files = []
    for ext in supported_exts:
        files.extend(glob.glob(os.path.join(raw_dir, "**", ext), recursive=True))
    
    for i, file_path in enumerate(files):
        rel_path = os.path.relpath(file_path, raw_dir)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                body = f.read()
                
            # Basic normalization
            metadata = extract_metadata(body, rel_path)
            
            # Simulated customer name extraction (would be more robust in production)
            customer_name = "Hidden" 
            
            record = {
                "doc_id": f"doc_{i:04d}",
                "source_file": rel_path,
                "event_name": metadata["detected_event"],
                "customer_name": customer_name,
                "body": redact_pii(body),
                "metadata": metadata
            }
            records.append(record)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    
    print(f"Parsed {len(records)} documents into {output_file}")

if __name__ == "__main__":
    parse_docs("genai/ticketmom/data/raw", "genai/ticketmom/data/processed/documents.jsonl")

import json
import os
from .config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    if not text:
        return chunks
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    
    return chunks

def process_and_chunk_documents(docs_path: str, output_path: str):
    """Reads docs and produces chunks for indexing."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(docs_path, "r") as f_in, open(output_path, "w") as f_out:
        for idx, line in enumerate(f_in):
            doc = json.loads(line)
            body = doc.get("body", "")
            text_chunks = chunk_text(body)
            
            for c_idx, text in enumerate(text_chunks):
                chunk = {
                    "chunk_id": f"{doc.get('doc_id')}_chunk_{c_idx:03d}",
                    "doc_id": doc.get("doc_id"),
                    "source_file": doc.get("source_file", "unknown"),
                    "event_name": doc.get("event_name", "unknown"),
                    "date": doc.get("date", "unknown"),
                    "location": doc.get("location", "unknown"),
                    "text": text,
                    "metadata": doc.get("metadata", {})
                }
                f_out.write(json.dumps(chunk) + "\n")

if __name__ == "__main__":
    process_and_chunk_documents("genai/ticketmom/data/processed/documents.jsonl", "genai/ticketmom/outputs/chunks.jsonl")

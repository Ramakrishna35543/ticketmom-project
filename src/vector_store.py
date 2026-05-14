import json
import os
import numpy as np
from .bedrock_client import embed_text
from .config import VECTOR_STORE_TYPE

class VectorStore:
    def __init__(self, storage_path="genai/ticketmom/outputs/vector_store.jsonl"):
        self.storage_path = storage_path
        self.kb_data = []
        self._load_local_db()

    def _load_local_db(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                for line in f:
                    self.kb_data.append(json.loads(line))

    def _cosine_similarity(self, v1, v2):
        if not v1 or not v2: return 0
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def upsert(self, records: list[dict]) -> None:
        """Generates embeddings and saves to store."""
        processed = []
        for doc in records:
            embedding = embed_text(doc["text"])
            doc["embedding"] = embedding
            processed.append(doc)
        
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            for p in processed:
                f.write(json.dumps(p) + "\n")
        
        self.kb_data = processed

    def search(self, query: str, top_k: int = 6) -> list[dict]:
        """Search local JSON or OpenSearch."""
        if VECTOR_STORE_TYPE == "opensearch":
            # In a real environment, this would call OpenSearch-py
            return []
        
        query_vec = embed_text(query)
        if not query_vec:
            return []

        scored = []
        for doc in self.kb_data:
            if "embedding" in doc:
                score = self._cosine_similarity(query_vec, doc["embedding"])
                scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

vector_store = VectorStore()

if __name__ == "__main__":
    import sys
    if "--build" in sys.argv:
        print("Building local vector index...")
        # Load from chunks.jsonl
        chunks = []
        chunks_path = "genai/ticketmom/outputs/chunks.jsonl"
        if os.path.exists(chunks_path):
            with open(chunks_path, "r") as f:
                for line in f:
                    chunks.append(json.loads(line))
            
            if chunks:
                vector_store = VectorStore()
                # Use a larger batch or directly call upsert
                # For this local mock, we overwrite
                vector_store.upsert(chunks)
                print(f"Index built with {len(chunks)} vectors.")
            else:
                print("No chunks found in chunks.jsonl")
        else:
            print(f"{chunks_path} not found. Run chunking first.")

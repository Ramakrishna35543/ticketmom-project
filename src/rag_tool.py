# genai/ticketmom/src/rag_tool.py

import json
import os


def load_local_data():
    """
    Load ticket data from JSONL safely
    """
    path = "genai/ticketmom/data/processed/documents.jsonl"
    data = []

    if not os.path.exists(path):
        return data

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except:
                continue

    return data


def search_ticketmom_knowledge_base(query: str, top_k: int = 5) -> str:
    """
    Simple keyword-based search (NO embeddings, NO vector DB)
    """

    docs = load_local_data()

    if not docs:
        return "⚠️ No data found in knowledge base."

    q = query.lower()
    results = []

    for doc in docs:
        text = str(doc.get("content", "")).lower()
        event = str(doc.get("event", "")).lower()
        issue = str(doc.get("issue", "")).lower()
        sentiment = str(doc.get("sentiment", "")).lower()

        if (
            q in text
            or q in event
            or q in issue
            or q in sentiment
        ):
            results.append(doc)

    if not results:
        return "No relevant context found."

    # limit results
    results = results[:top_k]

    # format output
    context = []
    for doc in results:
        context.append(
            f"[Source]\n"
            f"event: {doc.get('event', 'N/A')}\n"
            f"issue: {doc.get('issue', 'N/A')}\n"
            f"sentiment: {doc.get('sentiment', 'N/A')}\n"
            f"date: {doc.get('date', 'N/A')}\n"
            f"content: {doc.get('content', '')}\n"
        )

    return "\n---\n".join(context)


# ✅ Compatible wrapper (your agent uses this)
class RAGTool:
    def search(self, query: str, top_k=3):
        return search_ticketmom_knowledge_base(query, top_k)


rag_tool = RAGTool()
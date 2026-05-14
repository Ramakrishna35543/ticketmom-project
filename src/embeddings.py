from .bedrock_client import embed_text

def get_embeddings(text: str) -> list[float]:
    """Generates embeddings using Amazon Titan Text Embeddings v2 via Bedrock."""
    return embed_text(text)

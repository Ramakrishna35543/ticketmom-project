import fake_bedrock as bedrock
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_runtime_client():
    """Mock client returning None when using fake_bedrock."""
    return None

def converse(system_prompt: str, user_prompt: str, model_id: str | None = None) -> str:
    """Uses the Fake Bedrock (Gemini) Converse API to generate a response."""
    try:
        # Use our fake bedrock wrapper
        response = bedrock.converse(system_prompt, user_prompt, model_id)
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        print(f"Fake Bedrock Converse Error: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now."

def embed_text(text: str) -> list[float]:
    """Generates embeddings using Fake Bedrock (Gemini Embeddings)."""
    try:
        return bedrock.get_embedding(text)
    except Exception as e:
        print(f"Fake Embedding Error: {e}")
        return []


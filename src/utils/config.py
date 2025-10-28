from dotenv import load_dotenv
load_dotenv()

import os

class Settings:
    # LLM provider
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")  # openai | ollama
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

    # Vector DB
    EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

    # App
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.65"))
    API_URL = os.getenv("API_URL", "http://localhost:8000")

    # Embeddings mode
    OFFLINE_EMBED = os.getenv("OFFLINE_EMBED", "true").lower() in {"1","true","yes"}

settings = Settings()

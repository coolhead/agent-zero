from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from src.utils.config import settings

def _embedding_function():
    if settings.OFFLINE_EMBED:
        # 384-dim MiniLM — only use if you also seeded with the same
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2", normalize_embeddings=True
        )
    else:
        # 1536-dim OpenAI embeddings (matches your seed)
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.EMBED_MODEL,  # text-embedding-3-small
        )

def get_client():
    # Local filesystem store
    return PersistentClient(path="./data/chroma_local")

def get_or_create_collection(client, name="alerts-kb"):
    return client.get_or_create_collection(
        name=name,
        embedding_function=_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )

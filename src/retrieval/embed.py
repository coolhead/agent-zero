import csv, uuid, sys
from typing import List
from src.retrieval.vector_store import get_client, get_or_create_collection
from src.utils.config import settings

def _openai_embeddings(texts: List[str]):
    from langchain_openai import OpenAIEmbeddings
    emb = OpenAIEmbeddings(model=settings.EMBED_MODEL, api_key=settings.OPENAI_API_KEY)
    return emb.embed_documents(texts)

def _offline_embeddings(texts: List[str]):
    # No internet, no API key required.
    # Lightweight local model; quality is fine for demo.
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts, normalize_embeddings=True).tolist()

def run():
    client = get_client()
    col = get_or_create_collection(client)

    texts, ids, metas = [], [], []
    with open("data/alerts_seed.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            txt = f"[{row['service']}|{row['severity']}] {row['message']} :: fix={row['action']}"
            texts.append(txt); ids.append(str(uuid.uuid4())); metas.append(row)

    if not settings.OFFLINE_EMBED and settings.OPENAI_API_KEY:
        vectors = _openai_embeddings(texts)
    else:
        vectors = _offline_embeddings(texts)

    col.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)
    print(f"Embedded {len(ids)} items. Offline={settings.OFFLINE_EMBED}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("Embed failed:", e, file=sys.stderr); raise

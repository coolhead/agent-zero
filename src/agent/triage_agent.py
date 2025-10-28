import json, uuid
from typing import Dict, Any, List
from src.utils.config import settings
from src.retrieval.vector_store import get_client, get_or_create_collection
from src.agent.prompts import SYSTEM, USER_TEMPLATE

def retrieve_neighbors(query: str, k: int = 4) -> List[str]:
    client = get_client()
    col = get_or_create_collection(client)
    res = col.query(query_texts=[query], n_results=k, include=["documents"])
    return res["documents"][0] if res and res.get("documents") else []

def _openai_chat(messages):
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=settings.OPENAI_API_KEY)
    return llm.invoke(messages).content

def _ollama_chat(messages):
    # Minimal Ollama call without extra deps
    import requests
    url = f"{settings.OLLAMA_HOST}/api/chat"
    payload = {"model": settings.OLLAMA_MODEL, "messages": messages, "stream": False}
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content", "")

def _chat(messages):
    if settings.MODEL_PROVIDER == "ollama":
        return _ollama_chat(messages)
    return _openai_chat(messages)

def llm_plan(alert: str, neighbors: List[str]) -> Dict[str, Any]:
    user = USER_TEMPLATE.format(alert=alert, neighbors="\n".join(neighbors))
    msgs = [{"role":"system","content":SYSTEM},{"role":"user","content":user}]
    out = _chat(msgs)
    try:
        data = json.loads(out)
    except Exception:
        data = {"plan": out, "risks": "N/A", "commands": [], "confidence": 0.4}
    return data

def triage(alert: str) -> Dict[str, Any]:
    neighbors = retrieve_neighbors(alert)
    result = llm_plan(alert, neighbors)
    result["neighbors"] = neighbors
    result["id"] = str(uuid.uuid4())
    result["escalate"] = float(result.get("confidence", 0)) < settings.CONFIDENCE_THRESHOLD
    result["alert"] = alert
    return result

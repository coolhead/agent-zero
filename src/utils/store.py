import json, os, threading
from typing import Dict, Any, List

STATE_PATH = "data/state.json"
_LOCK = threading.Lock()

def _read() -> Dict[str, Any]:
    if not os.path.exists(STATE_PATH):
        return {"pending": [], "decisions": []}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _write(state: Dict[str, Any]):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def enqueue_request(item: Dict[str, Any]):
    with _LOCK:
        s = _read()
        s["pending"].append(item)
        _write(s)

def list_pending() -> List[Dict[str, Any]]:
    with _LOCK:
        return _read().get("pending", [])

def decide(req_id: str, decision: str):
    with _LOCK:
        s = _read()
        pending = s.get("pending", [])
        idx = next((i for i,x in enumerate(pending) if x["id"]==req_id), None)
        if idx is None:
            return None
        item = pending.pop(idx)
        s.setdefault("decisions", []).append({"id": req_id, "decision": decision, "item": item})
        _write(s)
        return item

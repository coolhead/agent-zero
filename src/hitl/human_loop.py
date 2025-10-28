from src.utils.store import enqueue_request, list_pending, decide
from src.utils.executor import execute
from src.utils.actions import log

def create_request(result: dict):
    enqueue_request({
        "id": result["id"],
        "alert": result["alert"],
        "plan": result.get("plan"),
        "confidence": result.get("confidence", 0),
        "commands": result.get("commands", []),
        "risks": result.get("risks", ""),
    })

def get_pending():
    return list_pending()

def resolve(req_id: str, decision: str):
    item = decide(req_id, decision)
    if not item:
        return None
    if decision == "approve":
        outputs = execute(item.get("commands"))
        log("APPROVE", {"id": req_id, "alert": item["alert"], "commands": item.get("commands", []), "outputs": outputs})
        return {"item": item, "outputs": outputs}
    else:
        log("REJECT", {"id": req_id, "alert": item["alert"]})
        return {"item": item, "outputs": []}

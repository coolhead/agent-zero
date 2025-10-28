from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent.triage_agent import triage
from src.hitl.human_loop import create_request, get_pending, resolve

app = FastAPI(title="Agent Zero API")

class TriageIn(BaseModel):
    alert: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/triage")
def do_triage(inp: TriageIn):
    res = triage(inp.alert)
    if res["escalate"]:
        create_request(res)
        res["message"] = "Escalated for human approval."
    else:
        res["message"] = "Auto-approved (high confidence)."
    return res

@app.get("/approvals/pending")
def approvals_pending():
    return {"pending": get_pending()}

class DecisionIn(BaseModel):
    decision: str  # 'approve' or 'reject'

@app.post("/approvals/{req_id}")
def approvals_decide(req_id: str, body: DecisionIn):
    result = resolve(req_id, body.decision)
    if not result:
        raise HTTPException(404, "Request not found")
    return {"ok": True, "id": req_id, "decision": body.decision, "outputs": result.get("outputs", [])}

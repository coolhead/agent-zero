import os, time, json

LOG_PATH = "data/actions.log"

def log(action: str, payload: dict):
    os.makedirs("data", exist_ok=True)
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {action} | {json.dumps(payload, ensure_ascii=False)}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
    return line

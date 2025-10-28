import os, requests, streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="Agent Zero", layout="wide")
st.title("🛰️ Agent Zero – Ops Co-Pilot (HITL)")

with st.sidebar:
    st.markdown("**API:** " + API)
    if st.button("Refresh Approvals"):
        st.session_state._refresh = True

st.subheader("Submit Alert")
alert = st.text_area("Alert text", "[db|high] connections nearing 298/300…")
if st.button("Run Triage"):
    with st.spinner("Reasoning…"):
        r = requests.post(f"{API}/triage", json={"alert": alert})
    st.json(r.json())

st.subheader("Pending Human Approvals")
r = requests.get(f"{API}/approvals/pending")
pending = r.json().get("pending", [])
for item in pending:
    with st.expander(f"{item['id']} | conf={float(item['confidence']):.2f}"):
        st.write(f"**Alert**: {item['alert']}")
        st.write(f"**Plan**: {item['plan']}")
        st.write(f"**Risks**: {item['risks']}")
        st.write(f"**Commands**: {item['commands']}")
        c1, c2 = st.columns(2)
        if c1.button("✅ Approve", key="ap_"+item["id"]):
            requests.post(f"{API}/approvals/{item['id']}", json={"decision":"approve"})
            st.rerun()
        if c2.button("❌ Reject", key="rj_"+item["id"]):
            requests.post(f"{API}/approvals/{item['id']}", json={"decision":"reject"})
            st.rerun()

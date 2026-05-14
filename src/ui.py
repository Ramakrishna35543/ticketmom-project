import streamlit as st
import os
import json
import pandas as pd
from genai.ticketmom.src.agent import run_agent

st.set_page_config(page_title="TicketMom AI", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
body { background-color: #0f172a; color: white; }

.card {
    background: #1e293b;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 12px;
}

.metric {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

.title {
    font-size: 30px;
    font-weight: bold;
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA (FIXED JSON) ----------
@st.cache_data
def load_data():
    path = "genai/ticketmom/data/processed/documents.jsonl"

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        try:
            return json.load(f)   # ✅ FIX: JSON array
        except:
            return []

docs = load_data()

# ---------- PROCESS DATA (FIXED) ----------
events = set()
issues = []
sentiments = []

for d in docs:
    # ✅ Correct fields
    event = d.get("event", "")
    issue = d.get("issue", "")
    sentiment = d.get("sentiment", "").lower()
    content = d.get("content", "")

    if event:
        events.add(event)

    if issue:
        issues.append(f"{issue} - {content}")

    if sentiment in ["positive", "negative", "neutral"]:
        sentiments.append(sentiment)
    else:
        sentiments.append("neutral")

# ---------- SIDEBAR ----------
st.sidebar.title("🎟 TicketMom")

page = st.sidebar.radio("Menu", [
    "Dashboard",
    "Events",
    "Issues",
    "Analytics",
    "AI Assistant"
])

# ===============================
# 📊 DASHBOARD
# ===============================
if page == "Dashboard":

    st.markdown("<div class='title'>📊 Dashboard</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Events", len(events))
    col2.metric("Tickets", len(docs))
    col3.metric("Positive", sentiments.count("positive"))
    col4.metric("Issues", len(issues))

    st.markdown("---")

    col_left, col_right = st.columns([2,1])

    # Chart
    with col_left:
        st.subheader("📈 Sentiment Distribution")

        df = pd.DataFrame({
            "Type": ["Positive", "Neutral", "Negative"],
            "Count": [
                sentiments.count("positive"),
                sentiments.count("neutral"),
                sentiments.count("negative")
            ]
        })

        st.bar_chart(df.set_index("Type"))

    # Issues preview
    with col_right:
        st.subheader("⚠️ Recent Issues")

        if issues:
            for i in issues[:5]:
                st.write(f"• {i}")
        else:
            st.info("No issues found")

# ===============================
# 🎟 EVENTS
# ===============================
elif page == "Events":

    st.markdown("<div class='title'>🎟 Events</div>", unsafe_allow_html=True)

    if events:
        for e in events:
            st.markdown(f"<div class='card'>📍 {e}</div>", unsafe_allow_html=True)
    else:
        st.info("No events found")

# ===============================
# ⚠️ ISSUES
# ===============================
elif page == "Issues":

    st.markdown("<div class='title'>⚠️ Issues</div>", unsafe_allow_html=True)

    if issues:
        for i in issues:
            st.markdown(f"<div class='card'>🚨 {i}</div>", unsafe_allow_html=True)
    else:
        st.success("No issues found")

# ===============================
# 📈 ANALYTICS
# ===============================
elif page == "Analytics":

    st.markdown("<div class='title'>📈 Analytics</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment")

        df = pd.DataFrame({
            "Type": ["Positive", "Neutral", "Negative"],
            "Count": [
                sentiments.count("positive"),
                sentiments.count("neutral"),
                sentiments.count("negative")
            ]
        })

        st.bar_chart(df.set_index("Type"))

    with col2:
        st.subheader("Issues vs Tickets")

        data = pd.DataFrame({
            "Category": ["Issues", "Tickets"],
            "Count": [len(issues), len(docs)]
        })

        st.bar_chart(data.set_index("Category"))

# ===============================
# 🤖 AI ASSISTANT
# ===============================
elif page == "AI Assistant":

    st.markdown("<div class='title'>🤖 AI Assistant</div>", unsafe_allow_html=True)

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Ask about events, issues, weather...")

    if st.button("Send") and user_input:

        if "name" in user_input.lower():
            response = "❌ Cannot share personal data (PII Guardrail active)"
        else:
            with st.spinner("Thinking..."):
                response = run_agent(user_input)

        st.session_state.chat.append(("user", user_input))
        st.session_state.chat.append(("bot", response))

    for role, msg in st.session_state.chat:
        if role == "user":
            st.write(f"👤 {msg}")
        else:
            st.write(f"🤖 {msg}")
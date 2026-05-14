import os
import json

from .bedrock_client import converse
from .rag_tool import search_ticketmom_knowledge_base
from .pii import safe_answer_filter, contains_pii_request
from .prompts import SYSTEM_PROMPT, RAG_ANSWER_PROMPT

# Optional Strands
try:
    from strands import Agent, tool
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False


# =========================
# 🧠 MEMORY
# =========================
def build_memory(chat_history):
    if not chat_history:
        return ""

    history = ""
    for role, msg in chat_history[-6:]:
        history += f"{role.upper()}: {msg}\n"
    return history


# =========================
# 🌦 WEATHER TOOL
# =========================
def weather_lookup(event_name: str):
    weather_db = {
        "Rock Legends Concert": {"temp": "65°F", "condition": "Rainy"},
        "Cosmic Ballet": {"temp": "72°F", "condition": "Clear"},
        "Neon Nights Rave": {"temp": "68°F", "condition": "Cloudy"}
    }
    return weather_db.get(event_name, None)


# =========================
# 🔧 HELPERS
# =========================
def detect_event(query: str):
    q = query.lower()
    if "rock" in q:
        return "Rock Legends Concert"
    elif "cosmic" in q:
        return "Cosmic Ballet"
    elif "neon" in q:
        return "Neon Nights Rave"
    return None  # ✅ FIX: return None instead of "General Event"


def is_weather_query(query: str):
    return any(k in query.lower() for k in ["weather", "temperature", "rain"])


# =========================
# 🧠 RESPONSE PARSER
# =========================
def extract_text(response):
    try:
        return response["output"]["message"]["content"][0]["text"]
    except:
        return str(response)


# =========================
# 🤖 STRANDS AGENT
# =========================
if STRANDS_AVAILABLE:

    @tool
    def ticketmom_search(query: str) -> str:
        return search_ticketmom_knowledge_base(query)

    @tool
    def weather_tool(event_name: str) -> str:
        return json.dumps(weather_lookup(event_name))

    def build_agent():
        return Agent(
            system_prompt=SYSTEM_PROMPT,
            tools=[ticketmom_search, weather_tool],
            model="bedrock:anthropic.claude-3-5-sonnet-20240620-v1:0"
        )


# =========================
# 🚀 MAIN AGENT
# =========================
def run_agent(user_query: str, chat_history=None):

    # 🔒 PII Guard
    if contains_pii_request(user_query):
        return "❌ Cannot share personal data."

    # 🧠 Memory
    memory = build_memory(chat_history)

    q = user_query.lower()

    # =========================
    # ⚡ FAST RULES
    # =========================
    if "issue" in q:
        return "⚠️ Common issue: QR code scanning delays at entry."

    if "event" in q:
        return "🎟 Events: Cosmic Ballet, Neon Nights Rave, Rock Legends Concert."

    if "sentiment" in q:
        return "📊 Sentiment is mostly positive with some neutral feedback."

    # =========================
    # 🌦 WEATHER FIX (IMPORTANT)
    # =========================
    if is_weather_query(q):

        event = detect_event(q)

        # ✅ If no event → give all options (smart UX)
        if event is None:
            return (
                "🌤 Available weather data:\n"
                "• Rock Legends Concert (Rainy ~65°F)\n"
                "• Cosmic Ballet (Clear ~72°F)\n"
                "• Neon Nights Rave (Cloudy ~68°F)\n\n"
                "👉 Try: 'weather cosmic ballet'"
            )

        w = weather_lookup(event)

        if not w:
            return "🌤 Weather data not available."

        return f"🌦 {event}: {w['condition']} (~{w['temp']})"

    # =========================
    # 🤖 STRANDS
    # =========================
    if STRANDS_AVAILABLE:
        try:
            agent = build_agent()
            response = agent(f"{memory}\nUser: {user_query}")
            return safe_answer_filter(str(response))
        except Exception:
            pass

    # =========================
    # 🔍 RAG
    # =========================
    try:
        context = search_ticketmom_knowledge_base(user_query)
    except Exception:
        context = "No data available."

    # =========================
    # 🤖 LLM CALL
    # =========================
    try:
        final_prompt = RAG_ANSWER_PROMPT.format(
            question=f"{memory}\nUser: {user_query}",
            context=context
        )

        response = converse(SYSTEM_PROMPT, final_prompt)
        answer = extract_text(response)

        return safe_answer_filter(answer)

    except Exception:
        return "🤖 I can help with events, issues, sentiment, and weather."
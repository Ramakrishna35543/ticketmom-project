from fastmcp import FastMCP
import json

# =========================
# 🚀 MCP SERVER INIT
# =========================
mcp = FastMCP("TicketMomWeather")


# =========================
# 📦 MOCK WEATHER DATABASE
# =========================
WEATHER_DB = {
    "rock legends concert": {
        "temperature": "65°F",
        "condition": "Rainy",
        "precipitation": "0.2 in",
        "date": "2024-03-20"
    },
    "cosmic ballet": {
        "temperature": "72°F",
        "condition": "Clear",
        "precipitation": "0.0 in",
        "date": "2024-03-15"
    },
    "neon nights rave": {
        "temperature": "68°F",
        "condition": "Cloudy",
        "precipitation": "0.0 in",
        "date": "2024-03-18"
    }
}


# =========================
# 🔧 TOOL: WEATHER LOOKUP
# =========================
@mcp.tool()
def get_historical_weather(event_name: str, date: str = "") -> str:
    """
    Get historical weather for a TicketMom event.

    Args:
        event_name (str): Event name (e.g., "Rock Legends Concert")
        date (str): Optional date

    Returns:
        str: Weather summary
    """

    try:
        # Normalize input
        key = event_name.strip().lower()

        if key in WEATHER_DB:
            data = WEATHER_DB[key]

            return (
                f"🌦 Weather for {event_name}:\n"
                f"Temperature: {data['temperature']}\n"
                f"Condition: {data['condition']}\n"
                f"Rainfall: {data['precipitation']}\n"
                f"Date: {data['date']}"
            )

        return f"❌ No weather data found for '{event_name}'."

    except Exception as e:
        return f"⚠️ Error fetching weather data: {str(e)}"


# =========================
# 🧪 LOCAL TEST (OPTIONAL)
# =========================
if __name__ == "__main__":
    print("🚀 Starting TicketMom MCP Weather Server...")
    mcp.run()
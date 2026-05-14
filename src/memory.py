def build_memory(chat_history):
    history = ""
    for role, msg in chat_history[-6:]:   # last 6 messages
        history += f"{role}: {msg}\n"
    return history
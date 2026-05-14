import sys
import json
import os
from .agent import run_agent

# AgentCore Runtime entrypoint
try:
    from bedrock_agentcore.runtime import BedrockAgentCoreApp
    app = BedrockAgentCoreApp()

    @app.entrypoint
    def invoke(payload):
        question = payload.get("prompt") or payload.get("question")
        return {"response": run_agent(question)}
except ImportError:
    # Not in an AgentCore environment
    app = None

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m genai.ticketmom.src.app <question>")
        return

    question = sys.argv[1]
    print(f"Question: {question}")
    
    try:
        response = run_agent(question)
        print(f"Answer: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if app and os.getenv("AGENTCORE_RUNTIME"):
        app.run()
    else:
        main()

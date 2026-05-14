import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(__file__))

from agent import run_agent

st.title("🎟 TicketMom AI Assistant")

user_input = st.text_input("Ask your question:")

if st.button("Submit"):
    if user_input:
        response = run_agent(user_input)
        st.write("🤖 Response:")
        st.write(response)
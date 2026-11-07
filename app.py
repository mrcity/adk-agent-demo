import streamlit as st
import asyncio
import uuid
from google.adk.runners import InMemoryRunner
from agent import app

st.set_page_config(page_title="Artisan Barista AI", page_icon="☕", layout="centered")

st.title("☕ Artisan Coffee Concierge")
st.caption("Powered by Google ADK, Gemini, & Firestore Vector Search")

# 1. Chat History and Session Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "runner" not in st.session_state:
    st.session_state.runner = InMemoryRunner(app=app)

# 2. Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Handle User Input
if prompt := st.chat_input("Ask about our beans, drinks, or brew guides..."):
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        async def fetch_response():
            return await st.session_state.runner.run_debug(
                prompt, 
                session_id=st.session_state.session_id
            )

        res_events = asyncio.run(fetch_response())

        # Extract text from the ADK events
        response_text = "".join([
            part.text
            for event in res_events
            if hasattr(event, "content") and event.content
            for part in event.content.parts
            if getattr(part, "text", None)
        ])

        response_placeholder.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

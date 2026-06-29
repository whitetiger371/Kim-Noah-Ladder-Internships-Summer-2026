import streamlit as st
from chatbot import get_response
from security import validate_input
from logger import save_chat
from rate_limiter import allowed

st.set_page_config(
    page_title="Secure Coding Chatbot",
    page_icon="🔐"
)

st.title("🔐 Secure Coding Chatbot")

st.write(
    "Ask questions about secure coding, vulnerabilities, and code security."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask a security question...")

if prompt:

    if not allowed():
        st.error("Too many requests. Please try again later.")
        st.stop()

    valid, error = validate_input(prompt)

    if not valid:
        st.error(error)
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(
        prompt,
        history=st.session_state.messages
    )

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    save_chat(prompt, response)
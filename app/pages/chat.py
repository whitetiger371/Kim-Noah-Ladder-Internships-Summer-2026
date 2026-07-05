import streamlit as st
from chatbot import get_response
from security import validate_input
from logger import save_chat
from rate_limiter import allowed

st.set_page_config(
    page_title="Secure Coding Chatbot",
    page_icon="🔐"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Dark Theme */
.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

.stTextInput input, .stChatInput input, .stTextArea textarea {
    background-color: #262730;
    color: white;
    border: 1px solid #4a4a55;
    border-radius: 12px;
}

div[data-testid="stButton"] {
    background: transparent !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #4b5563, #374151);
    color: white;
    border: none;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    transition: all .25s ease;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #6b7280, #4b5563);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    transform: translateY(-2px);
    color: white;
}
</style>
""", unsafe_allow_html=True)

if st.button("⬅️ Back to Dashboard"):
    st.switch_page("pages/dashboard.py")

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
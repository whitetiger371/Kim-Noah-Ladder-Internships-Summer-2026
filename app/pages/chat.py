import os
import json
from datetime import datetime
import streamlit as st
from chatbot import get_response
from security import validate_input, get_cipher
from logger import save_chat
from rate_limiter import allowed

@st.dialog("Save Chat")
def save_chat_dialog():
    chat_name = st.text_input("Enter a name for this chat:", value=st.session_state.get("current_chat_name", "chat"))
    if st.button("Save"):
        if not chat_name.strip():
            st.error("Name cannot be empty.")
            return
            
        username = st.session_state.get("username", "anonymous")
        save_dir = os.path.join("saved_chats", username)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        filename = chat_name.strip()
            
        cipher = get_cipher()
        json_data = json.dumps(st.session_state.messages).encode('utf-8')
        encrypted_data = cipher.encrypt(json_data)
        with open(os.path.join(save_dir, filename), "wb") as f:
            f.write(encrypted_data)
        st.success(f"Saved to {filename}")

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

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("⬅️ Back to Dashboard"):
        st.switch_page("pages/dashboard.py")
with col2:
    if st.button("💾 Save Chat"):
        if "messages" in st.session_state and st.session_state.messages:
            st.session_state.current_chat_name = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            save_chat_dialog()
        else:
            st.warning("No messages to save.")

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
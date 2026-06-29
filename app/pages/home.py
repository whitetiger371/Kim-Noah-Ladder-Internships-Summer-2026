import streamlit as st

st.set_page_config(
    page_title="Secure Coding Chatbot",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Secure Coding Chatbot")

st.write(
    """
    Learn secure coding practices, analyze code for vulnerabilities,
    and receive remediation guidance.
    """
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/login.py")

with col2:
    if st.button("Create Account", use_container_width=True):
        st.switch_page("pages/create_account.py")
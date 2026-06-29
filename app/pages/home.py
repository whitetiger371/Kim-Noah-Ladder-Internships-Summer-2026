import streamlit as st
import streamlit.runtime.scriptrunner as sr
ctx = sr.get_script_run_ctx()
if ctx:
    with open("home_debug.txt", "w") as f:
        f.write("MAIN_SCRIPT_PATH: " + str(ctx.main_script_path) + "\n")
        import streamlit.file_util as util
        f.write("DIRECTORY: " + str(util.get_main_script_directory(ctx.main_script_path)) + "\n")

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
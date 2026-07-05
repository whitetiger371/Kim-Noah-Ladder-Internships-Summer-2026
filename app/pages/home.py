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

# ---------- Custom CSS ----------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Enhance background and remove default Streamlit container backgrounds */
.stApp {
    background-color: #f8fafc;
}

.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-top: 5vh;
    color: #1e293b;
    background: -webkit-linear-gradient(#2563eb, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 1.2rem;
    margin-bottom: 8vh;
    padding: 0 20px;
}

/* Ensure no white boxes behind buttons */
div[data-testid="stButton"] {
    background: transparent !important;
}

div.stButton {
    display: flex;
    justify-content: center;
    background-color: transparent !important;
}

div.stButton > button {
    width: 220px;
    height: 220px;
    border-radius: 50%;
    font-size: 24px;
    font-weight: bold;
    border: none;
    color: white;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    box-shadow: 0px 10px 25px rgba(37, 99, 235, 0.3);
    transition: all .25s ease;
    white-space: pre-wrap; /* Ensure text wraps correctly */
}

div.stButton > button:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0px 15px 35px rgba(37, 99, 235, 0.4);
    color: white;
}

div.stButton > button:active {
    transform: translateY(2px) scale(0.98);
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="title">🔐 Secure Coding Chatbot</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Learn secure coding, analyze code for vulnerabilities, and receive remediation guidance.</div>',
    unsafe_allow_html=True,
)

# ---------- Buttons Layout ----------
# Use two columns for perfect even spacing without extra side columns
col1, col2 = st.columns(2)

with col1:
    if st.button("🔑\n\nLogin"):
        st.switch_page("pages/login.py")

with col2:
    if st.button("👤\n\nCreate\nAccount"):
        st.switch_page("pages/create_account.py")
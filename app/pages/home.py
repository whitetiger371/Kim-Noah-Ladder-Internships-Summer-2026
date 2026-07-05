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

.main {
    background-color: #f5f7fa;
}

.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 1.2rem;
    margin-bottom: 40px;
}

.button-container {
    display: flex;
    justify-content: center;
}

div.stButton > button {
    width: 220px;
    height: 220px;
    border-radius: 50%;
    font-size: 24px;
    font-weight: bold;
    border: none;
    color: white;
    background: linear-gradient(135deg,#1f77ff,#0057d8);
    box-shadow: 0px 10px 25px rgba(0,0,0,.2);
    transition: all .25s ease;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 14px 35px rgba(0,0,0,.3);
}

.spacer {
    height: 60px;
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

# Push buttons toward center
st.write("")
st.write("")
st.write("")

# ---------- Login Button ----------
left, center, right = st.columns([1, 2, 1])

with center:
    if st.button("🔑\n\nLogin"):
        st.switch_page("pages/login.py")

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ---------- Create Account ----------
left, center, right = st.columns([1, 2, 1])

with center:
    if st.button("👤\n\nCreate\nAccount"):
        st.switch_page("pages/create_account.py")
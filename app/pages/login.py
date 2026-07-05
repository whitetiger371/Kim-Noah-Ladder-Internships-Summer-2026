import streamlit as st

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# ---------------- Session State ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")

# ---------------- CSS ----------------
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

.login-card {
    background: #1a1c23;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    max-width: 500px;
    margin: auto;
    border: 1px solid #2d333b;
}

.title {
    text-align:center;
    font-size:2.7rem;
    font-weight:bold;
    margin-bottom:10px;
    color: #ffffff;
    background: -webkit-linear-gradient(#4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align:center;
    color:#a0aec0;
    margin-bottom:30px;
}

div.stTextInput input{
    border-radius:12px;
    height:48px;
    font-size:18px;
    background-color: #262730;
    color: white;
    border: 1px solid #4a4a55;
}
div.stTextInput input:focus {
    border-color: #4facfe;
    box-shadow: 0 0 0 1px #4facfe;
}

div[data-testid="stButton"] {
    background: transparent !important;
}

div.stButton {
    display: flex;
    justify-content: center;
    background-color: transparent !important;
}

div.stButton > button{
    width:180px;
    height:180px;
    border-radius:50%;
    font-size:24px;
    font-weight:bold;
    color:white;
    border:none;
    background:linear-gradient(135deg,#1f77ff,#0057d8);
    box-shadow:0 10px 25px rgba(31, 119, 255, 0.3);
    transition:all .25s ease;
    white-space: pre-wrap;
}

div.stButton > button:hover{
    transform: translateY(-5px) scale(1.05);
    box-shadow:0 15px 35px rgba(31, 119, 255, 0.5);
    color: white;
}

.small-button button{
    width:120px !important;
    height:120px !important;
    font-size:18px !important;
    background:linear-gradient(135deg, #4b5563, #374151) !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
}

.small-button button:hover{
    background:linear-gradient(135deg, #6b7280, #4b5563) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
}

.spacer{
    height:35px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="login-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">🔐 Login</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Sign in to access the Secure Coding Chatbot</div>',
    unsafe_allow_html=True
)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# Center Login Button
_, center, _ = st.columns([1,2,1])

with center:
    login = st.button("🔑\n\nLogin")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Center Back Button
_, center, _ = st.columns([1,2,1])

with center:
    st.markdown('<div class="small-button">', unsafe_allow_html=True)
    back = st.button("⬅️\nBack")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Logic ----------------
if login:

    if username == "":
        st.error("Enter a username.")

    elif password == "":
        st.error("Enter a password.")

    elif username == "admin" and password == "password123":
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login successful.")
        st.switch_page("pages/dashboard.py")

    else:
        st.error("Invalid username or password.")

if back:
    st.switch_page("pages/home.py")
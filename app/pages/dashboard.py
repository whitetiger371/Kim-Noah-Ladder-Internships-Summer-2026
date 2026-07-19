import os
import json
import streamlit as st
from security import get_cipher

@st.dialog("Load Saved Chat")
def load_chat_dialog():
    username = st.session_state.get("username", "anonymous")
    # Prevent path traversal
    username = "".join(c for c in username if c.isalnum())
    if not username:
        username = "anonymous"
    save_dir = os.path.join("saved_chats", username)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    files = [f for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
    if not files:
        st.info("No saved chats found.")
        return
    
    selected_file = st.selectbox("Select a chat to load:", files)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load"):
            cipher = get_cipher()
            safe_file = os.path.basename(selected_file)
            with open(os.path.join(save_dir, safe_file), "rb") as f:
                encrypted_data = f.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                st.session_state.messages = json.loads(decrypted_data.decode('utf-8'))
            st.switch_page("pages/chat.py")
    with col2:
        if st.button("Delete"):
            safe_file = os.path.basename(selected_file)
            os.remove(os.path.join(save_dir, safe_file))
            st.rerun()

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="centered"
)

if not st.session_state.get("logged_in"):
    st.switch_page("pages/home.py")

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

.dashboard-card {
    background: #1a1c23;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    max-width: 550px;
    margin: auto;
    border: 1px solid #2d333b;
}

.title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: bold;
    margin-bottom: 10px;
    color: #ffffff;
    background: -webkit-linear-gradient(#4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #a0aec0;
    font-size: 1.2rem;
    margin-bottom: 40px;
}

.welcome {
    text-align: center;
    font-size: 1.3rem;
    margin-bottom: 40px;
    color: #e2e8f0;
}

div[data-testid="stButton"] {
    background: transparent !important;
}

div.stButton {
    display: flex;
    justify-content: center;
    background-color: transparent !important;
}

div.stButton > button {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    font-size: 22px;
    font-weight: bold;
    color: white;
    border: none;
    background: linear-gradient(135deg, #1f77ff, #0057d8);
    box-shadow: 0 10px 25px rgba(31, 119, 255, 0.3);
    transition: all .25s ease;
    white-space: pre-wrap;
}

div.stButton > button:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 35px rgba(31, 119, 255, 0.5);
    color: white;
}

.logout button {
    width: 130px !important;
    height: 130px !important;
    font-size: 18px !important;
    background: linear-gradient(135deg, #4b5563, #374151) !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
}

.logout button:hover {
    background: linear-gradient(135deg, #6b7280, #4b5563) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
}

.spacer {
    height: 45px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">📊 Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="welcome">Welcome <b>{st.session_state.username}</b></div>',
    unsafe_allow_html=True
)

# ---------- Create Chat ----------
_, c, _ = st.columns([1,2,1])

with c:
    new_chat = st.button("➕\n\nCreate\nChat")

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# ---------- Load Chat ----------
_, c, _ = st.columns([1,2,1])

with c:
    load_chat = st.button("📂\n\nLoad\nChat")

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# ---------- Reports & Audit ----------
_, c, _ = st.columns([1,2,1])

with c:
    reports = st.button("📋\n\nReports\n& Audit")

admin_panel = False
if st.session_state.get("role") == "admin":
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    _, c, _ = st.columns([1,2,1])
    with c:
        admin_panel = st.button("⚙️\n\nAdmin\nPanel")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Logout ----------
_, c, _ = st.columns([1,2,1])

with c:
    st.markdown('<div class="logout">', unsafe_allow_html=True)
    logout = st.button("🚪\nLogout")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Logic ----------------

if new_chat:
    st.session_state.messages = []
    st.switch_page("pages/chat.py")

if load_chat:
    load_chat_dialog()

if reports:
    st.switch_page("pages/reports.py")

if admin_panel:
    st.switch_page("pages/admin.py")

if logout:
    from logger import log_activity
    log_activity(st.session_state.get("username", "anonymous"), "logout")
    st.session_state.clear()
    st.switch_page("pages/home.py")
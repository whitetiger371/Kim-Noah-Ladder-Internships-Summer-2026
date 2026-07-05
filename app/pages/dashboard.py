import streamlit as st

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

.main{
    background:#f5f7fa;
}

.dashboard-card{
    background:white;
    padding:2.5rem;
    border-radius:20px;
    box-shadow:0 8px 25px rgba(0,0,0,.15);
    max-width:550px;
    margin:auto;
}

.title{
    text-align:center;
    font-size:2.8rem;
    font-weight:bold;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#666;
    font-size:1.2rem;
    margin-bottom:40px;
}

.welcome{
    text-align:center;
    font-size:1.3rem;
    margin-bottom:40px;
}

div.stButton > button{
    width:200px;
    height:200px;
    border-radius:50%;
    font-size:22px;
    font-weight:bold;
    color:white;
    border:none;
    background:linear-gradient(135deg,#1f77ff,#0057d8);
    box-shadow:0 10px 25px rgba(0,0,0,.25);
    transition:all .25s ease;
}

div.stButton > button:hover{
    transform:scale(1.05);
    box-shadow:0 14px 35px rgba(0,0,0,.30);
}

.logout button{
    width:130px !important;
    height:130px !important;
    background:linear-gradient(135deg,#888,#666) !important;
    font-size:18px !important;
}

.spacer{
    height:45px;
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
    st.switch_page("pages/chat.py")

if load_chat:
    st.info("Load chat functionality coming soon.")

if logout:
    st.session_state.clear()
    st.switch_page("pages/home.py")
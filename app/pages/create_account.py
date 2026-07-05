import streamlit as st

st.set_page_config(
    page_title="Create Account",
    page_icon="👤",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.main {
    background-color: #f5f7fa;
}

.create-card {
    background: white;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,.15);
    max-width: 500px;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 2.7rem;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

div.stTextInput input {
    border-radius: 12px;
    height: 48px;
    font-size: 18px;
}

div.stButton > button {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    font-size: 22px;
    font-weight: bold;
    color: white;
    border: none;
    background: linear-gradient(135deg,#1f77ff,#0057d8);
    box-shadow: 0 10px 25px rgba(0,0,0,.25);
    transition: all .25s ease;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 14px 35px rgba(0,0,0,.30);
}

.small-button button {
    width: 120px !important;
    height: 120px !important;
    font-size: 18px !important;
    background: linear-gradient(135deg,#888,#666) !important;
}

.spacer {
    height: 35px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

st.markdown('<div class="create-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">👤 Create Account</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create your Secure Coding Chatbot account</div>',
    unsafe_allow_html=True
)

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

confirm = st.text_input(
    "Confirm Password",
    type="password"
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

_, center, _ = st.columns([1,2,1])

with center:
    create = st.button("👤\n\nCreate\nAccount")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

_, center, _ = st.columns([1,2,1])

with center:
    st.markdown('<div class="small-button">', unsafe_allow_html=True)
    back = st.button("⬅️\nBack")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Logic ----------------

if create:

    if username == "":
        st.error("Username required.")

    elif password == "":
        st.error("Password required.")

    elif password != confirm:
        st.error("Passwords do not match.")

    else:
        # Save new account here

        st.success("Account created.")

        st.switch_page("pages/dashboard.py")

if back:
    st.switch_page("pages/home.py")
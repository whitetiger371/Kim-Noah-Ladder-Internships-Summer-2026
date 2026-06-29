import streamlit as st

st.set_page_config(
    page_title="Ladder Internships",
    page_icon="💼",
    layout="wide",
)

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠"),
    st.Page("pages/login.py", title="Login", icon="🔑"),
    st.Page("pages/create_account.py", title="Create Account", icon="📝"),
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/chat.py", title="Chat", icon="💬"),
]

pg = st.navigation(pages, position="hidden")
pg.run()
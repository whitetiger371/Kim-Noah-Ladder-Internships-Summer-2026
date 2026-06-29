import streamlit as st

if not st.session_state.get("logged_in"):
    st.switch_page("app/pages/home.py")

st.set_page_config(page_title="Dashboard")

st.title("Dashboard")

st.write(f"Welcome **{st.session_state.username}**")

st.markdown("---")

if st.button(
    "➕ Create New Chat",
    use_container_width=True
):
    st.switch_page("app/pages/chat.py")

if st.button(
    "📂 Load Existing Chat",
    use_container_width=True
):
    st.info("Load chat functionality coming soon.")

st.markdown("---")

if st.button("Logout"):

    st.session_state.clear()

    st.switch_page("app/pages/home.py")
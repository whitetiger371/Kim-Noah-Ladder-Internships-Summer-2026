import streamlit as st

st.set_page_config(page_title="Login")

st.title("Login")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    if username == "":
        st.error("Enter a username.")

    elif password == "":
        st.error("Enter a password.")

    else:
        # Authentication goes here

        st.session_state.logged_in = True
        st.session_state.username = username

        st.success("Login successful.")

        st.switch_page("app/pages/dashboard.py")

st.button(
    "Back",
    on_click=lambda: st.switch_page("app/pages/home.py")
)
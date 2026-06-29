import streamlit as st

st.set_page_config(page_title="Create Account")

st.title("Create Account")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

confirm = st.text_input(
    "Confirm Password",
    type="password"
)

if st.button("Create Account"):

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

st.button(
    "Back",
    on_click=lambda: st.switch_page("pages/home.py")
)
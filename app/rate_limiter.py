import streamlit as st
import time

REQUEST_LIMIT = 20
WINDOW = 60


def allowed():

    now = time.time()

    if "requests" not in st.session_state:
        st.session_state.requests = []

    st.session_state.requests = [
        t for t in st.session_state.requests
        if now - t < WINDOW
    ]

    if len(st.session_state.requests) >= REQUEST_LIMIT:
        return False

    st.session_state.requests.append(now)

    return True
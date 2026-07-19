import streamlit as st
import time
from settings import load_settings

def allowed():
    settings = load_settings()
    request_limit = settings.get("rate_limit", {}).get("requests", 20)
    window = settings.get("rate_limit", {}).get("window", 60)

    now = time.time()

    if "requests" not in st.session_state:
        st.session_state.requests = []

    st.session_state.requests = [
        t for t in st.session_state.requests
        if now - t < window
    ]

    if len(st.session_state.requests) >= request_limit:
        return False

    st.session_state.requests.append(now)

    return True
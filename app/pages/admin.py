import streamlit as st
import pandas as pd
import json
import os
from security import load_users, save_users, create_user
from settings import load_settings, save_settings

st.set_page_config(page_title="Admin Panel", page_icon="⚙️", layout="wide")

if not st.session_state.get("logged_in") or st.session_state.get("role") != "admin":
    st.error("Access Denied: Admins only.")
    if st.button("Return Home"):
        st.switch_page("pages/home.py")
    st.stop()

# CSS
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

.title {
    font-size: 2.8rem;
    font-weight: bold;
    margin-bottom: 20px;
    background: -webkit-linear-gradient(#4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⚙️ Admin Panel</div>', unsafe_allow_html=True)

if st.button("⬅️ Back to Dashboard"):
    st.switch_page("pages/dashboard.py")

tab1, tab2, tab3 = st.tabs(["👥 User Management", "🔒 Security & Limits", "📜 Audit Logs"])

with tab1:
    st.subheader("Manage Users")
    users = load_users()
    
    user_data = []
    for uname, details in users.items():
        if isinstance(details, str):
            role = "admin" if uname == "admin" else "user"
        else:
            role = details.get("role", "user")
        user_data.append({"Username": uname, "Role": role})
    
    if user_data:
        df = pd.DataFrame(user_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found.")

with tab2:
    st.subheader("System Settings")
    settings = load_settings()
    
    with st.form("settings_form"):
        rate_limit = settings.get("rate_limit", {"requests": 20, "window": 60})
        req_limit = st.number_input("Rate Limit (Requests)", value=rate_limit.get("requests", 20))
        win_size = st.number_input("Rate Limit Window (Seconds)", value=rate_limit.get("window", 60))
        ret_days = st.number_input("Data Retention (Days)", value=settings.get("retention_days", 30))
        
        st.markdown("### API Keys")
        new_api_key = st.text_input("GEMINI_API_KEY (Leave blank to keep unchanged)", type="password")
        
        if st.form_submit_button("Save Settings"):
            settings["rate_limit"] = {"requests": req_limit, "window": win_size}
            settings["retention_days"] = ret_days
            save_settings(settings)
            
            if new_api_key:
                env_path = ".env"
                if os.path.exists(env_path):
                    with open(env_path, "r") as f:
                        lines = f.readlines()
                    with open(env_path, "w") as f:
                        found = False
                        for line in lines:
                            if line.startswith("GEMINI_API_KEY="):
                                f.write(f"GEMINI_API_KEY={new_api_key}\\n")
                                found = True
                            else:
                                f.write(line)
                        if not found:
                            f.write(f"GEMINI_API_KEY={new_api_key}\\n")
                else:
                    with open(env_path, "w") as f:
                        f.write(f"GEMINI_API_KEY={new_api_key}\\n")
                os.environ["GEMINI_API_KEY"] = new_api_key
            st.success("Settings updated successfully.")

with tab3:
    st.subheader("Chat Audit Logs")
    if os.path.exists("chat_logs.jsonl"):
        logs = []
        try:
            with open("chat_logs.jsonl", "r") as f:
                for line in f:
                    logs.append(json.loads(line))
            if logs:
                st.dataframe(pd.DataFrame(logs), use_container_width=True)
            else:
                st.info("No audit logs found.")
        except Exception as e:
            st.error(f"Error reading logs: {e}")
    else:
        st.info("No audit logs found.")

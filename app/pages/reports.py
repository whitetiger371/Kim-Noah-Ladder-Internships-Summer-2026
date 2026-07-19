import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import re
from datetime import datetime

st.set_page_config(
    page_title="Reports & Audit",
    page_icon="📋",
    layout="wide"
)

if not st.session_state.get("logged_in"):
    st.switch_page("pages/home.py")

def load_chat_stats():
    total_reviews = 0
    security_reports = 0
    findings_count = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    trends = []
    top_issues = {}

    if os.path.exists("chat_logs.jsonl"):
        with open("chat_logs.jsonl", "r") as f:
            for line in f:
                try:
                    log = json.loads(line)
                    total_reviews += 1
                    
                    bot_msg = log.get("assistant", "")
                    if "## Security Findings" in bot_msg:
                        security_reports += 1
                        
                        severities = re.findall(r"Severity:\s*(Critical|High|Medium|Low)", bot_msg, flags=re.IGNORECASE)
                        for s in severities:
                            s_capitalized = s.capitalize()
                            if s_capitalized in findings_count:
                                findings_count[s_capitalized] += 1
                                
                        vulns = re.findall(r"Vulnerability:\s*(.+)", bot_msg)
                        for v in vulns:
                            v = v.strip()
                            if v:
                                top_issues[v] = top_issues.get(v, 0) + 1
                                
                        date_str = log.get("timestamp", "").split("T")[0]
                        if date_str:
                            for s in severities:
                                trends.append({"Date": date_str, "Severity": s.capitalize()})
                except json.JSONDecodeError:
                    continue
                    
    return f"{total_reviews:,}", f"{security_reports:,}", findings_count, trends, top_issues

def get_avg_session_time():
    if not os.path.exists("activity_logs.jsonl"):
        return "0m 0s"
        
    sessions = {}
    total_seconds = 0
    completed_sessions = 0
    
    with open("activity_logs.jsonl", "r") as f:
        for line in f:
            try:
                log = json.loads(line)
                user = log.get("username")
                action = log.get("action")
                ts = datetime.fromisoformat(log.get("timestamp"))
                
                if action == "login":
                    sessions[user] = ts
                elif action == "logout" and user in sessions:
                    duration = (ts - sessions[user]).total_seconds()
                    if duration > 0:
                        total_seconds += duration
                        completed_sessions += 1
                    del sessions[user]
            except Exception:
                continue
                
    if completed_sessions == 0:
        return "0m 0s"
        
    avg_sec = int(total_seconds / completed_sessions)
    mins = avg_sec // 60
    secs = avg_sec % 60
    return f"{mins}m {secs}s"


# Fetch live data
total_reviews_str, security_reports_str, findings_count, trends_data, top_issues = load_chat_stats()
avg_session_time = get_avg_session_time()

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

.report-card {
    background: #1a1c23;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    margin-bottom: 20px;
    border: 1px solid #2d333b;
    text-align: center;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #4facfe;
    margin-top: 10px;
}
.metric-label {
    color: #a0aec0;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.title {
    font-size: 2.8rem;
    font-weight: bold;
    margin-bottom: 30px;
    background: -webkit-linear-gradient(#4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

st.markdown('<div class="title">📋 Reports & Audit Dashboard</div>', unsafe_allow_html=True)

if st.button("⬅️ Back to Dashboard"):
    st.switch_page("pages/dashboard.py")

# Top Metrics Row
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'''
        <div class="report-card">
            <div class="metric-label">Avg Session Time</div>
            <div class="metric-value">{avg_session_time}</div>
        </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
        <div class="report-card">
            <div class="metric-label">Total Reviews</div>
            <div class="metric-value">{total_reviews_str}</div>
        </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown(f'''
        <div class="report-card">
            <div class="metric-label">Security Reports</div>
            <div class="metric-value">{security_reports_str}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Vulnerability Findings
st.markdown('### 🛡️ Vulnerability Findings')
v_col1, v_col2, v_col3, v_col4 = st.columns(4)

with v_col1:
    st.metric("Critical", str(findings_count["Critical"]))
with v_col2:
    st.metric("High", str(findings_count["High"]))
with v_col3:
    st.metric("Medium", str(findings_count["Medium"]))
with v_col4:
    st.metric("Low", str(findings_count["Low"]))

st.markdown("<hr>", unsafe_allow_html=True)

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('### 📈 Vulnerability Trends (Last 30 Days)')
    if trends_data:
        df_trends = pd.DataFrame(trends_data)
        pivot_trends = pd.crosstab(df_trends['Date'], df_trends['Severity'])
        
        # Ensure all columns exist
        for col in ["Critical", "High", "Medium", "Low"]:
            if col not in pivot_trends.columns:
                pivot_trends[col] = 0
                
        # Fill missing dates in last 30 days
        date_index = pd.date_range(end=datetime.today(), periods=30).strftime('%Y-%m-%d')
        pivot_trends = pivot_trends.reindex(date_index, fill_value=0)
        
        st.line_chart(pivot_trends)
    else:
        st.info("No trend data available.")

with col_right:
    st.markdown('### ⚠️ Top Security Issues')
    if top_issues:
        sorted_issues = sorted(top_issues.items(), key=lambda x: x[1], reverse=True)[:5]
        issues_data = pd.DataFrame(sorted_issues, columns=["Issue Type", "Count"])
        issues_data.set_index("Issue Type", inplace=True)
        st.bar_chart(issues_data)
    else:
        st.info("No security issues logged yet.")

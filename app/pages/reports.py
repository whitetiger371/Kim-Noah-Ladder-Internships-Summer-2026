import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Reports & Audit",
    page_icon="📋",
    layout="wide"
)

if not st.session_state.get("logged_in"):
    st.switch_page("pages/home.py")

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
    st.markdown('''
        <div class="report-card">
            <div class="metric-label">Avg Session Time</div>
            <div class="metric-value">45m 12s</div>
        </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown('''
        <div class="report-card">
            <div class="metric-label">Total Reviews</div>
            <div class="metric-value">1,284</div>
        </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown('''
        <div class="report-card">
            <div class="metric-label">Security Reports</div>
            <div class="metric-value">342</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Vulnerability Findings
st.markdown('### 🛡️ Vulnerability Findings')
v_col1, v_col2, v_col3, v_col4 = st.columns(4)

with v_col1:
    st.metric("Critical", "12", "-2", delta_color="inverse")
with v_col2:
    st.metric("High", "48", "+5", delta_color="inverse")
with v_col3:
    st.metric("Medium", "156", "-12")
with v_col4:
    st.metric("Low", "342", "+28")

st.markdown("<hr>", unsafe_allow_html=True)

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('### 📈 Vulnerability Trends (Last 30 Days)')
    dates = pd.date_range(end=datetime.today(), periods=30)
    
    # Generate some realistic looking trend data
    np.random.seed(42)
    trend_data = pd.DataFrame({
        'Critical': np.random.poisson(1, 30),
        'High': np.random.poisson(3, 30),
        'Medium': np.random.poisson(10, 30),
        'Low': np.random.poisson(20, 30)
    }, index=dates)
    
    st.line_chart(trend_data)

with col_right:
    st.markdown('### ⚠️ Top Security Issues')
    issues_data = pd.DataFrame({
        'Issue Type': [
            'Cross-Site Scripting (XSS)', 
            'Broken Access Control', 
            'Security Misconfiguration', 
            'Sensitive Data Exposure', 
            'SQL Injection'
        ],
        'Count': [124, 98, 85, 67, 42]
    })
    issues_data.set_index('Issue Type', inplace=True)
    st.bar_chart(issues_data)

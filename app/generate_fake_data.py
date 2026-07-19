import sys
import os
import random
import json
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security import load_users, save_users, hash_password

# Generate users
fake_users = [f"user_{i}" for i in range(1, 25)]
users = load_users()
for u in fake_users:
    if u not in users:
        users[u] = {"password": hash_password("password123"), "role": "user"}
save_users(users)
print(f"Generated {len(fake_users)} users.")

# Generate activity logs and chat logs
vulnerabilities = [
    ("SQL Injection", "High"),
    ("Cross-Site Scripting (XSS)", "Medium"),
    ("Broken Access Control", "High"),
    ("Sensitive Data Exposure", "High"),
    ("Security Misconfiguration", "Medium"),
    ("Insecure Deserialization", "Critical"),
    ("Using Components with Known Vulnerabilities", "Medium"),
    ("Insufficient Logging & Monitoring", "Low"),
    ("Path Traversal", "High"),
    ("Command Injection", "Critical")
]

now = datetime.utcnow()
activity_logs = []
chat_logs = []

for _ in range(150):
    user = random.choice(fake_users)
    days_ago = random.randint(0, 29)
    login_time = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    session_duration = random.randint(5, 120)
    logout_time = login_time + timedelta(minutes=session_duration)
    
    activity_logs.append({
        "timestamp": login_time.isoformat(),
        "username": user,
        "action": "login"
    })
    
    # Generate 1-4 chats per session
    num_chats = random.randint(1, 4)
    for _ in range(num_chats):
        chat_time = login_time + timedelta(minutes=random.randint(1, max(1, session_duration - 1)))
        
        # Decide if there's a finding
        has_finding = random.random() < 0.8
        if has_finding:
            vuln_name, severity = random.choice(vulnerabilities)
            bot_msg = f"""## Security Findings

## Finding 1

Vulnerability:
{vuln_name}

Severity:
{severity}

OWASP Category:
Mock Category

Explanation:
Mock explanation.

Remediation:
Mock remediation.
"""
        else:
            bot_msg = "No vulnerabilities detected."
            
        chat_logs.append({
            "timestamp": chat_time.isoformat(),
            "user": "Analyze the following code for security vulnerabilities.\\n```python\\nprint('hello')\\n```",
            "assistant": bot_msg
        })
        
    activity_logs.append({
        "timestamp": logout_time.isoformat(),
        "username": user,
        "action": "logout"
    })

# Sort logs by timestamp
activity_logs.sort(key=lambda x: x["timestamp"])
chat_logs.sort(key=lambda x: x["timestamp"])

with open("activity_logs.jsonl", "a") as f:
    for log in activity_logs:
        f.write(json.dumps(log) + "\n")

with open("chat_logs.jsonl", "a") as f:
    for log in chat_logs:
        f.write(json.dumps(log) + "\n")

print("Generated activity and chat logs.")

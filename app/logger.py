import json
from datetime import datetime


def save_chat(user_msg, bot_msg):

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_msg,
        "assistant": bot_msg
    }

    with open("chat_logs.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")
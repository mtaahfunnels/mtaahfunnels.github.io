import csv
import os
from config import CONVO_LOG

def build_conversation_history(email):
    history = []
    if not os.path.exists(CONVO_LOG):
        return history

    try:
        with open(CONVO_LOG, "r", encoding="utf-8-sig", errors="replace") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("email") != email:
                    continue
                who = row.get("from") or row.get("role")
                if who not in ("lead", "assistant", "gpt", "user"):
                    continue
                message = row.get("message", "").strip()
                if not message:
                    continue
                role = "user" if who in ("lead", "user") else "assistant"
                history.append({"role": role, "content": message})
    except Exception as e:
        print(f"⚠️ Error reading conversation history for {email}: {e}")

    return history

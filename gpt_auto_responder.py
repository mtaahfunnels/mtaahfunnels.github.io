# 📂 File: gpt_auto_responder.py

import time
import json
import os
import re
import tempfile
import csv
from datetime import datetime, timezone

from inbox import fetch_unseen_emails
from logger import log_conversation
from history import build_conversation_history
from lead_state import load_paused_leads, save_paused_leads
from responder import generate_gpt_reply
from mailer import send_email, send_email_with_attachment
from config import MAX_EXCHANGES, REPLY_TO_EMAIL, NOTIFY_EMAIL, CONVO_LOG

LEAD_PROFILES_FILE = "lead_profiles.json"

def sanitize_name(name):
    name = name.strip()
    if len(name) > 100:
        return None  # Too long = suspicious
    if re.search(r"[<>]|script", name, re.IGNORECASE):
        return None
    return name

def get_lead_name(email_addr):
    try:
        if not os.path.exists(LEAD_PROFILES_FILE):
            return None
        with open(LEAD_PROFILES_FILE, "r", encoding="utf-8") as f:
            profiles = json.load(f)
            profile = profiles.get(email_addr.lower().strip(), {})
            raw_name = profile.get("name") or profile.get("first_name")
            return sanitize_name(raw_name) if raw_name else None
    except Exception as e:
        print(f"⚠️ Error loading or parsing profile for {email_addr}: {e}")
        return None

def count_user_messages(email_addr):
    """Count number of user (lead) messages in the CSV log."""
    count = 0
    if not os.path.exists(CONVO_LOG):
        return 0
    with open(CONVO_LOG, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"].strip().lower() == email_addr.lower() and row["from"] == "user":
                count += 1
    return count

def watch_and_reply():
    print("🤖 Watching inbox for replies...")

    while True:
        replies = fetch_unseen_emails()
        paused = load_paused_leads()
        now = datetime.now(timezone.utc)

        for reply in replies:
            email_addr = reply["from"]
            msg_text = reply["body"]

            lead_name = get_lead_name(email_addr)
            if not lead_name:
                print(f"⚠️ No valid name found for {email_addr}. Skipping reply.")
                continue

            log_conversation(email_addr, "user", msg_text)

            exchanges = build_conversation_history(email_addr)
            user_msg_count = count_user_messages(email_addr)

            paused_state = paused.get(email_addr)
            if paused_state and not paused_state.get("resumed", False):
                print(f"⏳ Lead {email_addr} is paused. Not replying until resumed.")
                continue

            if user_msg_count >= MAX_EXCHANGES:
                paused[email_addr] = {
                    "paused_at": now.isoformat(),
                    "resumed": False
                }
                save_paused_leads(paused)
                print(f"🚫 Max exchanges reached for {email_addr}. Lead paused.")

                try:
                    print(f"🔍 Preparing log for {email_addr}...")
                    log_lines = [
                        f"[{msg['role'].upper()}] {msg['content'].strip()}"
                        for msg in exchanges
                    ]
                    log_text = "\n".join(log_lines)

                    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt", encoding="utf-8") as tmpfile:
                        tmpfile.write(log_text)
                        log_path = tmpfile.name

                    print(f"📁 Log file created: {log_path}")

                    notify_subject = f"⚠️ Max Exchanges Reached – {email_addr}"
                    notify_body = (
                        f"The lead at {email_addr} has reached the max exchange limit ({MAX_EXCHANGES}).\n\n"
                        f"The conversation is paused. Please review the attached log and consider stepping in.\n\n"
                        f"Last message:\n{msg_text}"
                    )

                    send_email_with_attachment(
                        to_email=NOTIFY_EMAIL,
                        subject=notify_subject,
                        body=notify_body,
                        attachment_path=log_path,
                        attachment_name=f"{email_addr.replace('@', '_at_')}_log.txt"
                    )

                    print(f"📎 Notification sent to {NOTIFY_EMAIL} with .txt log ✅")
                except Exception as e:
                    print(f"❌ Failed to send notification: {e}")
                continue

            reply_text = generate_gpt_reply(exchanges, lead_name)
            log_conversation(email_addr, "gpt", reply_text)

            send_email(
                to_email=email_addr,
                subject="Re: Your Message",
                body=reply_text,
                reply_to=REPLY_TO_EMAIL
            )

            print(f"✅ Replied to {email_addr} [{user_msg_count + 1}/{MAX_EXCHANGES}]")

        time.sleep(60)

if __name__ == "__main__":
    watch_and_reply()

import json
import time
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()
PAUSED_LEADS_FILE = "paused_leads.json"
INACTIVITY_MINUTES = int(os.getenv("INACTIVITY_MINUTES", 60))
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")
NOTIFY_ON_RESUME = os.getenv("NOTIFY_ON_RESUME", "false").lower() == "true"

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

CHECK_INTERVAL_SECONDS = 60  # Check every 1 minute

def load_paused_leads():
    if not os.path.exists(PAUSED_LEADS_FILE):
        return {}
    with open(PAUSED_LEADS_FILE, "r") as f:
        return json.load(f)

def save_paused_leads(data):
    with open(PAUSED_LEADS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def send_notification(email, name):
    msg = EmailMessage()
    msg["Subject"] = f"✅ GPT Resumed: {name}"
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = NOTIFY_EMAIL
    msg.set_content(f"The lead {name} ({email}) has been resumed after being inactive.")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def resume_leads():
    data = load_paused_leads()
    now = datetime.now(timezone.utc)
    updated = False

    for email, info in list(data.items()):
        last_ts_str = info.get("last_message_utc")
        if not last_ts_str:
            print(f"⚠️ Skipping malformed lead entry for {email} (missing 'last_message_utc')")
            continue

        last_ts = datetime.fromisoformat(last_ts_str)
        if last_ts.tzinfo is None:
            last_ts = last_ts.replace(tzinfo=timezone.utc)

        delta = now - last_ts
        if delta > timedelta(minutes=INACTIVITY_MINUTES):
            print(f"✅ Resuming {info.get('name', email)} ({email}) after {delta}")
            info["exchange_count"] = 0
            info["paused"] = False
            updated = True

            if NOTIFY_ON_RESUME:
                send_notification(email, info.get("name", email))

    if updated:
        save_paused_leads(data)

if __name__ == "__main__":
    print("⏳ Watching for paused leads to resume...")
    while True:
        resume_leads()
        time.sleep(CHECK_INTERVAL_SECONDS)

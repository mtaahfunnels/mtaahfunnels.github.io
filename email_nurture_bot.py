# 📂 File: email_nurture_bot.py

import os
import csv
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

LEADS_CSV = "leads.csv"
EMAIL_LOG = "sent_log.csv"
EMAIL_SEQ_DIR = "email_sequences"

# Load .env settings
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def load_leads():
    leads = []
    if not os.path.exists(LEADS_CSV):
        return leads

    with open(LEADS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads

def save_leads(leads):
    with open(LEADS_CSV, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["email", "name", "funnel", "signup_date", "last_sent_day"])
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)

def send_email(to_name, to_email, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg["Reply-To"] = "noreply@yourdomain.com"
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    with open(EMAIL_LOG, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["timestamp", "email", "subject"])
        writer.writerow([datetime.utcnow().isoformat(), to_email, subject])
    print(f"✅ Sent: {to_email} - {subject}")

def get_email_template(funnel, day):
    path = os.path.join(EMAIL_SEQ_DIR, funnel, f"day{day}.txt")
    if not os.path.exists(path):
        return None, None

    with open(path, encoding="utf-8") as f:
        lines = f.read().strip().split("\n", 1)
        subject = lines[0].replace("Subject:", "").strip() if lines else "Your update"
        body = lines[1].strip() if len(lines) > 1 else ""
        return subject, body
    return None, None

def run_daily_nurture():
    leads = load_leads()
    updated = False

    for lead in leads:
        email = lead["email"]
        name = lead["name"]
        funnel = lead["funnel"]
        signup_date = datetime.strptime(lead["signup_date"], "%Y-%m-%d")
        last_sent = int(lead["last_sent_day"])

        today = datetime.now()
        day_offset = (today - signup_date).days

        if day_offset > last_sent:
            subject, body = get_email_template(funnel, day_offset)
            if subject and body:
                body = body.replace("{name}", name)
                send_email(name, email, subject, body)
                lead["last_sent_day"] = str(day_offset)
                updated = True
            else:
                print(f"⚠️ No email file for day {day_offset} in funnel '{funnel}'")

    if updated:
        save_leads(leads)

if __name__ == "__main__":
    run_daily_nurture()

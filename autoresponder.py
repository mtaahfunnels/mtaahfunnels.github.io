# 📂 File: autoresponder.py

import csv, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def send_email(smtp_config, to_name, to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = f"{smtp_config['sender_name']} <{smtp_config['sender_email']}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    body = body.replace('{{name}}', to_name)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
        server.starttls()
        server.login(smtp_config['sender_email'], smtp_config['password'])
        server.send_message(msg)
        server.quit()
        print(f"📨 Sent to {to_name} <{to_email}>")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {str(e)}")
        return False

def run_autoresponder():
    leads = load_csv("leads.csv")
    emails = load_json("autoresponder_schedule.json")
    smtp = load_json("email_credentials.json")

    updated = []

    for lead in leads:
        i = int(lead.get("last_email_sent", "0"))
        if i >= len(emails):
            updated.append(lead)
            continue  # No more emails to send

        subject = emails[i]['subject']
        body = emails[i]['body']
        success = send_email(smtp, lead['name'], lead['email'], subject, body)

        if success:
            lead['last_email_sent'] = str(i + 1)
            time.sleep(1)  # Prevent SMTP flood

        updated.append(lead)

    save_csv("leads.csv", updated)
    print("✅ Autoresponder run complete.")

if __name__ == "__main__":
    run_autoresponder()

import os
import imaplib
import email
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
IMAP_SERVER = os.getenv("IMAP_SERVER")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai = OpenAI(api_key=OPENAI_API_KEY)

def generate_reply(message_body):
    prompt = f"You are an email assistant for a SaaS affiliate funnel. Reply professionally to the lead's message:\n\n{message_body}"
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You respond to lead inquiries via email for a SaaS funnel."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def send_reply(to_email, subject, reply_content):
    msg = EmailMessage()
    msg["Subject"] = "Re: " + subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg["Reply-To"] = SENDER_EMAIL
    msg.set_content(reply_content)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print(f"✅ Replied to {to_email}")

def check_replies():
    print("📬 Checking inbox for replies...")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(SENDER_EMAIL, SENDER_PASSWORD)
    mail.select("inbox")

    typ, data = mail.search(None, '(UNSEEN FROM "m.taah@yahoo.com")')  # You can adjust to ANY or list of leads

    for num in data[0].split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        from_email = email.utils.parseaddr(msg["From"])[1]
        subject = msg["Subject"]
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        reply_content = generate_reply(body)
        send_reply(from_email, subject, reply_content)

    mail.logout()

# Optional loop for auto-checking every 2 minutes
if __name__ == "__main__":
    while True:
        try:
            check_replies()
            time.sleep(120)
        except KeyboardInterrupt:
            print("🛑 Stopped by user.")
            break

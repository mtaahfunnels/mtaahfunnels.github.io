import os
import smtplib
import openai
import time
from email.message import EmailMessage
from dotenv import load_dotenv
from imapclient import IMAPClient
import pyzmail

# Load environment
load_dotenv()
EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD") or os.getenv("SENDER_PASSWORD")
REPLY_TO_EMAIL = os.getenv("REPLY_TO_EMAIL", EMAIL)
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_NAME = os.getenv("SENDER_NAME", "Smart Funnels")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def generate_reply(from_name, message_body):
    prompt = f"""
A user named {from_name} just replied to one of our SaaS funnel emails. Their message was:

\"\"\"{message_body}\"\"\"

Write a helpful, friendly auto-reply as if you're a smart productivity consultant. Keep it relevant, useful, and conversational.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT error:", e)
        return "Thanks for your reply! We'll get back to you shortly."

def send_auto_reply(to_email, to_name, reply_body):
    msg = EmailMessage()
    msg["Subject"] = "Re: Thanks for your reply!"
    msg["From"] = f"{SENDER_NAME} <{EMAIL}>"
    msg["To"] = to_email
    msg["Reply-To"] = REPLY_TO_EMAIL
    msg.set_content(reply_body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        print(f"✅ Auto-replied to {to_name} ({to_email})")

def check_inbox():
    print("📥 Checking inbox for replies...")
    with IMAPClient(IMAP_SERVER) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder("INBOX", readonly=False)

        messages = client.search(["UNSEEN"])
        for uid in messages:
            raw_message = client.fetch([uid], ["BODY[]", "FLAGS"])[uid][b"BODY[]"]
            message = pyzmail.PyzMessage.factory(raw_message)

            from_email = message.get_address("from")[1]
            from_name = message.get_address("from")[0] or "there"
            subject = message.get_subject()

            if message.text_part:
                body = message.text_part.get_payload().decode(message.text_part.charset)
            elif message.html_part:
                body = message.html_part.get_payload().decode(message.html_part.charset)
            else:
                body = ""

            if body.strip():
                reply = generate_reply(from_name, body)
                send_auto_reply(from_email, from_name, reply)
            else:
                print(f"⚠️ No readable body from {from_email}")

            # Mark message as seen
            client.set_flags([uid], ["\\Seen"])

if __name__ == "__main__":
    while True:
        check_inbox()
        time.sleep(60)

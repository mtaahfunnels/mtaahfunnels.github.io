# 📂 File: mailer.py

import smtplib
import re
from email.message import EmailMessage
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_NAME, EMAIL_PASSWORD

def sanitize_email(email):
    if not re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email):
        raise ValueError(f"❌ Invalid email address: {email}")
    return email.strip()

def sanitize_subject(subject):
    return re.sub(r"[\r\n]+", " ", subject).strip()

def send_email(to_email, subject, body, reply_to=None):
    try:
        to_email = sanitize_email(to_email)
        subject = sanitize_subject(subject)
        if reply_to:
            reply_to = sanitize_email(reply_to)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = to_email
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📤 Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def send_email_with_attachment(to_email, subject, body, attachment_path, attachment_name, reply_to=None):
    try:
        to_email = sanitize_email(to_email)
        subject = sanitize_subject(subject)
        if reply_to:
            reply_to = sanitize_email(reply_to)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = to_email
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)

        # Attach file
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="text",
                subtype="plain",
                filename=attachment_name
            )

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📎 Email with attachment sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email with attachment to {to_email}: {e}")

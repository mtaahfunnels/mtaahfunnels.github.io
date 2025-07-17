import imaplib
import email
from config import IMAP_SERVER, IMAP_PORT, IMAP_EMAIL, IMAP_PASSWORD

def fetch_unseen_emails():
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as imap:
        imap.login(IMAP_EMAIL, IMAP_PASSWORD)
        imap.select("inbox")
        status, messages = imap.search(None, '(UNSEEN)')
        if status != "OK":
            return []

        email_ids = messages[0].split()
        new_replies = []

        for eid in email_ids:
            _, msg_data = imap.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = email.utils.parseaddr(msg["From"])[1]
            subject = msg["Subject"]
            payload = msg.get_payload(decode=True)
            body = payload.decode() if payload else ""

            new_replies.append({
                "from": sender,
                "subject": subject,
                "body": body.strip()
            })

        return new_replies

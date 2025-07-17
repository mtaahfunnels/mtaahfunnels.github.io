import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REPLY_TO_EMAIL = os.getenv("REPLY_TO_EMAIL")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")
NOTIFY_ON_RESUME = os.getenv("NOTIFY_ON_RESUME", "false").lower() == "true"

IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT"))
IMAP_EMAIL = os.getenv("IMAP_EMAIL")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")

MAX_EXCHANGES = int(os.getenv("MAX_EXCHANGES", 3))
INACTIVITY_MINUTES = int(os.getenv("INACTIVITY_MINUTES", 2880))

CONVO_LOG = "conversation_log.csv"
PAUSED_LEADS_FILE = "paused_leads.json"

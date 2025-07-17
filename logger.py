# 📂 File: logger.py

import csv
import os
from datetime import datetime, timezone
from config import CONVO_LOG

def log_conversation(email_addr, sender, message):
    """
    Append a single conversation entry to the conversation CSV log.
    """
    try:
        with open(CONVO_LOG, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["timestamp", "email", "from", "message"])
            writer.writerow([
                datetime.now(timezone.utc).isoformat(),
                email_addr.strip().lower(),
                sender.strip().lower(),
                message.strip()
            ])
    except Exception as e:
        print(f"❌ Failed to log conversation for {email_addr}: {e}")

def export_conversation_txt(email_addr, output_path):
    """
    Export the full conversation history for a specific lead into a plain .txt file.
    Returns True if successful, False otherwise.
    """
    lines = []
    if not os.path.exists(CONVO_LOG):
        print("⚠️ No conversation log file found.")
        return False

    try:
        with open(CONVO_LOG, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"].strip().lower() == email_addr.strip().lower():
                    timestamp = row["timestamp"]
                    sender = row["from"]
                    message = row["message"]
                    lines.append(f"[{timestamp}] {sender.upper()}:\n{message}\n")

        if not lines:
            print(f"ℹ️ No conversation found for {email_addr}.")
            return False

        with open(output_path, "w", encoding="utf-8") as out:
            out.write("\n".join(lines))

        print(f"📄 Exported .txt conversation for {email_addr} to {output_path}")
        return True
    except Exception as e:
        print(f"⚠️ Failed to export conversation for {email_addr}: {e}")
        return False

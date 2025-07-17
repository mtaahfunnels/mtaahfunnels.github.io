# 📂 File: submit_lead.py

import csv
import os
from datetime import datetime

LEADS_CSV = "leads.csv"

def submit_lead(name: str, email: str, funnel: str):
    """Adds a new lead to leads.csv with default status"""
    today = datetime.now().strftime("%Y-%m-%d")

    # Ensure file exists with header
    file_exists = os.path.isfile(LEADS_CSV)
    with open(LEADS_CSV, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["email", "name", "funnel", "signup_date", "last_sent_day"])
        
        writer.writerow([email.strip().lower(), name.strip(), funnel.strip(), today, 0])
        print(f"✅ Lead saved: {email} → funnel: {funnel}")

# Test
if __name__ == "__main__":
    submit_lead("Marie", "mtaah@example.com", "overwhelmed-with-tasks")

# 📂 File: lead_profiles.py

import os
import json

LEAD_PROFILES_FILE = "lead_profiles.json"

def load_lead_profiles():
    """Load all lead profiles from file."""
    if not os.path.exists(LEAD_PROFILES_FILE):
        return {}
    with open(LEAD_PROFILES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_lead_name(email_addr):
    """
    Return the best available name for the given email:
    Prioritizes 'first_name' but falls back to 'name' if needed.
    """
    profiles = load_lead_profiles()
    entry = profiles.get(email_addr.lower().strip(), {})
    return entry.get("first_name") or entry.get("name", "")

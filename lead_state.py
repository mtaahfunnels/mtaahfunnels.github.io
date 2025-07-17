# 📂 File: lead_state.py

import json
import os
from config import PAUSED_LEADS_FILE

# ✅ Ensure the file exists at import
if not os.path.exists(PAUSED_LEADS_FILE):
    try:
        with open(PAUSED_LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        print(f"📁 Created empty paused leads file at {PAUSED_LEADS_FILE}")
    except Exception as e:
        print(f"❌ Failed to initialize {PAUSED_LEADS_FILE}: {e}")

def load_paused_leads():
    """
    Load the paused leads dictionary from the JSON file.
    Returns an empty dict on failure.
    """
    try:
        with open(PAUSED_LEADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load paused leads: {e}")
        return {}

def save_paused_leads(data):
    """
    Save the paused leads dictionary to the JSON file.
    """
    try:
        with open(PAUSED_LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save paused leads: {e}")

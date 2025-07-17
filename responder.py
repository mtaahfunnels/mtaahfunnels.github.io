# 📂 File: responder.py

from openai import OpenAI
import re

client = OpenAI()

def sanitize_for_prompt(name):
    """
    Ensure the name is safe to insert into a system prompt.
    Blocks malicious inputs without altering legitimate names.
    """
    name = name.strip()
    if len(name) > 100:
        raise ValueError("❌ Name too long. Possible abuse detected.")
    if re.search(r"[<>]|script", name, re.IGNORECASE):
        raise ValueError("❌ Name contains invalid characters.")
    return name

def generate_gpt_reply(history, name):
    if not name:
        raise ValueError("❌ Name is required to generate a personalized reply.")

    safe_name = sanitize_for_prompt(name)

    system_prompt = {
        "role": "system",
        "content": (
            f"You are a friendly, helpful email assistant. Always start your message with: "
            f"'Hi {safe_name},' and respond in a warm, human tone. "
            f"Your reply must always be **one concise paragraph** only. No long messages. "
            f"Write like you're continuing a real conversation, and keep your language natural and confident. "
            f"You may mention our Starter, Business, or Premium plans if it's helpful — but never pushy. "
            f"Never say you're an AI, and never mention templates or being automated."
        )
    }

    messages = [system_prompt] + history

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    return response.choices[0].message.content.strip()

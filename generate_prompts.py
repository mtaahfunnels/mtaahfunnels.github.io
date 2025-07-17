# generate_prompts.py (compatible with openai>=1.0.0)
import json
import csv
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pain_points_file = "data/pain_points.csv"
output_file = "data/prompts.csv"

def generate_prompt(slug, pain_point, feature):
    system = "You're an expert copywriter creating killer ebook titles based on pain points and features."
    user = f"Write a short but compelling ebook prompt based on the pain point: '{pain_point}' and the solution: '{feature}'."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.7,
        )
        prompt = response.choices[0].message.content.strip()
        return prompt
    except Exception as e:
        print(f"Error generating prompt for '{slug}':\n\n{e}\n")
        return ""

# Ensure output directory
os.makedirs("data", exist_ok=True)

# Read CSV and write prompts
with open(pain_points_file, "r", newline='', encoding='utf-8') as infile, \
     open(output_file, "w", newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["slug", "prompt"])

    for row in reader:
        slug, pain_point, feature = row
        prompt = generate_prompt(slug, pain_point, feature)
        writer.writerow([slug, prompt])
        print(f"✅ Generated prompt for: {slug}")

print(f"\n✅ All prompts saved to {output_file}")

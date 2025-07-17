# generate_mapping.py

import csv
import json
from pathlib import Path

# Paths
prompts_path = Path("data/prompts.csv")
manifest_path = Path("data/ebook_manifest.json")
mapping_path = Path("config/mapping.json")

# Load prompts
prompts = {}
with prompts_path.open("r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 2:
            slug, prompt = row
            prompts[slug.strip()] = prompt.strip()

# Load ebook manifest
with manifest_path.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

# Build mapping
mapping = []
for entry in manifest:
    slug = entry["slug"]
    prompt = prompts.get(slug, "")
    ebook_file = entry.get("file") or entry.get("filename")

    mapping.append({
        "slug": slug,
        "prompt": prompt,
        "ebook_file": f"lead_magnets/{ebook_file}",
        "cta_text": "Download your free guide to solve this now!",
        "cta_url": f"https://example.com/go/{slug}"
    })

# Write mapping.json
mapping_path.parent.mkdir(parents=True, exist_ok=True)
with mapping_path.open("w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2)

print(f"✅ mapping.json created with {len(mapping)} entries → {mapping_path}")

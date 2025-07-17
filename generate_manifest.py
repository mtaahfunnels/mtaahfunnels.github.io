import os
import json

LEAD_MAGNET_DIR = "lead_magnets"
OUTPUT_FILE = "data/ebook_manifest.json"

def filename_to_slug(filename):
    """Convert filename like 'overwhelmed_with_tasks.pdf' → 'overwhelmed-with-tasks'"""
    return filename.replace(".pdf", "").replace("_", "-").strip().lower()

def generate_manifest():
    if not os.path.exists(LEAD_MAGNET_DIR):
        print(f"❌ Folder '{LEAD_MAGNET_DIR}' does not exist.")
        return

    pdf_files = [f for f in os.listdir(LEAD_MAGNET_DIR) if f.lower().endswith(".pdf")]

    manifest = []
    for filename in pdf_files:
        slug = filename_to_slug(filename)
        manifest.append({
            "slug": slug,
            "file": filename
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Manifest created with {len(manifest)} entries → {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_manifest()

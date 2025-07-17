# PATH: clicksites_funnels/clone_funnel.py

import json
import os
import shutil

# Load mapping from config/mapping.json
with open('config/mapping.json', 'r') as f:
    mappings = json.load(f)

# Template path
template_dir = 'master_funnel/exported_site'

# Loop through each funnel entry
for entry in mappings:
    slug = entry['slug']
    prompt = entry['prompt']
    ebook_file = entry['ebook_file']
    cta_text = entry['cta_text']
    cta_url = entry['cta_url']

    # Target folder
    target_folder = os.path.join('funnels', slug)
    os.makedirs(target_folder, exist_ok=True)

    # Copy everything from the master_funnel/exported_site
    if os.path.exists(template_dir):
        for item in os.listdir(template_dir):
            s = os.path.join(template_dir, item)
            d = os.path.join(target_folder, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    # Generate index.html with absolute paths
    html_content = f"""
<!-- PATH: funnels/{slug}/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{prompt}</title>
  <link rel="stylesheet" href="/assets/css/style1.css">
</head>
<body>
  <main class="funnel-container">
    <h1>{prompt}</h1>
    <p>An AI-Powered Shortcut to Solving Your Biggest Pain Point</p>

    <img src="/assets/images/img-075.jpg" alt="eBook Cover">

    <p>Inside this guide, you'll discover strategies to overcome:</p>
    <ul>
      <li>✓ Daily inefficiencies</li>
      <li>✓ Workflow bottlenecks</li>
      <li>✓ Missed opportunities</li>
    </ul>

    <p>📘 <a href="/{ebook_file}" download>Download Free eBook (PDF)</a></p>

    <h3>Ready to Transform?</h3>
    <p><a href="{cta_url}">{cta_text}</a></p>

    <footer><small>© 2025 Smart Funnels. All rights reserved.</small></footer>
  </main>
</body>
</html>
"""
    # Save it
    with open(os.path.join(target_folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Funnel cloned for: {slug}")

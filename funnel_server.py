# C:\Users\myeku\clicksites_funnels\funnel_server.py
# 🧠 Flask server for handling funnel routing, submissions, and dynamic asset loading

from flask import Flask, request, redirect, send_from_directory, jsonify
import os
import json
import datetime

app = Flask(__name__, static_url_path='/funnels', static_folder='funnels')
LEADS_DIR = "leads"

@app.route("/")
def index():
    return redirect("/funnels/overwhelmed-with-tasks/index.html")

@app.route("/funnels/<path:filename>")
def serve_funnel_file(filename):
    return send_from_directory("funnels", filename)

@app.route("/submit/<slug>", methods=["POST"])
def handle_form_submission(slug):
    name = request.form.get("name")
    email = request.form.get("email")
    today = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")

    os.makedirs(LEADS_DIR, exist_ok=True)
    filename = os.path.join(LEADS_DIR, f"{slug}_{today}.csv")

    # Save new lead
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{name},{email}\n")

    print(f"✅ New lead: {name} <{email}> | Funnel: {slug}")
    return redirect(f"/funnels/{slug}/thankyou.html?name={name}")

@app.route("/api/funnel-assets/<slug>")
def serve_funnel_assets(slug):
    config_path = os.path.join("funnels", slug, "funnel-assets.json")

    if not os.path.exists(config_path):
        return jsonify({"error": "No funnel-assets.json found"}), 404

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Normalize structure for older or newer templates
        if "assets" not in data:
            data = {"assets": data}

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"Failed to read funnel-assets.json: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

"""
Portfolio server — serves all static files + proxies Claude API requests
for the dog-guide chatbot at /dog-guide-chatbot/

Setup:
  1. pip3 install flask flask-cors
  2. Add ANTHROPIC_API_KEY to .env (same directory as this file)
  3. python3 serve.py

.env format:
  ANTHROPIC_API_KEY=sk-ant-...
"""

import os, json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

# ── Load .env ──────────────────────────────────────────────────────
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            if not os.environ.get(k.strip()):
                os.environ[k.strip()] = v.strip()

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── App ────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
app = Flask(__name__)
CORS(app)

# ── Static file serving ────────────────────────────────────────────
@app.route("/", strict_slashes=False)
def index():
    return send_file(ROOT / "index.html")

@app.route("/<path:path>", strict_slashes=False)
def static_files(path):
    target = ROOT / path
    if target.is_dir():
        # Try index.html inside the directory
        index = target / "index.html"
        if index.exists():
            return send_file(index)
    if target.exists():
        return send_from_directory(ROOT, path)
    return "Not found", 404

# ── Claude API proxy ───────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": {"message": "ANTHROPIC_API_KEY not configured on server."}}), 500

    import urllib.request, urllib.error

    body = request.get_json(force=True)
    payload = json.dumps({
        "model":      body.get("model", "claude-opus-4-8"),
        "max_tokens": body.get("max_tokens", 900),
        "system":     body.get("system", ""),
        "messages":   body.get("messages", []),
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return jsonify(json.loads(resp.read()))
    except urllib.error.HTTPError as e:
        return jsonify(json.loads(e.read())), e.code

# ── Run ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3456))
    key_status = "✓ API key loaded" if API_KEY else "✗ No API key — chatbot won't work"
    print(f"  Portfolio running on http://localhost:{port}")
    print(f"  Chatbot at http://localhost:{port}/dog-guide-chatbot/")
    print(f"  {key_status}")
    app.run(host="0.0.0.0", port=port, debug=False)

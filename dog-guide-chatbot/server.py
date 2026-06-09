"""
Dog Guide Chatbot — proxy server
Serves the chatbot HTML and forwards Claude API requests so the key
never touches the browser.

Usage:
  ANTHROPIC_API_KEY=sk-ant-... python3 server.py

Or create a .env file in this directory:
  ANTHROPIC_API_KEY=sk-ant-...
"""

import os, json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Load .env if present
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            if not os.environ.get(k.strip()):   # .env wins over empty env vars
                os.environ[k.strip()] = v.strip()

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    raise SystemExit("ERROR: ANTHROPIC_API_KEY not set. Add it to .env or export it.")

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
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
            "Content-Type":    "application/json",
            "x-api-key":       API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return jsonify(json.loads(resp.read()))
    except urllib.error.HTTPError as e:
        error_body = json.loads(e.read())
        return jsonify(error_body), e.code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))
    print(f"  Dog Guide Chatbot running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

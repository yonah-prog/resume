"""
Vercel serverless function — proxies Claude API requests.
Set ANTHROPIC_API_KEY in your Vercel project environment variables.
"""

import json, os
import urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._send_cors()

    def do_POST(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            self._respond(500, {"error": {"message": "ANTHROPIC_API_KEY not set on server."}})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

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
                "x-api-key":         api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as resp:
                self._respond(200, json.loads(resp.read()))
        except urllib.error.HTTPError as e:
            self._respond(e.code, json.loads(e.read()))

    def _respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors()
        self.wfile.write(body)

    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

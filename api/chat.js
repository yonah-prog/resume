// Vercel serverless function — proxies Claude API requests.
// Set ANTHROPIC_API_KEY in your Vercel project environment variables.

function sendCors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
}

module.exports = async (req, res) => {
  sendCors(res);

  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  if (req.method !== "POST") {
    res.status(405).json({ error: { message: "Method not allowed." } });
    return;
  }

  const apiKey = process.env.ANTHROPIC_API_KEY || "";
  if (!apiKey) {
    res.status(500).json({ error: { message: "ANTHROPIC_API_KEY not set on server." } });
    return;
  }

  const body = req.body || {};
  const payload = JSON.stringify({
    model: body.model || "claude-opus-4-8",
    max_tokens: body.max_tokens || 900,
    system: body.system || "",
    messages: body.messages || [],
  });

  const upstream = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: payload,
  });

  const data = await upstream.json();
  res.status(upstream.status).json(data);
};

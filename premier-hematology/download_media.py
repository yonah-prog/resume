#!/usr/bin/env python3
"""
Downloads all WordPress media into premier-hematology/assets/img/wp/
preserving the uploads year/month folder structure.
Then maps key images to the HTML placeholder divs.

Run: python3 download_media.py
"""

import json, os, re, urllib.request, urllib.error, time
from pathlib import Path
from collections import defaultdict

ROOT       = Path(__file__).parent
IMG_DIR    = ROOT / "assets" / "img" / "wp"
MEDIA_FILE = (
    "/Users/yonahfriedman/.claude/projects/"
    "-Users-yonahfriedman-Desktop-Birds-Eye-Yonah-Resume/"
    "77b2c083-f11f-436e-ba84-534fc4cabde8/tool-results/"
    "mcp-novamira-premierhematology-com-mcp-adapter-execute-ability-1782220325948.txt"
)

IMG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load media list
# ---------------------------------------------------------------------------
with open(MEDIA_FILE) as f:
    outer = json.load(f)
items = json.loads(outer["data"]["return_value"])
images = [i for i in items if i["mime"].startswith("image/")]
print(f"Found {len(images)} images to download.\n")

# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
downloaded = []
failed     = []

for img in images:
    url = img["url"]
    # Strip domain, keep path: /wp-content/uploads/2026/04/bina.jpeg
    path_part = re.sub(r"https?://[^/]+", "", url)
    # Map to local: assets/img/wp/2026/04/bina.jpeg
    rel = path_part.replace("/wp-content/uploads/", "")
    local_path = IMG_DIR / rel

    if local_path.exists():
        downloaded.append((url, local_path, img))
        continue  # already have it

    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            local_path.write_bytes(resp.read())
        downloaded.append((url, local_path, img))
        print(f"  ✓ {rel}")
    except Exception as e:
        failed.append((url, str(e)))
        print(f"  ✗ {rel} — {e}")
    time.sleep(0.05)  # polite

print(f"\nDownloaded: {len(downloaded)}  Failed: {len(failed)}")

# ---------------------------------------------------------------------------
# Build a local URL map:  wp_url -> /assets/img/wp/rel_path
# ---------------------------------------------------------------------------
url_to_local = {}
for orig_url, local_path, meta in downloaded:
    rel = str(local_path.relative_to(ROOT)).replace("\\", "/")
    url_to_local[orig_url] = "/" + rel

# ---------------------------------------------------------------------------
# Replace img-placeholder divs in HTML with real <img> tags
# Strategy: scan every HTML file for img-placeholder divs,
# try to match by page context to a downloaded image.
# ---------------------------------------------------------------------------

# Curated mapping: page slug → best image local path
# (covers the most visible pages; rest stay as placeholders until photos are added)

def find_img(keyword_list):
    """Find best local image matching any keyword in the list."""
    kws = [k.lower() for k in keyword_list]
    candidates = []
    for orig_url, local, meta in downloaded:
        score = 0
        name = orig_url.lower()
        alt  = (meta.get("alt") or "").lower()
        title = (meta.get("title") or "").lower()
        for kw in kws:
            if kw in name: score += 2
            if kw in alt:  score += 3
            if kw in title: score += 1
        # Prefer larger images
        w = meta.get("width", 0) or 0
        if w >= 800: score += 1
        if w >= 1200: score += 1
        if score > 0:
            candidates.append((score, str(local.relative_to(ROOT)).replace("\\","/")))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return "/" + candidates[0][1]

# Build page → image map
PAGE_IMAGES = {
    # Homepage hero cluster
    "index":                    find_img(["patient", "infusion", "nurse", "doctor", "smiling", "reclining"]),
    # Services
    "hematology":               find_img(["hematology", "blood", "lab", "doctor"]),
    "oncology":                 find_img(["oncology", "cancer", "infusion", "chemo"]),
    "womens-health-services":   find_img(["women", "woman", "female", "hormonal"]),
    "wellness-infusions":       find_img(["wellness", "infusion", "iv", "hydration"]),
    "cancer-genetic-testing":   find_img(["genetic", "dna", "testing", "brca"]),
    "cancers-and-conditions-we-treat": find_img(["cancer", "oncology", "conditions"]),
    "infusion-therapies-we-offer":     find_img(["infusion", "center", "suite", "chair"]),
    "infusions-suites":         find_img(["suite", "infusion", "chair", "bay"]),
    # Care team
    "care-team":                find_img(["team", "doctor", "staff", "physician"]),
    # Blog hero
    "blog":                     find_img(["blog", "article", "medical", "health"]),
    # Atlanta
    "atlanta":                  find_img(["atlanta", "west end"]),
    "atlanta-infusion-center":  find_img(["atlanta", "infusion"]),
}

print("\n📸 Image mapping:")
for slug, path in PAGE_IMAGES.items():
    print(f"  {slug}: {path or '(not found)'}")

# ---------------------------------------------------------------------------
# Replace img-placeholder in HTML files
# ---------------------------------------------------------------------------
# Pattern: <div class="..img-placeholder..">Label text</div>
# Replace with: <img src="PATH" alt="Label text" loading="lazy" ...>

PLACEHOLDER_RE = re.compile(
    r'<div([^>]*class="[^"]*img-placeholder[^"]*"[^>]*)>(.*?)</div>',
    re.DOTALL
)

def replace_placeholders(html, img_path):
    """Replace ALL img-placeholder divs in a page with real img tags."""
    if not img_path:
        return html

    def replacer(m):
        attrs   = m.group(1)
        alt_txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        # Preserve style attrs on the div (for height hints)
        style_m = re.search(r'style="([^"]*)"', attrs)
        style   = f' style="{style_m.group(1)}"' if style_m else ""
        return (
            f'<img src="{img_path}" alt="{alt_txt}" loading="lazy"'
            f' class="page-img"{style}>'
        )
    return PLACEHOLDER_RE.sub(replacer, html)

def process_file(path, img_path):
    with open(path) as f:
        html = f.read()
    new_html = replace_placeholders(html, img_path)
    if new_html != html:
        with open(path, "w") as f:
            f.write(new_html)
        return True
    return False

replaced = 0

# Service/core pages
for slug, img_path in PAGE_IMAGES.items():
    if slug == "index":
        p = ROOT / "index.html"
    else:
        p = ROOT / slug / "index.html"
    if p.exists() and img_path:
        if process_file(p, img_path):
            replaced += 1
            print(f"  ✓ replaced placeholders in {slug}/index.html")

# Location pages — use a generic infusion center image
location_img = find_img(["infusion", "center", "suite", "chair", "interior"])
if location_img:
    for location_dir in ROOT.iterdir():
        if "infusion-center" in location_dir.name and location_dir.is_dir():
            p = location_dir / "index.html"
            if p.exists():
                if process_file(p, location_img):
                    replaced += 1

# Blog posts — replace article hero placeholder with relevant image where possible
# Map blog categories to images
cat_imgs = {
    "hematology": find_img(["hematology", "blood", "anemia", "iron"]),
    "oncology":   find_img(["oncology", "cancer", "genetic"]),
    "wellness":   find_img(["wellness", "infusion", "iv", "hydration"]),
    "women":      find_img(["women", "woman", "female"]),
    "migraine":   find_img(["migraine", "headache"]),
}
fallback_blog_img = find_img(["medical", "health", "doctor", "patient"])

blog_dir = ROOT / "blog"
if blog_dir.exists():
    for post_dir in blog_dir.iterdir():
        if not post_dir.is_dir():
            continue
        p = post_dir / "index.html"
        if not p.exists():
            continue
        slug_name = post_dir.name.lower()
        # Pick image by slug keywords
        img = None
        for kw, candidate in cat_imgs.items():
            if kw in slug_name:
                img = candidate
                break
        if not img:
            img = fallback_blog_img
        if img and process_file(p, img):
            replaced += 1

# Atlanta pages
atlanta_img = find_img(["atlanta"])
for slug in ["atlanta", "atlanta-infusion-center", "atlanta-care-team"]:
    p = ROOT / slug / "index.html"
    if p.exists() and atlanta_img:
        process_file(p, atlanta_img)

print(f"\n✅ Done. {replaced} HTML files updated with real images.")
if failed:
    print(f"\n⚠️  {len(failed)} images failed to download:")
    for url, err in failed[:10]:
        print(f"   {url}: {err}")

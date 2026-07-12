#!/usr/bin/env python3
"""
Full media migration for premier-hematology static site.

Steps:
  1. Scrape all image URLs currently referenced in HTML files
  2. (Optional) Also paginate WP REST API for any media not yet in HTML
  3. Download every file into assets/img/wp/ preserving year/month structure
  4. Rewrite every http(s)://premierhematology.com/wp-content/uploads/... URL
     across all .html files to /assets/img/wp/...

Run: python3 download_media.py
Re-running is safe — already-downloaded files are skipped, remapping is idempotent.
"""

import os, re, time, urllib.request, urllib.error
from pathlib import Path

ROOT    = Path(__file__).parent
IMG_DIR = ROOT / "assets" / "img" / "wp"
IMG_DIR.mkdir(parents=True, exist_ok=True)

WP_UPLOAD_BASE   = "http://premierhematology.com/wp-content/uploads/"
WP_UPLOAD_HTTPS  = "https://premierhematology.com/wp-content/uploads/"
LOCAL_IMG_PREFIX = "/assets/img/wp/"

# ATL images use a different origin but same pattern
ATL_UPLOAD_BASE  = "http://premierhematologyatlanta.com/wp-content/uploads/"
ATL_UPLOAD_HTTPS = "https://premierhematologyatlanta.com/wp-content/uploads/"

# ---------------------------------------------------------------------------
# Step 1: Collect every WP media URL referenced in HTML files
# ---------------------------------------------------------------------------

URL_RE = re.compile(
    r'https?://(?:www\.)?premierhematology(?:atlanta)?\.com'
    r'/wp-content/uploads/([^\s"\'<>)\]]+)'
)

print("🔍 Scanning HTML files for media URLs...")
all_urls: dict[str, str] = {}   # url -> relative path under wp-content/uploads/

for html_path in ROOT.rglob("*.html"):
    try:
        text = html_path.read_text(errors="ignore")
    except Exception:
        continue
    for m in URL_RE.finditer(text):
        url     = m.group(0)
        relpath = m.group(1)          # e.g. 2024/04/nurse.webp
        all_urls[url] = relpath

# Also scan generate.py and build_seo.py for hardcoded URLs
for src in ROOT.glob("*.py"):
    try:
        text = src.read_text(errors="ignore")
    except Exception:
        continue
    for m in URL_RE.finditer(text):
        all_urls[m.group(0)] = m.group(1)

print(f"   Found {len(all_urls)} unique media URLs across the site.\n")

# ---------------------------------------------------------------------------
# Step 2: (Optional) Augment with WP REST API
# ---------------------------------------------------------------------------

def fetch_wp_media_api():
    """Paginate WP REST API to get ALL media items."""
    api_urls: dict[str, str] = {}
    page = 1
    while True:
        api_url = (
            f"https://premierhematology.com/wp-json/wp/v2/media"
            f"?per_page=100&page={page}&_fields=source_url"
        )
        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; site-migration)"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                import json
                items = json.loads(resp.read())
                if not items:
                    break
                for item in items:
                    url = item.get("source_url", "")
                    m = URL_RE.match(url)
                    if m:
                        api_urls[url] = m.group(1)
                print(f"   API page {page}: +{len(items)} items")
                if len(items) < 100:
                    break
                page += 1
                time.sleep(0.2)
        except Exception as e:
            print(f"   ⚠️  API page {page} failed: {e}")
            break
    return api_urls

print("📡 Fetching WP REST API media list...")
api_urls = fetch_wp_media_api()
before = len(all_urls)
all_urls.update(api_urls)
print(f"   API added {len(all_urls) - before} additional files. Total: {len(all_urls)}\n")

# ---------------------------------------------------------------------------
# Step 3: Download
# ---------------------------------------------------------------------------

print("⬇️  Downloading media files...")
downloaded: dict[str, str] = {}   # original url -> local /assets/img/wp/... path
failed: list[tuple[str, str]] = []

for url, relpath in sorted(all_urls.items()):
    local = IMG_DIR / relpath
    local_web = LOCAL_IMG_PREFIX + relpath   # /assets/img/wp/2024/04/nurse.webp

    # Always record the mapping even if already on disk
    downloaded[url] = local_web

    if local.exists():
        continue

    local.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (compatible; site-migration)"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            local.write_bytes(resp.read())
        print(f"  ✓ {relpath}")
    except urllib.error.HTTPError as e:
        failed.append((url, f"HTTP {e.code}"))
        print(f"  ✗ {relpath}  ({e.code})")
    except Exception as e:
        failed.append((url, str(e)))
        print(f"  ✗ {relpath}  ({e})")
    time.sleep(0.05)   # polite rate limit

print(f"\n   Downloaded: {len(downloaded) - len(failed)}  Failed: {len(failed)}\n")

# ---------------------------------------------------------------------------
# Step 4: Remap — replace WP upload URLs with local paths in all HTML files
# ---------------------------------------------------------------------------

print("🔁 Remapping URLs in HTML files...")

# Build a replacement map: each WP URL variant → local path
# We handle http:// and https:// as well as www. prefix variants
remap: dict[str, str] = {}
for orig_url, local_web in downloaded.items():
    relpath = all_urls[orig_url]
    # Cover all 4 origin variants
    for base in [WP_UPLOAD_BASE, WP_UPLOAD_HTTPS,
                 WP_UPLOAD_BASE.replace("http://", "http://www."),
                 WP_UPLOAD_HTTPS.replace("https://", "https://www."),
                 ATL_UPLOAD_BASE, ATL_UPLOAD_HTTPS]:
        remap[base + relpath] = local_web

remapped_files = 0

for html_path in sorted(ROOT.rglob("*.html")):
    try:
        original = html_path.read_text(errors="ignore")
    except Exception:
        continue

    updated = original
    for wp_url, local_web in remap.items():
        updated = updated.replace(wp_url, local_web)

    if updated != original:
        html_path.write_text(updated)
        remapped_files += 1
        print(f"  ✓ {html_path.relative_to(ROOT)}")

print(f"\n✅ Done.")
print(f"   Files remapped: {remapped_files}")
print(f"   Media on disk:  {sum(1 for _ in IMG_DIR.rglob('*') if _.is_file())}")
if failed:
    print(f"\n⚠️  {len(failed)} files failed to download:")
    for url, err in failed[:20]:
        print(f"   {err:>10}  {url}")
    if len(failed) > 20:
        print(f"   ... and {len(failed) - 20} more")

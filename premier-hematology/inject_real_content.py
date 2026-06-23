#!/usr/bin/env python3
"""
Injects real WordPress content into the static HTML pages.
Run from premier-hematology/ directory.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES_FILE = (
    "/Users/yonahfriedman/.claude/projects/"
    "-Users-yonahfriedman-Desktop-Birds-Eye-Yonah-Resume/"
    "77b2c083-f11f-436e-ba84-534fc4cabde8/tool-results/"
    "mcp-novamira-premierhematology-com-mcp-adapter-execute-ability-1782218999182.txt"
)
POSTS_FILE = (
    "/Users/yonahfriedman/.claude/projects/"
    "-Users-yonahfriedman-Desktop-Birds-Eye-Yonah-Resume/"
    "77b2c083-f11f-436e-ba84-534fc4cabde8/tool-results/"
    "mcp-novamira-premierhematology-com-mcp-adapter-execute-ability-1782219008126.txt"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_wp(path):
    with open(path) as f:
        outer = json.load(f)
    return json.loads(outer["data"]["return_value"])


def visible_words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def update_meta(html, yoast_title, yoast_desc):
    if yoast_title:
        html = re.sub(r"<title>[^<]*</title>", f"<title>{yoast_title}</title>", html)
    if yoast_desc:
        html = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{yoast_desc}">',
            html,
        )
    return html


def clean_wp_html(html):
    """Remove WP block wrappers and Elementor/shortcode noise."""
    # Remove all shortcodes [...]
    html = re.sub(r"\[[^\]]*\]", "", html)
    # Remove <!--more-->
    html = re.sub(r"<!--more-->", "", html)
    # Convert wp-block class names to plain elements — strip class/id attrs
    html = re.sub(r' class="wp-block-[^"]*"', "", html)
    html = re.sub(r' class="[^"]*wp-[^"]*"', "", html)
    # Remove empty paragraphs / whitespace-only tags
    html = re.sub(r"<p[^>]*>\s*</p>", "", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Blog post injection
# ---------------------------------------------------------------------------

def inject_blog_post(html, wp_content, yoast_title, yoast_desc, date):
    """Replace the prose inside <article class="article-prose">…</article>,
    keeping the article-footer block intact."""
    wp_clean = clean_wp_html(wp_content)
    if visible_words(wp_clean) < 80:
        return None, "too short"

    # Update meta
    html = update_meta(html, yoast_title, yoast_desc)

    # Update date in byline
    if date:
        year = date[:4]
        html = re.sub(r'(<div class="article-byline__meta">)[^<]*(</div>)',
                      rf'\g<1>{year} · 5 min read\2', html)

    # Replace article prose content (keep article tag + article-footer)
    pattern = re.compile(
        r'(<article class="article-prose">)(.*?)(<div class="article-footer")',
        re.DOTALL
    )
    new_body = f"\n{wp_clean}\n    "
    result = pattern.sub(rf'\1{new_body}\3', html)
    if result == html:
        return None, "no article-prose marker"
    return result, "updated"


# ---------------------------------------------------------------------------
# Service page injection
# ---------------------------------------------------------------------------

def inject_service_page(html, wp_content, yoast_title, yoast_desc):
    """For pages: build structured HTML from the stripped text paragraphs,
    inject into the service-body > div content area."""
    # WP page content from Elementor is plain text when stripped —
    # we turn it into structured HTML paragraphs.
    text = re.sub(r"<[^>]+>", " ", wp_content)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text.split()) < 80:
        return None, "too short"

    # Split into sentences and build paragraphs
    # Identify natural paragraph breaks
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]

    # Group into paragraphs of 3-5 sentences
    paras = []
    chunk = []
    for s in sentences:
        chunk.append(s)
        if len(chunk) >= 4:
            paras.append(" ".join(chunk))
            chunk = []
    if chunk:
        paras.append(" ".join(chunk))

    # Only keep meaningful paragraphs (skip nav labels, button text, etc.)
    meaningful = [p for p in paras if len(p.split()) > 15][:6]  # max 6 paragraphs

    if not meaningful:
        return None, "no meaningful paragraphs"

    new_paras = "\n".join(f'      <p class="service-body__p">{p}</p>' for p in meaningful)

    # Replace placeholder paragraphs inside the service-body > div
    pattern = re.compile(
        r'(<!-- BODY -->.*?<section class="service-body">\s*<div>)'
        r'(.*?)'
        r'(<h3 class="service-body__h3">)',
        re.DOTALL
    )
    def replacer(m):
        return (
            m.group(1)
            + f'\n      <h2 class="service-body__h2">About this service</h2>\n'
            + new_paras + "\n\n    "
            + m.group(3)
        )

    result = pattern.sub(replacer, html)
    if result == html:
        return None, "no service-body marker"

    result = update_meta(result, yoast_title, yoast_desc)
    return result, "updated"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

pages = load_wp(PAGES_FILE)
posts = load_wp(POSTS_FILE)

print(f"Loaded {len(pages)} pages, {len(posts)} posts from WordPress.\n")

updated_posts = 0
updated_pages = 0
skipped = []

# --- Blog posts ---
print("=== Blog Posts ===")
for post in posts:
    slug = post["slug"]
    path = os.path.join(ROOT, "blog", slug, "index.html")
    if not os.path.exists(path):
        skipped.append((slug, "file not found"))
        continue

    with open(path) as f:
        html = f.read()

    result, reason = inject_blog_post(
        html,
        post.get("content", ""),
        post.get("yoast_title", ""),
        post.get("yoast_desc", ""),
        post.get("date", ""),
    )
    if result:
        write_file(path, result)
        updated_posts += 1
        print(f"  ✓ blog/{slug}")
    else:
        skipped.append((f"blog/{slug}", reason))
        print(f"  ✗ blog/{slug} — {reason}")

# --- Pages ---
print("\n=== Pages ===")

# Slugs that map to service-page template
SERVICE_SLUGS = {
    "hematology", "oncology", "womens-health-services", "wellness-infusions",
    "cancer-genetic-testing", "cancers-and-conditions-we-treat",
    "infusion-therapies-we-offer", "atlanta", "infusions-suites",
}
# Slugs to skip entirely
SKIP_SLUGS = {
    "home", "", "sample-page",
    # homepage already done
    "premier-hematology-and-oncology",
}

for page in pages:
    slug = page["slug"]
    if slug in SKIP_SLUGS:
        continue

    # Check if this is a service page
    if slug in SERVICE_SLUGS:
        path = os.path.join(ROOT, slug, "index.html")
    else:
        # Could be a lead-gen, location, or other page
        path = os.path.join(ROOT, slug, "index.html")

    if not os.path.exists(path):
        skipped.append((slug, "file not found"))
        print(f"  ✗ {slug} — file not found")
        continue

    content = page.get("content", "")
    if visible_words(re.sub(r"<[^>]+>", " ", content)) < 80:
        # Update meta only
        with open(path) as f:
            html = f.read()
        updated = update_meta(html, page.get("yoast_title",""), page.get("yoast_desc",""))
        if updated != html:
            write_file(path, updated)
            print(f"  ~ {slug} — meta only (short content)")
        else:
            skipped.append((slug, "short content, no meta to update"))
        continue

    with open(path) as f:
        html = f.read()

    # Service pages: keep custom-written copy, only update meta
    result = update_meta(html, page.get("yoast_title",""), page.get("yoast_desc",""))
    reason = "meta updated"

    if result and result != html:
        write_file(path, result)
        updated_pages += 1
        print(f"  ✓ {slug}")
    else:
        skipped.append((slug, reason or "no change"))
        print(f"  ~ {slug} — {reason or 'no change'}")

print(f"\n✅ Done. Updated: {updated_posts} blog posts, {updated_pages} pages.")
print(f"⏭  Skipped: {len(skipped)}")

#!/usr/bin/env python3
"""
inject_content.py
Reads WordPress data dumps (pages + posts) and injects real content into
the static HTML files at premier-hematology/.
"""

import json
import os
import re

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DUMP_DIR = (
    "/Users/yonahfriedman/.claude/projects"
    "/-Users-yonahfriedman-Desktop-Birds-Eye-Yonah-Resume"
    "/77b2c083-f11f-436e-ba84-534fc4cabde8/tool-results"
)
PAGES_FILE = os.path.join(DUMP_DIR, "mcp-novamira-premierhematology-com-mcp-adapter-execute-ability-1782218999182.txt")
POSTS_FILE = os.path.join(DUMP_DIR, "mcp-novamira-premierhematology-com-mcp-adapter-execute-ability-1782219008126.txt")

# ── Slugs to skip entirely ─────────────────────────────────────────────────────
SKIP_SLUGS = {"", "home", "sample-page"}

# ── Page-type classification ───────────────────────────────────────────────────
LOCATION_SLUGS = {
    "astoria-infusion-center", "boro-park-infusion-center", "brooklyn-infusion-center",
    "five-towns-infusion-center", "great-neck-infusion-center", "howard-beach-infusion-center",
    "jamaica-infusion-center", "manhattan-infusion-center", "monroe-infusion-center",
    "monsey-infusion-center", "port-jefferson-infusion-center", "queens-infusion-center",
    "staten-island-infusion-center", "atlanta", "atlanta-infusion-center",
    "infusions-suites",
}
SIMPLE_PAGE_SLUGS = {
    "care-team", "contact", "billing-inquiries", "privacy-policy", "sms-privacy-policy",
    "atlanta-care-team", "contact-atlanta-center",
}
LEAD_GEN_SLUGS = {
    "anemia-iron-deficiency-consultation", "consultation-request", "energy-boost",
    "iron-infusions-request", "hematology-and-iron-infusion-appointments",
    "physician-referal", "physician-referal-atlanta", "physician-career-opportunity",
    "contact-confirmation", "contact-confirmation-atlanta-iron-consult",
    "contact-confirmation-energyboost", "contact-confirmation-gracias",
    "contact-confirmation-hematology-and-iron", "contact-confirmation-iron-request",
    "atlanta-contact-confirmation-energyboost",
    "welcome",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_dump(path):
    with open(path) as f:
        outer = json.load(f)
    return json.loads(outer["data"]["return_value"])


def strip_shortcodes(html: str) -> str:
    # Strip Elementor / WP shortcodes like [et_pb_*]...[/et_pb_*]
    html = re.sub(r'\[et_pb_[^\]]*\].*?\[/et_pb_[^\]]+\]', '', html, flags=re.DOTALL)
    # Strip all remaining shortcodes
    html = re.sub(r'\[/?[^\]]+\]', '', html)
    # Clean up <!--more-->
    html = re.sub(r'<!--more-->', '', html)
    return html.strip()


def word_count(html: str) -> int:
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&[a-z#0-9]+;', ' ', text)
    return len(text.split())


def update_meta(html: str, yoast_title: str, yoast_desc: str) -> str:
    if yoast_title:
        html = re.sub(r'<title>[^<]*</title>', f'<title>{yoast_title}</title>', html)
    if yoast_desc:
        html = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{yoast_desc}"',
            html,
        )
    return html


def inject_service_body(html: str, content: str) -> str:
    """
    Replace the placeholder paragraphs and checklist inside .service-body > div
    with real WP content. Keeps the <section class="service-body"> wrapper,
    the sidebar, and the pullquote structure intact.
    """
    # Find the opening <div> inside service-body (first child div before sidebar)
    # Strategy: replace everything between service-body's inner div open tag
    # and the <aside class="service-sidebar"> (or closing </section> if no aside)
    pattern = re.compile(
        r'(<section class="service-body">\s*<div>)(.*?)(<aside class="service-sidebar"|</section>)',
        re.DOTALL,
    )
    m = pattern.search(html)
    if not m:
        return None  # can't find target

    new_inner = f'\n{content}\n    '
    replacement = m.group(1) + new_inner + m.group(3)
    return pattern.sub(replacement, html, count=1)


def inject_article_prose(html: str, content: str) -> str:
    """
    Replace everything between <article class="article-prose"> and
    <div class="article-footer"> with real WP content.
    """
    pattern = re.compile(
        r'(<article class="article-prose">)(.*?)(<div class="article-footer">)',
        re.DOTALL,
    )
    m = pattern.search(html)
    if not m:
        return None

    replacement = m.group(1) + '\n' + content + '\n    ' + m.group(3)
    return pattern.sub(replacement, html, count=1)


def classify_page(slug: str) -> str:
    if slug in LOCATION_SLUGS or "infusion-center" in slug:
        return "location"
    if slug in SIMPLE_PAGE_SLUGS:
        return "simple"
    if slug in LEAD_GEN_SLUGS or "contact" in slug or "confirmation" in slug:
        return "lead_gen"
    return "service"


# ── Main ───────────────────────────────────────────────────────────────────────

def process_items(items, is_post=False):
    updated = []
    skipped = []

    for item in items:
        slug = item.get("slug", "").strip()
        raw_content = item.get("content", "")
        yoast_title = item.get("yoast_title", "") or ""
        yoast_desc = item.get("yoast_desc", "") or ""

        # Skip homepage / blank slugs
        if not slug or slug in SKIP_SLUGS:
            skipped.append((slug, "homepage/blank slug"))
            continue

        # Determine file path
        if is_post:
            html_path = os.path.join(BASE, "blog", slug, "index.html")
        else:
            html_path = os.path.join(BASE, slug, "index.html")

        if not os.path.exists(html_path):
            skipped.append((slug, "file not found"))
            continue

        # Clean WP content
        content = strip_shortcodes(raw_content)

        # Word count check
        wc = word_count(content)

        if is_post:
            # Blog post
            if wc < 50:
                skipped.append((slug, f"too short ({wc} words)"))
                continue

            with open(html_path) as f:
                html = f.read()

            new_html = inject_article_prose(html, content)
            if new_html is None:
                skipped.append((slug, "article-prose marker not found"))
                continue

            new_html = update_meta(new_html, yoast_title, yoast_desc)
            with open(html_path, "w") as f:
                f.write(new_html)
            updated.append((slug, "blog post"))

        else:
            # Page
            page_type = classify_page(slug)

            if page_type == "location":
                if wc < 100:
                    skipped.append((slug, f"location page too short ({wc} words)"))
                    continue
            elif page_type in ("lead_gen", "simple"):
                if wc < 100:
                    skipped.append((slug, f"{page_type} page too short ({wc} words)"))
                    continue
            else:
                # service page
                if wc < 50:
                    skipped.append((slug, f"service page too short ({wc} words)"))
                    continue

            with open(html_path) as f:
                html = f.read()

            if page_type == "service":
                new_html = inject_service_body(html, content)
                if new_html is None:
                    skipped.append((slug, "service-body marker not found"))
                    continue
            else:
                # For lead_gen, location, simple — inject into article-prose if present,
                # otherwise inject into service-body if present, else skip.
                if 'class="article-prose"' in html:
                    new_html = inject_article_prose(html, content)
                elif 'class="service-body"' in html:
                    new_html = inject_service_body(html, content)
                else:
                    skipped.append((slug, f"{page_type}: no injectable section found"))
                    continue
                if new_html is None:
                    skipped.append((slug, f"{page_type}: injection failed"))
                    continue

            new_html = update_meta(new_html, yoast_title, yoast_desc)
            with open(html_path, "w") as f:
                f.write(new_html)
            updated.append((slug, page_type))

    return updated, skipped


def main():
    print("Loading data dumps...")
    pages = load_dump(PAGES_FILE)
    posts = load_dump(POSTS_FILE)
    print(f"  Pages: {len(pages)}, Posts: {len(posts)}")

    print("\n── Processing pages ──")
    p_updated, p_skipped = process_items(pages, is_post=False)

    print("\n── Processing posts ──")
    b_updated, b_skipped = process_items(posts, is_post=True)

    all_updated = p_updated + b_updated
    all_skipped = p_skipped + b_skipped

    print("\n── Updated ──")
    for slug, kind in all_updated:
        print(f"  [OK] {slug}  ({kind})")

    print("\n── Skipped ──")
    for slug, reason in all_skipped:
        print(f"  [SKIP] {slug or '(empty)'}  — {reason}")

    # Count skip reasons
    from collections import Counter
    reason_counts = Counter(r for _, r in all_skipped)

    print("\n── Summary ──")
    print(f"  Pages updated : {len(p_updated)}")
    print(f"  Posts updated : {len(b_updated)}")
    print(f"  Total updated : {len(all_updated)}")
    print(f"  Total skipped : {len(all_skipped)}")
    print("\n  Top skip reasons:")
    for reason, count in reason_counts.most_common(10):
        print(f"    {count:3d}x  {reason}")


if __name__ == "__main__":
    main()

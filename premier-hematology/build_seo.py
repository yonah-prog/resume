#!/usr/bin/env python3
"""
SEO build pipeline for premier-hematology static site.

What this does:
  1. Reads seo.json  — the single source of truth for every page's metadata
  2. Injects into each page's <head>:
       - <title>
       - <meta name="description">
       - <link rel="canonical">
       - Open Graph tags (og:title, og:description, og:url, og:image, og:type)
       - Twitter Card tags
       - JSON-LD structured data (MedicalWebPage, BlogPosting, MedicalClinic,
         LocalBusiness, BreadcrumbList)
  3. Writes sitemap.xml
  4. Writes robots.txt

Run: python3 build_seo.py
"""

import json, os, re, datetime

ROOT    = os.path.dirname(os.path.abspath(__file__))
SEO_FILE = os.path.join(ROOT, "seo.json")
SITE_URL = "https://www.premierhematology.com"
DEFAULT_OG_IMAGE = f"{SITE_URL}/assets/img/og-default.jpg"
ORG_NAME = "Premier Hematology & Oncology"
PHONE    = "+17189972281"
ADDRESS  = {
    "streetAddress": "Multiple locations across New York metro",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "11373",
    "addressCountry": "US"
}

# ---------------------------------------------------------------------------
# Schema builders
# ---------------------------------------------------------------------------

def org_schema():
    return {
        "@type": "MedicalOrganization",
        "@id": f"{SITE_URL}/#organization",
        "name": ORG_NAME,
        "url": SITE_URL,
        "logo": f"{SITE_URL}/assets/img/logo.png",
        "telephone": PHONE,
        "sameAs": [
            "https://www.facebook.com/premierhematology",
        ],
        "address": ADDRESS,
    }

def webpage_schema(url, title, description, breadcrumbs=None):
    s = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": title,
                "description": description,
                "isPartOf": {"@id": f"{SITE_URL}/#website"},
                "about": {"@id": f"{SITE_URL}/#organization"},
            },
            {
                "@type": "WebSite",
                "@id": f"{SITE_URL}/#website",
                "url": SITE_URL,
                "name": ORG_NAME,
                "publisher": {"@id": f"{SITE_URL}/#organization"},
            },
            org_schema(),
        ]
    }
    if breadcrumbs:
        s["@graph"].append(breadcrumb_schema(breadcrumbs))
    return s

def blog_schema(url, title, description, date, author=ORG_NAME, image=None):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": f"{url}#article",
                "url": url,
                "headline": title,
                "description": description,
                "datePublished": date,
                "dateModified": date,
                "author": {
                    "@type": "Organization",
                    "name": author,
                    "url": SITE_URL,
                },
                "publisher": {
                    "@type": "Organization",
                    "name": ORG_NAME,
                    "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/assets/img/logo.png"},
                },
                "image": image or DEFAULT_OG_IMAGE,
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            },
            org_schema(),
        ]
    }

def location_schema(url, city, address_str, phone, description):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["MedicalClinic", "LocalBusiness"],
                "@id": f"{url}#clinic",
                "name": f"{ORG_NAME} — {city}",
                "url": url,
                "description": description,
                "telephone": phone or PHONE,
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": address_str,
                    "addressLocality": city,
                    "addressRegion": "NY" if city != "Atlanta" else "GA",
                    "addressCountry": "US",
                },
                "medicalSpecialty": ["Hematology", "Oncology"],
                "availableService": [
                    {"@type": "MedicalTherapy", "name": "Iron Infusion Therapy"},
                    {"@type": "MedicalTherapy", "name": "Chemotherapy Administration"},
                    {"@type": "MedicalTherapy", "name": "Wellness Infusions"},
                ],
                "openingHours": "Mo-Fr 09:00-17:00",
                "isPartOf": {"@id": f"{SITE_URL}/#organization"},
            },
            org_schema(),
        ]
    }

def breadcrumb_schema(items):
    """items = [("Home", "/"), ("Hematology", "/hematology/")]"""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": f"{SITE_URL}{path}",
            }
            for i, (name, path) in enumerate(items)
        ],
    }

# ---------------------------------------------------------------------------
# Head block builder
# ---------------------------------------------------------------------------

def build_head_block(title, description, url, og_image, schema_json,
                     og_type="website", is_noindex=False):
    esc_title = title.replace('"', '&quot;')
    esc_desc  = description.replace('"', '&quot;')
    esc_url   = url
    schema_str = json.dumps(schema_json, indent=2)

    noindex = '\n  <meta name="robots" content="noindex, nofollow">' if is_noindex else ""

    return f"""\
  <title>{title}</title>
  <meta name="description" content="{esc_desc}">{noindex}
  <link rel="canonical" href="{esc_url}">
  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{esc_title}">
  <meta property="og:description" content="{esc_desc}">
  <meta property="og:url" content="{esc_url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:site_name" content="{ORG_NAME}">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc_title}">
  <meta name="twitter:description" content="{esc_desc}">
  <meta name="twitter:image" content="{og_image}">
  <!-- JSON-LD -->
  <script type="application/ld+json">
{schema_str}
  </script>"""

# ---------------------------------------------------------------------------
# Inject into HTML file
# ---------------------------------------------------------------------------

def inject_into_file(path, head_block):
    with open(path) as f:
        html = f.read()

    # Remove any existing title / meta description / canonical / OG / LD+JSON
    # that were previously injected (idempotent)
    html = re.sub(r'  <title>.*?</title>\n', '', html, flags=re.DOTALL)
    html = re.sub(r'  <meta name="description"[^\n]*\n', '', html)
    html = re.sub(r'  <meta name="robots"[^\n]*\n', '', html)
    html = re.sub(r'  <link rel="canonical"[^\n]*\n', '', html)
    html = re.sub(r'  <!-- Open Graph -->.*?<!-- JSON-LD -->\n  <script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)

    # Insert after the last <link> in <head> (before </head>)
    html = html.replace('</head>', head_block + '\n</head>', 1)

    with open(path, 'w') as f:
        f.write(html)

# ---------------------------------------------------------------------------
# Page classification helpers
# ---------------------------------------------------------------------------

LOCATION_SLUGS = {
    "astoria-infusion-center":      ("Astoria",       "23-10 31st St, Astoria, NY 11105",     "+17188663037"),
    "boro-park-infusion-center":    ("Boro Park",     "4915 13th Ave, Brooklyn, NY 11219",     "+17188663037"),
    "brooklyn-infusion-center":     ("Brooklyn",      "Brooklyn, NY",                          "+17188663037"),
    "five-towns-infusion-center":   ("Five Towns",    "Lawrence, NY 11559",                    "+17188663037"),
    "great-neck-infusion-center":   ("Great Neck",    "Great Neck, NY 11021",                  "+17188663037"),
    "howard-beach-infusion-center": ("Howard Beach",  "Howard Beach, Queens, NY 11414",        "+17188663037"),
    "jamaica-infusion-center":      ("Jamaica",       "Jamaica, Queens, NY 11432",             "+17188663037"),
    "manhattan-infusion-center":    ("Manhattan",     "Manhattan, New York, NY",               "+17188663037"),
    "monroe-infusion-center":       ("Monroe",        "Monroe, NY 10950",                      "+17188663037"),
    "monsey-infusion-center":       ("Monsey",        "Monsey, NY 10952",                      "+17188663037"),
    "port-jefferson-infusion-center":("Port Jefferson","Port Jefferson, NY 11777",             "+17188663037"),
    "queens-infusion-center":       ("Queens",        "Queens, NY",                            "+17188663037"),
    "staten-island-infusion-center":("Staten Island", "Staten Island, NY",                     "+17188663037"),
    "atlanta-infusion-center":      ("Atlanta",       "325 Hammond Dr SW, Atlanta, GA 30315",  "+14045550100"),
}

SERVICE_SLUGS = {
    "hematology", "oncology", "womens-health-services", "wellness-infusions",
    "cancer-genetic-testing", "cancers-and-conditions-we-treat",
    "infusion-therapies-we-offer", "infusions-suites",
}

NOINDEX_SLUGS = {
    "contact-confirmation", "contact-confirmation-iron-request",
    "contact-confirmation-energyboost", "contact-confirmation-hematology-and-iron",
    "contact-confirmation-gracias", "contact-confirmation-atlanta-iron-consult",
    "atlanta-contact-confirmation-energyboost", "welcome",
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

with open(SEO_FILE) as f:
    seo = json.load(f)

updated = 0
sitemap_urls = []

for page_slug, meta in seo.items():
    is_post = meta.get("is_post", False)

    if is_post:
        path = os.path.join(ROOT, "blog", page_slug, "index.html")
        url  = f"{SITE_URL}/blog/{page_slug}/"
        breadcrumbs = [("Home", "/"), ("Blog", "/blog/"), (meta["title"][:40] if meta["title"] else page_slug, f"/blog/{page_slug}/")]
    elif page_slug in ("", "home", "premier-hematology-and-oncology"):
        path = os.path.join(ROOT, "index.html")
        url  = f"{SITE_URL}/"
        breadcrumbs = [("Home", "/")]
    else:
        path = os.path.join(ROOT, page_slug, "index.html")
        url  = f"{SITE_URL}/{page_slug}/"
        breadcrumbs = [("Home", "/"), (meta["title"][:40] if meta["title"] else page_slug, f"/{page_slug}/")]

    if not os.path.exists(path):
        continue

    title       = meta.get("title") or f"{ORG_NAME}"
    description = meta.get("description") or f"Expert hematology and oncology care at {ORG_NAME}."
    date        = meta.get("date", datetime.date.today().isoformat())
    og_image    = meta.get("og_image", DEFAULT_OG_IMAGE)
    is_noindex  = page_slug in NOINDEX_SLUGS

    # Pick schema type
    if is_post:
        schema = blog_schema(url, title, description, date, image=og_image)
        og_type = "article"
    elif page_slug in LOCATION_SLUGS:
        city, addr, phone = LOCATION_SLUGS[page_slug]
        schema = location_schema(url, city, addr, phone, description)
        og_type = "website"
    else:
        schema = webpage_schema(url, title, description)
        og_type = "website"

    head = build_head_block(title, description, url, og_image, schema,
                            og_type=og_type, is_noindex=is_noindex)
    inject_into_file(path, head)
    updated += 1

    if not is_noindex:
        sitemap_urls.append((url, date if is_post else datetime.date.today().isoformat()))

# ---------------------------------------------------------------------------
# Homepage (not in seo.json if slug is blank/home) — ensure it's covered
# ---------------------------------------------------------------------------
home_path = os.path.join(ROOT, "index.html")
if os.path.exists(home_path):
    home_url = f"{SITE_URL}/"
    home_schema = webpage_schema(
        home_url,
        "Premier Hematology & Oncology | Infusion Therapy & Cancer Care",
        "Expert hematology & oncology care in New York. Services include cancer genetic testing, infusion therapy, & women's health support.",
    )
    home_schema["@graph"].append({
        "@type": "MedicalOrganization",
        "name": ORG_NAME,
        "url": SITE_URL,
        "telephone": PHONE,
        "medicalSpecialty": ["Hematology", "Oncology"],
        "areaServed": ["New York", "Atlanta"],
        "address": ADDRESS,
        "sameAs": ["https://www.facebook.com/premierhematology"],
    })
    head = build_head_block(
        "Premier Hematology & Oncology | Infusion Therapy & Cancer Care",
        "Expert hematology & oncology care in New York. Services include cancer genetic testing, infusion therapy, & women's health support.",
        home_url,
        DEFAULT_OG_IMAGE,
        home_schema,
    )
    inject_into_file(home_path, head)
    sitemap_urls.insert(0, (home_url, datetime.date.today().isoformat()))
    updated += 1

# ---------------------------------------------------------------------------
# sitemap.xml
# ---------------------------------------------------------------------------

sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, lastmod in sorted(set(sitemap_urls)):
    sitemap_lines.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>")
sitemap_lines.append("</urlset>")

with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write("\n".join(sitemap_lines))

# ---------------------------------------------------------------------------
# robots.txt
# ---------------------------------------------------------------------------

robots = f"""User-agent: *
Allow: /

# Block confirmation/utility pages from indexing
Disallow: /contact-confirmation/
Disallow: /contact-confirmation-iron-request/
Disallow: /contact-confirmation-energyboost/
Disallow: /contact-confirmation-hematology-and-iron/
Disallow: /contact-confirmation-gracias/
Disallow: /contact-confirmation-atlanta-iron-consult/
Disallow: /atlanta-contact-confirmation-energyboost/
Disallow: /welcome/

Sitemap: {SITE_URL}/sitemap.xml
"""
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(robots)

print(f"✅ SEO build complete.")
print(f"   Pages updated: {updated}")
print(f"   Sitemap URLs:  {len(sitemap_urls)}")
print(f"   robots.txt:    written")
print(f"   sitemap.xml:   written")

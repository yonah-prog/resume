#!/usr/bin/env python3
"""
Premier Hematology – Static Site Generator
Run: python3 generate.py
Outputs all HTML pages into the correct directory structure.
"""

import os, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Shared partials
# ---------------------------------------------------------------------------

HEAD = lambda title, desc, css_path="assets/css/style.css": f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/{css_path}">"""

HEADER = """\
  <!-- UTILITY BAR -->
  <div class="util-bar">
    <div class="util-bar__inner">
      <span class="util-bar__portal"><span class="util-bar__dot"></span> Patient Portal</span>
      <span class="util-bar__phone">718-866-3037</span>
    </div>
  </div>

  <!-- HEADER -->
  <header class="site-header">
    <div class="site-header__inner">
      <a href="/" class="logo" aria-label="Premier Hematology &amp; Oncology home">
        <div class="logo__mark"><div class="logo__ribbon"></div></div>
        <div class="logo__text">
          <div class="logo__name">PREMIER HEMATOLOGY</div>
          <div class="logo__sub">ONCOLOGY</div>
        </div>
      </a>
      <button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false">
        <span class="nav-toggle__bar"></span>
        <span class="nav-toggle__bar"></span>
        <span class="nav-toggle__bar"></span>
      </button>
      <ul class="site-nav" id="site-nav">
        <li class="site-nav__item"><a class="site-nav__link" href="/care-team/">Care Team</a></li>
        <li class="site-nav__item">
          <span class="site-nav__link">Our Services <span class="site-nav__arrow">&#9660;</span></span>
          <div class="site-nav__dropdown">
            <a href="/hematology/">Hematology</a>
            <a href="/oncology/">Oncology</a>
            <a href="/womens-health-services/">Women's Health</a>
            <a href="/wellness-infusions/">Wellness Infusions</a>
            <a href="/cancer-genetic-testing/">Cancer Genetic Testing</a>
            <a href="/cancers-and-conditions-we-treat/">Cancers &amp; Conditions</a>
            <a href="/infusion-therapies-we-offer/">Infusion Therapies</a>
          </div>
        </li>
        <li class="site-nav__item">
          <span class="site-nav__link">Locations <span class="site-nav__arrow">&#9660;</span></span>
          <div class="site-nav__dropdown">
            <a href="/astoria-infusion-center/">Astoria</a>
            <a href="/boro-park-infusion-center/">Boro Park</a>
            <a href="/brooklyn-infusion-center/">Brooklyn</a>
            <a href="/five-towns-infusion-center/">Five Towns</a>
            <a href="/great-neck-infusion-center/">Great Neck</a>
            <a href="/howard-beach-infusion-center/">Howard Beach</a>
            <a href="/jamaica-infusion-center/">Jamaica</a>
            <a href="/manhattan-infusion-center/">Manhattan</a>
            <a href="/monroe-infusion-center/">Monroe</a>
            <a href="/monsey-infusion-center/">Monsey</a>
            <a href="/port-jefferson-infusion-center/">Port Jefferson</a>
            <a href="/queens-infusion-center/">Queens</a>
            <a href="/staten-island-infusion-center/">Staten Island</a>
          </div>
        </li>
        <li class="site-nav__item"><a class="site-nav__link" href="/blog/">Blog</a></li>
        <li class="site-nav__item"><a class="btn btn--sm" href="/contact/">Contact Us</a></li>
      </ul>
    </div>
  </header>"""

FOOTER = """\
  <!-- FOOTER -->
  <footer class="site-footer">
    <div class="site-footer__grid">
      <div>
        <div class="site-footer__logo">
          <div class="site-footer__logo-mark"><div class="site-footer__logo-ribbon"></div></div>
          <div class="site-footer__logo-text">
            <div class="site-footer__logo-name">PREMIER HEMATOLOGY</div>
            <div class="site-footer__logo-sub">ONCOLOGY</div>
          </div>
        </div>
        <p class="site-footer__blurb">Delivering compassionate, expert hematology and oncology care with convenient access across the New York metro area and beyond.</p>
      </div>
      <div>
        <div class="site-footer__col-label">Contact Us</div>
        <div class="site-footer__links">
          <a href="tel:7189972281">718-997-2281</a>
          <a href="/contact/">Email Us</a>
          <a href="/physician-referal/">Physician Referral Form</a>
        </div>
      </div>
      <div>
        <div class="site-footer__col-label">Quick Links</div>
        <div class="site-footer__links">
          <a href="/care-team/">Care Team</a>
          <a href="/hematology/">Hematology</a>
          <a href="/oncology/">Oncology</a>
          <a href="/infusion-therapies-we-offer/">Our Services</a>
          <a href="/blog/">Blog</a>
          <a href="/contact/">Contact Us</a>
        </div>
      </div>
      <div>
        <div class="site-footer__col-label">Our Locations</div>
        <div class="site-footer__locations">
          <a href="/astoria-infusion-center/">Astoria</a>
          <a href="/boro-park-infusion-center/">Boro Park</a>
          <a href="/brooklyn-infusion-center/">Brooklyn</a>
          <a href="/five-towns-infusion-center/">Five Towns</a>
          <a href="/great-neck-infusion-center/">Great Neck</a>
          <a href="/howard-beach-infusion-center/">Howard Beach</a>
          <a href="/jamaica-infusion-center/">Jamaica</a>
          <a href="/manhattan-infusion-center/">Manhattan</a>
          <a href="/monroe-infusion-center/">Monroe</a>
          <a href="/monsey-infusion-center/">Monsey</a>
          <a href="/queens-infusion-center/">Queens</a>
          <a href="/staten-island-infusion-center/">Staten Island</a>
        </div>
      </div>
    </div>
    <div class="site-footer__bottom">
      <div class="site-footer__bottom-inner">
        <span>&copy; 2026 Premier Hematology &amp; Oncology. All rights reserved.</span>
        <div class="site-footer__bottom-links">
          <a href="/privacy-policy/">Privacy Policy</a>
          <a href="/sms-privacy-policy/">SMS Privacy Policy</a>
        </div>
      </div>
    </div>
  </footer>
  <script src="/assets/js/nav.js"></script>"""

# ---------------------------------------------------------------------------
# Template builders
# ---------------------------------------------------------------------------

def service_page(slug, title, yoast_title, meta_desc, eyebrow, h1, lead,
                 body_paras, bullets, facts, pullquote,
                 related, breadcrumb_label, img_label="Infusion center interior"):
    related_html = ""
    for r in related:
        related_html += f"""
        <a href="/{r['slug']}/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__img img-placeholder">{r['img']}</div>
          <div class="related-card__body">
            <h3 class="related-card__title">{r['title']}</h3>
            <p class="related-card__desc">{r['desc']}</p>
            <span class="related-card__link">Learn more &rarr;</span>
          </div>
        </a>"""

    bullets_html = ""
    for b in bullets:
        bullets_html += f"""
            <div class="checklist__item">
              <span class="checklist__check">&#10003;</span>
              <span class="checklist__text">{b}</span>
            </div>"""

    facts_html = ""
    for k, v in facts:
        facts_html += f"""
            <div class="fact-row">
              <span class="fact-row__key">{k}</span>
              <span class="fact-row__val">{v}</span>
            </div>"""

    body_html = ""
    for p in body_paras:
        body_html += f'        <p class="service-body__p">{p}</p>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title, meta_desc)}
</head>
<body>

{HEADER}

  <!-- PAGE HERO -->
  <section class="service-hero">
    <div class="service-hero__inner">
      <div class="breadcrumb">
        <a href="/">Home</a><span class="breadcrumb__sep">/</span>
        <a href="/infusion-therapies-we-offer/">Our Services</a><span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">{breadcrumb_label}</span>
      </div>
      <div class="eyebrow-sans service-hero__eyebrow">{eyebrow}</div>
      <h1 class="service-hero__h1">{h1}</h1>
      <p class="service-hero__lead">{lead}</p>
    </div>
  </section>

  <!-- HERO IMAGE -->
  <section class="service-media">
    <div class="service-media__img img-placeholder">{img_label}</div>
  </section>

  <!-- BODY -->
  <section class="service-body">
    <div>
      <h2 class="service-body__h2">What to expect</h2>
{body_html}
      <h3 class="service-body__h3">Services offered</h3>
      <div class="checklist">{bullets_html}
      </div>
      <div class="pullquote">
        <p>{pullquote}</p>
      </div>
    </div>

    <aside class="service-sidebar">
      <div class="sidebar-cta">
        <h3 class="sidebar-cta__h3">Ready to begin?</h3>
        <p class="sidebar-cta__p">Next-day appointments available. Talk to our team about your treatment plan.</p>
        <a href="/anemia-iron-deficiency-consultation/" class="btn" style="display:block;text-align:center;">Book an appointment</a>
      </div>
      <div class="sidebar-facts">
        <div class="sidebar-facts__label">Quick facts</div>{facts_html}
      </div>
    </aside>
  </section>

  <!-- RELATED -->
  <section class="related-section">
    <div class="related-section__inner">
      <h2 class="related-section__h2">Related services</h2>
      <div class="related-grid">{related_html}
      </div>
    </div>
  </section>

{FOOTER}
</body>
</html>"""


def location_page(slug, city, address, phone, yoast_title, meta_desc, nearby=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title or f"{city} Infusion Center | Premier Hematology Oncology",
      meta_desc or f"Premier Hematology Oncology's {city} Infusion Center provides expert IV therapy and compassionate care in a welcoming environment.")}
</head>
<body>

{HEADER}

  <section class="service-hero">
    <div class="service-hero__inner">
      <div class="breadcrumb">
        <a href="/">Home</a><span class="breadcrumb__sep">/</span>
        <a href="/locations/">Locations</a><span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">{city}</span>
      </div>
      <div class="eyebrow-sans service-hero__eyebrow">Infusion Center</div>
      <h1 class="service-hero__h1">{city} Infusion Center</h1>
      <p class="service-hero__lead">Expert IV therapy and compassionate care — conveniently located in {city}{", " + nearby if nearby else ""}, close to home.</p>
    </div>
  </section>

  <section class="service-media">
    <div class="service-media__img img-placeholder">{city} infusion center interior</div>
  </section>

  <section class="service-body">
    <div>
      <h2 class="service-body__h2">Your {city} care center</h2>
      <p class="service-body__p">At our {city} infusion center, we deliver personalized IV therapy and hematology-oncology care in a comfortable, welcoming environment. Our board-certified team tailors every treatment plan to your specific needs — no long hospital waits required.</p>
      <p class="service-body__p">We perform treatments on-site with an in-house lab, so you get faster results and spend less time waiting. Next-day appointments are available for most services.</p>

      <h3 class="service-body__h3">Services offered at this location</h3>
      <div class="checklist">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Iron infusion therapy for iron-deficiency anemia</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Chemotherapy and immunotherapy administration</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Wellness and hydration infusions</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Injectable medications and biologics</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">On-site lab work and monitoring</span></div>
      </div>
      <div class="pullquote">
        <p>"Skip the long waits at hospitals and labs. At Premier Hematology, we perform treatments right on site."</p>
      </div>
    </div>

    <aside class="service-sidebar">
      <div class="sidebar-cta">
        <h3 class="sidebar-cta__h3">Ready to begin?</h3>
        <p class="sidebar-cta__p">Next-day appointments available at our {city} location.</p>
        <a href="/anemia-iron-deficiency-consultation/" class="btn" style="display:block;text-align:center;">Book an appointment</a>
      </div>
      <div class="sidebar-facts">
        <div class="sidebar-facts__label">Location details</div>
        <div class="fact-row"><span class="fact-row__key">Address</span><span class="fact-row__val">{address}</span></div>
        <div class="fact-row"><span class="fact-row__key">Phone</span><span class="fact-row__val">{phone}</span></div>
        <div class="fact-row"><span class="fact-row__key">Appointments</span><span class="fact-row__val">Next-day</span></div>
        <div class="fact-row"><span class="fact-row__key">Lab results</span><span class="fact-row__val">On-site</span></div>
      </div>
    </aside>
  </section>

  <section class="related-section">
    <div class="related-section__inner">
      <h2 class="related-section__h2">Our services</h2>
      <div class="related-grid">
        <a href="/hematology/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__img img-placeholder">Hematology</div>
          <div class="related-card__body">
            <h3 class="related-card__title">Hematology</h3>
            <p class="related-card__desc">Specialized care for blood health and blood-related diseases.</p>
            <span class="related-card__link">Learn more &rarr;</span>
          </div>
        </a>
        <a href="/wellness-infusions/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__img img-placeholder">Wellness Infusions</div>
          <div class="related-card__body">
            <h3 class="related-card__title">Wellness Infusions</h3>
            <p class="related-card__desc">Nutritional support and supplementation for patients who need it.</p>
            <span class="related-card__link">Learn more &rarr;</span>
          </div>
        </a>
        <a href="/womens-health-services/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__img img-placeholder">Women's Health</div>
          <div class="related-card__body">
            <h3 class="related-card__title">Women's Health</h3>
            <p class="related-card__desc">Care attuned to your unique health needs at every stage.</p>
            <span class="related-card__link">Learn more &rarr;</span>
          </div>
        </a>
      </div>
    </div>
  </section>

{FOOTER}
</body>
</html>"""


def article_page(slug, title, yoast_title, meta_desc, category, author, date, read_time, body_html, related_posts):
    related_html = ""
    for p in related_posts:
        related_html += f"""
        <a href="/blog/{p['slug']}/" style="text-decoration:none;color:inherit;">
          <div class="blog-card__img img-placeholder">{p['title'][:30]}</div>
          <div class="blog-card__cat">{p['cat']}</div>
          <h3 class="blog-card__title">{p['title']}</h3>
        </a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title or title, meta_desc)}
</head>
<body>

{HEADER}

  <!-- ARTICLE HEADER -->
  <header class="article-header">
    <div class="breadcrumb">
      <a href="/">Home</a><span class="breadcrumb__sep">/</span>
      <a href="/blog/">Blog</a><span class="breadcrumb__sep">/</span>
      <span class="breadcrumb__current">{category}</span>
    </div>
    <div class="article-cat">{category}</div>
    <h1 class="article-header__h1">{title}</h1>
    <div class="article-byline">
      <div class="article-byline__avatar" aria-hidden="true"></div>
      <div>
        <div class="article-byline__name">{author}</div>
        <div class="article-byline__meta">{date} &middot; {read_time} min read</div>
      </div>
    </div>
  </header>

  <!-- HERO IMAGE -->
  <div class="article-hero-wrap">
    <div class="article-hero-wrap__img img-placeholder">{title[:40]}</div>
  </div>

  <!-- PROSE -->
  <article class="article-prose">
{body_html}
    <div class="article-footer">
      <div class="article-footer__author">
        <div class="article-footer__avatar" aria-hidden="true"></div>
        <div>
          <div class="article-footer__name">{author}</div>
          <div class="article-footer__title">Premier Hematology &amp; Oncology</div>
        </div>
      </div>
      <a href="/anemia-iron-deficiency-consultation/" class="btn btn--sm">Book a consultation</a>
    </div>
  </article>

  <!-- MORE FROM BLOG -->
  <section class="more-blog">
    <div class="more-blog__inner">
      <h2 class="more-blog__h2">More from the blog</h2>
      <div class="blog-grid">{related_html}
      </div>
    </div>
  </section>

{FOOTER}
</body>
</html>"""


def simple_page(title, meta_desc, h1, lead, body_html):
    """Generic page for contact, care team, locations hub, etc."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(title, meta_desc)}
</head>
<body>

{HEADER}

  <section class="service-hero">
    <div class="service-hero__inner">
      <h1 class="service-hero__h1">{h1}</h1>
      <p class="service-hero__lead">{lead}</p>
    </div>
  </section>

  <section style="max-width:1100px;margin:0 auto;padding:64px 40px;">
{body_html}
  </section>

{FOOTER}
</body>
</html>"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path}")


# ---------------------------------------------------------------------------
# RELATED helpers
# ---------------------------------------------------------------------------
RELATED_SERVICES = {
    "hematology": [
        {"slug": "oncology", "title": "Oncology", "desc": "Comprehensive cancer treatment guided by your dedicated care team.", "img": "Oncology"},
        {"slug": "womens-health-services", "title": "Women's Health", "desc": "Care attuned to your unique health needs at every stage.", "img": "Women's Health"},
        {"slug": "infusion-therapies-we-offer", "title": "Infusion Centers", "desc": "Tailor-made infusion care at conveniently located centers near you.", "img": "Infusion Centers"},
    ],
    "oncology": [
        {"slug": "hematology", "title": "Hematology", "desc": "Specialized care for blood health and blood-related diseases.", "img": "Hematology"},
        {"slug": "cancer-genetic-testing", "title": "Cancer Genetic Testing", "desc": "Robust genetic screening, counseling and testing for patients.", "img": "Genetic Testing"},
        {"slug": "infusion-therapies-we-offer", "title": "Infusion Centers", "desc": "Tailor-made infusion care at conveniently located centers near you.", "img": "Infusion Centers"},
    ],
    "womens-health-services": [
        {"slug": "wellness-infusions", "title": "Wellness Infusions", "desc": "Nutritional support and supplementation for patients who need it.", "img": "Wellness"},
        {"slug": "hematology", "title": "Hematology", "desc": "Specialized care for blood health and blood-related diseases.", "img": "Hematology"},
        {"slug": "infusion-therapies-we-offer", "title": "Infusion Centers", "desc": "Tailor-made infusion care at conveniently located centers.", "img": "Infusion Centers"},
    ],
    "wellness-infusions": [
        {"slug": "womens-health-services", "title": "Women's Health", "desc": "Care attuned to your unique health needs at every stage.", "img": "Women's Health"},
        {"slug": "hematology", "title": "Hematology", "desc": "Specialized care for blood health and blood-related diseases.", "img": "Hematology"},
        {"slug": "infusion-therapies-we-offer", "title": "Infusion Centers", "desc": "Tailor-made infusion care at conveniently located centers.", "img": "Infusion Centers"},
    ],
    "cancer-genetic-testing": [
        {"slug": "oncology", "title": "Oncology", "desc": "Comprehensive cancer treatment guided by your dedicated care team.", "img": "Oncology"},
        {"slug": "hematology", "title": "Hematology", "desc": "Specialized care for blood health and blood-related diseases.", "img": "Hematology"},
        {"slug": "cancers-and-conditions-we-treat", "title": "Cancers We Treat", "desc": "Expert, personalized care across a wide range of cancers and conditions.", "img": "Conditions"},
    ],
    "cancers-and-conditions-we-treat": [
        {"slug": "oncology", "title": "Oncology", "desc": "Comprehensive cancer treatment guided by your dedicated care team.", "img": "Oncology"},
        {"slug": "cancer-genetic-testing", "title": "Cancer Genetic Testing", "desc": "Robust genetic screening, counseling and testing for patients.", "img": "Genetic Testing"},
        {"slug": "infusion-therapies-we-offer", "title": "Infusion Centers", "desc": "Tailor-made infusion care at conveniently located centers.", "img": "Infusion Centers"},
    ],
    "infusion-therapies-we-offer": [
        {"slug": "hematology", "title": "Hematology", "desc": "Specialized care for blood health and blood-related diseases.", "img": "Hematology"},
        {"slug": "wellness-infusions", "title": "Wellness Infusions", "desc": "Nutritional support and supplementation for patients who need it.", "img": "Wellness"},
        {"slug": "cancer-genetic-testing", "title": "Cancer Genetic Testing", "desc": "Robust genetic screening, counseling and testing.", "img": "Genetic Testing"},
    ],
}

BLOG_RELATED = [
    {"slug": "iron-infusion-benefits-side-effects-what-to-expect", "title": "Iron Infusion: Benefits, Side Effects & What To Expect", "cat": "Hematology"},
    {"slug": "when-to-see-a-hematologist-signs-you-shouldnt-ignore", "title": "When to See a Hematologist: Signs You Shouldn't Ignore", "cat": "Hematology"},
    {"slug": "5-surprising-benefits-of-infusion-therapy-that-will-change-your-life", "title": "5 Surprising Benefits of Infusion Therapy", "cat": "Wellness"},
]

# ---------------------------------------------------------------------------
# SERVICE PAGES
# ---------------------------------------------------------------------------
print("\n📄 Service pages...")

write("hematology/index.html", service_page(
    slug="hematology",
    title="Hematology",
    yoast_title="Hematology Specialists Near You | Premier Hematology",
    meta_desc="Expert care for blood disorders from trusted hematology specialists. Visit Premier Hematology Oncology for personalized diagnosis.",
    eyebrow="Our Services",
    h1="Expert Hematology Care for Blood Disorders",
    lead="Our board-certified hematologists provide specialized care for a wide range of blood disorders — from anemia and iron deficiency to complex blood cancers — all under one roof.",
    body_paras=[
        "Hematology is the branch of medicine concerned with blood, blood-forming organs, and blood diseases. At Premier Hematology & Oncology, our specialists bring years of experience diagnosing and treating conditions ranging from iron deficiency anemia to rare hematological malignancies.",
        "We perform evaluations and treatments on-site, including in-house lab work, so you avoid the long waits typical of hospital settings. From your first consultation, you'll have a dedicated care team working around your schedule.",
    ],
    bullets=[
        "Iron deficiency anemia diagnosis and iron infusion therapy",
        "Evaluation and management of blood cancers (leukemia, lymphoma, myeloma)",
        "Bleeding and clotting disorder treatment",
        "Bone marrow evaluation and biopsy coordination",
        "On-site blood draw and in-house lab analysis",
    ],
    facts=[("Appointments", "Next-day"), ("Lab results", "On-site"), ("Locations", "13 centers")],
    pullquote='"Our hematologists work with you to understand your complete picture — not just a single lab value — so you get care that actually fits your life."',
    related=RELATED_SERVICES["hematology"],
    breadcrumb_label="Hematology",
    img_label="Hematology consultation",
))

write("oncology/index.html", service_page(
    slug="oncology",
    title="Oncology",
    yoast_title="Compassionate Oncology Care | Premier Hematology Clinic",
    meta_desc="Discover advanced cancer care at Premier Hematology Oncology. Our oncology clinic offers expert treatment with personalized support.",
    eyebrow="Our Services",
    h1="Compassionate Oncology Care — Expert Treatment Close to Home",
    lead="Our oncology team delivers evidence-based cancer care with a personal touch — from diagnosis through treatment and follow-up, all at our conveniently located centers.",
    body_paras=[
        "A cancer diagnosis changes everything. At Premier Hematology & Oncology, we believe the path forward should include not just world-class treatment, but compassionate support at every step. Our oncologists partner closely with you and your family to build a care plan that fits your needs.",
        "We administer chemotherapy, immunotherapy, and biologic treatments on-site — meaning you get the same quality of care as a major hospital center, without the overwhelming environment. Our in-house lab speeds up results so your team can make timely, informed decisions.",
    ],
    bullets=[
        "Chemotherapy and immunotherapy infusion administration",
        "Biologic and targeted therapy infusions",
        "Cancer staging and treatment planning",
        "Coordination with surgical and radiation oncology teams",
        "Ongoing monitoring and follow-up care",
    ],
    facts=[("Appointments", "Next-day"), ("Lab results", "On-site"), ("Locations", "13 centers")],
    pullquote='"We believe every patient deserves both expert treatment and genuine compassion — because fighting cancer is hard enough without fighting the system."',
    related=RELATED_SERVICES["oncology"],
    breadcrumb_label="Oncology",
    img_label="Oncology consultation",
))

write("womens-health-services/index.html", service_page(
    slug="womens-health-services",
    title="Women's Health Services",
    yoast_title="Women's Health Services | Premier Hematology & Oncology",
    meta_desc="Premier Hematology Oncology offers IV therapy, hormone care, and wellness services tailored for women at our trusted women's health clinic.",
    eyebrow="Our Services",
    h1="Women's Health Services Built Around Your Needs",
    lead="We understand the unique health challenges women face at every stage of life. From iron deficiency to hormonal imbalances, our women's health services are designed to help you feel your best.",
    body_paras=[
        "Women's health requires a nuanced approach. Conditions like iron deficiency anemia, hormonal imbalances, and autoimmune diseases can affect women differently — and our specialists are trained to recognize and address these differences.",
        "Whether you're dealing with heavy menstrual cycles that have left you depleted, the fatigue of pregnancy, or post-partum recovery, our team is here to provide targeted IV therapy, infusions, and personalized care plans that get you back to feeling like yourself.",
    ],
    bullets=[
        "Iron infusion therapy for menstrual-related iron deficiency",
        "IV hydration and nutritional support for pregnancy and postpartum",
        "Hormonal imbalance evaluation and infusion support",
        "Autoimmune disease management and biologic infusions",
        "Wellness infusions for energy, immunity, and overall vitality",
    ],
    facts=[("Appointments", "Next-day"), ("Lab results", "On-site"), ("Specialists", "Board-certified")],
    pullquote='"Women\'s health is at the core of what we do. We\'re here to listen, to diagnose accurately, and to treat with the compassion you deserve."',
    related=RELATED_SERVICES["womens-health-services"],
    breadcrumb_label="Women's Health",
    img_label="Women's health consultation",
))

write("wellness-infusions/index.html", service_page(
    slug="wellness-infusions",
    title="Wellness Infusions",
    yoast_title="IV Wellness Infusions | Premier Hematology & Oncology",
    meta_desc="Recharge your body with IV wellness infusions for energy, hydration, immunity. Visit Premier Hematology Oncology for expert infusion care.",
    eyebrow="Our Services",
    h1="IV Wellness Infusions for Energy, Immunity & Vitality",
    lead="Our wellness infusions deliver nutrients, hydration, and vitamins directly into your bloodstream — for faster, more complete absorption than oral supplements can provide.",
    body_paras=[
        "IV wellness infusions bypass the digestive system entirely, delivering essential vitamins, minerals, and fluids directly to your cells. This means faster results and higher bioavailability compared to oral supplements.",
        "Whether you're recovering from illness, battling chronic fatigue, dealing with migraines, or simply want to optimize your health, our clinical team will build an infusion protocol tailored to your goals and labs.",
    ],
    bullets=[
        "Hydration infusions for dehydration and recovery",
        "Vitamin C, B-complex, and micronutrient infusions",
        "Migraine relief infusions",
        "Immune support and antioxidant therapy",
        "Energy and performance optimization protocols",
    ],
    facts=[("Session duration", "1–3 hours"), ("Appointments", "Next-day"), ("Lab results", "On-site")],
    pullquote='"The difference between feeling okay and feeling great is often what your cells are actually getting — and IV therapy ensures they get everything they need."',
    related=RELATED_SERVICES["wellness-infusions"],
    breadcrumb_label="Wellness Infusions",
    img_label="Wellness infusion suite",
))

write("cancer-genetic-testing/index.html", service_page(
    slug="cancer-genetic-testing",
    title="Cancer Genetic Testing",
    yoast_title="Cancer Genetic Testing | Premier Hematology Oncology",
    meta_desc="Premier Hematology Oncology offers cancer genetic testing to detect hereditary risks and support early, personalized treatment decisions.",
    eyebrow="Our Services",
    h1="Cancer Genetic Testing — Know Your Risk, Take Control",
    lead="Our genetic testing services help identify hereditary cancer risks early — giving you and your care team the information needed to prevent, detect, and treat cancer more effectively.",
    body_paras=[
        "Cancer genetic testing analyzes your DNA for mutations associated with hereditary cancers, including BRCA1/BRCA2 for breast and ovarian cancer, Lynch syndrome for colorectal cancer, and many others. Knowing your genetic risk puts you in a powerful position — you can take proactive steps long before cancer develops.",
        "Our team provides comprehensive genetic counseling before and after testing, helping you understand your results and what they mean for you and your family. We then work with you to create a personalized surveillance or prevention plan based on your findings.",
    ],
    bullets=[
        "BRCA1/BRCA2 testing for breast and ovarian cancer risk",
        "Lynch syndrome and hereditary colorectal cancer panels",
        "Multi-gene hereditary cancer panel testing",
        "Pre- and post-test genetic counseling",
        "Personalized surveillance and prevention planning",
    ],
    facts=[("Results turnaround", "1–2 weeks"), ("Counseling", "Included"), ("Appointments", "Next-day")],
    pullquote='"Knowledge is the most powerful tool in cancer prevention. Our genetic testing gives patients the clarity to act early — when it matters most."',
    related=RELATED_SERVICES["cancer-genetic-testing"],
    breadcrumb_label="Cancer Genetic Testing",
    img_label="Genetic counseling session",
))

write("cancers-and-conditions-we-treat/index.html", service_page(
    slug="cancers-and-conditions-we-treat",
    title="Cancers and Conditions We Treat",
    yoast_title="Conditions We Treat | Premier Hematology & Oncology Care",
    meta_desc="Premier Hematology Oncology treats a wide range of cancers and conditions with expert, personalized care at our trusted treatment center.",
    eyebrow="Our Services",
    h1="Cancers &amp; Conditions We Treat",
    lead="From blood disorders and hematological malignancies to solid tumors and hereditary conditions, our specialists provide expert, personalized care across a broad range of diagnoses.",
    body_paras=[
        "Premier Hematology & Oncology is equipped to evaluate and treat a wide spectrum of blood-related and oncological conditions. Our multidisciplinary team combines clinical expertise with compassionate support to deliver care that addresses both your medical and personal needs.",
        "We treat patients at all stages — whether you're seeking a second opinion, starting treatment for the first time, or managing a chronic blood condition that requires ongoing monitoring and infusion therapy.",
    ],
    bullets=[
        "Leukemia, lymphoma, and multiple myeloma",
        "Iron deficiency anemia and iron infusion therapy",
        "Sickle cell disease and thalassemia",
        "Bleeding and clotting disorders (thrombocytopenia, DVT, hemophilia)",
        "Autoimmune conditions requiring biologic infusions",
        "Solid tumor oncology and chemotherapy administration",
        "Chronic heart failure with anemia",
        "Bariatric surgery-related nutritional deficiencies",
    ],
    facts=[("Specialists", "Board-certified"), ("Appointments", "Next-day"), ("Lab results", "On-site")],
    pullquote='"Every condition we treat is personal to the patient in front of us. We bring our full expertise to every case — with care that never feels clinical."',
    related=RELATED_SERVICES["cancers-and-conditions-we-treat"],
    breadcrumb_label="Conditions We Treat",
    img_label="Care team consultation",
))

write("infusion-therapies-we-offer/index.html", service_page(
    slug="infusion-therapies-we-offer",
    title="Infusion Centers — Therapies We Offer",
    yoast_title="Therapies We Offer | Premier Hematology & Oncology",
    meta_desc="Premier Hematology Oncology offers expert infusion therapies for cancer, blood disorders, and immune conditions at our trusted center.",
    eyebrow="Our Services",
    h1="Infusion Centers Built Around Your Comfort",
    lead="Quality care delivered by our expert staff at conveniently located centers — for a tailor-made infusion experience close to home.",
    body_paras=[
        "At Premier Hematology & Oncology, our infusion centers are designed to make treatment as comfortable and stress-free as possible. From your first appointment, you'll be paired with a dedicated care team who tailors every detail of your plan.",
        "We perform treatments on-site, skipping the long waits at hospitals and labs — so you can get back to your life sooner. Our 13 locations across the New York metro area and Atlanta make expert infusion therapy more accessible than ever.",
    ],
    bullets=[
        "Iron infusion therapy for iron-deficiency anemia",
        "Chemotherapy and immunotherapy administration",
        "Hydration and electrolyte support",
        "Injectable medications and biologics",
        "IVIG therapy for immune conditions",
        "On-site lab work and monitoring",
    ],
    facts=[("Locations", "13 centers"), ("Appointments", "Next-day"), ("Lab results", "On-site")],
    pullquote='"Skip the long waits at hospitals and labs. At Premier Hematology, we perform treatments right on site — in a calm, comfortable environment."',
    related=RELATED_SERVICES["infusion-therapies-we-offer"],
    breadcrumb_label="Infusion Centers",
    img_label="Infusion center interior",
))

# ---------------------------------------------------------------------------
# SIMPLE PAGES
# ---------------------------------------------------------------------------
print("\n📄 Simple pages...")

write("care-team/index.html", simple_page(
    title="Meet Our Expert Cancer Care Team | Premier Hematology",
    meta_desc="Meet the expert cancer care team at Premier Hematology Oncology. Compassionate specialists providing trusted hematology and oncology support.",
    h1="Meet Our Care Team",
    lead="Our board-certified specialists bring decades of combined experience in hematology and oncology — and a genuine commitment to every patient.",
    body_html="""    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:30px;">
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Dr. Maged Khalil, MD</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Medical Director, Hematology &amp; Oncology</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Board-certified in internal medicine and hematology/oncology with expertise in blood disorders and cancer treatment.</p>
      </div>
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Clinical Team</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Registered Nurses &amp; Infusion Specialists</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Experienced RNs and infusion nurses across all 13 locations, trained in IV therapy, chemotherapy administration, and patient comfort.</p>
      </div>
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Support Staff</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Patient Care Coordinators</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Dedicated coordinators who handle scheduling, insurance verification, and referrals — so your experience is seamless from day one.</p>
      </div>
    </div>
    <div style="margin-top:48px;text-align:center;">
      <a href="/contact/" class="btn">Get in touch with our team</a>
    </div>""",
))

write("locations/index.html", simple_page(
    title="Our Locations | Premier Hematology & Oncology Centers",
    meta_desc="Find infusion therapy locations near you. Premier Hematology Oncology offers expert care for cancer, blood disorders, and wellness support.",
    h1="Our Locations",
    lead="13 infusion centers across the New York metro area and Atlanta — expert care close to home.",
    body_html="""    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">
      <a href="/astoria-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;transition:border-color 0.15s;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Astoria</h3>
        <p style="font-size:14px;color:#6a6480;">Queens, NY</p>
      </a>
      <a href="/boro-park-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Boro Park</h3>
        <p style="font-size:14px;color:#6a6480;">Brooklyn, NY</p>
      </a>
      <a href="/brooklyn-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Brooklyn</h3>
        <p style="font-size:14px;color:#6a6480;">Brooklyn, NY</p>
      </a>
      <a href="/five-towns-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Five Towns</h3>
        <p style="font-size:14px;color:#6a6480;">Lawrence, NY</p>
      </a>
      <a href="/great-neck-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Great Neck</h3>
        <p style="font-size:14px;color:#6a6480;">Great Neck, NY</p>
      </a>
      <a href="/howard-beach-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Howard Beach</h3>
        <p style="font-size:14px;color:#6a6480;">Queens, NY</p>
      </a>
      <a href="/jamaica-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Jamaica</h3>
        <p style="font-size:14px;color:#6a6480;">Queens, NY</p>
      </a>
      <a href="/manhattan-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Manhattan</h3>
        <p style="font-size:14px;color:#6a6480;">New York, NY</p>
      </a>
      <a href="/monroe-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Monroe</h3>
        <p style="font-size:14px;color:#6a6480;">Monroe, NY</p>
      </a>
      <a href="/monsey-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Monsey</h3>
        <p style="font-size:14px;color:#6a6480;">Rockland County, NY</p>
      </a>
      <a href="/port-jefferson-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Port Jefferson</h3>
        <p style="font-size:14px;color:#6a6480;">Suffolk County, NY</p>
      </a>
      <a href="/queens-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Queens</h3>
        <p style="font-size:14px;color:#6a6480;">Queens, NY</p>
      </a>
      <a href="/staten-island-infusion-center/" class="card" style="padding:24px;text-decoration:none;color:inherit;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#EEE7F7'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Staten Island</h3>
        <p style="font-size:14px;color:#6a6480;">Staten Island, NY</p>
      </a>
      <a href="/atlanta/" class="card" style="padding:24px;text-decoration:none;color:inherit;border-color:#c3aef0;" onmouseover="this.style.borderColor='#5B3FA0'" onmouseout="this.style.borderColor='#c3aef0'">
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Atlanta</h3>
        <p style="font-size:14px;color:#6a6480;">West End, Atlanta, GA</p>
      </a>
    </div>""",
))

write("contact/index.html", simple_page(
    title="Contact Us | Premier Hematology Oncology",
    meta_desc="Get in touch with Premier Hematology Oncology for appointments, questions, or support. We're here to help you every step of the way.",
    h1="Contact Us",
    lead="We're here to help. Reach out to schedule an appointment, ask a question, or connect with the right member of our care team.",
    body_html="""    <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;">
      <div>
        <h2 style="font-family:'Newsreader',serif;font-size:28px;color:#1C1633;margin-bottom:20px;">Get in touch</h2>
        <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:36px;">
          <div><strong style="color:#1C1633;">Phone</strong><br><a href="tel:7189972281" style="color:#5B3FA0;">718-997-2281</a></div>
          <div><strong style="color:#1C1633;">General Inquiries</strong><br><a href="tel:7188663037" style="color:#5B3FA0;">718-866-3037</a></div>
          <div><strong style="color:#1C1633;">Physician Referrals</strong><br><a href="/physician-referal/" style="color:#5B3FA0;">Submit a referral form</a></div>
          <div><strong style="color:#1C1633;">Billing</strong><br><a href="/billing-inquiries/" style="color:#5B3FA0;">Billing inquiries</a></div>
        </div>
        <a href="/anemia-iron-deficiency-consultation/" class="btn">Book an appointment</a>
      </div>
      <div class="sidebar-cta" style="border-radius:18px;">
        <h3 class="sidebar-cta__h3">Next-day appointments</h3>
        <p class="sidebar-cta__p">Most appointments are available the next business day. Fill out our consultation form and our team will reach out to confirm your visit.</p>
        <a href="/anemia-iron-deficiency-consultation/" class="btn btn--white" style="display:block;text-align:center;">Request a consultation</a>
      </div>
    </div>""",
))

write("billing-inquiries/index.html", simple_page(
    title="Billing Inquiries | Premier Hematology Oncology",
    meta_desc="Have questions about your bill? Contact Premier Hematology Oncology for help with insurance, payments, and billing support.",
    h1="Billing Inquiries",
    lead="Have questions about your bill or insurance coverage? Our billing team is here to help.",
    body_html="""    <div style="max-width:640px;">
      <p style="font-size:16.5px;line-height:1.75;margin-bottom:20px;">We accept most major insurance plans and work with our patients to ensure billing is as clear and straightforward as possible. If you have a question about a charge, your insurance coverage, or payment options, please contact our billing department directly.</p>
      <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:36px;">
        <div><strong style="color:#1C1633;">Billing Phone</strong><br><a href="tel:7189972281" style="color:#5B3FA0;">718-997-2281</a></div>
        <div><strong style="color:#1C1633;">Hours</strong><br>Monday–Friday, 9am–5pm EST</div>
      </div>
      <a href="/contact/" class="btn">Contact us</a>
    </div>""",
))

# ---------------------------------------------------------------------------
# LOCATION PAGES (NY)
# ---------------------------------------------------------------------------
print("\n📍 Location pages...")

NY_LOCATIONS = [
    ("astoria-infusion-center",    "Astoria",       "23-10 31st St, Astoria, NY 11105",         "718-866-3037", "near Ditmars Blvd"),
    ("boro-park-infusion-center",  "Boro Park",     "4915 13th Ave, Brooklyn, NY 11219",         "718-866-3037", ""),
    ("brooklyn-infusion-center",   "Brooklyn",      "Brooklyn, NY",                              "718-866-3037", ""),
    ("five-towns-infusion-center", "Five Towns",    "Lawrence, NY 11559",                        "718-866-3037", "serving Woodmere, Hewlett & Lawrence"),
    ("great-neck-infusion-center", "Great Neck",    "Great Neck, NY 11021",                      "718-866-3037", ""),
    ("howard-beach-infusion-center","Howard Beach", "Howard Beach, Queens, NY 11414",            "718-866-3037", ""),
    ("jamaica-infusion-center",    "Jamaica",       "Jamaica, Queens, NY 11432",                 "718-866-3037", ""),
    ("manhattan-infusion-center",  "Manhattan",     "Manhattan, New York, NY",                   "718-866-3037", ""),
    ("monroe-infusion-center",     "Monroe",        "Monroe, NY 10950",                          "718-866-3037", "serving Orange County"),
    ("monsey-infusion-center",     "Monsey",        "Monsey, NY 10952",                          "718-866-3037", "serving Rockland County"),
    ("port-jefferson-infusion-center","Port Jefferson","Port Jefferson, NY 11777",               "718-866-3037", "serving Suffolk County"),
    ("queens-infusion-center",     "Queens",        "Queens, NY",                                "718-866-3037", ""),
    ("staten-island-infusion-center","Staten Island","Staten Island, NY",                        "718-866-3037", ""),
]

LOCATION_YOAST = {
    "astoria-infusion-center":     ("Astoria Infusion Center | Premier Hematology Oncology", "Premier Hematology Oncology's Astoria Infusion Center provides personalized IV therapy and expert care in a safe, supportive environment."),
    "boro-park-infusion-center":   ("Boro Park Infusion Center | Premier Hematology Oncology", "Premier Hematology Oncology's Boro Park Infusion Center provides expert IV therapy and compassionate care in a welcoming environment."),
    "brooklyn-infusion-center":    ("Brooklyn Infusion Center | Premier Hematology Oncology", "Premier Hematology Oncology's Brooklyn Infusion Center offers expert IV therapy and compassionate care tailored to your health needs."),
    "five-towns-infusion-center":  ("Five Towns Infusion Center | Premier Hematology Oncology", "Premier Hematology Oncology's Five Towns Infusion Center provides expert IV therapy and compassionate care in a comfortable setting."),
    "great-neck-infusion-center":  ("Great Neck Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Great Neck Infusion Center offers personalized IV therapy and expert care in a safe, welcoming environment."),
    "howard-beach-infusion-center":("Howard Beach Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Howard Beach Infusion Center provides expert IV therapy and personalized care in a safe, supportive setting."),
    "jamaica-infusion-center":     ("Jamaica Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Jamaica Infusion Center provides expert IV therapy and compassionate care in a welcoming environment."),
    "manhattan-infusion-center":   ("Manhattan Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Manhattan Infusion Center provides expert IV therapy and compassionate care in a welcoming environment."),
    "monroe-infusion-center":      ("Monroe Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Monroe Infusion Center offers expert IV therapy and personalized care in a calm, supportive setting."),
    "monsey-infusion-center":      ("Monsey Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Monsey Infusion Center provides expert IV therapy and compassionate care in a comfortable setting."),
    "port-jefferson-infusion-center":("Port Jefferson Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Port Jefferson Infusion Center delivers expert IV therapy and personalized care in a supportive environment."),
    "queens-infusion-center":      ("Queens Infusion Center | Premier Hematology Care", "Premier Hematology Oncology's Queens Infusion Center offers expert IV therapy and compassionate care in a safe, supportive environment."),
    "staten-island-infusion-center":("Staten Island Infusion Center | Premier Hematology Oncology", "Premier Hematology Oncology's Staten Island Infusion Center provides expert IV therapy and compassionate care close to home."),
}

for slug, city, address, phone, nearby in NY_LOCATIONS:
    yt, md = LOCATION_YOAST.get(slug, ("", ""))
    write(f"{slug}/index.html", location_page(slug, city, address, phone, yt, md, nearby))

# Atlanta cluster
print("\n🍑 Atlanta pages...")

write("atlanta/index.html", service_page(
    slug="atlanta",
    title="Premier Hematology and Oncology - Atlanta",
    yoast_title="Premier Hematology & Oncology | Atlanta Infusion Therapy",
    meta_desc="Expert hematology & oncology care in Atlanta. Services include cancer genetic testing treatment, infusion therapy, & women's health support.",
    eyebrow="Atlanta Center",
    h1="Premier Hematology &amp; Oncology — Atlanta",
    lead="Expert hematology and oncology care in the heart of Atlanta's West End. Iron infusions, women's health, and cancer care — next-day appointments available.",
    body_paras=[
        "Premier Hematology & Oncology is proud to serve the Atlanta community with the same high standard of care that has made us the trusted choice across the New York metro area. Our West End location offers a full suite of hematology and infusion services in a comfortable, welcoming environment.",
        "Whether you're dealing with iron deficiency anemia, need chemotherapy administration, or are looking for women's health infusion services, our Atlanta team is ready to help. Board-certified specialists and experienced infusion nurses provide personalized care from your very first visit.",
    ],
    bullets=[
        "Iron infusion therapy for iron-deficiency anemia",
        "Women's health infusions and hormonal support",
        "Wellness and hydration infusions",
        "Cancer genetic testing and counseling",
        "On-site lab work and monitoring",
    ],
    facts=[("Address", "325 Hammond Dr SW"), ("City", "Atlanta, GA"), ("Appointments", "Next-day")],
    pullquote='"Atlanta deserves the same exceptional hematology and oncology care that we\'ve built our reputation on — and we\'re here to deliver it."',
    related=[
        {"slug": "atlanta-infusion-center", "title": "Our Atlanta Center", "desc": "Tour our West End infusion center and meet the care team.", "img": "Atlanta center"},
        {"slug": "atlanta-care-team", "title": "Atlanta Care Team", "desc": "Meet the specialists serving our Atlanta patients.", "img": "Care team"},
        {"slug": "atlanta-anemia-iron-deficiency-consultation", "title": "Book a Consultation", "desc": "Schedule your next-day anemia and iron deficiency consultation.", "img": "Consultation"},
    ],
    breadcrumb_label="Atlanta",
    img_label="Atlanta West End infusion center",
))

write("atlanta-infusion-center/index.html", location_page(
    "atlanta-infusion-center", "Atlanta", "325 Hammond Dr SW, Atlanta, GA 30315",
    "404-555-0100",
    "Atlanta Center | Premier Hematology Oncology",
    "Visit Premier Hematology's Atlanta infusion center at 325 Hammond Dr SW, West End. Comfortable private infusion bays, in-house lab, and next-day appointments.",
    nearby="West End, Atlanta",
))

write("atlanta-care-team/index.html", simple_page(
    title="Meet Our Expert Cancer Care Team | Premier Hematology",
    meta_desc="Meet the expert cancer care team at Premier Hematology Oncology in Atlanta. Compassionate specialists providing trusted hematology and oncology support.",
    h1="Atlanta Care Team",
    lead="Our Atlanta specialists bring board-certified hematology and oncology expertise — and a genuine commitment to every patient.",
    body_html="""    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:30px;max-width:700px;">
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:#ebe3fa;margin:0 auto 16px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Atlanta Medical Director</h3>
        <p style="font-size:13px;color:#5B3FA0;font-weight:600;">Hematology &amp; Oncology</p>
      </div>
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:90px;height:90px;border-radius:50%;background:#ebe3fa;margin:0 auto 16px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:20px;color:#1C1633;margin-bottom:6px;">Infusion Nursing Team</h3>
        <p style="font-size:13px;color:#5B3FA0;font-weight:600;">Registered Nurses</p>
      </div>
    </div>
    <div style="margin-top:36px;"><a href="/contact-atlanta-center/" class="btn">Contact the Atlanta team</a></div>""",
))

write("contact-atlanta-center/index.html", simple_page(
    title="Contact Us | Premier Hematology Oncology Atlanta",
    meta_desc="Get in touch with Premier Hematology Oncology's Atlanta center for appointments, questions, or support.",
    h1="Contact — Atlanta Center",
    lead="Reach out to our Atlanta West End location to schedule an appointment or ask our team a question.",
    body_html="""    <div style="max-width:560px;">
      <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:36px;">
        <div><strong style="color:#1C1633;">Address</strong><br>325 Hammond Dr SW, Atlanta, GA 30315</div>
        <div><strong style="color:#1C1633;">Phone</strong><br><a href="tel:4045550100" style="color:#5B3FA0;">404-555-0100</a></div>
      </div>
      <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn">Book an Atlanta appointment</a>
    </div>""",
))

write("atlanta-anemia-iron-deficiency-consultation/index.html", simple_page(
    title="Anemia & Iron Deficiency Consultation | Premier Hematology",
    meta_desc="Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans for anemia and iron deficiency.",
    h1="Atlanta Anemia &amp; Iron Deficiency Consultation",
    lead="Struggling with fatigue, dizziness, or shortness of breath? Get a next-day consultation at our Atlanta center.",
    body_html="""    <div style="max-width:640px;">
      <p style="font-size:16.5px;line-height:1.75;margin-bottom:24px;">Iron deficiency and anemia are among the most common — and most undertreated — conditions we see. A single consultation gives our specialists the information they need to build a targeted treatment plan, which may include iron infusion therapy available as soon as the next day.</p>
      <a href="/contact-atlanta-center/" class="btn">Schedule your consultation</a>
    </div>""",
))

# ---------------------------------------------------------------------------
# LEAD-GEN PAGES
# ---------------------------------------------------------------------------
print("\n🎯 Lead-gen pages...")

LEADGEN_TEMPLATE = lambda slug, title, yoast_title, meta_desc, h1, lead, cta_url="/anemia-iron-deficiency-consultation/": f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title or title, meta_desc)}
</head>
<body>

{HEADER}

  <section class="service-hero">
    <div class="service-hero__inner" style="max-width:820px;">
      <div class="eyebrow-sans service-hero__eyebrow">Premier Hematology &amp; Oncology</div>
      <h1 class="service-hero__h1">{h1}</h1>
      <p class="service-hero__lead">{lead}</p>
      <div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:32px;">
        <a href="{cta_url}" class="btn btn--lg">Book an appointment &rarr;</a>
        <a href="/contact/" class="link-text">Speak with our team</a>
      </div>
    </div>
  </section>

  <section style="background:#faf8fd;border-top:1px solid #efeaf8;border-bottom:1px solid #efeaf8;">
    <div style="max-width:1100px;margin:0 auto;padding:72px 40px;display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;">
      <div>
        <div class="eyebrow-serif" style="margin-bottom:14px;">The practice that cares</div>
        <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;line-height:1.15;letter-spacing:-0.015em;color:#1C1633;margin-bottom:20px;">Expert care. Next-day appointments.</h2>
        <p style="font-size:16.5px;line-height:1.75;margin-bottom:16px;">Our board-certified specialists provide personalized treatment plans — whether you need an iron infusion, a consultation, or ongoing care. We work around your schedule, not the other way around.</p>
        <div style="display:flex;flex-direction:column;gap:12px;margin-top:24px;">
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Board-certified hematology &amp; oncology specialists</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">In-house lab — faster results, no extra trips</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">13 convenient locations across NY metro + Atlanta</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day appointments for most services</span></div>
        </div>
      </div>
      <div class="sidebar-cta" style="border-radius:18px;">
        <h3 class="sidebar-cta__h3">Ready to feel better?</h3>
        <p class="sidebar-cta__p">Next-day appointments available. Our team will reach out to confirm your visit within 24 hours.</p>
        <a href="{cta_url}" class="btn btn--white" style="display:block;text-align:center;">Book an appointment</a>
      </div>
    </div>
  </section>

{FOOTER}
</body>
</html>"""

LEADGEN_PAGES = [
    ("anemia-iron-deficiency-consultation", "Anemia & Iron Deficiency Consultation",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans for anemia and iron deficiency.",
     "Anemia &amp; Iron Deficiency Consultation",
     "Struggling with fatigue, dizziness, or shortness of breath? Our specialists offer next-day consultations and personalized treatment plans — including advanced iron infusion therapy."),
    ("energy-boost", "Energy Boost | Hematology and Iron Infusion Appointments",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans for anemia and iron deficiency.",
     "Reclaim Your Energy with Iron Infusion Therapy",
     "Constant fatigue, brain fog, or shortness of breath? It may be iron deficiency — and it's highly treatable. Our specialists deliver next-day iron infusions at 13 convenient locations."),
    ("hematology-and-iron-infusion-appointments", "Hematology and Iron Infusion Appointments",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans.",
     "Hematology &amp; Iron Infusion Appointments",
     "Expert hematology care and iron infusion therapy — available next day at 13 locations. No long hospital waits. Just the care you need, when you need it."),
    ("iron-infusions-request", "Iron Infusions Request",
     "Iron Infusion Therapy Request | Premier Hematology",
     "Experience rapid relief from iron deficiency with our expert-administered iron infusions. Request your appointment today.",
     "Request Your Iron Infusion Appointment",
     "Fast, effective iron infusion therapy administered by our expert clinical team. Most patients are seen the next business day at their preferred location."),
    ("anemia-iron-deficiency-consultation-for-aging-symptoms", "Anemia & Iron Deficiency Consultation for Aging Symptoms",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans.",
     "Is It Aging — or Is It Iron Deficiency?",
     "Fatigue, brain fog, and shortness of breath are often chalked up to aging. But iron deficiency anemia may be the real culprit — and it's very treatable. Find out with a next-day consultation."),
    ("bariatric-iron-infusions", "Bariatric Iron Infusions",
     "Bariatric Iron Infusions | Premier Hematology",
     "Post-bariatric surgery iron deficiency is common and treatable. Premier Hematology offers specialized iron infusion therapy for bariatric patients.",
     "Iron Infusions for Bariatric Surgery Patients",
     "Post-bariatric surgery often leads to iron malabsorption and deficiency. Our specialized infusion therapy replenishes iron stores safely and effectively — without the GI side effects of oral supplements."),
    ("chronic-heart-failure", "Chronic Heart Failure",
     "Anemia & Chronic Heart Failure | Premier Hematology",
     "At Premier Hematology, we provide specialized care for anemia related to chronic heart failure. Expert diagnosis and treatment.",
     "Anemia &amp; Chronic Heart Failure Care",
     "Iron deficiency anemia is common in patients with chronic heart failure and can worsen outcomes. Our specialists provide targeted iron infusion therapy that is safe and effective for cardiac patients."),
    ("iv-iron-shortage", "IV Iron Shortage",
     "IV Iron Shortage | Premier Hematology",
     "Learn about the nationwide IV iron shortage and how Premier Hematology is managing supply to continue providing uninterrupted care.",
     "IV Iron Supply Update",
     "We are actively monitoring the nationwide IV iron supply and working with our pharmacy partners to ensure our patients continue to receive uninterrupted care."),
    ("physician-referal", "Physician Referral",
     "Physician Referral | Premier Hematology",
     "Connect with Premier Hematology for seamless physician referrals. Our streamlined process ensures quick and efficient service.",
     "Refer a Patient to Premier Hematology &amp; Oncology",
     "Our streamlined referral process ensures your patients receive prompt, expert hematology and oncology care. Most patients are seen within 24 hours of referral."),
    ("physician-referal-atlanta", "Physician Referral — Atlanta",
     "Physician Referral — Atlanta | Premier Hematology",
     "Refer patients to our Atlanta hematology and oncology center. Fast, expert care for your patients.",
     "Refer a Patient — Atlanta Center",
     "Referring physicians can connect their Atlanta-area patients with our board-certified hematology and oncology specialists. Next-day appointments available."),
    ("consultation-request", "Consultation Request",
     "Request a Consultation | Premier Hematology",
     "Request a consultation with Premier Hematology & Oncology. Our team will reach out within 24 hours to schedule your appointment.",
     "Request a Consultation",
     "Fill out the form below and our team will reach out within 24 hours to schedule your appointment at the location most convenient for you."),
]

for slug, title, yt, md, h1, lead in LEADGEN_PAGES:
    write(f"{slug}/index.html", LEADGEN_TEMPLATE(slug, title, yt, md, h1, lead))

# ---------------------------------------------------------------------------
# BLOG INDEX
# ---------------------------------------------------------------------------
print("\n📰 Blog pages...")

ALL_POSTS = [
    ("anemia-fatigue-in-older-adults", "When Fatigue Isn't Just Aging: The Overlooked Role of Anemia in Older Adults", "Hematology", "anemia in older adults"),
    ("iron-deficiency-fatigue-in-older-adults", "7 Signs Your Fatigue Isn't 'Normal for Your Age'", "Hematology", "iron deficiency"),
    ("feeling-tired-iron-deficiency-vs-aging", "Feeling Tired All the Time? It Might Not Be Aging — It Might Be Iron Deficiency", "Hematology", "iron deficiency"),
    ("what-you-need-to-know-about-anemia-iron-infusion-treatment", "What You Need to Know About Anemia Iron Infusion Treatment", "Hematology", "Anemia"),
    ("iron-infusion-benefits-side-effects-what-to-expect", "Iron Infusion: Benefits, Side Effects & What To Expect", "Hematology", "Iron Infusion"),
    ("iron-infusion-center-near-me-benefits-risks-and-who-needs-it", "Iron Infusion Center Near Me: Benefits, Risks, and Who Needs It", "Hematology", "Iron Infusion"),
    ("iron-infusion-therapy-how-an-infusion-center-can-help-without-a-prescription", "Iron Infusion Therapy: How an Infusion Center Can Help Without a Prescription", "Hematology", "Iron Infusion"),
    ("low-iron-symptoms-get-the-right-treatment-at-a-specialized-clinic", "Low Iron Symptoms? Get the Right Treatment at a Specialized Clinic", "Hematology", "Low Iron"),
    ("feeling-fatigued-book-an-anemia-consultation-near-you", "Feeling Fatigued? Book an Anemia Consultation Near You", "Hematology", "Anemia"),
    ("how-an-anemia-consultation-can-help-you-manage-your-symptoms-and-improve-your-health", "How an Anemia Consultation Can Help You Manage Your Symptoms", "Hematology", "Anemia"),
    ("understanding-anemia-and-fatigue-in", "Understanding Anemia and Fatigue in Women", "Hematology", "Anemia"),
    ("pregnancy-iron-deficiency-a-comprehensive-guide", "Understanding Pregnancy Iron Deficiency and Iron Infusions", "Hematology", "Iron Deficiency"),
    ("nationwide-iron-shortage", "Nationwide Iron Shortage", "Hematology", "Iron Shortage"),
    ("is-infusion-therapy-worth-the-hype-10-key-reasons-you-should-try-it-now", "Is Infusion Therapy Worth the Hype? 10 Key Reasons", "Wellness", "Infusion Therapy"),
    ("5-surprising-benefits-of-infusion-therapy-that-will-change-your-life", "5 Surprising Benefits of Infusion Therapy", "Wellness", "Infusion Therapy"),
    ("can-infusion-therapy-help-you-combat-chronic-fatigue-heres-what-you-should-know", "Can Infusion Therapy Help You Combat Chronic Fatigue?", "Wellness", "Chronic Fatigue"),
    ("infusion-therapy-for-dehydration-a-quick-and-effective-solution", "Infusion Therapy for Dehydration: A Quick and Effective Solution", "Wellness", "Infusion Therapy"),
    ("how-infusion-therapy-centers-ensure-patient-safety-and-comfort", "How Infusion Therapy Centers Ensure Patient Safety and Comfort", "Wellness", "Infusion Therapy"),
    ("what-conditions-are-treated-at-an-infusion-center", "What Conditions Are Treated at an Infusion Center?", "Wellness", "Infusion Therapy"),
    ("the-power-of-infusion-therapy", "The Power of Infusion Therapy", "Wellness", "Infusion Therapy"),
    ("beyond-the-basics-why-ivig-therapy-matters-for-rare-disease-patients", "Beyond the Basics: Why IVIG Therapy Matters for Rare Disease Patients", "Wellness", "IVIG Therapy"),
    ("onpattro-mechanism-benefits-and-what-it-means-for-hattr", "Onpattro: Mechanism, Benefits, and What It Means for hATTR", "Wellness", "Onpattro"),
    ("iv-infusions-for-a-sharper-mind-enhance-focus-and-brain-function", "IV Infusions for a Sharper Mind: Enhance Focus and Brain Function", "Wellness", "IV Infusions"),
    ("womens-health-infusion-therapy-near-me-what-to-know-before-you-book", "Women's Health Infusion Therapy Near Me: What to Know Before You Book", "Women's Health", "Women's Health"),
    ("why-more-women-are-turning-to-infusion-therapy-for-better-health", "Why More Women Are Turning to Infusion Therapy for Better Health", "Women's Health", "Infusion Therapy"),
    ("what-services-make-womens-wellness-clinics-unique", "What Services Make Women's Wellness Clinics Unique?", "Women's Health", "Women's Wellness"),
    ("infusion-treatments-for-autoimmune-diseases-in-women", "Infusion Treatments for Autoimmune Diseases in Women", "Women's Health", "Autoimmune"),
    ("iv-infusion-therapy-for-hormonal-imbalance-in-women", "IV Infusion Therapy for Hormonal Imbalance in Women", "Women's Health", "Hormonal Imbalance"),
    ("the-benefits-of-iv-therapy-for-expecting-and-new-mothers", "The Benefits of IV Therapy for Expecting and New Mothers", "Women's Health", "IV Therapy"),
    ("the-top-benefits-of-iv-hydration-therapy-for-womens-health", "The Top Benefits of IV Hydration Therapy for Women's Health", "Women's Health", "IV Hydration"),
    ("essential-wellness-services-every-woman-needs-for-a-healthier-life", "Essential Wellness Services Every Woman Needs", "Women's Health", "Women's Wellness"),
    ("private-womens-health-specialists-for-hormonal-imbalances", "Private Women's Health Specialists for Hormonal Imbalances", "Women's Health", "Women's Health"),
    ("why-more-patients-are-switching-to-home-iv-infusion-therapy", "Why More Patients Are Switching to Home IV Infusion Therapy", "Wellness", "Home IV Therapy"),
    ("when-periods-drain-more-than-just-energy-understanding-hidden-health-signs", "When Periods Drain More Than Just Energy: Understanding Hidden Health Signs", "Women's Health", "Women's Health"),
    ("feeling-run-down-its-time-for-a-wellness-infusion-boost", "Feeling Run Down? It's Time for a Wellness Infusion Boost", "Wellness", "Wellness Infusions"),
    ("how-iv-infusion-therapy-supports-hiv-treatment-and-management", "How IV Infusion Therapy Supports HIV Treatment and Management", "Wellness", "IV Therapy"),
    ("when-to-see-a-hematologist-signs-you-shouldnt-ignore", "When to See a Hematologist: Signs You Shouldn't Ignore", "Hematology", "Hematology"),
    ("top-treatment-options-for-blood-disorders", "Top Treatment Options for Blood Disorders", "Hematology", "Blood Disorders"),
    ("full-service-hematology-care-near-you-diagnosis-treatment-in-one-place", "Full-Service Hematology Care Near You – Diagnosis & Treatment in One Place", "Hematology", "Hematology"),
    ("how-to-find-the-best-hematology-clinic-near-me", "How to Find the Best Hematology Clinic Near Me", "Hematology", "Hematology"),
    ("the-benefits-of-choosing-a-nearby-oncology-and-hematology-clinic", "The Benefits of Choosing a Nearby Oncology and Hematology Clinic", "Hematology", "Hematology"),
    ("essential-hematology-and-oncology-care-treatments-innovations-and-support", "Essential Hematology and Oncology Care: Treatments, Innovations, and Support", "Hematology", "Hematology"),
    ("worried-about-your-blood-health-get-compassionate-expert-hematology-care", "Worried About Your Blood Health? Get Compassionate, Expert Hematology Care", "Hematology", "Hematology"),
    ("facing-a-blood-disorder-or-cancer-expert-care-for-hope-and-healing", "Facing a Blood Disorder or Cancer? Expert Care for Hope and Healing", "Hematology", "Blood Disorder"),
    ("navigating-hematological-malignancies", "Navigating Hematological Malignancies", "Hematology", "Hematology"),
    ("pregnancy-related-hematological-disorders", "Pregnancy Related Hematological Disorders", "Hematology", "Hematology"),
    ("breast-cancer-genetic-testing-what-you-should-know-about-brca-genes", "Breast Cancer Genetic Testing: What You Should Know About BRCA Genes", "Oncology", "Genetic Testing"),
    ("genetic-testing-and-cancer-risk-what-are-the-benefits", "Genetic Testing and Cancer Risk: What Are the Benefits?", "Oncology", "Genetic Testing"),
    ("a-test-today-peace-of-mind-tomorrow-exploring-your-genetic-risk-for-cancer", "A Test Today, Peace of Mind Tomorrow: Exploring Your Genetic Risk for Cancer", "Oncology", "Genetic Testing"),
    ("colon-cancer-risk-the-role-of-family-history-and-genetic-testing", "Colon Cancer Risk: The Role of Family History and Genetic Testing", "Oncology", "Cancer Genetic Testing"),
    ("where-to-get-genetic-testing-for-cancer-near-me", "Where to Get Genetic Testing for Cancer Near Me", "Oncology", "Cancer DNA Testing"),
    ("cancer-testing-near-me-types-costs-and-locations-explained", "Cancer Testing Near Me: Types, Costs, and Locations Explained", "Oncology", "Cancer Testing"),
    ("common-questions-about-finding-the-best-oncologists-for-cancer-treatment", "Common Questions About Finding the Best Oncologists", "Oncology", "Oncology"),
    ("cancer-treatment-center-top-qualities-to-look-for-cancer-specialist", "Top Qualities to Look for in a Cancer Specialist", "Oncology", "Cancer Treatment"),
    ("appendix-cancer-early-signs-diagnosis-and-infusion-therapy-treatment-strategies", "Appendix Cancer: Early Signs, Diagnosis, and Infusion Therapy Treatment Strategies", "Oncology", "Appendix Cancer"),
    ("how-many-positive-cologuard-tests-indicate-cancer", "How Many Positive Cologuard Tests Indicate Cancer?", "Oncology", "Cancer Testing"),
    ("cancer-prevention", "Cancer Prevention", "Oncology", "Cancer Prevention"),
    ("cancer-screening", "Cancer Screening", "Oncology", "Cancer Screening"),
    ("next-generation-sequencing", "Next-Generation Sequencing", "Oncology", "Genetic Testing"),
    ("iv-therapy-for-migraines-and-headaches-fast-effective-relief", "IV Therapy for Migraines and Headaches: Fast, Effective Relief", "Wellness", "Migraines"),
    ("struggling-with-migraines-how-iv-therapy-can-offer-fast-relief", "Struggling with Migraines? How IV Therapy Can Offer Fast Relief", "Wellness", "IV Therapy"),
    ("how-long-does-iv-therapy-take-to-relieve-a-migraine", "How Long Does IV Therapy Take to Relieve a Migraine?", "Wellness", "IV Therapy"),
    ("headache-after-meal-causes-prevention-and-treatment", "Headache After Meal: Causes, Prevention, and Treatment", "Wellness", "Headache"),
    ("what-is-post-viral-fatigue-causes-symptoms-and-recovery-explained", "What Is Post-Viral Fatigue? Causes, Symptoms, and Recovery Explained", "Wellness", "Fatigue"),
    ("four-pillars-of-total-wellness", "Four Pillars of Total Wellness", "Wellness", "Wellness"),
]

# Blog index
blog_cards = ""
for slug, title, cat, _ in ALL_POSTS:
    blog_cards += f"""
        <a href="/blog/{slug}/" style="text-decoration:none;color:inherit;">
          <div class="blog-card__img img-placeholder">{title[:35]}</div>
          <div class="blog-card__cat">{cat}</div>
          <h3 class="blog-card__title">{title}</h3>
        </a>"""

blog_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Blog | Premier Hematology Oncology Insights", "Explore the Premier Hematology Oncology blog for expert insights on cancer care, blood disorders, infusion therapy, and wellness topics.")}
</head>
<body>

{HEADER}

  <section class="blog-hero">
    <div class="blog-hero__inner">
      <div class="eyebrow-sans" style="margin-bottom:14px;">Premier Hematology &amp; Oncology</div>
      <h1 class="blog-hero__h1">Health Insights &amp; Expert Guidance</h1>
      <p class="blog-hero__lead">Expert articles on hematology, oncology, infusion therapy, women's health, and wellness — written by our clinical team.</p>
    </div>
  </section>

  <div class="blog-main">
    <div class="blog-index-grid">{blog_cards}
    </div>
  </div>

{FOOTER}
</body>
</html>"""

write("blog/index.html", blog_index)

# Individual blog posts — pull content from WordPress via a simple placeholder body
# Full content will be migrated in Phase 2 (Novamira pull)
for slug, title, cat, focus_kw in ALL_POSTS:
    body = f"""    <p>Iron deficiency and anemia are among the most common — and most underdiagnosed — conditions affecting patients today. In this article, our specialists at Premier Hematology &amp; Oncology walk you through everything you need to know about <strong>{focus_kw}</strong>, including symptoms, causes, and the most effective treatment options available.</p>

    <h2>Understanding {focus_kw}</h2>
    <p>Many patients dismiss their symptoms as stress or aging, when in fact they may be experiencing a treatable medical condition. Recognizing the signs early is the most important step toward feeling better — often within days of beginning treatment.</p>

    <h2>Symptoms to watch for</h2>
    <ul>
      <li>Persistent fatigue that rest doesn't resolve</li>
      <li>Unusual shortness of breath during light activity</li>
      <li>Pale skin, brittle nails, or hair thinning</li>
      <li>Difficulty concentrating or frequent headaches</li>
      <li>Cold hands and feet</li>
    </ul>

    <blockquote><p>"The good news is that most conditions related to {focus_kw} are highly treatable — often with a single next-day infusion at one of our conveniently located centers."</p></blockquote>

    <h2>How Premier Hematology can help</h2>
    <p>At our infusion centers, treatments are delivered on-site by an expert team, with most patients in and out the same day. We build a plan around your labs, your schedule, and your comfort — no long hospital waits required.</p>
    <p>If any of this sounds familiar, reach out. A short consultation is often all it takes to determine whether this is affecting your health — and what to do about it.</p>"""

    # rotate related posts (pick 3 different ones)
    post_index = next((i for i, p in enumerate(ALL_POSTS) if p[0] == slug), 0)
    rel = [ALL_POSTS[(post_index + 1) % len(ALL_POSTS)],
           ALL_POSTS[(post_index + 2) % len(ALL_POSTS)],
           ALL_POSTS[(post_index + 3) % len(ALL_POSTS)]]
    related_posts = [{"slug": r[0], "title": r[1], "cat": r[2]} for r in rel]

    write(f"blog/{slug}/index.html", article_page(
        slug=slug,
        title=title,
        yoast_title=title,
        meta_desc=f"Learn about {focus_kw} from the specialists at Premier Hematology & Oncology. Expert insights on treatment, symptoms, and care.",
        category=cat,
        author="Premier Hematology & Oncology",
        date="2026",
        read_time="5",
        body_html=body,
        related_posts=related_posts,
    ))

# ---------------------------------------------------------------------------
# UTILITY PAGES
# ---------------------------------------------------------------------------
print("\n⚙️  Utility pages...")

CONFIRMATION_HTML = lambda name="": f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Thank You | Premier Hematology Oncology", "Thank you for reaching out to Premier Hematology. Your message has been received.")}
</head>
<body>
{HEADER}
  <section style="max-width:600px;margin:100px auto;padding:0 40px;text-align:center;">
    <div style="width:72px;height:72px;border-radius:50%;background:#ebe3fa;display:flex;align-items:center;justify-content:center;margin:0 auto 28px;">
      <span style="font-size:28px;color:#5B3FA0;">&#10003;</span>
    </div>
    <h1 style="font-family:'Newsreader',serif;font-size:40px;color:#1C1633;margin-bottom:16px;">Thank you!</h1>
    <p style="font-size:17px;line-height:1.65;color:#56526A;margin-bottom:32px;">Your message has been received. A member of our care team will reach out within 24 hours to confirm your appointment.</p>
    <a href="/" class="btn">Return to home</a>
  </section>
{FOOTER}
</body>
</html>"""

for conf_slug in [
    "contact-confirmation", "contact-confirmation-iron-request",
    "contact-confirmation-energyboost", "contact-confirmation-hematology-and-iron",
    "contact-confirmation-gracias", "contact-confirmation-atlanta-iron-consult",
    "atlanta-contact-confirmation-energyboost",
]:
    write(f"{conf_slug}/index.html", CONFIRMATION_HTML(conf_slug))

# Welcome page
write("welcome/index.html", simple_page(
    title="Welcome | Premier Hematology Oncology",
    meta_desc="Welcome to Premier Hematology. Discover expert hematology services and compassionate care.",
    h1="Welcome to Premier Hematology &amp; Oncology",
    lead="We're glad you're here. Explore our services, find a location near you, or book your next-day appointment.",
    body_html="""    <div style="display:flex;gap:20px;flex-wrap:wrap;">
      <a href="/hematology/" class="btn">Explore Hematology</a>
      <a href="/locations/" class="btn" style="background:#ebe3fa;color:#5B3FA0;">Find a Location</a>
      <a href="/anemia-iron-deficiency-consultation/" class="btn btn--white" style="border:1.5px solid #5B3FA0;color:#5B3FA0;">Book an Appointment</a>
    </div>""",
))

# Physician Career
write("physician-career-opportunity/index.html", simple_page(
    title="Physician Career Opportunity | Premier Hematology",
    meta_desc="Join the Premier Hematology & Oncology team. We're looking for board-certified hematologists and oncologists.",
    h1="Physician Career Opportunities",
    lead="We're growing — and we're looking for exceptional board-certified hematologists and oncologists to join our team.",
    body_html="""    <div style="max-width:640px;">
      <p style="font-size:16.5px;line-height:1.75;margin-bottom:20px;">Premier Hematology & Oncology is expanding across the New York metro area and Atlanta. We offer competitive compensation, a collaborative environment, and the opportunity to build meaningful patient relationships in a modern, well-equipped clinical setting.</p>
      <p style="font-size:16.5px;line-height:1.75;margin-bottom:30px;">If you are a board-certified hematologist or oncologist interested in joining our team, we'd love to hear from you.</p>
      <a href="/contact/" class="btn">Get in touch</a>
    </div>""",
))

# Infusion Suites
write("infusions-suites/index.html", service_page(
    slug="infusions-suites",
    title="Infusion Suites | Premier Hematology",
    yoast_title="Infusion Suites | Premier Hematology & Oncology",
    meta_desc="Premier Hematology offers state-of-the-art infusion suites designed for comfort and efficiency.",
    eyebrow="Our Facilities",
    h1="State-of-the-Art Infusion Suites",
    lead="Our infusion suites are designed around patient comfort — private bays, calming environments, and attentive clinical care every step of the way.",
    body_paras=[
        "Our infusion suites are purposefully designed to feel nothing like a hospital. Private bays, comfortable recliner chairs, entertainment options, and attentive nursing staff create an environment where patients can relax during treatment.",
        "Each suite is equipped with the clinical tools our nurses need to deliver safe, effective care — including real-time monitoring and direct access to our on-site lab.",
    ],
    bullets=["Private infusion bays", "Comfortable recliners and entertainment", "Attentive RN staff at all times", "On-site lab for real-time monitoring", "Next-day appointment availability"],
    facts=[("Locations", "13 centers"), ("Privacy", "Private bays"), ("Appointments", "Next-day")],
    pullquote='"Our suites are designed to be the opposite of a hospital waiting room — calm, private, and focused entirely on your comfort."',
    related=RELATED_SERVICES["infusion-therapies-we-offer"],
    breadcrumb_label="Infusion Suites",
))

# Bariatric (already covered in leadgen, skip duplicate)
# Spanish page
write("consulta-sobre-anemia-y-deficiencia-de-hierro/index.html", LEADGEN_TEMPLATE(
    "consulta-sobre-anemia-y-deficiencia-de-hierro",
    "Consulta sobre Anemia y Deficiencia de Hierro",
    "Consulta sobre Anemia y Deficiencia de Hierro | Premier Hematology",
    "¿Sufre de fatiga, mareos o dificultad para respirar? Premier Hematology ofrece consultas al día siguiente y planes de tratamiento personalizados.",
    "Consulta sobre Anemia y Deficiencia de Hierro",
    "¿Sufre de fatiga, mareos o dificultad para respirar? Nuestros especialistas ofrecen consultas al día siguiente y planes de tratamiento personalizados, incluyendo terapia de infusión de hierro.",
))

# Privacy pages
write("privacy-policy/index.html", simple_page(
    title="Privacy Policy | Premier Hematology Oncology",
    meta_desc="Review Premier Hematology's Privacy Policy.",
    h1="Privacy Policy",
    lead="Last updated: 2026",
    body_html="""    <div style="max-width:720px;font-size:16px;line-height:1.75;color:#43405a;">
      <p style="margin-bottom:20px;">Premier Hematology &amp; Oncology ("we," "us," or "our") is committed to protecting your personal information. This Privacy Policy explains how we collect, use, and protect information you provide when you visit our website or use our services.</p>
      <h2 style="font-family:'Newsreader',serif;font-size:26px;color:#1C1633;margin:32px 0 14px;">Information We Collect</h2>
      <p style="margin-bottom:20px;">We may collect personal information including your name, email address, phone number, and health-related information when you submit a form or contact us. We also collect non-personal data such as browser type, pages visited, and time spent on the site.</p>
      <h2 style="font-family:'Newsreader',serif;font-size:26px;color:#1C1633;margin:32px 0 14px;">How We Use Your Information</h2>
      <p style="margin-bottom:20px;">We use your information to respond to inquiries, schedule appointments, and provide medical care. We do not sell your personal information to third parties.</p>
      <h2 style="font-family:'Newsreader',serif;font-size:26px;color:#1C1633;margin:32px 0 14px;">Contact</h2>
      <p>For privacy-related questions, contact us at <a href="/contact/" style="color:#5B3FA0;">our contact page</a>.</p>
    </div>""",
))

write("sms-privacy-policy/index.html", simple_page(
    title="SMS Privacy Policy | Premier Hematology Oncology",
    meta_desc="Review Premier Hematology's SMS Privacy Policy.",
    h1="SMS Privacy Policy",
    lead="How we handle SMS communications with patients.",
    body_html="""    <div style="max-width:720px;font-size:16px;line-height:1.75;color:#43405a;">
      <p style="margin-bottom:20px;">By providing your mobile phone number and opting in to SMS communications, you consent to receive text messages from Premier Hematology &amp; Oncology related to appointments, confirmations, and care reminders.</p>
      <p style="margin-bottom:20px;">Message and data rates may apply. You may opt out at any time by replying STOP to any message. For help, reply HELP or contact us directly.</p>
      <p>We do not share your mobile number with third parties for marketing purposes.</p>
    </div>""",
))

print(f"\n✅ Done! Site generated in {ROOT}")

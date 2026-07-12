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
          <a class="site-nav__link" href="/locations/">Locations <span class="site-nav__arrow">&#9660;</span></a>
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

# ---------------------------------------------------------------------------
# ATLANTA ECOSYSTEM
# All Atlanta pages MUST use ATLANTA_HEADER and ATLANTA_FOOTER (not HEADER/FOOTER).
# Atlanta slugs: atlanta/, atlanta-infusion-center/, atlanta-care-team/,
#   contact-atlanta-center/, atlanta-anemia-iron-deficiency-consultation/,
#   physician-referal-atlanta/, energy-boost-atlanta-hematology-and-iron-infusion-appointments/
#   atlanta-contact-confirmation-energyboost/, contact-confirmation-atlanta-iron-consult/
# Atlanta phone: (770) 588-3530
# Atlanta address: 325 Hammond Drive, Suite 201, Atlanta, GA 30328
# Atlanta forms: form_type "atlanta-*", redirect to /atlanta-contact-confirmation-energyboost/
# ---------------------------------------------------------------------------

ATLANTA_HEADER = """\
  <!-- ATLANTA UTILITY BAR -->
  <div class="util-bar">
    <div class="util-bar__inner">
      <span class="util-bar__portal"><span class="util-bar__dot"></span> Patient Portal</span>
      <span class="util-bar__phone">(770) 588-3530</span>
    </div>
  </div>

  <!-- ATLANTA HEADER -->
  <header class="site-header">
    <div class="site-header__inner">
      <a href="/atlanta/" class="logo" aria-label="Premier Hematology &amp; Oncology Atlanta home">
        <div class="logo__mark"><div class="logo__ribbon"></div></div>
        <div class="logo__text">
          <div class="logo__name">PREMIER HEMATOLOGY</div>
          <div class="logo__sub">ATLANTA</div>
        </div>
      </a>
      <button class="nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false">
        <span class="nav-toggle__bar"></span>
        <span class="nav-toggle__bar"></span>
        <span class="nav-toggle__bar"></span>
      </button>
      <ul class="site-nav" id="site-nav">
        <li class="site-nav__item"><a class="site-nav__link" href="/atlanta-care-team/">Care Team</a></li>
        <li class="site-nav__item">
          <span class="site-nav__link">Our Services <span class="site-nav__arrow">&#9660;</span></span>
          <div class="site-nav__dropdown">
            <a href="/hematology/">Hematology</a>
            <a href="/oncology/">Oncology</a>
            <a href="/womens-health-services/">Women&rsquo;s Health</a>
            <a href="/wellness-infusions/">Wellness Infusions</a>
            <a href="/cancer-genetic-testing/">Cancer Genetic Testing</a>
            <a href="/infusion-therapies-we-offer/">Infusion Therapies</a>
          </div>
        </li>
        <li class="site-nav__item"><a class="site-nav__link" href="/atlanta-infusion-center/">Our Location</a></li>
        <li class="site-nav__item"><a class="site-nav__link" href="/blog/">Blog</a></li>
        <li class="site-nav__item"><a class="btn btn--sm" href="/contact-atlanta-center/">Contact Us</a></li>
      </ul>
    </div>
  </header>"""

ATLANTA_FOOTER = """\
  <!-- ATLANTA FOOTER -->
  <footer class="site-footer">
    <div class="site-footer__grid">
      <div>
        <div class="site-footer__logo">
          <div class="site-footer__logo-mark"><div class="site-footer__logo-ribbon"></div></div>
          <div class="site-footer__logo-text">
            <div class="site-footer__logo-name">PREMIER HEMATOLOGY</div>
            <div class="site-footer__logo-sub">ATLANTA</div>
          </div>
        </div>
        <p class="site-footer__blurb">Delivering compassionate, expert hematology and oncology care at our Atlanta location — 325 Hammond Drive, Suite 201, Atlanta, GA 30328.</p>
      </div>
      <div>
        <div class="site-footer__col-label">Contact Us</div>
        <div class="site-footer__links">
          <a href="tel:7705883530">(770) 588-3530</a>
          <a href="/contact-atlanta-center/">Email Us</a>
          <a href="/physician-referal-atlanta/">Physician Referral Form</a>
        </div>
      </div>
      <div>
        <div class="site-footer__col-label">Quick Links</div>
        <div class="site-footer__links">
          <a href="/atlanta-care-team/">Care Team</a>
          <a href="/hematology/">Hematology</a>
          <a href="/oncology/">Oncology</a>
          <a href="/infusion-therapies-we-offer/">Our Services</a>
          <a href="/blog/">Blog</a>
          <a href="/contact-atlanta-center/">Contact Us</a>
        </div>
      </div>
      <div>
        <div class="site-footer__col-label">Our Location</div>
        <div class="site-footer__links">
          <a href="/atlanta-infusion-center/">Atlanta — Hammond Drive</a>
          <p style="color:#968fb0;font-size:13px;margin-top:8px;line-height:1.6;">325 Hammond Drive<br>Suite 201<br>Atlanta, GA 30328</p>
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
          <a href="/billing-inquiries/">Billing Inquiries</a>
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
                 related, breadcrumb_label, img_label="Infusion center interior",
                 header=None, footer=None):
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

    _header = header if header is not None else HEADER
    _footer = footer if footer is not None else FOOTER
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title, meta_desc)}
</head>
<body>

{_header}

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
        <a href="/contact/" class="btn btn--white" style="display:block;text-align:center;">Book an appointment</a>
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

{_footer}
</body>
</html>"""


def location_page(slug, city, address, phone, yoast_title, meta_desc, nearby="", place_id="", header=None, footer=None):
    maps_q = address.replace(" ", "+")
    maps_embed = f"https://maps.google.com/maps?q={maps_q}&output=embed&z=15"
    place_id_attr = f'data-place-id="{place_id}"' if place_id else ""
    _header = header if header is not None else HEADER
    _footer = footer if footer is not None else FOOTER

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title or f"{city} Infusion Center | Premier Hematology Oncology",
      meta_desc or f"Premier Hematology Oncology's {city} Infusion Center provides expert IV therapy and compassionate care in a welcoming environment.")}
  <script src="/assets/js/reviews.js" defer></script>
</head>
<body>

{_header}

  <!-- Location hero — text only, no image -->
  <section class="loc-hero">
    <div class="loc-hero__inner">
      <div class="breadcrumb">
        <a href="/">Home</a><span class="breadcrumb__sep">/</span>
        <a href="/locations/">Locations</a><span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">{city}</span>
      </div>
      <div class="eyebrow-sans" style="margin-bottom:12px;">Infusion Center</div>
      <h1 class="loc-hero__h1">{city} Infusion Center</h1>
      <p class="loc-hero__lead">Expert IV therapy and compassionate care — conveniently located in {city}{", " + nearby if nearby else ""}, close to home.</p>
    </div>
  </section>

  <!-- Two-column: content left, contact + map right -->
  <section class="loc-body">
    <div class="loc-body__inner">

      <!-- LEFT: copy + services + reviews -->
      <div class="loc-content">
        <h2 class="loc-content__h2">Your {city} care center</h2>
        <p class="loc-content__p">At our {city} infusion center, we deliver personalized IV therapy and hematology-oncology care in a comfortable, welcoming environment. Our board-certified team tailors every treatment plan to your specific needs — no long hospital waits required.</p>
        <p class="loc-content__p">We perform treatments on-site with an in-house lab, so you get faster results and spend less time waiting. Next-day appointments are available for most services.</p>

        <h3 class="loc-content__h3">Services at this location</h3>
        <div class="checklist">
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Iron infusion therapy for iron-deficiency anemia</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Chemotherapy and immunotherapy administration</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Wellness and hydration infusions</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Injectable medications and biologics</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">On-site lab work and monitoring</span></div>
        </div>

        <!-- Google Reviews carousel — populated by reviews.js when place_id is set -->
        <div class="reviews-section" {place_id_attr}>
          <div class="reviews-section__header">
            <h3 class="reviews-section__title">What our patients say</h3>
            <div class="reviews-section__rating" id="reviews-rating-{slug}"></div>
          </div>
          <div class="reviews-carousel" id="reviews-carousel-{slug}">
            <!-- Skeleton shown until JS loads reviews -->
            <div class="reviews-skeleton">
              <div class="reviews-skeleton__card"></div>
              <div class="reviews-skeleton__card"></div>
              <div class="reviews-skeleton__card"></div>
            </div>
          </div>
          <div class="reviews-nav" id="reviews-nav-{slug}"></div>
        </div>
      </div>

      <!-- RIGHT: contact card + map -->
      <aside class="loc-sidebar">
        <div class="loc-contact-card">
          <div class="loc-contact-card__label">Location details</div>
          <div class="loc-contact-card__row">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
            <span>{address}</span>
          </div>
          <div class="loc-contact-card__row">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
            <a href="tel:{phone.replace('-','')}" style="color:var(--purple);text-decoration:none;">{phone}</a>
          </div>
          <div class="loc-contact-card__row">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>Mon–Fri, 9 am – 5 pm</span>
          </div>
          <div class="loc-contact-card__row">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
            <span>Next-day appointments · In-house lab</span>
          </div>
          <a href="/anemia-iron-deficiency-consultation/" class="btn" style="display:block;text-align:center;margin-top:20px;">Book an appointment &rarr;</a>
        </div>

        <!-- Google Maps embed — no API key required -->
        <div class="loc-map">
          <iframe
            src="{maps_embed}"
            width="100%"
            height="320"
            style="border:0;border-radius:14px;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
            title="{city} Infusion Center map">
          </iframe>
        </div>
      </aside>

    </div>
  </section>

  <section class="related-section">
    <div class="related-section__inner">
      <h2 class="related-section__h2">Our services</h2>
      <div class="related-grid">
        <a href="/hematology/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__body"><h3 class="related-card__title">Hematology</h3><p class="related-card__desc">Specialized care for blood health and blood-related diseases.</p><span class="related-card__link">Learn more &rarr;</span></div>
        </a>
        <a href="/wellness-infusions/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__body"><h3 class="related-card__title">Wellness Infusions</h3><p class="related-card__desc">Nutritional support and supplementation for patients who need it.</p><span class="related-card__link">Learn more &rarr;</span></div>
        </a>
        <a href="/womens-health-services/" class="card" style="text-decoration:none;color:inherit;">
          <div class="related-card__body"><h3 class="related-card__title">Women's Health</h3><p class="related-card__desc">Care attuned to your unique health needs at every stage.</p><span class="related-card__link">Learn more &rarr;</span></div>
        </a>
      </div>
    </div>
  </section>

{_footer}
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


def simple_page(title, meta_desc, h1, lead, body_html, header=None, footer=None):
    """Generic page for contact, care team, locations hub, etc."""
    _header = header if header is not None else HEADER
    _footer = footer if footer is not None else FOOTER
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(title, meta_desc)}
</head>
<body>

{_header}

  <section class="service-hero">
    <div class="service-hero__inner">
      <h1 class="service-hero__h1">{h1}</h1>
      <p class="service-hero__lead">{lead}</p>
    </div>
  </section>

  <section style="max-width:1100px;margin:0 auto;padding:64px 40px;">
{body_html}
  </section>

{_footer}
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
    eyebrow="Your Hematology Care Experts",
    h1="Your Hematology Care Experts",
    lead="Expert Hematology Services Tailored to Your Needs",
    body_paras=[
        "At Premier Hematology, we specialize in providing comprehensive care for a wide range of hematological conditions, also known as blood disorders. Our expert medical team is dedicated to diagnosing, treating, and managing various hematological conditions to ensure the best possible outcomes for our patients.",
        "<strong>Pregnancy Related Hematological Disorders</strong><br>During pregnancy, women may experience various hematological disorders, including anemia, red blood cell disorders, white blood cell disorders, platelet disorders, and others. Our team specializes in diagnosing and managing these conditions to ensure the health and well-being of both the mother and the baby.",
        "<strong>Hematological Malignancies</strong><br>We provide comprehensive care for hematological malignancies, including lymphoma, myeloma, chronic lymphocytic leukemia (CLL), chronic myeloid leukemia (CML), Hodgkin's disease, non-Hodgkin's lymphoma, and plasma cell dyscrasias. Our multidisciplinary approach ensures that patients receive personalized treatment plans tailored to their specific needs.",
        "<strong>Proactive Care for Blood Disorders — Empowering Patients Through Early Intervention</strong><br>Red Blood Cell Disorder Symptoms: Fatigue, shortness of breath, weakness, and headaches. White Blood Cell Disorder Symptoms: Fever, frequent infections, and general malaise. Platelet Disorder Symptoms: Excessive bleeding, clotting issues, bruising, and skin rash.",
        "<strong>Diagnosis and Treatment — Comprehensive Evaluation and Tailored Care</strong><br>Diagnosis and treatment of blood disorders involve a thorough assessment of your medical history and a physical examination. Our team conducts a series of blood tests to determine the specific disorder and its severity. Treatment strategies are then customized based on the diagnosis, aiming to cure the disorder when possible and alleviate symptoms for improved quality of life. Contact us today to schedule your evaluation and begin your personalized treatment plan.",
    ],
    bullets=[
        "Anemia", "Cancer", "Chronic Lymphocytic Leukemia (CLL)", "Hemophilia",
        "Hodgkin's Disease", "Hypoxia", "Leukocytosis", "Lymphoma",
        "Platelet disorders", "Polycythemia vera", "Red blood cell disorders",
        "Myeloma", "Sickle cell disease", "Thalassemia", "Thrombosis",
        "Von Willebrand disease", "White blood cell disorders",
        "Chronic Myeloid Leukemia (CML)", "Non-Hodgkin's Lymphoma", "Plasma cell dyscrasias",
    ],
    facts=[("Appointments", "Next-day"), ("Lab results", "On-site"), ("Locations", "Broad network throughout NY")],
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
    eyebrow="Your Oncology Care Experts",
    h1="Your Oncology Care Experts",
    lead="Individualized Care for Your Oncology Needs",
    body_paras=[
        "At Premier Hematology, we pride ourselves on providing leading-edge oncology care coupled with personalized, compassionate attention. Our team of experts combine top medical expertise with warm, individualized care.",
        "<strong>A Holistic View of Cancer Care</strong>",
        "<strong>Cancer Screening:</strong> Cancer screenings are crucial for early detection when treatment is most effective. We provide screenings for various types of cancer, tailored to your age and gender, including breast, cervical, colorectal, prostate, and skin cancer.",
        "<strong>Cancer Prevention:</strong> Prevention is key to reducing cancer risk. Our team offers guidance on lifestyle modifications such as tobacco cessation, maintaining a healthy diet and weight, limiting alcohol consumption, sun protection, and regular health screenings.",
        "<strong>Next-Gen Sequencing:</strong> Early intervention is essential in cancer management. Through advanced screenings and next-generation sequencing, we can detect and customize treatment plans based on individual genetic variants. This precision approach enhances the effectiveness of cancer treatment and improves patient outcomes.",
        "<strong>Onsite Infusion Therapy:</strong> For patient convenience and comfort, Premier Hematology provides onsite intravenous chemotherapy and immunotherapy for both solid tumors and hematological malignancies. Additionally, we offer intravenous hydration therapy, as well as all supportive care infusions.",
    ],
    bullets=[
        "Cancer Screening", "Cancer Prevention", "Next-Generation Sequencing",
        "Chemotherapy and immunotherapy infusion administration",
        "Biologic and targeted therapy infusions",
        "Cancer staging and treatment planning",
        "Coordination with surgical and radiation oncology teams",
        "Ongoing monitoring and follow-up care",
    ],
    facts=[("Appointments", "Next-day"), ("Lab results", "On-site"), ("Locations", "Broad network throughout NY")],
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
    eyebrow="Your Hematology Care Experts",
    h1="Women's Health Where You Come First.",
    lead="At Premier Hematology, we understand that women's health needs evolve throughout life's journey. Our dedicated team is here to provide expert care and support for all your hematology concerns. Partnering with Ob/Gyn physicians to address clotting disorders, abnormal blood counts, iron deficiency anemia, and bleeding disorders.",
    body_paras=[
        "<strong>Are You Experiencing Any of These Symptoms?</strong><br>Anemia, Breathlessness during exercise, Cold intolerance, Desire to chew ice, Dizziness, Fatigue, Headaches, Heavy menstrual bleeding, Irritability, Long menstrual periods, Poor concentration, Restless legs, Weakness",
        "<strong>For Pregnancy:</strong> Our team specializes in ensuring that expectant mothers have adequate iron levels to support both their own health and the development of their babies. Intravenous iron is a safe and easy way to increase iron levels in patients with a history of anemia, avoiding blood transfusions.",
        "<strong>For Women:</strong> From managing heavy menstrual bleeding to addressing symptoms of iron deficiency, our comprehensive approach to women's health focuses on empowering you to live your best life. Whether you're experiencing fatigue, weakness, or other iron deficiency symptoms, our team is here to provide personalized, effective care.",
        "<strong>For Bariatrics:</strong> For those undergoing bariatric surgery, proper hematology management is crucial to support overall wellness and ensure a successful outcome. Our team works closely with bariatric specialists to provide comprehensive care.",
        "<strong>Women's Health Expert: Yocheved Brazil</strong><br>Yocheved Brazil is an adult primary care nurse practitioner who specializes in hematology and women's health. She completed her Associates in Nursing at the Phillip's Beth Israel School of Nursing, background in cardiology, oncology, and hematology.",
    ],
    bullets=[
        "Anemia", "Breathlessness during exercise", "Cold intolerance",
        "Desire to chew ice", "Dizziness", "Fatigue", "Headaches",
        "Heavy menstrual bleeding", "Irritability", "Long menstrual periods",
        "Poor concentration", "Restless legs", "Weakness",
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
    eyebrow="For enhanced Vitality",
    h1="Revitalize Your Wellbeing with Wellness Infusions",
    lead="Transform your health and elevate your vitality with our wellness infusions at Premier Hematology. Our specially curated blend of nutrients, vitamins, and minerals is designed to rejuvenate your body, boost your immune system, and enhance your overall well-being.",
    body_paras=[
        "Experience the Benefits",
        "Enhanced hydration for improved overall wellness. Essential vitamins and minerals for immune support. Increased energy levels and overall vitality. Detoxification and elimination of toxins from the body. Stress reduction and mental clarity. Accelerated recovery after physical exertion or illness.",
        "<strong>Tailored Infusions for Your Unique Needs</strong><br>At Premier Hematology, we understand that each individual has unique health requirements. That\'s why we offer personalized wellness infusion plans tailored to your specific needs and goals. Our experienced healthcare team will work closely with you to create a customized infusion plan that addresses your specific concerns and helps you achieve your wellness goals.",
        "<strong>Safe and Expert Care You Can Trust</strong><br>Rest assured that your well-being is our top priority at Premier Hematology. Our wellness infusions are administered by experienced healthcare professionals in a safe and controlled environment. We adhere to strict safety protocols and use only the highest quality ingredients to ensure your safety and satisfaction.",
        "<strong>Four Major Components for Overall Wellness</strong><br>Nutrition — Maximize energy utilization and fitness through a well-balanced diet tailored to your body's nutritional needs. Exercise — Regular physical activity is essential for maintaining overall health and well-being. Mental Health — A positive mindset and mental health are key components of a balanced wellness routine. Intravenous Supplements — Support overall wellness with targeted supplementation of essential nutrients, vitamins, and minerals, delivered directly into the bloodstream for optimal absorption.",
    ],
    bullets=[
        "Enhanced hydration for improved overall wellness",
        "Essential vitamins and minerals for immune support",
        "Increased energy levels and overall vitality",
        "Detoxification and elimination of toxins from the body",
        "Stress reduction and mental clarity",
        "Accelerated recovery after physical exertion or illness",
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
    eyebrow="We are here for you",
    h1="Unlocking Insights with Guided Care",
    lead="Discovering your genetic predisposition to cancer can be a powerful tool in your healthcare journey. At Premier Hematology, we offer advanced genetic testing services tailored to your unique needs, providing you with valuable insights that can help guide your healthcare decisions.",
    body_paras=[
        "<strong>Genetic Testing for Cancer Risk</strong><br>Supported by the latest technology, our specially trained genetics specialist is able to identify those who are at high-risk. Individuals can be referred for consultation and genetic testing or receive testing directly from our genetics team.",
        "<strong>Next Generation Sequencing Clinical Testing</strong><br>NGS testing allows geneticists to detect mutations in hundreds of different genes simultaneously, giving a more unique understanding of each patient's individual diagnosis. Our state-of-the-art Laboratory at Premier Hematology performs this testing in-house.",
        "<strong>Cancer Consultation: What to Expect?</strong><br>Your personal and family cancer history will be reviewed, including type(s) of cancer and age(s) at diagnosis. Based on this information, a genetics professional will evaluate your risk of inherited cancer syndromes and make recommendations for genetic testing.",
    ],
    bullets=[
        "BRCA1/BRCA2 testing for breast and ovarian cancer risk",
        "Lynch syndrome and hereditary colorectal cancer panels",
        "Multi-gene hereditary cancer panel testing",
        "Pre- and post-test genetic counseling",
        "Personalized surveillance and prevention planning",
        "In-house NGS laboratory testing",
    ],
    facts=[("Results turnaround", "1–2 weeks"), ("Counseling", "Included"), ("Appointments", "Next-day")],
    pullquote='"Knowledge is the most powerful tool in cancer prevention. Our genetic testing gives patients the clarity to act early — when it matters most."',
    related=RELATED_SERVICES["cancer-genetic-testing"],
    breadcrumb_label="Cancer Genetic Testing",
    img_label="Genetic counseling session",
))

_CONDITIONS = [
    "Adrenal cancer", "Anal cancer", "Appendix cancer", "Astrocytoma",
    "Basal cell carcinoma", "Bile duct cancer", "Bladder", "Blood Cancer",
    "Brain", "Brain tumor", "Breast cancer", "Cervical cancer",
    "Colon cancer", "Colorectal cancer", "Cutaneous T-cell lymphoma",
    "Ductal carcinoma in situ", "Endometrial (uterine) cancer",
    "Esophageal cancer", "Gallbladder cancer",
    "Gastrointestinal carcinoid tumor",
    "GIST (gastrointestinal stromal tumor)", "Glioblastoma",
    "Head and neck cancer", "HER2 positive breast cancer",
    "Hodgkin’s lymphoma", "Inflammatory breast cancer",
    "Invasive ductal carcinoma", "Kidney (renal cell) cancer", "Leukemia",
    "Liver (hepatocellular) cancer", "Low-grade glioma", "Lung cancer",
    "Lymphomas (Hodgkin’s and Non-Hodgkin’s)", "Melanoma",
    "Meningioma", "Merkel cell carcinoma", "Mesothelioma",
    "Metastatic breast cancer", "Multiple myeloma-plasma cell tumor",
    "Myelodysplastic syndromes (MDS)", "Neuroendocrine tumor",
    "Neurofibromatosis", "Non-Hodgkin’s lymphoma",
    "Oral cavity or throat cancer", "Osteosarcoma", "Ovarian cancer",
    "Pancoast tumor", "Pancreatic cancer", "Penile cancer",
    "Pituitary adenoma", "Prostate cancer", "Rectal cancer", "Sarcoma",
    "Skin cancer (nonmelanoma)", "Skull base tumors", "Small Intestine cancer",
    "Spinal tumor", "Squamous cell carcinoma", "Stomach (gastric) cancer",
    "Testicular cancer", "Thyroid cancer", "Triple negative breast cancer",
    "Thymoma", "Vaginal cancer", "Vulvar cancer",
]
_CONDITIONS_HTML = "".join(
    f'<div style="padding:10px 0;border-bottom:1px solid var(--border);font-size:15px;color:#43405a;">{c}</div>'
    for c in _CONDITIONS
)

write("cancers-and-conditions-we-treat/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Conditions We Treat | Premier Hematology &amp; Oncology Care", "Premier Hematology Oncology treats a wide range of cancers and conditions with expert, personalized care at our trusted treatment center.")}
</head>
<body>
{HEADER}

<!-- BREADCRUMB -->
<div class="breadcrumb"><div class="breadcrumb__inner"><a href="/">Home</a><span class="breadcrumb__sep">/</span><span class="breadcrumb__current">Cancers and Conditions We Treat</span></div></div>

<!-- HERO — 2 col -->
<section style="max-width:1200px;margin:0 auto;padding:72px 40px 80px;display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">We Are Here for You</div>
    <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:50px;line-height:1.06;letter-spacing:-0.02em;color:#1C1633;margin-bottom:10px;">Comprehensive Care at Premier Hematology</h1>
    <p style="font-size:17px;line-height:1.75;color:#56526A;margin-bottom:16px;">At Premier Hematology, we understand that every patient is unique, and so are their cancer and blood disorder treatments. Our approach is tailored to your specific needs, considering factors like cancer type, stage, overall health, and genetic factors.</p>
    <p style="font-size:17px;line-height:1.75;color:#56526A;margin-bottom:32px;">Together with your doctor, we&rsquo;ll craft a personalized treatment plan aimed at achieving the best possible outcome.</p>
    <a href="/anemia-iron-deficiency-consultation/" class="btn btn--lg">Schedule an Appointment &rarr;</a>
  </div>
  <div style="border-radius:20px;overflow:hidden;height:480px;">
    <img src="http://premierhematology.com/wp-content/uploads/2024/04/office-interior.webp" alt="Premier Hematology office interior" style="width:100%;height:100%;object-fit:cover;display:block;">
  </div>
</section>

<!-- CONDITIONS LIST -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:1200px;margin:0 auto;padding:80px 40px;">
    <div style="margin-bottom:48px;">
      <div class="eyebrow-sans" style="margin-bottom:12px;">Your Oncology and Hematology Experts</div>
      <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;letter-spacing:-0.015em;color:#1C1633;">Cancers, Blood Disorders and Conditions We Treat</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 40px;">
      {_CONDITIONS_HTML}
    </div>
  </div>
</section>

<!-- CTA BAND -->
<div style="background:var(--purple);">
  <div style="max-width:1200px;margin:0 auto;padding:28px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
    <p style="font-size:17px;font-weight:500;color:#fff;margin:0;">Ready to begin? Next-day appointments are available.</p>
    <a href="/anemia-iron-deficiency-consultation/" class="btn btn--white">Schedule an Appointment &rarr;</a>
  </div>
</div>

<!-- FOOTER -->
{FOOTER}
</body>
</html>""")

write("infusion-therapies-we-offer/index.html", service_page(
    slug="infusion-therapies-we-offer",
    title="Infusion Centers — Therapies We Offer",
    yoast_title="Therapies We Offer | Premier Hematology & Oncology",
    meta_desc="Premier Hematology Oncology offers expert infusion therapies for cancer, blood disorders, and immune conditions at our trusted center.",
    eyebrow="Explore Our Range of Treatments",
    h1="Therapies We Offer",
    lead="Comprehensive Infusion Therapies for Optimal Health — From therapies targeting autoimmune disorders to those supporting bone health and beyond, our expert team is dedicated to providing personalized care and support throughout your infusion therapy journey.",
    body_paras=[
        "<strong>Remicade (infliximab), Entyvio (vedolizumab), Stelara (ustekinumab), Inflectra (infliximab-dyyb), Renflexis (infliximab-abda), Tysabri (natalizumab), Ocrevus (ocrelizumab), Lemtrada (alemtuzumab)</strong>",
        "<strong>Radicava (edaravone), Soliris (eculizumab), Tepezza (teprotumumab-trbw), Onpattro (patisiran), Cerezyme (imiglucerase), Lumizyme (alglucosidase alfa), Fabrazyme (agalsidase beta), Simponi Aria (golimumab)</strong>",
        "<strong>Rituxan (rituximab), Benlysta IV (belimumab), Cimzia (certolizumab pegol), Krystexxa (pegloticase), Actemra (tocilizumab), Intravenous Immunoglobulin therapy, Injectafer (ferric carboxymaltose), Reclast (zoledronic acid)</strong>",
    ],
    bullets=[
        "Remicade (infliximab)", "Entyvio (vedolizumab)", "Stelara (ustekinumab)",
        "Tysabri (natalizumab)", "Ocrevus (ocrelizumab)", "Rituxan (rituximab)",
        "Benlysta IV (belimumab)", "Actemra (tocilizumab)", "Soliris (eculizumab)",
        "Tepezza (teprotumumab-trbw)", "Injectafer (ferric carboxymaltose)",
        "Intravenous Immunoglobulin therapy", "Reclast (zoledronic acid)",
    ],
    facts=[("Appointments", "Next-day"), ("Lab results", "On-site"), ("Locations", "Broad network throughout NY")],
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
    body_html="""    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:30px;">
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Dr. Delfino Crescenzo</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Hematologist And Oncologist</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Dr. Delfino Crescenzo received his undergraduate degree from Manhattan College in New York City, New York and earned his medical degree from the University of Bologna in Bologna, Italy. Following this, he completed his residency in Internal Medicine and Fellowship in Hematology/Oncology at Brookdale Hospital Medical Center.</p>
      </div>
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Shani Spector</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Nurse Practitioner</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Shani Spector is a dedicated Nurse Practitioner with a Master's in Nursing from Stony Brook University. She brings a wealth of expertise in in-patient oncology, hematology, and infusion services. Beyond her clinical role, Shani serves as a devoted patient advocate.</p>
      </div>
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Yocheved Brazil</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Nurse Practitioner</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Yocheved Brazil is an adult primacy care nurse practitioner who specializes in hematology and women's health. She completed her Associates in Nursing at the Phillip's Beth Israel School of Nursing, background in cardiology, oncology, and hematology.</p>
      </div>
      <div class="card" style="padding:28px;text-align:center;">
        <div style="width:100px;height:100px;border-radius:50%;background:#ebe3fa;margin:0 auto 18px;"></div>
        <h3 style="font-family:'Newsreader',serif;font-size:22px;color:#1C1633;margin-bottom:6px;">Ariella Goldhammer</h3>
        <p style="font-size:14px;color:#5B3FA0;font-weight:600;margin-bottom:10px;">Family Nurse Practitioner</p>
        <p style="font-size:14.5px;line-height:1.6;color:#6a6480;">Ariella Goldhammer is a compassionate Family Nurse Practitioner, holding a Master's in Nursing from the College of Mount Saint Vincent. With a focus on primary care, hematology, and infusion services.</p>
      </div>
    </div>
    <div style="margin-top:48px;text-align:center;">
      <a href="/contact/" class="btn">Get in touch with our team</a>
    </div>""",
))

write("locations/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Our Locations | Premier Hematology & Oncology Centers", "Find a Premier Hematology & Oncology infusion center near you. 13 convenient locations across the New York metro area plus Atlanta, GA.")}
</head>
<body>
{HEADER}

<!-- HERO -->
<section style="background:var(--lavender-bg);border-bottom:1px solid var(--border);padding:72px 40px 64px;">
  <div style="max-width:900px;margin:0 auto;text-align:center;">
    <div class="eyebrow-sans" style="margin-bottom:14px;">Infusion Centers</div>
    <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:52px;line-height:1.06;letter-spacing:-0.02em;color:#1C1633;margin-bottom:18px;">Our Locations</h1>
    <p style="font-size:17px;line-height:1.7;color:#56526A;max-width:620px;margin:0 auto 32px;">A broad network of convenient infusion centers throughout the New York metro area and Atlanta, GA &mdash; expert hematology and oncology care close to home.</p>
    <a href="/anemia-iron-deficiency-consultation/" class="btn btn--lg">Book an Appointment &rarr;</a>
  </div>
</section>

<!-- NY LOCATIONS GRID -->
<section style="max-width:1200px;margin:0 auto;padding:80px 40px 40px;">
  <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:8px;">New York Locations</h2>
  <p style="font-size:16px;color:#6a6480;margin-bottom:40px;">13 locations across the New York metro area</p>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;">

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=25-31+30th+Rd+Astoria+NY+11102&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Astoria</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Queens, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">25-31 30th Rd #1F<br>Astoria, NY 11102</p>
        <a href="/astoria-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=3711+13th+Ave+Brooklyn+NY+11218&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Boro Park</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Brooklyn, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">3711 13th Ave<br>Brooklyn, NY 11218</p>
        <a href="/boro-park-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=5221+Foster+Ave+Brooklyn+NY+11203&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Brooklyn</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Brooklyn, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">5221 Foster Ave<br>Brooklyn, NY 11203</p>
        <a href="/brooklyn-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=270+Doughty+Blvd+Inwood+NY+11096&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Five Towns</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Inwood, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">270 Doughty Blvd<br>Inwood, NY 11096</p>
        <a href="/five-towns-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=170+Great+Neck+Rd+Great+Neck+NY+11021&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Great Neck</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Long Island, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">170 Great Neck Rd Ste 1<br>Great Neck, NY 11021</p>
        <a href="/great-neck-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=161-50+92nd+St+Howard+Beach+NY+11414&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Howard Beach</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Queens, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">161-50 92nd St<br>Howard Beach, NY 11414</p>
        <a href="/howard-beach-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=140-40+Queens+Blvd+Jamaica+NY+11435&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Jamaica</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Queens, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">140-40 Queens Blvd<br>Jamaica, NY 11435</p>
        <a href="/jamaica-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=55+E+87th+St+New+York+NY+10128&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Manhattan</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">New York, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">55 E 87th St #1D<br>New York, NY 10128</p>
        <a href="/manhattan-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=505+NY-208+Monroe+NY+10950&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Monroe</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Orange County, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">505 NY-208<br>Monroe, NY 10950</p>
        <a href="/monroe-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=10+Johnsons+Ln+New+City+NY+10956&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Monsey</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Rockland County, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">10 Johnsons Ln<br>New City, NY 10956</p>
        <a href="/monsey-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=2+Medical+Dr+Port+Jefferson+Station+NY+11776&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Port Jefferson</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Suffolk County, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">2 Medical Dr<br>Port Jefferson Station, NY 11776</p>
        <a href="/port-jefferson-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=163-03+Horace+Harding+Expy+Fresh+Meadows+NY+11365&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Queens</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Fresh Meadows, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">163-03 Horace Harding Expy<br>Fresh Meadows, NY 11365</p>
        <a href="/queens-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;">
      <iframe src="https://maps.google.com/maps?q=1332+Rockland+Ave+Staten+Island+NY+10314&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
      <div style="padding:22px 24px 20px;">
        <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Staten Island</h3>
        <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Staten Island, NY</p>
        <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">1332 Rockland Ave<br>Staten Island, NY 10314</p>
        <a href="/staten-island-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Location &rarr;</a>
      </div>
    </div>

  </div>
</section>

<!-- ATLANTA DIVIDER -->
<section style="max-width:1200px;margin:0 auto;padding:16px 40px 64px;">
  <div style="border-top:1px solid var(--border);padding-top:64px;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:8px;">Atlanta</h2>
    <p style="font-size:16px;color:#6a6480;margin-bottom:36px;">Now serving patients in the greater Atlanta, GA area</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px;">
      <div class="card" style="padding:0;overflow:hidden;border:2px solid var(--purple);">
        <iframe src="https://maps.google.com/maps?q=325+Hammond+Drive+Suite+201+Atlanta+GA+30328&output=embed&z=15" width="100%" height="180" style="border:0;display:block;" loading="lazy"></iframe>
        <div style="padding:22px 24px 20px;">
          <h3 style="font-family:'Newsreader',serif;font-size:21px;color:#1C1633;margin-bottom:3px;">Atlanta</h3>
          <p style="font-size:12.5px;font-weight:700;color:#5B3FA0;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px;">Buckhead, GA</p>
          <p style="font-size:13.5px;line-height:1.6;color:#6a6480;margin-bottom:16px;">325 Hammond Drive, Suite 201<br>Atlanta, GA 30328</p>
          <a href="/atlanta-infusion-center/" class="btn btn--sm" style="display:block;text-align:center;">View Atlanta Center &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- CTA BAND -->
<div style="background:var(--purple);">
  <div style="max-width:1200px;margin:0 auto;padding:28px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
    <p style="font-size:17px;font-weight:500;color:#fff;margin:0;">Ready to book? Next-day appointments are available.</p>
    <a href="/anemia-iron-deficiency-consultation/" class="btn btn--white">Book an Appointment &rarr;</a>
  </div>
</div>

<!-- FOOTER -->
{FOOTER}
</body>
</html>""")

# placeholder replaced — keep old simple_page stub removed

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
        <a href="/contact/" class="btn btn--white" style="display:block;text-align:center;">Book an appointment</a>
      </div>
      <div class="sidebar-cta" style="border-radius:18px;">
        <h3 class="sidebar-cta__h3">Next-day appointments</h3>
        <p class="sidebar-cta__p">Most appointments are available the next business day. Fill out our consultation form and our team will reach out to confirm your visit.</p>
        <a href="/contact/" class="btn btn--white" style="display:block;text-align:center;">Request a consultation</a>
      </div>
    </div>""",
))

write("billing-inquiries/index.html", simple_page(
    title="Billing Inquiries | Premier Hematology Oncology",
    meta_desc="Have questions about your bill? Contact Premier Hematology Oncology for help with insurance, payments, and billing support.",
    h1="Billing Inquiries",
    lead="Have a question about your bill or insurance coverage? Our billing team is here to help.",
    body_html="""    <div style="display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start;">
      <div>
        <h2 style="font-family:'Newsreader',serif;font-size:28px;color:#1C1633;margin-bottom:18px;">Contact our billing team</h2>
        <p style="font-size:16px;line-height:1.75;color:#56526A;margin-bottom:24px;">Our dedicated billing team can help with insurance questions, payment plans, statements, and general billing concerns. Please fill out the form and a team member will follow up within 1&ndash;2 business days.</p>
        <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:32px;">
          <div class="card" style="padding:20px 24px;display:flex;gap:14px;align-items:center;">
            <div style="width:38px;height:38px;min-width:38px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;color:var(--purple);font-size:15px;">&#9993;</div>
            <div>
              <div style="font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A84A0;margin-bottom:3px;">Billing Email</div>
              <a href="mailto:BillingInquiries@premierhematology.com" style="font-size:14.5px;color:#5B3FA0;font-weight:600;">BillingInquiries@premierhematology.com</a>
            </div>
          </div>
          <div class="card" style="padding:20px 24px;display:flex;gap:14px;align-items:center;">
            <div style="width:38px;height:38px;min-width:38px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;color:var(--purple);font-size:15px;">&#128222;</div>
            <div>
              <div style="font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A84A0;margin-bottom:3px;">Phone</div>
              <a href="tel:7189972281" style="font-size:14.5px;color:#5B3FA0;font-weight:600;">718-997-2281</a>
            </div>
          </div>
          <div class="card" style="padding:20px 24px;display:flex;gap:14px;align-items:center;">
            <div style="width:38px;height:38px;min-width:38px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;color:var(--purple);font-size:15px;">&#128337;</div>
            <div>
              <div style="font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A84A0;margin-bottom:3px;">Hours</div>
              <div style="font-size:14.5px;color:#1C1633;">Monday&ndash;Friday, 9 am&ndash;5 pm EST</div>
            </div>
          </div>
        </div>
      </div>
      <div><!-- form injected by build_forms.py --></div>
    </div>""",
))

# ---------------------------------------------------------------------------
# LOCATION PAGES (NY)
# ---------------------------------------------------------------------------
print("\n📍 Location pages...")

NY_LOCATIONS = [
    # (slug, city, address, phone, nearby, place_id)
    ("astoria-infusion-center",       "Astoria",       "25-31 30th Rd #1F, Astoria, NY 11102",       "718-866-3037", "near Ditmars Blvd",             "ChIJg60C9lZfwokRzA4bIgPAXbk"),
    ("boro-park-infusion-center",     "Boro Park",     "3711 13th Ave, Brooklyn, NY 11218",           "718-866-3037", "",                              "ChIJAZ5hwH5bwokRWoxGhP4DcE8"),
    ("brooklyn-infusion-center",      "Brooklyn",      "5221 Foster Ave, Brooklyn, NY 11203",         "718-866-3037", "",                              "ChIJmerIfYpdwokRLo8zhagmYlg"),
    ("five-towns-infusion-center",    "Five Towns",    "270 Doughty Blvd, Inwood, NY 11096",          "718-866-3037", "serving Woodmere, Hewlett & Lawrence", "ChIJVXjmhIBlwokRqigOUHWGWck"),
    ("great-neck-infusion-center",    "Great Neck",    "170 Great Neck Rd Ste 1, Great Neck, NY 11021","718-866-3037", "",                             "ChIJJZslEYuJwokRna9wNqr4L4Q"),
    ("howard-beach-infusion-center",  "Howard Beach",  "161-50 92nd St, Howard Beach, NY 11414",      "718-866-3037", "",                              "ChIJq6nwSQVnwokRj0V1ztABhjs"),
    ("jamaica-infusion-center",       "Jamaica",       "140-40 Queens Blvd, Jamaica, NY 11435",       "718-866-3037", "",                              "ChIJNwOmYyJhwokRx7hZmFvGbRc"),
    ("manhattan-infusion-center",     "Manhattan",     "55 E 87th St #1D, New York, NY 10128",        "718-866-3037", "",                              "ChIJJyBDVG1ZwokRdVP1rWYW600"),
    ("monroe-infusion-center",        "Monroe",        "505 NY-208, Monroe, NY 10950",                "718-866-3037", "serving Orange County",         "ChIJn6_qi3zXwokRg_0rsa6X_TM"),
    ("monsey-infusion-center",        "Monsey",        "10 Johnsons Ln, New City, NY 10956",          "718-866-3037", "serving Rockland County",       "ChIJh59lZp7DwokRld2Fi9W2Zxo"),
    ("port-jefferson-infusion-center","Port Jefferson","2 Medical Dr, Port Jefferson Station, NY 11776","718-866-3037","serving Suffolk County",       "ChIJOeZ2HzVB6IkRjp-ur_X99os"),
    ("queens-infusion-center",        "Queens",        "163-03 Horace Harding Expy Lower Level, Fresh Meadows, NY 11365", "718-866-3037", "Fresh Meadows", "ChIJhXQgkCphwokRgw0nKWHFD1M"),
    ("staten-island-infusion-center", "Staten Island", "1332 Rockland Ave, Staten Island, NY 10314",  "718-866-3037", "",                              "ChIJYX8jISdNwokRaNma5nzguEw"),
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

for slug, city, address, phone, nearby, place_id in NY_LOCATIONS:
    yt, md = LOCATION_YOAST.get(slug, ("", ""))
    write(f"{slug}/index.html", location_page(slug, city, address, phone, yt, md, nearby, place_id))

# Atlanta cluster
print("\n🍑 Atlanta pages...")

ATL_IMG = "http://premierhematology.com/wp-content/uploads/"

# ── Atlanta Home ──────────────────────────────────────────────────────────────
write("atlanta/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Premier Hematology & Oncology | Atlanta Infusion Therapy", "Expert hematology & oncology care in Atlanta. Iron infusions, women's health, and cancer care — next-day appointments available.")}
</head>
<body>
{ATLANTA_HEADER}

<!-- HERO -->
<section style="max-width:1200px;margin:0 auto;padding:80px 40px 72px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center;">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:16px;">Atlanta Iron Infusion &amp; Women&rsquo;s Health</div>
    <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:52px;line-height:1.06;letter-spacing:-0.02em;color:#1C1633;margin-bottom:20px;">Atlanta&rsquo;s Iron Infusion &amp; Women&rsquo;s Health Specialists</h1>
    <p style="font-size:17px;line-height:1.7;color:#56526A;margin-bottom:32px;">Next-day iron infusions and expert women&rsquo;s health care, now available in Atlanta. No long waits. No hospital referrals. Just the care you need, when you need it.</p>
    <div style="display:flex;gap:16px;flex-wrap:wrap;">
      <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn btn--lg">Next-Day Iron Infusions &rarr;</a>
      <a href="/contact-atlanta-center/" class="btn btn--lg" style="background:#fff;color:#5B3FA0;border:2px solid #5B3FA0;">Schedule a Consultation</a>
    </div>
  </div>
  <div>
    <img src="{ATL_IMG}2025/12/WhatsApp-Image-2025-12-10-at-12.58.04.jpeg" alt="Atlanta infusion care" style="width:100%;border-radius:20px;object-fit:cover;height:480px;display:block;">
  </div>
</section>

<!-- ANNOUNCE BAND -->
<div style="background:var(--purple);">
  <div style="max-width:1200px;margin:0 auto;padding:20px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
    <p style="font-size:17px;font-weight:500;color:#fff;margin:0;">Next-day appointments are here. Get started now!</p>
    <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn btn--white">Book an Appointment</a>
  </div>
</div>

<!-- ABOUT — img left, text right -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1.1fr;gap:64px;align-items:center;">
  <div>
    <img src="{ATL_IMG}2025/07/intro.webp" alt="Premier Hematology Atlanta clinic" style="width:100%;border-radius:20px;object-fit:cover;height:440px;display:block;">
  </div>
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">The Practice That Cares</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:20px;">Atlanta&rsquo;s Premier Hematology Clinic</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:16px;">Premier Hematology is proud to bring board-certified hematology and women&rsquo;s health services to the greater Atlanta, GA community. Located at 325 Hammond Drive, Suite 201, our Atlanta clinic specializes in iron infusions, iron deficiency treatment, and a full range of women&rsquo;s health services for patients across the greater Atlanta area.</p>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;">We know Atlanta women don&rsquo;t have time to wait weeks for a specialist or sit in a hospital infusion bay. That&rsquo;s why we offer next-day appointments, on-site lab work, and infusion treatments &mdash; all in one convenient location.</p>
  </div>
</section>

<!-- WOMEN'S HEALTH — text left, img right -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center;">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">The Quality Care That You Deserve</div>
      <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:20px;">Women&rsquo;s Health Services in Atlanta, GA</h2>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:16px;">Premier Hematology&rsquo;s Atlanta clinic provides specialized women&rsquo;s health services with a focus on iron deficiency, anemia, and blood health conditions that disproportionately affect women. Iron deficiency is the most common nutritional deficiency in women worldwide, affecting up to 22.6% of U.S. females aged 12&ndash;49 (CDC).</p>
      <p style="font-size:16px;font-weight:600;color:#1C1633;margin-bottom:12px;">Conditions We Treat</p>
      <div class="checklist" style="margin-bottom:32px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Iron deficiency anemia</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Fatigue and exhaustion caused by low iron</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Heavy menstrual bleeding (menorrhagia)</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Anemia during pregnancy or postpartum</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Blood disorders affecting women&rsquo;s health</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Nutritional deficiencies requiring IV supplementation</span></div>
      </div>
    </div>
    <div>
      <img src="{ATL_IMG}2025/07/womens-infusion.png" alt="Women's health infusion Atlanta" style="width:100%;border-radius:20px;object-fit:cover;height:480px;display:block;">
    </div>
  </div>
</section>

<!-- ANNOUNCE BAND 2 -->
<div style="background:var(--purple);">
  <div style="max-width:1200px;margin:0 auto;padding:20px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
    <p style="font-size:17px;font-weight:500;color:#fff;margin:0;">Flexible Next-Day Appointments To Fit Your Lifestyle.</p>
    <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn btn--white">Book an Appointment</a>
  </div>
</div>

<!-- IRON INFUSION — text left, img right -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center;">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">The Practice That Cares</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:20px;">Iron Infusion Center in Atlanta, GA</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:24px;">An iron infusion is an intravenous treatment that delivers iron directly into the bloodstream, bypassing the digestive system. Unlike oral iron supplements &mdash; which can cause nausea, constipation, and GI discomfort in up to 60% of users &mdash; IV iron therapy works faster and is better tolerated. Most patients see improvements in energy levels within days of treatment rather than months.</p>
    <a href="/contact-atlanta-center/" class="btn">Contact Us Today &rarr;</a>
  </div>
  <div>
    <img src="{ATL_IMG}2024/04/0_0.webp" alt="Iron infusion treatment Atlanta" style="width:100%;border-radius:20px;object-fit:cover;height:440px;display:block;">
  </div>
</section>

<!-- 3 FEATURES -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:1100px;margin:0 auto;padding:88px 40px;text-align:center;">
    <div class="eyebrow-sans" style="margin-bottom:12px;">The Clinic You Can Trust</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:52px;">Quality Care with Premier Hematology</h2>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:40px;">
      <div>
        <div style="width:64px;height:64px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;"><div style="width:9px;height:22px;background:var(--purple);border-radius:5px;transform:rotate(20deg);"></div></div>
        <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:21px;color:#1C1633;margin-bottom:10px;">Personalized Care</h3>
        <p style="font-size:15px;line-height:1.65;color:#6A6480;max-width:280px;margin:0 auto;">We are board certified in hematology and oncology therapy and specialize in nutritional counseling and vitamin infusion therapy.</p>
      </div>
      <div>
        <div style="width:64px;height:64px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;"><div style="width:9px;height:22px;background:var(--purple);border-radius:5px;transform:rotate(20deg);"></div></div>
        <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:21px;color:#1C1633;margin-bottom:10px;">On-Site Treatments</h3>
        <p style="font-size:15px;line-height:1.65;color:#6A6480;max-width:280px;margin:0 auto;">Skip the long waits at hospitals and labs; at Premier Hematology, we perform treatments right on site.</p>
      </div>
      <div>
        <div style="width:64px;height:64px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;"><div style="width:9px;height:22px;background:var(--purple);border-radius:5px;transform:rotate(20deg);"></div></div>
        <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:21px;color:#1C1633;margin-bottom:10px;">In-House Lab</h3>
        <p style="font-size:15px;line-height:1.65;color:#6A6480;max-width:280px;margin:0 auto;">Lab tests are performed right onsite, reducing turnaround time and helping you get results quicker.</p>
      </div>
    </div>
  </div>
</section>

<!-- 3-STEP JOURNEY -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;">
  <div style="text-align:center;margin-bottom:52px;">
    <div class="eyebrow-sans" style="margin-bottom:12px;">It&rsquo;s Never Been This Convenient</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;letter-spacing:-0.015em;color:#1C1633;">The 3-Step Journey to Optimal Health</h2>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;">
    <div style="border-radius:20px;overflow:hidden;height:460px;background-image:url('{ATL_IMG}2025/07/smiling.png');background-size:cover;background-position:center;"></div>
    <div style="display:flex;flex-direction:column;gap:32px;">
      <div style="display:flex;gap:20px;align-items:flex-start;">
        <div style="font-family:'Newsreader',serif;font-style:italic;font-size:30px;color:#C3AEF0;line-height:1;min-width:34px;">1</div>
        <div><h3 style="font-weight:700;font-size:17px;color:#1C1633;margin-bottom:6px;">Next-Day Consultation</h3><p style="font-size:15px;line-height:1.65;color:#6A6480;">Start with a virtual appointment with one of our hematology experts.</p></div>
      </div>
      <div style="display:flex;gap:20px;align-items:flex-start;">
        <div style="font-family:'Newsreader',serif;font-style:italic;font-size:30px;color:#C3AEF0;line-height:1;min-width:34px;">2</div>
        <div><h3 style="font-weight:700;font-size:17px;color:#1C1633;margin-bottom:6px;">Treatment at Our Center</h3><p style="font-size:15px;line-height:1.65;color:#6A6480;">Visit our infusion center at 325 Hammond Drive, Suite 201 Atlanta. Our clinical team administers your iron infusion or treatment in a comfortable, professional setting &mdash; no hospital required.</p></div>
      </div>
      <div style="display:flex;gap:20px;align-items:flex-start;">
        <div style="font-family:'Newsreader',serif;font-style:italic;font-size:30px;color:#C3AEF0;line-height:1;min-width:34px;">3</div>
        <div><h3 style="font-weight:700;font-size:17px;color:#1C1633;margin-bottom:6px;">Follow-up Care</h3><p style="font-size:15px;line-height:1.65;color:#6A6480;margin-bottom:14px;">Benefit from personalized follow-up care to keep your health on track.</p><a href="/contact-atlanta-center/" class="btn btn--sm">Contact Us Today &rarr;</a></div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section style="background:var(--off-white);border-top:1px solid var(--border);padding:88px 40px;">
  <div style="max-width:1100px;margin:0 auto;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:40px;">Frequently Asked Questions About Iron Infusions in Atlanta</h2>
    <div style="display:flex;flex-direction:column;gap:0;">
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Where can I get an iron infusion in Atlanta, GA?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Premier Hematology offers iron infusion services at our Atlanta clinic located at 325 Hammond Dr Suite 201, Atlanta, GA 30328. We accept same-day and next-day appointments. Call our Atlanta office to schedule.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How long does an iron infusion take?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">An iron infusion at our Atlanta clinic typically takes between 45 and 90 minutes, depending on the dose and your treatment plan. You can relax in a comfortable chair while our clinical team monitors you throughout. Most patients return to normal activities the same day.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Is IV iron better than iron pills?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">For many women, IV iron therapy is more effective than oral supplements. Oral iron can cause gastrointestinal side effects in up to 60% of users, and absorption can be affected by food and other medications. IV iron bypasses digestion entirely, delivering iron directly to the bloodstream. Most patients see improvements in energy within days rather than months.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Do I need a referral to see a hematologist in Atlanta?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">No referral is required to schedule an appointment at Premier Hematology&rsquo;s Atlanta clinic. You can call us directly to book a consultation. If you have existing lab results showing low iron or anemia, bring those to your first appointment.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">What causes iron deficiency in women?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Iron deficiency in women is most commonly caused by heavy menstrual bleeding, pregnancy, postpartum blood loss, or inadequate dietary intake. It is the most common nutritional deficiency worldwide, affecting up to 22.6% of U.S. females aged 12&ndash;49 (CDC). Symptoms include fatigue, shortness of breath, brain fog, pale skin, and cold hands and feet.</p></div>
      <div style="padding:22px 0;"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Where is Premier Hematology&rsquo;s Atlanta office located?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Our Atlanta clinic is located at 325 Hammond Dr Suite 201, Atlanta, GA 30328.</p></div>
    </div>
  </div>
</section>

{ATLANTA_FOOTER}
</body>
</html>""")

# ── Atlanta Infusion Center ───────────────────────────────────────────────────
write("atlanta-infusion-center/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Atlanta Infusion Center | Premier Hematology Oncology", "Premier Hematology's Atlanta infusion center at 325 Hammond Drive, Suite 201. Expert women's health and iron infusion care — next-day appointments available.")}
</head>
<body>
{ATLANTA_HEADER}

<!-- HERO — bg image -->
<section style="background-image:url('{ATL_IMG}2025/07/infusion-nurse.jpg');background-size:cover;background-position:center;position:relative;">
  <div style="background:rgba(28,22,51,0.72);padding:100px 40px;">
    <div style="max-width:700px;margin:0 auto;text-align:center;">
      <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:54px;line-height:1.06;letter-spacing:-0.02em;color:#fff;margin-bottom:20px;">Our Atlanta Center</h1>
      <p style="font-size:18px;line-height:1.65;color:#d4c9f0;margin-bottom:36px;">Expert women&rsquo;s health and iron infusion care in a comfortable, private setting right in Atlanta. Next-day appointments available.</p>
      <div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;">
        <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn btn--lg">Next-Day Iron Infusions &rarr;</a>
        <a href="/contact-atlanta-center/" class="btn btn--lg btn--white">Schedule a Consultation</a>
      </div>
    </div>
  </div>
</section>

<!-- ABOUT — text left, details right -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:start;">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">The Quality Care That You Deserve</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:20px;">Expert Hematology &amp; Infusion Care. Now in Atlanta.</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:16px;">Premier Hematology is proud to bring board-certified hematology and women&rsquo;s health services to Atlanta, GA. Our Atlanta center at 325 Hammond Dr Suite 201 specializes in iron infusions and women&rsquo;s health care for patients across Atlanta and the surrounding communities &mdash; including Buckhead, Midtown, East Point, College Park, and Southwest Atlanta.</p>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;">We understand that patients managing iron deficiency, anemia, or other blood health conditions don&rsquo;t have time to spend hours in a hospital. Our Atlanta center was designed to change that &mdash; shorter wait times, a warm and welcoming team, and treatments delivered in a comfortable, private setting on a schedule that works for you.</p>
  </div>
  <div class="card" style="padding:32px;">
    <div style="font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#8A84A0;margin-bottom:20px;">Location Details</div>
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div style="font-size:15px;color:#56526A;line-height:1.6;"><strong style="color:#1C1633;display:block;margin-bottom:2px;">Address</strong>325 Hammond Drive, Suite 201<br>Atlanta, GA 30328</div>
      <div style="font-size:15px;color:#56526A;"><strong style="color:#1C1633;display:block;margin-bottom:2px;">Phone</strong><a href="tel:7705883530" style="color:#5B3FA0;">(770) 588-3530</a></div>
      <div style="font-size:15px;color:#56526A;"><strong style="color:#1C1633;display:block;margin-bottom:2px;">Appointments</strong>Next-day available</div>
      <div style="font-size:15px;color:#56526A;"><strong style="color:#1C1633;display:block;margin-bottom:2px;">Nearby Areas</strong>Buckhead, Midtown, Sandy Springs, East Point, College Park</div>
    </div>
    <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn" style="margin-top:24px;display:block;text-align:center;">Book an Appointment &rarr;</a>
  </div>
</section>

<!-- ANNOUNCE BAND -->
<div style="background:var(--purple);">
  <div style="max-width:1200px;margin:0 auto;padding:20px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px;">
    <p style="font-size:17px;font-weight:500;color:#fff;margin:0;">Flexible Next-Day Appointments To Fit Your Lifestyle.</p>
    <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn btn--white">Book an Appointment</a>
  </div>
</div>

<!-- AMENITIES — img left, white card right -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;">
  <div style="border-radius:20px;overflow:hidden;height:460px;">
    <img src="{ATL_IMG}2025/07/yonah0704_15145_a_35_year_old_caucasian_woman_sitting_on_the_co_640fe1ed-20d2-4d04-908b-21dd07994e4a.webp" alt="Patient receiving infusion" style="width:100%;height:100%;object-fit:cover;display:block;">
  </div>
  <div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:10px;">Expert Outpatient Infusion Care in Atlanta, GA</h2>
    <h3 style="font-size:16px;font-weight:700;color:#5B3FA0;letter-spacing:.04em;text-transform:uppercase;margin-bottom:24px;">Infusion Center Amenities</h3>
    <div class="checklist">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Private, comfortable infusion bays</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">On-site lab &mdash; no extra trips</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Board-certified clinical team</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day and same-day appointments</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Most major insurance accepted</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Free parking</span></div>
    </div>
    <div style="margin-top:32px;">
      <a href="/contact-atlanta-center/" class="btn">Contact Our Atlanta Team &rarr;</a>
    </div>
  </div>
</section>

<!-- MAP -->
<section style="max-width:1200px;margin:0 auto;padding:0 40px 88px;">
  <div style="border-radius:16px;overflow:hidden;height:380px;">
    <iframe src="https://maps.google.com/maps?q=325+Hammond+Drive+Suite+201+Atlanta+GA+30328&output=embed&z=15" width="100%" height="100%" style="border:0;display:block;" allowfullscreen loading="lazy"></iframe>
  </div>
</section>

{ATLANTA_FOOTER}
</body>
</html>""")

# ── Atlanta Care Team ─────────────────────────────────────────────────────────
write("atlanta-care-team/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Atlanta Care Team | Premier Hematology Oncology", "Meet the expert care team at Premier Hematology Oncology in Atlanta. Compassionate specialists providing trusted hematology and oncology support.")}
</head>
<body>
{ATLANTA_HEADER}

<!-- HERO — bg image -->
<section style="background-image:url('{ATL_IMG}2025/07/infusion-nurse.jpg');background-size:cover;background-position:center;">
  <div style="background:rgba(28,22,51,0.72);padding:100px 40px;text-align:center;">
    <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:54px;line-height:1.06;letter-spacing:-0.02em;color:#fff;margin-bottom:0;">Atlanta Care Team</h1>
  </div>
</section>

<!-- SANTORIA FELTON -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:360px 1fr;gap:64px;align-items:start;">
  <div>
    <img src="{ATL_IMG}2025/12/torri.jpeg" alt="Santoria Felton, NP" style="width:100%;border-radius:20px;object-fit:cover;aspect-ratio:3/4;display:block;">
  </div>
  <div style="padding-top:8px;">
    <div class="eyebrow-sans" style="margin-bottom:12px;">Nurse Practitioner</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:8px;">Santoria Felton, FNP-C</h2>
    <p style="font-size:14px;font-weight:600;color:#5B3FA0;margin-bottom:24px;">Family Nurse Practitioner &mdash; Hematology &amp; Oncology</p>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;">Santoria Felton, FNP-C is a dedicated nurse practitioner specializing in Hematology and oncology, committed to providing compassionate, patient-centered care to individuals navigating complex blood disorders and cancer diagnoses. With a strong clinical foundation and a deep sense of empathy, Santoria focuses on delivering comprehensive, evidence-based care while supporting patients and their families through every stage of treatment. She is especially passionate about patient education and advocacy, empowering individuals to understand their diagnosis, treatment options, and overall health.</p>
  </div>
</section>

<!-- BINA DAVIDSON -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:360px 1fr;gap:64px;align-items:start;">
    <div>
      <img src="{ATL_IMG}2025/12/bina.jpeg" alt="Bina Davidson, RN" style="width:100%;border-radius:20px;object-fit:cover;aspect-ratio:3/4;display:block;">
    </div>
    <div style="padding-top:8px;">
      <div class="eyebrow-sans" style="margin-bottom:12px;">Registered Nurse</div>
      <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:8px;">Bina Davidson, RN</h2>
      <p style="font-size:14px;font-weight:600;color:#5B3FA0;margin-bottom:24px;">Infusion Registered Nurse</p>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;">Bina Davidson is a dedicated Registered Nurse who earned her Bachelor of Science in Nursing from the Mount Sinai Phillips School of Nursing. As an Infusion RN, she demonstrates professional and compassionate administration of intravenous therapies, ensuring each patient feels comfortable and well-cared for during their treatment. When she isn&rsquo;t at the infusion center, she loves spending time with her family and cooking new recipes.</p>
    </div>
  </div>
</section>

<!-- CTA -->
<section style="max-width:1200px;margin:0 auto;padding:80px 40px;">
  <div style="background:linear-gradient(110deg,var(--purple),var(--purple-deep));border-radius:22px;padding:52px 56px;display:flex;align-items:center;justify-content:space-between;gap:32px;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:34px;line-height:1.2;color:#fff;max-width:540px;margin:0;">Ready to meet our Atlanta team? Book your next-day appointment.</h2>
    <a href="/atlanta-anemia-iron-deficiency-consultation/" class="btn btn--white btn--lg" style="white-space:nowrap;">Book an Appointment &rarr;</a>
  </div>
</section>

{ATLANTA_FOOTER}
</body>
</html>""")

# ── Contact Atlanta Center ────────────────────────────────────────────────────
write("contact-atlanta-center/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Contact Us | Premier Hematology Oncology Atlanta", "Get in touch with Premier Hematology Oncology's Atlanta center for appointments, questions, or support.")}
</head>
<body>
{ATLANTA_HEADER}

<!-- HERO — bg image -->
<section style="background-image:url('{ATL_IMG}2025/07/infusion-nurse.jpg');background-size:cover;background-position:center;">
  <div style="background:rgba(28,22,51,0.72);padding:100px 40px;text-align:center;">
    <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:54px;line-height:1.06;letter-spacing:-0.02em;color:#fff;margin-bottom:16px;">Contact Us</h1>
    <p style="font-size:18px;color:#d4c9f0;max-width:500px;margin:0 auto;">Your Atlanta Hematology Care Experts</p>
  </div>
</section>

<!-- CONTACT BODY — text left, form right -->
<section style="max-width:1100px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1.1fr;gap:72px;align-items:start;">
  <div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:34px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:16px;">Let us know how we can help.</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:32px;">To schedule an appointment, please call our office at <strong>(770) 588-3530</strong>. For general information, please complete the form. It will be directed to the appropriate individual in our office.</p>
    <div style="display:flex;flex-direction:column;gap:20px;">
      <div class="card" style="padding:24px 28px;display:flex;gap:16px;align-items:flex-start;">
        <div style="width:40px;height:40px;min-width:40px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;color:var(--purple);font-size:16px;">&#128205;</div>
        <div><div style="font-size:12.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A84A0;margin-bottom:4px;">Address</div><div style="font-size:15px;color:#1C1633;line-height:1.55;">325 Hammond Drive, Suite 201<br>Atlanta, GA 30328</div></div>
      </div>
      <div class="card" style="padding:24px 28px;display:flex;gap:16px;align-items:center;">
        <div style="width:40px;height:40px;min-width:40px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;color:var(--purple);font-size:16px;">&#128222;</div>
        <div><div style="font-size:12.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A84A0;margin-bottom:4px;">Phone</div><a href="tel:7705883530" style="font-size:15px;color:#5B3FA0;font-weight:600;">(770) 588-3530</a></div>
      </div>
      <div class="card" style="padding:24px 28px;display:flex;gap:16px;align-items:center;">
        <div style="width:40px;height:40px;min-width:40px;border-radius:50%;background:var(--lavender-chip);display:flex;align-items:center;justify-content:center;color:var(--purple);font-size:16px;">&#128337;</div>
        <div><div style="font-size:12.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A84A0;margin-bottom:4px;">Appointments</div><div style="font-size:15px;color:#1C1633;">Next-day available</div></div>
      </div>
    </div>
  </div>
  <div><!-- form injected by build_forms.py --></div>
</section>

{ATLANTA_FOOTER}
</body>
</html>""")

# ── Atlanta Anemia Consultation ───────────────────────────────────────────────
write("atlanta-anemia-iron-deficiency-consultation/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Atlanta Anemia & Iron Deficiency Consultation | Premier Hematology", "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology Atlanta offers next-day consultations and personalized treatment plans for anemia and iron deficiency.")}
</head>
<body>
{ATLANTA_HEADER}

<!-- INSURANCE BANNER -->
<div style="background:var(--purple);color:#fff;text-align:center;padding:11px 20px;font-size:13.5px;font-weight:600;letter-spacing:.06em;">We Accept Most Insurances &mdash; Get Started Today to Get Approved</div>

<!-- HERO — 2 col -->
<section style="background:var(--lavender-bg);border-bottom:1px solid var(--border);">
  <div style="max-width:1200px;margin:0 auto;padding:80px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center;">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:16px;">Atlanta Hematology &amp; Iron Infusions</div>
      <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:46px;line-height:1.06;letter-spacing:-0.02em;color:#1C1633;margin-bottom:20px;">Book Your Next-Day Iron Infusion with Atlanta&rsquo;s Trusted Hematology Experts.</h1>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:20px;">Whether you are feeling generally fatigued and tired or have existing labs, book your next-day consultation and start taking advantage of Premier Hematology&rsquo;s comfortable and convenient infusion services. Conveniently located in the Metro-Atlanta area.</p>
      <div style="padding:18px 22px;background:#fff;border-radius:14px;border-left:3px solid var(--purple);margin-bottom:28px;">
        <p style="font-family:'Newsreader',serif;font-style:italic;font-size:15.5px;line-height:1.55;color:#1C1633;margin:0;">&ldquo;Had an amazing experience at Premier Hematology! Varda took incredible care of me, so kind, knowledgeable, and made the whole process feel effortless. The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo; &mdash; Anastasia McKay</p>
      </div>
      <a href="#bottom_form" class="btn btn--lg">Book My Consultation &rarr;</a>
    </div>
    <div style="border-radius:20px;overflow:hidden;height:520px;">
      <img src="{ATL_IMG}2025/07/yonah0704_15145_a_30_year_old_woman_reclining_in_a_black_leat_cfbaa486-c462-4702-bcb6-3e7d8f14b5c1_1.png" alt="Patient at Atlanta infusion center" style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
  </div>
</section>

<!-- EVERYTHING YOU NEED — bg image -->
<section style="background-image:url('{ATL_IMG}2021/05/GettyImages-1189547726.jpg');background-size:cover;background-position:center;">
  <div style="background:rgba(28,22,51,0.8);padding:88px 40px;text-align:center;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;line-height:1.15;color:#fff;margin-bottom:18px;">Everything you Need. All in One Location.</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#d4c9f0;max-width:680px;margin:0 auto 32px;">Located conveniently in the metro-Atlanta area, we are able to make sure that your infusion care doesn&rsquo;t get in the way of your busy life. Visit our offices at 325 Hammond Drive, Atlanta, GA.</p>
    <div style="display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin-bottom:32px;">
      <span style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.25);color:#fff;padding:10px 18px;border-radius:8px;font-size:14.5px;">&#10003; Next-day consultations</span>
      <span style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.25);color:#fff;padding:10px 18px;border-radius:8px;font-size:14.5px;">&#10003; Covered by most major insurances</span>
      <span style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.25);color:#fff;padding:10px 18px;border-radius:8px;font-size:14.5px;">&#10003; Safe, fast, medically supervised iron infusions</span>
      <span style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.25);color:#fff;padding:10px 18px;border-radius:8px;font-size:14.5px;">&#10003; Labs + treatment under one roof</span>
      <span style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.25);color:#fff;padding:10px 18px;border-radius:8px;font-size:14.5px;">&#10003; Designed specifically for women&rsquo;s needs</span>
    </div>
    <a href="#bottom_form" class="btn btn--white btn--lg">Schedule an Appointment &rarr;</a>
  </div>
</section>

<!-- PREMIER ADVANTAGE + SYMPTOMS -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start;">
  <div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:16px;">The Premier Advantage</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:16px;">Get the care you need quickly with our next-day consultations. We offer comprehensive treatment for iron deficiency and anemia.</p>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:28px;">With convenient infusion suites in Atlanta, plus telehealth options, expert care is always within reach.</p>
    <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:28px;">
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:var(--off-white);border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#9889;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Next Day Consultations</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Get the care you need quickly with our next-day consultations.</p></div>
      </div>
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:var(--off-white);border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#10024;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Specialized Care</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Comprehensive treatment for iron deficiency and anemia.</p></div>
      </div>
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:var(--off-white);border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#128187;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Telehealth Services</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Enjoy the benefits of telehealth consultations available for your convenience.</p></div>
      </div>
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:var(--off-white);border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#9829;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Women&rsquo;s Health Experts</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Specialists in women&rsquo;s iron health — diagnosis, infusion, and recovery.</p></div>
      </div>
    </div>
    <a href="#bottom_form" class="btn">Schedule an Appointment &rarr;</a>
  </div>
  <div><!-- right col placeholder --></div>
</section>

<!-- SYMPTOMS — text left, img right -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center;">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">Women&rsquo;s Health Experts</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:18px;">Are You Experiencing Any of These Symptoms?</h2>
    <div class="checklist" style="margin-bottom:32px;">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Breathlessness during exercise</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Cold intolerance</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Desire to chew ice</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Dizziness</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Fatigue</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Headaches</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Heavy menstrual bleeding</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Irritability</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Long menstrual periods</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Poor concentration</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Restless legs</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Weakness</span></div>
    </div>
    <a href="#bottom_form" class="btn">Schedule an Appointment &rarr;</a>
  </div>
  <div style="border-radius:20px;overflow:hidden;height:500px;">
    <img src="{ATL_IMG}2024/04/fatigue.webp" alt="Woman experiencing fatigue from iron deficiency" style="width:100%;height:100%;object-fit:cover;display:block;">
  </div>
</section>

<!-- WHAT IS IRON DEFICIENCY — img left, text right -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1.1fr;gap:64px;align-items:center;">
    <div style="border-radius:20px;overflow:hidden;height:440px;">
      <img src="{ATL_IMG}2024/04/nurse-care.webp" alt="Infusion nurse providing care" style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
    <div>
      <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:18px;">What Is Iron Deficiency and Anemia?</h2>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:24px;">Iron deficiency and anemia are conditions where the body lacks enough healthy red blood cells to carry adequate oxygen to the body&rsquo;s tissues. Symptoms include fatigue, weakness, and shortness of breath. Book a consultation today to see if iron infusions are right for you.</p>
      <a href="#bottom_form" class="btn">Learn More &rarr;</a>
    </div>
  </div>
</section>

<!-- HOW PREMIER HELPS — 4 service cards -->
<section style="background:var(--lavender-bg);border-bottom:1px solid var(--border);">
  <div style="max-width:1100px;margin:0 auto;padding:88px 40px;text-align:center;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:48px;">How Premier Hematology Helps</h2>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:40px;">
      <div class="card" style="padding:0;overflow:hidden;text-align:left;">
        <div style="height:160px;overflow:hidden;"><img src="{ATL_IMG}2024/04/experience.webp" alt="Iron Infusion Therapy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-size:17px;font-weight:500;color:#1C1633;margin-bottom:8px;">Iron Infusion Therapy</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">Fast, safe, medically supervised IV iron — typically completed in under 2 hours.</p>
        </div>
      </div>
      <div class="card" style="padding:0;overflow:hidden;text-align:left;">
        <div style="height:160px;overflow:hidden;"><img src="{ATL_IMG}2024/04/consult-1.png" alt="Hematology Appointments" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-size:17px;font-weight:500;color:#1C1633;margin-bottom:8px;">Hematology Appointments</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">Expert consultations with board-certified hematologists specializing in women&rsquo;s iron health.</p>
        </div>
      </div>
      <div class="card" style="padding:0;overflow:hidden;text-align:left;">
        <div style="height:160px;overflow:hidden;"><img src="{ATL_IMG}2024/04/telehealth.webp" alt="Telehealth Appointments" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-size:17px;font-weight:500;color:#1C1633;margin-bottom:8px;">Telehealth Appointments</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">Connect with our specialists from home for follow-ups, results reviews, and care planning.</p>
        </div>
      </div>
      <div class="card" style="padding:0;overflow:hidden;text-align:left;">
        <div style="height:160px;overflow:hidden;"><img src="{ATL_IMG}2024/04/nurse.webp" alt="Diagnostic Services" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-size:17px;font-weight:500;color:#1C1633;margin-bottom:8px;">Diagnostic Services</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">On-site labs for CBC, ferritin, B12, and other tests — diagnosis and treatment in one visit.</p>
        </div>
      </div>
    </div>
    <a href="#bottom_form" class="btn btn--lg">Contact Us Today &rarr;</a>
  </div>
</section>

<!-- LET'S GET STARTED — form anchor -->
<section id="bottom_form" style="background:#fff;padding:64px 40px;text-align:center;border-top:1px solid var(--border);">
  <div style="max-width:700px;margin:0 auto;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;color:#1C1633;margin-bottom:14px;">Let&rsquo;s get started.</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:32px;">Book your Atlanta anemia consultation today. Next-day appointments available. Most major insurance accepted.</p>
    <div><!-- form injected by build_forms.py --></div>
  </div>
</section>

<!-- FAQ -->
<section style="background:#fff;padding:88px 40px;">
  <div style="max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start;">
    <div>
      <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:28px;">Frequently Asked Questions</h2>
      <img src="{ATL_IMG}2024/04/care.webp" alt="Premier Hematology care" style="width:100%;border-radius:18px;object-fit:cover;">
    </div>
    <div style="display:flex;flex-direction:column;">
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">What causes anemia in women?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Anemia in women can be caused by iron deficiency, vitamin deficiencies, chronic diseases, pregnancy, and heavy menstrual bleeding.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How does anemia cause fatigue?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Anemia leads to fatigue because it reduces the number of red blood cells available to carry oxygen to the body&rsquo;s tissues, resulting in a constant feeling of tiredness and weakness.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How is anemia diagnosed?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Anemia is diagnosed through blood tests such as a Complete Blood Count (CBC), serum ferritin levels, and assessments of vitamin B12 and folate.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Are iron infusions safe?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Yes, iron infusions are generally safe and are an effective treatment for severe anemia or when oral supplements are not suitable.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How long does it take to feel better after an iron infusion?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Many patients start to feel better within a few days to a week after the infusion, with significant improvements in energy and reduction in fatigue.</p></div>
      <div style="padding:22px 0;"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Can I prevent anemia?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Preventing anemia involves maintaining a balanced diet rich in iron, vitamins B12 and folate, and managing any underlying health conditions.</p></div>
    </div>
  </div>
</section>

{ATLANTA_FOOTER}
</body>
</html>""")

# ---------------------------------------------------------------------------
# LEAD-GEN PAGES
# ---------------------------------------------------------------------------
print("\n🎯 Lead-gen pages...")

def LEADGEN_TEMPLATE(slug, title, yoast_title, meta_desc, h1, lead, cta_url="/anemia-iron-deficiency-consultation/", header=None, footer=None):
    _header = header if header is not None else HEADER
    _footer = footer if footer is not None else FOOTER
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD(yoast_title or title, meta_desc)}
</head>
<body>

{_header}

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
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Broad network of convenient locations throughout NY</span></div>
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

{_footer}
</body>
</html>"""

LEADGEN_PAGES = [
    # anemia-iron-deficiency-consultation is built as a dedicated full-content page below — skip LEADGEN_TEMPLATE for it
    # energy-boost is built as a dedicated full-content page below — skip LEADGEN_TEMPLATE for it
    ("hematology-and-iron-infusion-appointments", "Hematology and Iron Infusion Appointments",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans.",
     "Book Your Next-Day Appointment with a Women's Health Expert.",
     "Whether you are feeling generally fatigued and tired or have existing labs, book your next-day appointment and start taking advantage of Premier Hematology's comfortable and convenient infusion and hematology services."),
    ("iron-infusions-request", "Iron Infusions Request",
     "Iron Infusion Therapy Request | Premier Hematology",
     "Experience rapid relief from iron deficiency with our expert-administered iron infusions. Request your appointment today.",
     "Request Your Iron Infusion Appointment",
     "Fast, effective iron infusion therapy administered by our expert clinical team. Most patients are seen the next business day at their preferred location."),
    ("anemia-iron-deficiency-consultation-for-aging-symptoms", "Anemia & Iron Deficiency Consultation for Aging Symptoms",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans.",
     "Think It's Just Aging? It Might Be Anemia.",
     "Fatigue, brain fog, and shortness of breath are often chalked up to aging. But iron deficiency anemia may be the real culprit — and it's very treatable."),
    ("bariatric-iron-infusions", "Bariatric Iron Infusions",
     "Bariatric Iron Infusions | Premier Hematology",
     "Post-bariatric surgery iron deficiency is common and treatable. Premier Hematology offers specialized iron infusion therapy for bariatric patients.",
     "Take the next step in Bariatric recovery.",
     "Studies show that up to 50% of Bariatric patients suffer from Iron Deficiency post-surgery. Book an appointment today and find out if Iron Infusions are right for you."),
    ("chronic-heart-failure", "Chronic Heart Failure",
     "Anemia & Chronic Heart Failure | Premier Hematology",
     "At Premier Hematology, we provide specialized care for anemia related to chronic heart failure. Expert diagnosis and treatment.",
     "Do you experience fatigue despite treatment for Chronic Heart Failure?",
     "If you're a heart failure patient struggling with fatigue, iron deficiency may be a contributing factor. Our specialized iron infusion services are designed to improve your functional status and quality of life."),
    ("iv-iron-shortage", "IV Iron Shortage",
     "IV Iron Shortage | Premier Hematology",
     "Learn about the nationwide IV iron shortage and how Premier Hematology is managing supply to continue providing uninterrupted care.",
     "IV Iron Supply Update",
     "We are actively monitoring the nationwide IV iron supply and working with our pharmacy partners to ensure our patients continue to receive uninterrupted care."),
    # physician-referal is built as a dedicated full-content page below
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
    # WP ad landing page variants — separate slugs for tracking, same content as energy-boost
    # energy-boost-atlanta built as dedicated full-content page below — skip LEADGEN_TEMPLATE
    ("energy-boost-hematology-and-iron-infusion-appointments-openai",
     "Energy Boost — Hematology and Iron Infusion Appointments",
     "Anemia & Iron Deficiency Consultation | Premier Hematology",
     "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans.",
     "Have Low Iron? Get Seen in 24 Hours By a Top NY Hematologist.",
     "Stop waiting weeks. Stop being told 'just take pills.' Our board-certified hematologists treat iron deficiency fast - with personalized infusions covered by insurance."),
]

ATLANTA_LEADGEN_SLUGS = {
    "physician-referal-atlanta",
}
for slug, title, yt, md, h1, lead in LEADGEN_PAGES:
    if slug in ATLANTA_LEADGEN_SLUGS:
        write(f"{slug}/index.html", LEADGEN_TEMPLATE(slug, title, yt, md, h1, lead,
              cta_url="/atlanta-anemia-iron-deficiency-consultation/",
              header=ATLANTA_HEADER, footer=ATLANTA_FOOTER))
    else:
        write(f"{slug}/index.html", LEADGEN_TEMPLATE(slug, title, yt, md, h1, lead))

# ---------------------------------------------------------------------------
# ANEMIA & IRON DEFICIENCY CONSULTATION — full-content page matching WP original
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# PHYSICIAN REFERRAL — dedicated page matching WP original
# ---------------------------------------------------------------------------
write("physician-referal/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Physician Referral | Premier Hematology &amp; Oncology", "Refer your patients to Premier Hematology &amp; Oncology. Our team will contact the patient within 24 hours. Submit the secure referral form online.")}
<style>
  .ref-hero {{
    background-image: url('http://premierhematology.com/wp-content/uploads/2021/05/GettyImages-1189547726.jpg');
    background-size: cover; background-position: center;
  }}
  .ref-hero__inner {{
    background: rgba(28,22,51,0.68);
    padding: 90px 40px;
    text-align: center;
  }}
  .ref-hero__h1 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 54px;
    letter-spacing: -0.02em; line-height: 1.06; color: #fff; margin: 0;
  }}
  .ref-body {{
    max-width: 1100px; margin: 0 auto;
    padding: 80px 40px 96px;
    display: grid; grid-template-columns: 1fr 1.2fr; gap: 72px; align-items: start;
  }}
  .ref-left__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 36px;
    line-height: 1.12; letter-spacing: -0.015em; color: #1C1633; margin-bottom: 18px;
  }}
  .ref-left__p {{
    font-size: 15.5px; line-height: 1.78; color: #56526A; margin-bottom: 14px;
  }}
  .ref-left__note {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 15.5px; line-height: 1.6; color: #1C1633; margin-bottom: 20px;
  }}
  /* form card */
  .ref-form-card {{
    background: #fff; border: 1px solid #DDD8F0;
    border-radius: 18px; padding: 36px 32px; box-shadow: 0 4px 24px rgba(28,22,51,0.07);
  }}
  .ref-form-card h3 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 24px;
    color: #1C1633; margin-bottom: 24px;
  }}
  .ref-form-card .section-label {{
    font-size: 12px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #7C6FAD;
    border-bottom: 1px solid #EDE9F8; padding-bottom: 6px; margin: 24px 0 16px;
  }}
  .ref-row {{ display: grid; gap: 12px; margin-bottom: 12px; }}
  .ref-row--2 {{ grid-template-columns: 1fr 1fr; }}
  .ref-row--1 {{ grid-template-columns: 1fr; }}
  .ref-field {{ display: flex; flex-direction: column; gap: 5px; }}
  .ref-field label {{
    font-size: 12px; font-weight: 600; color: #43405a;
    letter-spacing: 0.03em;
  }}
  .ref-field label .req {{ color: #DC2626; margin-left: 2px; }}
  .ref-field input,
  .ref-field select,
  .ref-field textarea {{
    width: 100%; padding: 10px 13px; font-size: 14px; font-family: inherit;
    border: 1.5px solid #DDD8F0; border-radius: 8px; background: #fff; color: #1C1633;
    outline: none; transition: border-color 0.15s;
  }}
  .ref-field input::placeholder,
  .ref-field textarea::placeholder {{ color: #a89ecf; }}
  .ref-field input:focus,
  .ref-field select:focus,
  .ref-field textarea:focus {{ border-color: #5B4FCF; }}
  .ref-field textarea {{ resize: vertical; min-height: 100px; }}
  .ref-field--file label {{ cursor: pointer; }}
  .ref-field input[type="file"] {{
    padding: 7px 10px; font-size: 13px; cursor: pointer;
    background: #F7F6FB;
  }}
  .ref-submit {{
    width: 100%; margin-top: 22px; padding: 13px;
    background: var(--purple); color: #fff;
    border: none; border-radius: 8px; font-size: 14px;
    font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    cursor: pointer; transition: background 0.15s;
  }}
  .ref-submit:hover {{ background: var(--purple-deep); }}
  @media (max-width: 860px) {{
    .ref-body {{ grid-template-columns: 1fr; gap: 40px; padding: 48px 24px; }}
    .ref-row--2 {{ grid-template-columns: 1fr; }}
    .ref-hero__h1 {{ font-size: 38px; }}
  }}
</style>
</head>
<body>
{HEADER}

<!-- HERO -->
<div class="ref-hero">
  <div class="ref-hero__inner">
    <h1 class="ref-hero__h1">Physician Referral</h1>
  </div>
</div>

<!-- BODY: 2-col -->
<div class="ref-body">

  <!-- LEFT: copy -->
  <div>
    <h2 class="ref-left__h2">Your Trusted Care Partner.</h2>
    <p class="ref-left__p">Thank you for choosing Premier Hematology and Oncology as your trusted care partner. We greatly appreciate your confidence in our team to provide exceptional care for your patients. Your referral is invaluable to us, and we are committed to ensuring a seamless and collaborative experience.</p>
    <p class="ref-left__note"><em>Our care team will contact the patient within 24 hours.</em></p>
    <p class="ref-left__p">Thank you for taking the time to fill out this form and for your continued partnership in delivering outstanding patient care.</p>
  </div>

  <!-- RIGHT: form -->
  <div class="ref-form-card">
    <h3>Referral Form</h3>
    <form action="/contact-confirmation/" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="form_type" value="physician-referral">

      <div class="ref-row ref-row--1">
        <div class="ref-field">
          <label for="ref_doctor">Referring Doctor <span class="req">*</span></label>
          <input type="text" id="ref_doctor" name="referring_doctor" placeholder="Referring Doctor" required>
        </div>
      </div>

      <div class="ref-row ref-row--2">
        <div class="ref-field">
          <label for="ref_phone">Office Phone <span class="req">*</span></label>
          <input type="tel" id="ref_phone" name="office_phone" placeholder="(000)-000-0000" required>
        </div>
        <div class="ref-field">
          <label for="ref_fax">Office Fax <span class="req">*</span></label>
          <input type="tel" id="ref_fax" name="office_fax" placeholder="(000)-000-0000" required>
        </div>
      </div>

      <div class="section-label">Patient Information</div>

      <div class="ref-row ref-row--2">
        <div class="ref-field">
          <label for="pt_first">Patient's First Name <span class="req">*</span></label>
          <input type="text" id="pt_first" name="patient_first_name" placeholder="First Name" required>
        </div>
        <div class="ref-field">
          <label for="pt_last">Patient's Last Name <span class="req">*</span></label>
          <input type="text" id="pt_last" name="patient_last_name" placeholder="Last Name" required>
        </div>
      </div>

      <div class="ref-row ref-row--2">
        <div class="ref-field">
          <label for="pt_dob">Patients Date of Birth <span class="req">*</span></label>
          <input type="date" id="pt_dob" name="patient_dob" placeholder="Date of Birth" required>
        </div>
        <div class="ref-field">
          <label for="pt_phone">Patient's Phone Number <span class="req">*</span></label>
          <input type="tel" id="pt_phone" name="patient_phone" placeholder="Phone Number" required>
        </div>
      </div>

      <div class="ref-row ref-row--1">
        <div class="ref-field">
          <label for="pt_address">Patient's Address <span class="req">*</span></label>
          <input type="text" id="pt_address" name="patient_address" placeholder="Address" required>
        </div>
      </div>

      <div class="ref-row ref-row--1">
        <div class="ref-field">
          <label for="pt_email">Patient's Email <span class="req">*</span></label>
          <input type="email" id="pt_email" name="patient_email" placeholder="Patient's Email" required>
        </div>
      </div>

      <div class="ref-row ref-row--2">
        <div class="ref-field">
          <label for="pt_insurance">Patient's Insurance <span class="req">*</span></label>
          <input type="text" id="pt_insurance" name="patient_insurance" placeholder="Insurance Carrier" required>
        </div>
        <div class="ref-field">
          <label for="pt_ins_id">Patient's Insurance ID <span class="req">*</span></label>
          <input type="text" id="pt_ins_id" name="patient_insurance_id" placeholder="Insurance ID #" required>
        </div>
      </div>

      <div class="ref-row ref-row--1">
        <div class="ref-field">
          <label for="ref_reason">Reason for Referral <span class="req">*</span></label>
          <textarea id="ref_reason" name="reason_for_referral" placeholder="Reason for Referral" required></textarea>
        </div>
      </div>

      <div class="ref-row ref-row--1">
        <div class="ref-field ref-field--file">
          <label for="chart_note">Upload a Chart Note</label>
          <input type="file" id="chart_note" name="chart_note" accept=".pdf,.doc,.docx,.jpg,.png">
        </div>
      </div>

      <div class="ref-row ref-row--1">
        <div class="ref-field">
          <label for="ref_priority">Referral Priority <span class="req">*</span></label>
          <select id="ref_priority" name="referral_priority" required>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>
      </div>

      <button type="submit" class="ref-submit">Send</button>
    </form>
  </div>

</div>

{FOOTER}
</body>
</html>""")

WP_IMG = "http://premierhematology.com/wp-content/uploads/"

write("anemia-iron-deficiency-consultation/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Anemia & Iron Deficiency Consultation | Premier Hematology", "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans for anemia and iron deficiency.")}
</head>
<body>
{HEADER}

<!-- INSURANCE BANNER -->
<div style="background:var(--purple);color:#fff;text-align:center;padding:11px 20px;font-size:13.5px;font-weight:600;letter-spacing:.06em;">We Accept Most Insurances &mdash; Get Started Today to Get Approved</div>

<!-- HERO — 2 col -->
<section style="background:#F3F5F8;">
  <div style="max-width:1200px;margin:0 auto;padding:80px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:64px;align-items:center;">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:16px;">NY Hematology &amp; Iron Infusions</div>
      <h1 style="font-family:'Newsreader',serif;font-weight:500;font-size:46px;line-height:1.06;letter-spacing:-0.02em;color:#1C1633;margin-bottom:20px;">Book Your Next-Day Iron Infusion with NY&rsquo;s Trusted Hematology Expert.</h1>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:8px;">Whether you are feeling generally fatigued and tired or have existing labs, book your next-day consultation and start taking advantage of Premier Hematology&rsquo;s comfortable and convenient infusion services. Offering iron infusions for Anemia patients and other hematological issues.</p>
      <p style="font-size:16px;font-weight:600;color:#1C1633;margin-bottom:24px;">Conveniently located in 10 locations throughout the New York area.</p>
      <div style="padding:18px 22px;background:#fff;border-radius:14px;border-left:3px solid var(--purple);margin-bottom:28px;">
        <p style="font-family:'Newsreader',serif;font-style:italic;font-size:15.5px;line-height:1.55;color:#1C1633;margin:0;">&ldquo;Had an amazing experience at Premier Hematology! Varda took incredible care of me, so kind, knowledgeable, and made the whole process feel effortless. The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo; &mdash; Anastasia McKay</p>
      </div>
      <a href="#bottom_form" class="btn btn--lg">Book an appointment &rarr;</a>
    </div>
    <div style="border-radius:20px;overflow:hidden;height:520px;">
      <img src="{WP_IMG}2025/07/yonah0704_15145_a_30_year_old_woman_reclining_in_a_black_leat_cfbaa486-c462-4702-bcb6-3e7d8f14b5c1_1.png" alt="Patient at Premier Hematology infusion center" style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
  </div>
</section>

<!-- LOCATIONS BANNER — bg image -->
<section style="background-image:url('{WP_IMG}2021/05/GettyImages-1189547726.jpg');background-size:cover;background-position:center;">
  <div style="background:rgba(28,22,51,0.78);padding:72px 40px;text-align:center;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;color:#fff;margin-bottom:16px;">Find a Location Near You</h2>
    <p style="font-size:17px;line-height:1.7;color:#d4c9f0;margin-bottom:32px;max-width:600px;margin-left:auto;margin-right:auto;">With 10 convenient locations across New York, we are able to make sure that your infusion care doesn&rsquo;t get in the way of your busy life.</p>
    <a href="/locations/" class="btn btn--white btn--lg">View Locations &rarr;</a>
  </div>
</section>

<!-- PREMIER ADVANTAGE + SYMPTOMS -->
<section style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start;">

  <!-- Left: Premier Advantage -->
  <div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:16px;">The Premier Advantage</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:16px;">Get the care you need quickly with our next-day consultations. We offer comprehensive treatment for iron deficiency and anemia.</p>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:28px;">With convenient locations in Queens, Brooklyn, Howard Beach, Long Island, Manhattan, and Five Towns, plus telehealth options, expert care is always within reach.</p>
    <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:28px;">
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:#fff;border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#9889;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Next Day Consultations</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Get the care you need quickly with our next-day consultations.</p></div>
      </div>
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:#fff;border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#10024;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Specialized Care</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Comprehensive treatment for iron deficiency and anemia.</p></div>
      </div>
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:#fff;border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#128205;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Convenient Locations</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Serving Queens, Brooklyn, Howard Beach, Long Island, Manhattan, and Five Towns.</p></div>
      </div>
      <div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:#fff;border-radius:12px;border:1px solid var(--border-card);">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--lavender-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px;color:var(--purple);">&#128187;</div>
        <div><strong style="font-size:15px;color:#1C1633;">Telehealth Services</strong><p style="font-size:14.5px;line-height:1.6;color:#56526A;margin:4px 0 0;">Enjoy the benefits of telehealth consultations available for your convenience.</p></div>
      </div>
    </div>
    <a href="#bottom_form" class="btn">Schedule an Appointment &rarr;</a>
  </div>

  <!-- Right: Symptoms -->
  <div>
    <div class="eyebrow-sans" style="margin-bottom:12px;">Women&rsquo;s Health Experts</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:24px;">Are you experiencing any of these symptoms?</h2>
    <div class="checklist" style="margin-bottom:28px;">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Breathlessness during exercise</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Cold intolerance</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Desire to chew ice</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Dizziness</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Fatigue</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Headaches</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Heavy menstrual bleeding</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Irritability</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Long menstrual periods</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Poor concentration</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Restless legs</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Weakness</span></div>
    </div>
    <img src="{WP_IMG}2024/04/fatigue.webp" alt="Woman experiencing fatigue from iron deficiency" style="width:100%;border-radius:16px;object-fit:cover;max-height:260px;display:block;">
    <a href="#bottom_form" class="btn" style="margin-top:24px;">Schedule an Appointment &rarr;</a>
  </div>
</section>

<!-- WHAT IS IRON DEFICIENCY — img left, text right -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1.1fr;gap:64px;align-items:center;">
    <div style="border-radius:20px;overflow:hidden;height:440px;">
      <img src="{WP_IMG}2024/04/nurse-care.webp" alt="Infusion nurse providing care" style="width:100%;height:100%;object-fit:cover;display:block;">
    </div>
    <div>
      <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;line-height:1.12;letter-spacing:-0.015em;color:#1C1633;margin-bottom:18px;">What is Iron Deficiency and Anemia?</h2>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:16px;">Iron deficiency and anemia are conditions where the body lacks enough healthy red blood cells to carry adequate oxygen to the body&rsquo;s tissues.</p>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:24px;">Symptoms include fatigue, weakness, and shortness of breath.</p>
      <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:24px;">Book a consultation today to see if iron infusions are right for you.</p>
      <a href="/understanding-anemia-and-fatigue-in/" class="btn">Learn More &rarr;</a>
    </div>
  </div>
</section>

<!-- HOW PREMIER HELPS — 4 service cards -->
<section style="background:#F3F5F8;">
  <div style="max-width:1100px;margin:0 auto;padding:88px 40px;text-align:center;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:48px;">How Premier Hematology Helps</h2>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:40px;">
      <div style="background:#fff;border-radius:16px;overflow:hidden;border:1px solid var(--border-card);text-align:left;">
        <div style="height:180px;overflow:hidden;"><img src="{WP_IMG}2024/04/experience.webp" alt="Iron infusion therapy" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:17px;color:#1C1633;margin-bottom:8px;">Iron Infusion Therapy</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">Our iron infusion therapy is designed to quickly replenish your iron levels, providing relief from the symptoms of iron deficiency and anemia. Our experienced staff ensures a comfortable and safe treatment process.</p>
        </div>
      </div>
      <div style="background:#fff;border-radius:16px;overflow:hidden;border:1px solid var(--border-card);text-align:left;">
        <div style="height:180px;overflow:hidden;"><img src="{WP_IMG}2024/04/consult-1.png" alt="Hematology appointments" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:17px;color:#1C1633;margin-bottom:8px;">Hematology Appointments</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">Our hematologists provide personalized care and treatment plans tailored to your specific needs. We offer thorough evaluations and comprehensive treatment options.</p>
        </div>
      </div>
      <div style="background:#fff;border-radius:16px;overflow:hidden;border:1px solid var(--border-card);text-align:left;">
        <div style="height:180px;overflow:hidden;"><img src="{WP_IMG}2024/04/telehealth.webp" alt="Telehealth appointments" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:17px;color:#1C1633;margin-bottom:8px;">Telehealth Appointments</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">For your convenience, we offer remote consultations, allowing you to receive expert care from the comfort of your home. Ideal for initial and follow-up appointments.</p>
        </div>
      </div>
      <div style="background:#fff;border-radius:16px;overflow:hidden;border:1px solid var(--border-card);text-align:left;">
        <div style="height:180px;overflow:hidden;"><img src="{WP_IMG}2024/04/nurse.webp" alt="Diagnostic services" style="width:100%;height:100%;object-fit:cover;display:block;"></div>
        <div style="padding:20px;">
          <h3 style="font-family:'Newsreader',serif;font-weight:600;font-size:17px;color:#1C1633;margin-bottom:8px;">Diagnostic Services</h3>
          <p style="font-size:14px;line-height:1.65;color:#56526A;">We provide a full range of diagnostic services, including blood tests and other tools, to accurately diagnose and monitor your condition.</p>
        </div>
      </div>
    </div>
    <a href="#bottom_form" class="btn btn--lg">Contact us today &rarr;</a>
  </div>
</section>

<!-- FORM + IMAGE — 2 col -->
<section id="bottom_form" style="max-width:1200px;margin:0 auto;padding:88px 40px;display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start;">
  <div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:38px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:14px;">Let&rsquo;s get started</h2>
    <p style="font-size:16.5px;line-height:1.75;color:#56526A;margin-bottom:28px;">Whether you are feeling generally fatigued and tired or have existing labs, book your next-day consultation and start taking advantage of Premier Hematology&rsquo;s comfortable and convenient infusion services. Conveniently located in 10 locations throughout the New York area.</p>
    <img src="{WP_IMG}2024/04/care.webp" alt="Premier Hematology care" style="width:100%;border-radius:18px;object-fit:cover;">
  </div>
  <div><!-- form injected by build_forms.py --></div>
</section>

<!-- FAQ -->
<section style="background:var(--off-white);border-top:1px solid var(--border);padding:88px 40px;">
  <div style="max-width:900px;margin:0 auto;">
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:36px;letter-spacing:-0.015em;color:#1C1633;margin-bottom:40px;">Frequently Asked Questions</h2>
    <div style="display:flex;flex-direction:column;gap:0;">
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">What causes anemia in women?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Anemia in women can be caused by iron deficiency, vitamin deficiencies, chronic diseases, pregnancy, and heavy menstrual bleeding.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How does anemia cause fatigue?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Anemia leads to fatigue because it reduces the number of red blood cells available to carry oxygen to the body&rsquo;s tissues, resulting in a constant feeling of tiredness and weakness.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How is anemia diagnosed?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Anemia is diagnosed through blood tests such as a Complete Blood Count (CBC), serum ferritin levels, and assessments of vitamin B12 and folate.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Are iron infusions safe?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Yes, iron infusions are generally safe and are an effective treatment for severe anemia or when oral supplements are not suitable.</p></div>
      <div style="padding:22px 0;border-bottom:1px solid var(--border);"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">How long does it take to feel better after an iron infusion?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Many patients start to feel better within a few days to a week after the infusion, with significant improvements in energy and reduction in fatigue.</p></div>
      <div style="padding:22px 0;"><h3 style="font-size:17px;color:#1C1633;margin-bottom:9px;">Can I prevent anemia?</h3><p style="font-size:15.5px;line-height:1.72;color:#56526A;">Preventing anemia involves maintaining a balanced diet rich in iron, vitamins B12 and folate, and managing any underlying health conditions.</p></div>
    </div>
  </div>
</section>

<!-- FOOTER -->
{FOOTER}
</body>
</html>""")

# ---------------------------------------------------------------------------
# ENERGY BOOST — full-content page matching WP original
# ---------------------------------------------------------------------------
ENERGY_BOOST_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Anemia & Iron Deficiency Consultation | Premier Hematology", "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology offers next-day consultations and personalized treatment plans for anemia and iron deficiency.")}
<style>
  /* ---- Energy Boost page overrides ---- */
  .eb-insurance-bar {{
    background: var(--purple); color: #fff;
    text-align: center; padding: 11px 20px;
    font-size: 13.5px; font-weight: 600; letter-spacing: 0.06em;
  }}
  .eb-hero {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px 72px;
    display: grid; grid-template-columns: 1.1fr 1fr; gap: 64px; align-items: center;
  }}
  .eb-hero__h1 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 48px;
    line-height: 1.06; letter-spacing: -0.02em; color: var(--ink); margin-bottom: 20px;
  }}
  .eb-hero__lead {{
    font-size: 17px; line-height: 1.7; color: var(--body); margin-bottom: 26px; max-width: 480px;
  }}
  .eb-hero__imgs {{ display: flex; flex-direction: column; gap: 14px; }}
  .eb-hero__img {{
    width: 100%; border-radius: 18px; object-fit: cover; display: block;
  }}
  .eb-hero__img--top {{ height: 260px; }}
  .eb-hero__img--bottom {{ height: 220px; }}
  .eb-hero__testimonial {{
    margin-top: 28px; padding: 18px 22px;
    background: var(--lavender-bg); border-radius: 14px;
    border-left: 3px solid var(--purple);
  }}
  .eb-hero__testimonial p {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 15.5px; line-height: 1.55; color: var(--ink); margin-bottom: 8px;
  }}
  .eb-hero__testimonial cite {{
    font-size: 13px; font-weight: 600; color: var(--purple); font-style: normal;
  }}
  /* ---- section with image on right ---- */
  .eb-split {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px;
    display: grid; gap: 64px; align-items: center;
  }}
  .eb-split--img-right {{ grid-template-columns: 1fr 1fr; }}
  .eb-split--img-left  {{ grid-template-columns: 1fr 1fr; }}
  .eb-split__img {{
    width: 100%; border-radius: 20px; object-fit: cover;
    display: block; height: 440px;
  }}
  .eb-split__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 38px;
    line-height: 1.12; letter-spacing: -0.015em; color: var(--ink); margin-bottom: 18px;
  }}
  .eb-split__body {{
    font-size: 16.5px; line-height: 1.75; color: var(--body); margin-bottom: 18px;
  }}
  /* ---- dark band ---- */
  .eb-dark {{
    background: var(--ink);
  }}
  .eb-dark__inner {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
  }}
  .eb-dark__img {{
    width: 100%; border-radius: 20px; object-fit: cover;
    display: block; height: 440px;
  }}
  .eb-dark__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 38px;
    line-height: 1.12; color: #fff; margin-bottom: 18px;
  }}
  .eb-dark__body {{ font-size: 16px; line-height: 1.75; color: #c9c3e0; margin-bottom: 24px; }}
  .eb-dark .checklist__check {{
    background: rgba(255,255,255,0.12); color: #fff; border: none;
  }}
  .eb-dark .checklist__text {{ color: #c9c3e0; }}
  /* ---- full-width image strip ---- */
  .eb-img-strip {{
    width: 100%; overflow: hidden; height: 380px;
  }}
  .eb-img-strip img {{
    width: 100%; height: 100%; object-fit: cover; display: block;
  }}
  /* ---- how it works ---- */
  .eb-how {{
    background: var(--off-white);
    border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  }}
  .eb-how__inner {{
    max-width: 1200px; margin: 0 auto; padding: 88px 40px;
  }}
  .eb-how__header {{
    text-align: center; margin-bottom: 56px;
  }}
  .eb-how__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 14px;
  }}
  .eb-how__lead {{
    font-size: 17px; line-height: 1.65; color: var(--body); max-width: 560px; margin: 0 auto;
  }}
  .eb-how__grid {{
    display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; margin-bottom: 44px;
  }}
  .eb-step-card {{
    background: #fff; border: 1px solid var(--border-card);
    border-radius: 20px; overflow: hidden;
  }}
  .eb-step-card__img {{
    width: 100%; height: 190px; object-fit: cover; display: block;
  }}
  .eb-step-card__body {{ padding: 28px 26px 30px; }}
  .eb-step-card__num {{
    font-family: 'Newsreader', serif; font-style: italic; font-size: 28px;
    color: var(--step-numeral); margin-bottom: 8px; line-height: 1;
  }}
  .eb-step-card__title {{
    font-family: 'Newsreader', serif; font-weight: 600; font-size: 20px;
    color: var(--ink); margin-bottom: 10px;
  }}
  .eb-step-card__desc {{ font-size: 14.5px; line-height: 1.65; color: var(--body-muted); }}
  /* ---- purple CTA band ---- */
  .eb-cta-band {{ max-width: 1200px; margin: 0 auto; padding: 80px 40px; }}
  .eb-cta-band__inner {{
    background: linear-gradient(110deg, var(--purple), var(--purple-deep));
    border-radius: 22px; padding: 52px 56px;
    display: flex; align-items: center; justify-content: space-between; gap: 32px;
  }}
  .eb-cta-band__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 36px;
    line-height: 1.2; color: #fff; max-width: 560px;
  }}
  /* ---- reviews ---- */
  .eb-reviews {{
    background: var(--off-white);
    border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  }}
  .eb-reviews__inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-reviews__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 40px; text-align: center;
  }}
  .eb-reviews__grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }}
  .eb-review-card {{
    background: #fff; border: 1px solid var(--border-card);
    border-radius: 18px; padding: 28px 26px;
  }}
  .eb-review-card__stars {{ color: #f59e0b; font-size: 17px; margin-bottom: 14px; letter-spacing: 2px; }}
  .eb-review-card__quote {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 16px; line-height: 1.65; color: var(--ink); margin-bottom: 18px;
  }}
  .eb-review-card__name {{
    font-size: 13.5px; font-weight: 600; color: var(--purple);
  }}
  /* ---- FAQ ---- */
  .eb-faq {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-faq__grid {{
    display: grid; grid-template-columns: 360px 1fr; gap: 72px; align-items: start;
  }}
  .eb-faq__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 28px;
  }}
  .eb-faq__img {{ width: 100%; border-radius: 18px; object-fit: cover; height: 320px; display: block; }}
  .eb-faq__item {{ padding: 22px 0; border-bottom: 1px solid var(--border); }}
  .eb-faq__item:first-child {{ padding-top: 0; }}
  .eb-faq__q {{
    font-family: 'Newsreader', serif; font-weight: 600; font-size: 18px;
    color: var(--ink); margin-bottom: 9px;
  }}
  .eb-faq__a {{ font-size: 15.5px; line-height: 1.72; color: var(--body); }}
  /* ---- responsive ---- */
  @media (max-width: 900px) {{
    .eb-hero, .eb-split--img-right, .eb-split--img-left,
    .eb-dark__inner, .eb-faq__grid {{ grid-template-columns: 1fr; gap: 36px; }}
    .eb-hero {{ padding: 48px 24px; }}
    .eb-hero__h1 {{ font-size: 36px; }}
    .eb-split {{ padding: 56px 24px; }}
    .eb-dark__inner {{ padding: 56px 24px; }}
    .eb-how__grid {{ grid-template-columns: 1fr; }}
    .eb-reviews__grid {{ grid-template-columns: 1fr; }}
    .eb-cta-band__inner {{ flex-direction: column; text-align: center; padding: 40px 32px; }}
    .eb-how__inner, .eb-reviews__inner, .eb-faq {{ padding: 56px 24px; }}
    .eb-cta-band {{ padding: 48px 24px; }}
    .eb-img-strip {{ height: 220px; }}
    .eb-split__img, .eb-dark__img {{ height: 300px; }}
  }}
</style>
</head>
<body>

{HEADER}

  <div class="eb-insurance-bar">We Accept Most Major Insurances &mdash; Get Approved Today</div>

  <!-- HERO -->
  <section class="eb-hero">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:16px;">Hematology Consults and Iron Infusions</div>
      <h1 class="eb-hero__h1">Have Low Iron? Get Seen in 24 Hours By a Top NY Hematologist.</h1>
      <p class="eb-hero__lead">Stop waiting weeks. Stop being told &ldquo;just take pills.&rdquo; Our board-certified hematologists treat iron deficiency fast &mdash; with personalized infusions covered by insurance.</p>
      <div class="checklist" style="margin-bottom:28px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Board-certified hematology specialists</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day appointments available</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Most major insurance accepted</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Broad network of convenient locations throughout NY</span></div>
      </div>
      <a href="#bottom_form" class="btn btn--lg">Schedule an Appointment &rarr;</a>
      <div class="eb-hero__testimonial">
        <p>&ldquo;The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo;</p>
        <cite>&mdash; Anastasia M.</cite>
      </div>
    </div>
    <div class="eb-hero__imgs">
      <img class="eb-hero__img eb-hero__img--top" src="http://premierhematology.com/wp-content/uploads/2024/04/0_0.webp" alt="Women's iron infusion care">
      <img class="eb-hero__img eb-hero__img--bottom" src="http://premierhematology.com/wp-content/uploads/2025/02/yonah0704_15145_headshot._smiling_latina_physician._purple_blou_6043a991-d6fd-41e8-ae2f-4ce291077430.png" alt="Premier Hematology physician">
    </div>
  </section>

  <!-- Real Reason — text left, image right -->
  <section class="eb-split eb-split--img-right" style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">Why Supplements Fail</div>
      <h2 class="eb-split__h2">The Real Reason You&rsquo;re Still Tired</h2>
      <p class="eb-split__body">Most women with low iron are told to &ldquo;take supplements&rdquo; and wait months. But pills fail up to <strong>67% of the time</strong> &mdash; and don&rsquo;t work when your levels are critically low.</p>
      <p class="eb-split__body">You&rsquo;ve tried the iron pills. You&rsquo;ve blamed stress. But the real reason you&rsquo;re exhausted might be right there in your bloodwork &mdash; if someone would just look.</p>
      <a href="#bottom_form" class="btn" style="margin-top:8px;">Find Out What&rsquo;s Really Going On &rarr;</a>
    </div>
    <div>
      <img class="eb-split__img" src="http://premierhematology.com/wp-content/uploads/2025/07/questions.png" alt="Iron deficiency questions">
    </div>
  </section>

  <!-- Hidden Crisis — dark band, image left, text right -->
  <section class="eb-dark">
    <div class="eb-dark__inner">
      <div>
        <img class="eb-dark__img" src="http://premierhematology.com/wp-content/uploads/2025/07/aging-2-1.png" alt="Aging and iron deficiency">
      </div>
      <div>
        <div class="eyebrow-sans" style="color:#c3aef0;margin-bottom:14px;">The Overlooked Epidemic</div>
        <h2 class="eb-dark__h2">The Hidden Crisis That Impacts 1 in 5 Women</h2>
        <p class="eb-dark__body">Anemia affects 20% of women &mdash; but most are misdiagnosed, dismissed, or ignored. Here&rsquo;s what your doctor might not tell you:</p>
        <div class="checklist">
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Iron pills don&rsquo;t work for everyone</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Basic labs can miss low ferritin &mdash; the protein that fuels your energy</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Most doctors aren&rsquo;t trained to spot iron deficiency in women</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">If severely deficient, supplements can take 6&ndash;12 months to work</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- How the Program Works — cards on light bg -->
  <section class="eb-how">
    <div class="eb-how__inner">
      <div class="eb-how__header">
        <div class="eyebrow-sans" style="margin-bottom:12px;">Fast, Personalized &amp; Proven</div>
        <h2 class="eb-how__h2">How the EnergyBoost Iron Care Program&#8482; Works</h2>
        <p class="eb-how__lead">A 3-part protocol designed to identify the real problem and treat it fast. No more guessing. No more waiting.</p>
      </div>
      <div class="eb-how__grid">
        <div class="eb-step-card">
          <img class="eb-step-card__img" src="http://premierhematology.com/wp-content/uploads/2025/07/womens-infusion.png" alt="Lab-guided diagnosis">
          <div class="eb-step-card__body">
            <div class="eb-step-card__num">01</div>
            <h3 class="eb-step-card__title">Lab-Guided Diagnosis</h3>
            <p class="eb-step-card__desc">We don&rsquo;t guess. We check your ferritin, hemoglobin, B12, folate &amp; more to get the full picture.</p>
          </div>
        </div>
        <div class="eb-step-card">
          <img class="eb-step-card__img" src="http://premierhematology.com/wp-content/uploads/2024/04/0_0.webp" alt="Personalized infusion protocol">
          <div class="eb-step-card__body">
            <div class="eb-step-card__num">02</div>
            <h3 class="eb-step-card__title">Personalized Infusion Protocol</h3>
            <p class="eb-step-card__desc">Based on your labs and symptoms, our hematologists design a custom treatment plan for your body.</p>
          </div>
        </div>
        <div class="eb-step-card">
          <img class="eb-step-card__img" src="http://premierhematology.com/wp-content/uploads/2024/04/care.webp" alt="Track and support your recovery">
          <div class="eb-step-card__body">
            <div class="eb-step-card__num">03</div>
            <h3 class="eb-step-card__title">Track + Support Your Recovery</h3>
            <p class="eb-step-card__desc">Most patients feel a difference within 5&ndash;10 days.</p>
          </div>
        </div>
      </div>
      <div style="text-align:center;">
        <a href="#bottom_form" class="btn btn--lg">Take the First Step &rarr;</a>
      </div>
    </div>
  </section>

  <!-- Symptoms — text left, image right -->
  <section class="eb-split eb-split--img-right">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">Recognize the Signs</div>
      <h2 class="eb-split__h2">Your Body Is Trying to Tell You Something.</h2>
      <p class="eb-split__body">Do any of these sound familiar?</p>
      <div class="checklist" style="margin-bottom:32px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Chronic fatigue &mdash; even after 8 hours of sleep</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Heavy or long periods</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Brain fog or trouble concentrating</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Hair loss or brittle nails</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Shortness of breath</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Dizziness or lightheadedness</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Restless legs or cold hands/feet</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Low mood, irritability, or feeling &ldquo;off&rdquo;</span></div>
      </div>
      <p class="eb-split__body" style="margin-top:0;">If you checked 2 or more&hellip; You may be iron deficient &mdash; and we can help.</p>
      <a href="#bottom_form" class="btn">Book Your Appointment Now &rarr;</a>
    </div>
    <div>
      <img class="eb-split__img" src="http://premierhematology.com/wp-content/uploads/2024/04/fatigue.webp" alt="Woman experiencing fatigue from iron deficiency">
    </div>
  </section>

  <!-- Why Choose Premier — image left, text right -->
  <section class="eb-split eb-split--img-left" style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
    <div>
      <img class="eb-split__img" src="http://premierhematology.com/wp-content/uploads/2025/07/smiling.png" alt="Happy patient after treatment">
    </div>
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">Thousands Helped Across New York</div>
      <h2 class="eb-split__h2">Why Women Who&rsquo;ve Tried Everything Else Are Choosing Premier Hematology</h2>
      <p class="eb-split__body">Tired of being told &ldquo;you&rsquo;re fine&rdquo; when you feel anything but? Here&rsquo;s what makes us different:</p>
      <div class="checklist" style="margin-bottom:32px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">No Long Waits</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">No &ldquo;just take pills&rdquo; advice</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">No cookie-cutter plans</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Women-first, doctor-led care</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Built for busy moms and professionals</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Trusted by NYC&rsquo;s best OBGYNs &amp; PCPs</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">10 convenient locations &mdash; fast, real results</span></div>
      </div>
      <a href="#bottom_form" class="btn">Get Started Today &rarr;</a>
    </div>
  </section>

  <!-- Meet the Experts — dark band -->
  <section class="eb-dark">
    <div class="eb-dark__inner">
      <div>
        <div class="eyebrow-sans" style="color:#c3aef0;margin-bottom:14px;">Premier Hematology &amp; Oncology</div>
        <h2 class="eb-dark__h2">Meet New York&rsquo;s Women&rsquo;s Iron Health Experts</h2>
        <p class="eb-dark__body">Premier Hematology &amp; Oncology is New York&rsquo;s leading center for personalized iron deficiency care. Led by board-certified hematologists and women&rsquo;s health specialists, our mission is simple: Help you feel like yourself again.</p>
        <p class="eb-dark__body">We&rsquo;ve helped thousands of women across New York reclaim their energy, their clarity, and their lives.</p>
        <a href="#bottom_form" class="btn btn--white">Book a Consultation &rarr;</a>
      </div>
      <div>
        <img class="eb-dark__img" src="http://premierhematology.com/wp-content/uploads/2025/07/premier-team.png" alt="Premier Hematology care team">
      </div>
    </div>
  </section>

  <!-- Reviews -->
  <section class="eb-reviews">
    <div class="eb-reviews__inner">
      <div class="eyebrow-sans" style="text-align:center;margin-bottom:12px;">Patient Stories</div>
      <h2 class="eb-reviews__h2">What Our Patients Are Saying</h2>
      <div class="eb-reviews__grid">
        <div class="eb-review-card">
          <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="eb-review-card__quote">&ldquo;The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo;</p>
          <div class="eb-review-card__name">&mdash; Anastasia M.</div>
        </div>
        <div class="eb-review-card">
          <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="eb-review-card__quote">&ldquo;Getting my blood work infusions and shot shots at Premier Hematology has been nothing short of a pleasure everybody who works here is so kind extremely responsive communicative in a way that seems very unusual in the medical space and I cannot recommend this place highly enough!&rdquo;</p>
          <div class="eb-review-card__name">&mdash; Chani Shalmoni</div>
        </div>
        <div class="eb-review-card">
          <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="eb-review-card__quote">&ldquo;The team here is exceptionally professional and welcoming. Since starting my iron infusions and B12 shots, I&rsquo;ve felt noticeably healthier and more energized. They go above and beyond to ensure a comfortable experience, even offering great snacks during treatment. Highly recommend!&rdquo;</p>
          <div class="eb-review-card__name">&mdash; Karla Ximena V&aacute;zquez Prada</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Everything You Need -->
  <section class="eb-split eb-split--img-left" style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
    <div>
      <img class="eb-split__img" src="http://premierhematology.com/wp-content/uploads/2025/07/smiling.png" alt="Premier Hematology infusion center">
    </div>
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">10 Locations Across New York</div>
      <h2 class="eb-split__h2">Everything you Need. All in One Location.</h2>
      <p class="eb-split__body">With 10 convenient locations across New York, we are able to make sure that your infusion care doesn&rsquo;t get in the way of your busy life.</p>
      <div class="checklist" style="margin-bottom:32px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day consultations</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Covered by most major insurances</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Safe, fast, medically supervised iron infusions</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Labs + treatment under one roof</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Designed specifically for women&rsquo;s needs</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Available in 10 NYC locations + telehealth consults</span></div>
      </div>
      <a href="#bottom_form" class="btn">Get Started Today &rarr;</a>
    </div>
  </section>

  <!-- CTA Band -->
  <div class="eb-cta-band">
    <div class="eb-cta-band__inner">
      <h2 class="eb-cta-band__h2">Feeling Tired All the Time Isn&rsquo;t Normal. Let&rsquo;s Fix It.</h2>
      <a href="#bottom_form" class="btn btn--white btn--lg">Book Your Appointment Now &rarr;</a>
    </div>
  </div>

  <!-- FAQ -->
  <section class="eb-faq">
    <div class="eb-faq__grid">
      <div>
        <h2 class="eb-faq__h2">Frequently Asked Questions</h2>
        <img class="eb-faq__img" src="http://premierhematology.com/wp-content/uploads/2024/04/care.webp" alt="Premier Hematology infusion care">
      </div>
      <div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">What causes anemia in women?</h3>
          <p class="eb-faq__a">Anemia in women can be caused by iron deficiency, vitamin deficiencies, chronic diseases, pregnancy, and heavy menstrual bleeding.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">How does anemia cause fatigue?</h3>
          <p class="eb-faq__a">Anemia leads to fatigue because it reduces the number of red blood cells available to carry oxygen to the body&rsquo;s tissues, resulting in a constant feeling of tiredness and weakness.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">How is anemia diagnosed?</h3>
          <p class="eb-faq__a">Anemia is diagnosed through blood tests such as a Complete Blood Count (CBC), serum ferritin levels, and assessments of vitamin B12 and folate.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">Are iron infusions safe?</h3>
          <p class="eb-faq__a">Yes, iron infusions are generally safe and are an effective treatment for severe anemia or when oral supplements are not suitable.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">How long does it take to feel better after an iron infusion?</h3>
          <p class="eb-faq__a">Many patients start to feel better within a few days to a week after the infusion, with significant improvements in energy and reduction in fatigue.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">Can I prevent anemia?</h3>
          <p class="eb-faq__a">Preventing anemia involves maintaining a balanced diet rich in iron, vitamins B12 and folate, and managing any underlying health conditions.</p>
        </div>
      </div>
    </div>
  </section>

{FOOTER}
</body>
</html>"""

write("energy-boost/index.html", ENERGY_BOOST_PAGE)

# ---------------------------------------------------------------------------
# ENERGY BOOST ATLANTA — full-content page matching WP original
# ---------------------------------------------------------------------------
ENERGY_BOOST_ATLANTA_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Anemia & Iron Deficiency Consultation | Premier Hematology Atlanta", "Struggling with fatigue, dizziness, or shortness of breath? Premier Hematology Atlanta offers next-day consultations and personalized treatment plans for anemia and iron deficiency.")}
<style>
  .eb-insurance-bar {{
    background: var(--purple); color: #fff;
    text-align: center; padding: 11px 20px;
    font-size: 13.5px; font-weight: 600; letter-spacing: 0.06em;
  }}
  .eb-hero {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px 72px;
    display: grid; grid-template-columns: 1.1fr 1fr; gap: 64px; align-items: center;
  }}
  .eb-hero__h1 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 48px;
    line-height: 1.06; letter-spacing: -0.02em; color: var(--ink); margin-bottom: 20px;
  }}
  .eb-hero__lead {{
    font-size: 17px; line-height: 1.7; color: var(--body); margin-bottom: 26px; max-width: 480px;
  }}
  .eb-hero__imgs {{ display: flex; flex-direction: column; gap: 14px; }}
  .eb-hero__img {{ width: 100%; border-radius: 18px; object-fit: cover; display: block; }}
  .eb-hero__img--top {{ height: 260px; }}
  .eb-hero__img--bottom {{ height: 220px; }}
  .eb-hero__testimonial {{
    margin-top: 28px; padding: 18px 22px;
    background: var(--lavender-bg); border-radius: 14px;
    border-left: 3px solid var(--purple);
  }}
  .eb-hero__testimonial p {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 15.5px; line-height: 1.55; color: var(--ink); margin-bottom: 8px;
  }}
  .eb-hero__testimonial cite {{
    font-size: 13px; font-weight: 600; color: var(--purple); font-style: normal;
  }}
  .eb-split {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px;
    display: grid; gap: 64px; align-items: center;
  }}
  .eb-split--img-right {{ grid-template-columns: 1fr 1fr; }}
  .eb-split--img-left  {{ grid-template-columns: 1fr 1fr; }}
  .eb-split__img {{ width: 100%; border-radius: 20px; object-fit: cover; display: block; height: 440px; }}
  .eb-split__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 38px;
    line-height: 1.12; letter-spacing: -0.015em; color: var(--ink); margin-bottom: 18px;
  }}
  .eb-split__body {{ font-size: 16.5px; line-height: 1.75; color: var(--body); margin-bottom: 18px; }}
  .eb-dark {{ background: var(--ink); }}
  .eb-dark__inner {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
  }}
  .eb-dark__img {{ width: 100%; border-radius: 20px; object-fit: cover; display: block; height: 440px; }}
  .eb-dark__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 38px;
    line-height: 1.12; color: #fff; margin-bottom: 18px;
  }}
  .eb-dark__body {{ font-size: 16px; line-height: 1.75; color: #c9c3e0; margin-bottom: 24px; }}
  .eb-dark .checklist__check {{ background: rgba(255,255,255,0.12); color: #fff; border: none; }}
  .eb-dark .checklist__text {{ color: #c9c3e0; }}
  .eb-how {{ background: var(--off-white); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
  .eb-how__inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-how__header {{ text-align: center; margin-bottom: 56px; }}
  .eb-how__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 14px;
  }}
  .eb-how__lead {{ font-size: 17px; line-height: 1.65; color: var(--body); max-width: 560px; margin: 0 auto; }}
  .eb-how__grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; margin-bottom: 44px; }}
  .eb-step-card {{ background: #fff; border: 1px solid var(--border-card); border-radius: 20px; overflow: hidden; }}
  .eb-step-card__img {{ width: 100%; height: 190px; object-fit: cover; display: block; }}
  .eb-step-card__body {{ padding: 28px 26px 30px; }}
  .eb-step-card__num {{
    font-family: 'Newsreader', serif; font-style: italic; font-size: 28px;
    color: var(--step-numeral); margin-bottom: 8px; line-height: 1;
  }}
  .eb-step-card__title {{ font-family: 'Newsreader', serif; font-weight: 600; font-size: 20px; color: var(--ink); margin-bottom: 10px; }}
  .eb-step-card__desc {{ font-size: 14.5px; line-height: 1.65; color: var(--body-muted); }}
  .eb-cta-band {{ max-width: 1200px; margin: 0 auto; padding: 80px 40px; }}
  .eb-cta-band__inner {{
    background: linear-gradient(110deg, var(--purple), var(--purple-deep));
    border-radius: 22px; padding: 52px 56px;
    display: flex; align-items: center; justify-content: space-between; gap: 32px;
  }}
  .eb-cta-band__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 36px;
    line-height: 1.2; color: #fff; max-width: 560px;
  }}
  .eb-reviews {{ background: var(--off-white); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
  .eb-reviews__inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-reviews__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 40px; text-align: center;
  }}
  .eb-reviews__grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }}
  .eb-review-card {{ background: #fff; border: 1px solid var(--border-card); border-radius: 18px; padding: 28px 26px; }}
  .eb-review-card__stars {{ color: #f59e0b; font-size: 17px; margin-bottom: 14px; letter-spacing: 2px; }}
  .eb-review-card__quote {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 16px; line-height: 1.65; color: var(--ink); margin-bottom: 18px;
  }}
  .eb-review-card__name {{ font-size: 13.5px; font-weight: 600; color: var(--purple); }}
  .eb-faq {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-faq__grid {{ display: grid; grid-template-columns: 360px 1fr; gap: 72px; align-items: start; }}
  .eb-faq__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 28px;
  }}
  .eb-faq__img {{ width: 100%; border-radius: 18px; object-fit: cover; height: 320px; display: block; }}
  .eb-faq__item {{ padding: 22px 0; border-bottom: 1px solid var(--border); }}
  .eb-faq__item:first-child {{ padding-top: 0; }}
  .eb-faq__q {{ font-family: 'Newsreader', serif; font-weight: 600; font-size: 18px; color: var(--ink); margin-bottom: 9px; }}
  .eb-faq__a {{ font-size: 15.5px; line-height: 1.72; color: var(--body); }}
  @media (max-width: 900px) {{
    .eb-hero, .eb-split, .eb-dark__inner {{ grid-template-columns: 1fr; }}
    .eb-hero__imgs {{ display: none; }}
    .eb-how__grid, .eb-reviews__grid {{ grid-template-columns: 1fr; }}
    .eb-cta-band__inner {{ flex-direction: column; text-align: center; }}
    .eb-faq__grid {{ grid-template-columns: 1fr; }}
    .eb-faq__img {{ display: none; }}
  }}
</style>
</head>
<body>
{ATLANTA_HEADER}

<div class="eb-insurance-bar">We Accept Most Insurances &mdash; Get Approved Today</div>

<!-- HERO -->
<section style="background:#F3F5F8;">
  <div class="eb-hero">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:16px;">Hematology Consults and Iron Infusions</div>
      <h1 class="eb-hero__h1">Have Low Iron? Get Seen in 24 Hours By Atlanta&rsquo;s Trusted Hematologists.</h1>
      <p class="eb-hero__lead">Stop waiting weeks. Stop being told &ldquo;just take pills.&rdquo; Our board-certified hematologists treat iron deficiency fast &mdash; with personalized infusions covered by insurance.</p>
      <div class="checklist" style="margin-bottom:28px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">See a Women&rsquo;s Iron Specialist (Board-Certified Hematologist) within 24 hours</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Conveniently-Located in Atlanta</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Safe, fast, personalized iron infusions</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">For Women Who Are Tired of Feeling Tired&hellip; and Being Told It&rsquo;s &ldquo;Normal.&rdquo;</span></div>
      </div>
      <a href="#bottom_form" class="btn btn--lg">Schedule an Appointment &rarr;</a>
      <div class="eb-hero__testimonial">
        <p>&ldquo;The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo;</p>
        <cite>&mdash; Anastasia M.</cite>
      </div>
    </div>
    <div class="eb-hero__imgs">
      <img class="eb-hero__img eb-hero__img--top" src="{WP_IMG}2025/07/yonah0704_15145_a_30_year_old_woman_reclining_in_a_black_leat_cfbaa486-c462-4702-bcb6-3e7d8f14b5c1_1.png" alt="Patient at Premier Hematology Atlanta">
      <img class="eb-hero__img eb-hero__img--bottom" src="{WP_IMG}2024/04/0_0.webp" alt="Iron infusion at Premier Hematology Atlanta">
    </div>
  </div>
</section>

<!-- The Real Reason — text left, image right -->
<section class="eb-split eb-split--img-right">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">Why Supplements Fail</div>
    <h2 class="eb-split__h2">The Real Reason You&rsquo;re Still Tired</h2>
    <p class="eb-split__body">Most women with low iron are told to &ldquo;take supplements&rdquo; and wait months. But pills fail up to <strong>67% of the time</strong> &mdash; and don&rsquo;t work when your levels are critically low.</p>
    <p class="eb-split__body">That&rsquo;s where our EnergyBoost Iron Care Program&#8482; is different.</p>
    <div class="checklist" style="margin-bottom:20px;">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">You&rsquo;ve tried the iron pills.</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">You&rsquo;ve blamed stress, hormones, even age.</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">You&rsquo;re tired all the time &mdash; and nothing&rsquo;s changing.</span></div>
    </div>
    <p class="eb-split__body">&ldquo;We hear it every day: &lsquo;I&rsquo;m tired of being tired. And I just want to feel normal again.&rsquo;&rdquo;</p>
    <p class="eb-split__body">If that&rsquo;s you, you&rsquo;re not alone. And you&rsquo;re not crazy.</p>
    <p class="eb-split__body">Your body might be screaming for help&hellip; and iron infusions may be the answer.</p>
    <a href="#bottom_form" class="btn" style="margin-top:8px;">Find Out What&rsquo;s Really Going On &rarr;</a>
  </div>
  <div>
    <img class="eb-split__img" src="{WP_IMG}2025/07/questions.png" alt="Iron deficiency questions">
  </div>
</section>

<!-- Hidden Crisis — dark band -->
<section class="eb-dark">
  <div class="eb-dark__inner">
    <div>
      <img class="eb-dark__img" src="{WP_IMG}2025/07/aging-2-1.png" alt="Aging and iron deficiency">
    </div>
    <div>
      <div class="eyebrow-sans" style="color:#c3aef0;margin-bottom:14px;">The Overlooked Epidemic</div>
      <h2 class="eb-dark__h2">The Hidden Crisis That Impacts 1 in 5 Women</h2>
      <p class="eb-dark__body">Anemia affects 20% of women &mdash; but most are misdiagnosed, dismissed, or ignored. Here&rsquo;s what your doctor might not tell you:</p>
      <div class="checklist">
        <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Iron pills don&rsquo;t work for everyone</span></div>
        <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Basic labs can miss low ferritin (the protein that stores iron and fuels your body&rsquo;s energy)</span></div>
        <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">If you&rsquo;re severely deficient, supplements won&rsquo;t work fast enough</span></div>
        <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">And symptoms can mimic anxiety, depression, or burnout</span></div>
      </div>
      <p class="eb-dark__body" style="margin-top:20px;">Meanwhile, you&rsquo;re left exhausted, foggy, and barely functioning.</p>
    </div>
  </div>
</section>

<!-- EnergyBoost Program Intro -->
<section style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div style="max-width:760px;margin:0 auto;padding:80px 40px;text-align:center;">
    <div class="eyebrow-sans" style="margin-bottom:14px;">Fast, Personalized &amp; Proven</div>
    <h2 style="font-family:'Newsreader',serif;font-weight:500;font-size:40px;letter-spacing:-0.015em;color:var(--ink);margin-bottom:20px;">The EnergyBoost Iron Care Program&#8482;</h2>
    <p style="font-size:17px;line-height:1.75;color:var(--body);margin-bottom:12px;">We created the <strong>EnergyBoost Iron Care Program&#8482;</strong> to give women a better answer.</p>
    <p style="font-size:17px;line-height:1.75;color:var(--body);margin-bottom:12px;">No more guessing. No more waiting. No more being dismissed.</p>
    <p style="font-size:17px;line-height:1.75;color:var(--body);margin-bottom:32px;">It&rsquo;s a 3-part protocol designed to <strong>identify the real problem and treat it fast.</strong></p>
    <a href="#bottom_form" class="btn btn--lg">Get Started Today &rarr;</a>
  </div>
</section>

<!-- How the Program Works -->
<section class="eb-how">
  <div class="eb-how__inner">
    <div class="eb-how__header">
      <div class="eyebrow-sans" style="margin-bottom:12px;">How the Program Works</div>
      <h2 class="eb-how__h2">A 3-Part Protocol</h2>
      <p class="eb-how__lead">Designed to identify the real problem and treat it fast. No more guessing. No more waiting.</p>
    </div>
    <div class="eb-how__grid">
      <div class="eb-step-card">
        <img class="eb-step-card__img" src="{WP_IMG}2025/07/womens-infusion.png" alt="Lab-guided diagnosis">
        <div class="eb-step-card__body">
          <div class="eb-step-card__num">01</div>
          <h3 class="eb-step-card__title">Lab-Guided Diagnosis</h3>
          <p class="eb-step-card__desc">We don&rsquo;t guess. We check your ferritin, hemoglobin, B12, folate &amp; more to get the full picture. (or help examine your existing labs)</p>
        </div>
      </div>
      <div class="eb-step-card">
        <img class="eb-step-card__img" src="{WP_IMG}2024/04/0_0.webp" alt="Personalized infusion protocol">
        <div class="eb-step-card__body">
          <div class="eb-step-card__num">02</div>
          <h3 class="eb-step-card__title">Personalized Infusion Protocol</h3>
          <p class="eb-step-card__desc">Based on your labs and symptoms, our hematologists design a custom treatment plan for your body.</p>
        </div>
      </div>
      <div class="eb-step-card">
        <img class="eb-step-card__img" src="{WP_IMG}2024/04/care.webp" alt="Track and support your recovery">
        <div class="eb-step-card__body">
          <div class="eb-step-card__num">03</div>
          <h3 class="eb-step-card__title">Track + Support Your Recovery</h3>
          <p class="eb-step-card__desc">Most patients feel a difference within 5&ndash;10 days. We follow up to make sure you&rsquo;re not just functioning &mdash; you&rsquo;re thriving and create your customized path towards better health.</p>
        </div>
      </div>
    </div>
    <div style="text-align:center;">
      <a href="#bottom_form" class="btn btn--lg">Take the First Step &rarr;</a>
    </div>
  </div>
</section>

<!-- Symptoms — text left, image right -->
<section class="eb-split eb-split--img-right">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">Recognize the Signs</div>
    <h2 class="eb-split__h2">Your body is trying to tell you something.</h2>
    <p class="eb-split__body"><strong>Do any of these sound familiar?</strong></p>
    <div class="checklist" style="margin-bottom:20px;">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Chronic fatigue (even after 8 hours of sleep)</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Heavy or long periods</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Brain fog or trouble concentrating</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Hair loss or brittle nails</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Shortness of breath</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Dizziness or lightheadedness</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Restless legs or cold hands/feet</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Low mood, irritability, or feeling &ldquo;off&rdquo;</span></div>
    </div>
    <p class="eb-split__body" style="margin-top:0;">If you checked 2 or more&hellip; <strong>You may be iron deficient &mdash; and we can help.</strong></p>
    <a href="#bottom_form" class="btn">Book Your Appointment Now &rarr;</a>
  </div>
  <div>
    <img class="eb-split__img" src="{WP_IMG}2024/04/fatigue.webp" alt="Woman experiencing fatigue from iron deficiency">
  </div>
</section>

<!-- Reviews -->
<section class="eb-reviews">
  <div class="eb-reviews__inner">
    <div class="eyebrow-sans" style="text-align:center;margin-bottom:12px;">Don&rsquo;t Take Our Word For It</div>
    <h2 class="eb-reviews__h2">What Our Patients Are Saying</h2>
    <div class="eb-reviews__grid">
      <div class="eb-review-card">
        <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="eb-review-card__quote">&ldquo;Had an amazing experience at Premier Hematology! Varda took incredible care of me, so kind, knowledgeable, and made the whole process feel effortless. The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo;</p>
        <div class="eb-review-card__name">&mdash; Anastasia Hing Mackay</div>
      </div>
      <div class="eb-review-card">
        <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="eb-review-card__quote">&ldquo;Getting my blood work infusions and shot shots at Premier Hematology has been nothing short of a pleasure everybody who works here is so kind extremely responsive communicative in a way that seems very unusual in the medical space and I cannot recommend this place highly enough!&rdquo;</p>
        <div class="eb-review-card__name">&mdash; Chani Shalmoni</div>
      </div>
      <div class="eb-review-card">
        <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="eb-review-card__quote">&ldquo;The team here is exceptionally professional and welcoming. Since starting my iron infusions and B12 shots, I&rsquo;ve felt noticeably healthier and more energized. They go above and beyond to ensure a comfortable experience, even offering great snacks during treatment. Highly recommend!&rdquo;</p>
        <div class="eb-review-card__name">&mdash; Karla Ximena V&aacute;zquez Prada</div>
      </div>
    </div>
  </div>
</section>

<!-- Everything You Need — Atlanta -->
<section class="eb-split eb-split--img-left" style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
  <div>
    <img class="eb-split__img" src="{WP_IMG}2025/07/smiling.png" alt="Premier Hematology Atlanta infusion center">
  </div>
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">Metro-Atlanta Location</div>
    <h2 class="eb-split__h2">Everything you Need. All in One Location.</h2>
    <p class="eb-split__body">Located conveniently in the metro-Atlanta area, we are able to make sure that your infusion care doesn&rsquo;t get in the way of your busy life. Visit our offices at <strong>325 Hammond Dr Suite 201, Atlanta, GA 30328</strong>.</p>
    <div class="checklist" style="margin-bottom:32px;">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day consultations</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Covered by most major insurances</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Safe, fast, medically supervised iron infusions</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Labs + treatment under one roof</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Designed specifically for women&rsquo;s needs</span></div>
    </div>
    <a href="#bottom_form" class="btn">Get Started Today &rarr;</a>
  </div>
</section>

<!-- Why Women Choose — image left, text right -->
<section class="eb-split eb-split--img-right">
  <div>
    <div class="eyebrow-sans" style="margin-bottom:14px;">Thousands Helped</div>
    <h2 class="eb-split__h2">Why Women Who&rsquo;ve Tried Everything Else Are Choosing Premier Hematology</h2>
    <p class="eb-split__body">Tired of being told &ldquo;you&rsquo;re fine&rdquo; when you feel anything but? Here&rsquo;s what makes us different:</p>
    <div class="checklist" style="margin-bottom:32px;">
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">No Long Waits</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">No &ldquo;just take pills&rdquo; advice</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">No cookie-cutter plans</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Women-first, doctor-led care</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Built for busy moms and professionals</span></div>
      <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Trusted by Atlanta&rsquo;s best OBGYNs &amp; PCPs</span></div>
    </div>
    <a href="#bottom_form" class="btn">Click Here to Get Started &rarr;</a>
  </div>
  <div>
    <img class="eb-split__img" src="{WP_IMG}2025/07/smiling.png" alt="Happy patient after treatment">
  </div>
</section>

<!-- Meet the Experts — dark band -->
<section class="eb-dark">
  <div class="eb-dark__inner">
    <div>
      <div class="eyebrow-sans" style="color:#c3aef0;margin-bottom:14px;">Premier Hematology &amp; Oncology</div>
      <h2 class="eb-dark__h2">Meet Atlanta&rsquo;s Women&rsquo;s Iron Health Experts</h2>
      <p class="eb-dark__body">Premier Hematology &amp; Oncology is Atlanta&rsquo;s fastest-growing center for personalized iron deficiency care. Led by board-certified hematologists and women&rsquo;s health experts, our mission is simple: Help you feel better, fast &mdash; with care you can actually trust.</p>
      <p class="eb-dark__body">We&rsquo;ve helped thousands of women reclaim their energy, mental clarity, and quality of life through our science-backed infusion system.</p>
      <a href="#bottom_form" class="btn btn--white">Book a Consultation &rarr;</a>
    </div>
    <div>
      <img class="eb-dark__img" src="{WP_IMG}2025/07/premier-team.png" alt="Premier Hematology Atlanta care team">
    </div>
  </div>
</section>

<!-- CTA Band -->
<div class="eb-cta-band">
  <div class="eb-cta-band__inner">
    <h2 class="eb-cta-band__h2">Feeling Tired All The Time Isn&rsquo;t Normal. Let&rsquo;s Fix It.</h2>
    <a href="#bottom_form" class="btn btn--white btn--lg">Book Your Appointment Now &rarr;</a>
  </div>
</div>

<!-- FAQ -->
<section class="eb-faq">
  <div class="eb-faq__grid">
    <div>
      <h2 class="eb-faq__h2">Frequently Asked Questions (FAQs)</h2>
      <img class="eb-faq__img" src="{WP_IMG}2024/04/care.webp" alt="Premier Hematology Atlanta infusion care">
    </div>
    <div>
      <div class="eb-faq__item">
        <h3 class="eb-faq__q">What causes anemia in women?</h3>
        <p class="eb-faq__a">Anemia in women can be caused by iron deficiency, vitamin deficiencies, chronic diseases, pregnancy, and heavy menstrual bleeding.</p>
      </div>
      <div class="eb-faq__item">
        <h3 class="eb-faq__q">How does anemia cause fatigue?</h3>
        <p class="eb-faq__a">Anemia leads to fatigue because it reduces the number of red blood cells available to carry oxygen to the body&rsquo;s tissues, resulting in a constant feeling of tiredness and weakness.</p>
      </div>
      <div class="eb-faq__item">
        <h3 class="eb-faq__q">How is anemia diagnosed?</h3>
        <p class="eb-faq__a">Anemia is diagnosed through blood tests such as a Complete Blood Count (CBC), serum ferritin levels, and assessments of vitamin B12 and folate.</p>
      </div>
      <div class="eb-faq__item">
        <h3 class="eb-faq__q">Are iron infusions safe?</h3>
        <p class="eb-faq__a">Yes, iron infusions are generally safe and are an effective treatment for severe anemia or when oral supplements are not suitable.</p>
      </div>
      <div class="eb-faq__item">
        <h3 class="eb-faq__q">How long does it take to feel better after an iron infusion?</h3>
        <p class="eb-faq__a">Many patients start to feel better within a few days to a week after the infusion, with significant improvements in energy and reduction in fatigue.</p>
      </div>
      <div class="eb-faq__item">
        <h3 class="eb-faq__q">Can I prevent anemia?</h3>
        <p class="eb-faq__a">Preventing anemia involves maintaining a balanced diet rich in iron, vitamins B12 and folate, and managing any underlying health conditions.</p>
      </div>
    </div>
  </div>
</section>

{ATLANTA_FOOTER}
</body>
</html>"""

write("energy-boost-atlanta-hematology-and-iron-infusion-appointments/index.html", ENERGY_BOOST_ATLANTA_PAGE)

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

# Individual blog posts — use real WordPress content where available
import json as _json
_wp_map = {}
try:
    with open(os.path.join(ROOT, "wp_blogs.json")) as _f:
        for _p in _json.load(_f):
            _wp_map[_p["slug"]] = _p
except Exception:
    pass

_all_post_slugs = {s for s, *_ in ALL_POSTS}

for slug, title, cat, focus_kw in ALL_POSTS:
    wp = _wp_map.get(slug)
    if wp and wp.get("html_content"):
        body = wp["html_content"]
        title = wp["title"] or title
        meta_desc = wp["meta_desc"] or f"Learn about {focus_kw} from the specialists at Premier Hematology & Oncology. Expert insights on treatment, symptoms, and care."
        yoast_title = wp["yoast_title"] or title
    else:
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
        meta_desc = f"Learn about {focus_kw} from the specialists at Premier Hematology & Oncology. Expert insights on treatment, symptoms, and care."
        yoast_title = title

    # rotate related posts (pick 3 different ones)
    post_index = next((i for i, p in enumerate(ALL_POSTS) if p[0] == slug), 0)
    rel = [ALL_POSTS[(post_index + 1) % len(ALL_POSTS)],
           ALL_POSTS[(post_index + 2) % len(ALL_POSTS)],
           ALL_POSTS[(post_index + 3) % len(ALL_POSTS)]]
    related_posts = [{"slug": r[0], "title": r[1], "cat": r[2]} for r in rel]

    write(f"blog/{slug}/index.html", article_page(
        slug=slug,
        title=title,
        yoast_title=yoast_title,
        meta_desc=meta_desc,
        category=cat,
        author="Premier Hematology & Oncology",
        date="2026",
        read_time="5",
        body_html=body,
        related_posts=related_posts,
    ))

# WP posts not in ALL_POSTS — write them too
for _wp_slug, wp in _wp_map.items():
    if _wp_slug not in _all_post_slugs:
        _body = wp.get("html_content") or ""
        _title = wp.get("title") or _wp_slug
        _meta = wp.get("meta_desc") or f"Expert hematology insights from Premier Hematology & Oncology."
        _yoast = wp.get("yoast_title") or _title
        write(f"blog/{_wp_slug}/index.html", article_page(
            slug=_wp_slug,
            title=_title,
            yoast_title=_yoast,
            meta_desc=_meta,
            category="Hematology",
            author="Premier Hematology & Oncology",
            date="2025",
            read_time="5",
            body_html=_body,
            related_posts=BLOG_RELATED,
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
write("physician-career-opportunity/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Physician Career Opportunity | Premier Hematology &amp; Oncology", "Join Premier Hematology &amp; Oncology — a multi-site community practice offering clinical autonomy, competitive compensation, and a collaborative environment across New York.")}
<style>
  /* ── hero ── */
  .pco-hero {{
    background-image: url('{WP_IMG}2021/05/GettyImages-1189547726.jpg');
    background-size: cover; background-position: center top;
  }}
  .pco-hero__inner {{
    background: rgba(28,22,51,0.70);
    padding: 108px 40px 100px;
    text-align: center;
  }}
  .pco-hero__h1 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 54px;
    letter-spacing: -0.02em; line-height: 1.08; color: #fff;
    max-width: 780px; margin: 0 auto 22px; text-wrap: balance;
  }}
  .pco-hero__lead {{
    font-size: 18px; line-height: 1.7; color: #d4c9f0;
    max-width: 600px; margin: 0 auto 36px;
  }}
  .pco-hero__btns {{ display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }}

  /* ── shared layout ── */
  .pco-section {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .pco-eyebrow {{
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--purple); margin-bottom: 12px;
  }}
  .pco-h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 42px;
    letter-spacing: -0.018em; line-height: 1.1; color: #1C1633;
    margin-bottom: 20px; text-wrap: balance;
  }}
  .pco-body {{ font-size: 16.5px; line-height: 1.78; color: #56526A; margin-bottom: 18px; }}

  /* ── welcome: 3 pillars ── */
  .pco-welcome {{ background: var(--off-white); border-bottom: 1px solid var(--border); }}
  .pco-welcome-inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .pco-pillars {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; margin-top: 52px; }}
  .pco-pillar {{
    background: #fff; border: 1px solid var(--border-card);
    border-radius: 18px; padding: 36px 30px;
  }}
  .pco-pillar__icon {{
    width: 44px; height: 44px; border-radius: 50%;
    background: var(--lavender-bg); display: flex; align-items: center;
    justify-content: center; margin-bottom: 18px;
    font-size: 20px;
  }}
  .pco-pillar__h3 {{
    font-family: 'Newsreader', serif; font-weight: 600; font-size: 22px;
    color: #1C1633; margin-bottom: 10px;
  }}
  .pco-pillar__p {{ font-size: 15px; line-height: 1.72; color: #56526A; }}

  /* ── patient care: 2-col ── */
  .pco-split {{
    max-width: 1200px; margin: 0 auto; padding: 88px 40px;
    display: grid; gap: 64px; align-items: center;
  }}
  .pco-split--2col {{ grid-template-columns: 1fr 1fr; }}
  .pco-split__img {{ width: 100%; border-radius: 20px; object-fit: cover; height: 460px; display: block; }}

  /* ── tagline trio ── */
  .pco-tagline-trio {{
    display: flex; gap: 0; margin: 28px 0 36px;
  }}
  .pco-tagline-trio span {{
    font-size: 14px; font-weight: 600; color: var(--purple);
    padding-right: 18px; margin-right: 18px;
    border-right: 1.5px solid var(--border);
  }}
  .pco-tagline-trio span:last-child {{ border-right: none; padding-right: 0; margin-right: 0; }}

  /* ── 9-benefit grid ── */
  .pco-benefits-bg {{ background: var(--ink); }}
  .pco-benefits-inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .pco-benefits-header {{ margin-bottom: 52px; }}
  .pco-benefits-header .pco-eyebrow {{ color: #c3aef0; }}
  .pco-benefits-header .pco-h2 {{ color: #fff; }}
  .pco-benefits-grid {{
    display: grid; grid-template-columns: repeat(3,1fr); gap: 20px;
  }}
  .pco-benefit-card {{
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px; padding: 28px 24px;
  }}
  .pco-benefit-card__h3 {{
    font-family: 'Newsreader', serif; font-weight: 600; font-size: 18px;
    color: #fff; margin-bottom: 10px;
  }}
  .pco-benefit-card__p {{ font-size: 14.5px; line-height: 1.68; color: #c9c3e0; }}

  /* ── community care: 3 cards ── */
  .pco-community-bg {{ background: var(--off-white); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
  .pco-community-inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .pco-community-intro {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px;
    align-items: center; margin-bottom: 56px;
  }}
  .pco-community-cards {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }}
  .pco-community-card {{ background: #fff; border: 1px solid var(--border-card); border-radius: 18px; overflow: hidden; }}
  .pco-community-card__img {{ width: 100%; height: 200px; object-fit: cover; display: block; }}
  .pco-community-card__body {{ padding: 26px 24px 28px; }}
  .pco-community-card__h3 {{
    font-family: 'Newsreader', serif; font-weight: 600; font-size: 20px;
    color: #1C1633; margin-bottom: 10px;
  }}
  .pco-community-card__p {{ font-size: 14.5px; line-height: 1.68; color: #56526A; }}

  /* ── benefits + leadership: 2-col info ── */
  .pco-info-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px;
    max-width: 1200px; margin: 0 auto; padding: 88px 40px;
  }}
  .pco-info-col__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 34px;
    letter-spacing: -0.015em; color: #1C1633; margin-bottom: 16px; line-height: 1.15;
  }}
  .pco-info-col__lead {{ font-size: 16px; line-height: 1.75; color: #56526A; margin-bottom: 28px; }}
  .pco-bullets {{ list-style: none; display: flex; flex-direction: column; gap: 18px; }}
  .pco-bullets li {{ display: flex; gap: 14px; align-items: flex-start; }}
  .pco-bullets li::before {{
    content: ''; width: 7px; height: 7px; border-radius: 50%;
    background: var(--purple); flex-shrink: 0; margin-top: 8px;
  }}
  .pco-bullets li strong {{ color: #1C1633; display: block; margin-bottom: 3px; font-size: 15px; }}
  .pco-bullets li span {{ font-size: 14.5px; line-height: 1.68; color: #56526A; }}

  /* ── final CTA band ── */
  .pco-cta-band {{ background: var(--purple); }}
  .pco-cta-band__inner {{
    max-width: 1200px; margin: 0 auto; padding: 60px 40px;
    display: flex; align-items: center; justify-content: space-between; gap: 32px; flex-wrap: wrap;
  }}
  .pco-cta-band__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 34px;
    line-height: 1.2; color: #fff; max-width: 600px; text-wrap: balance;
  }}

  @media (max-width: 900px) {{
    .pco-hero__h1 {{ font-size: 36px; }}
    .pco-pillars, .pco-benefits-grid, .pco-community-cards {{ grid-template-columns: 1fr; }}
    .pco-split--2col, .pco-community-intro, .pco-info-grid {{ grid-template-columns: 1fr; gap: 36px; }}
    .pco-section, .pco-welcome-inner, .pco-benefits-inner,
    .pco-community-inner, .pco-info-grid, .pco-split {{ padding: 56px 24px; }}
    .pco-hero__inner {{ padding: 72px 24px; }}
  }}
</style>
</head>
<body>
{HEADER}

<!-- HERO -->
<div class="pco-hero">
  <div class="pco-hero__inner">
    <h1 class="pco-hero__h1">Reenvision Your Career as a Community Specialist</h1>
    <p class="pco-hero__lead">Whether you&rsquo;re seeking to expand your expertise, take on a leadership role, or establish long-term stability in your career, Premier Hematology &amp; Oncology provides the support and opportunities to help you thrive.</p>
    <div class="pco-hero__btns">
      <a href="#benefits" class="btn btn--white btn--lg">Learn How &rarr;</a>
      <a href="/contact/" class="btn btn--lg" style="background:rgba(255,255,255,0.15);border:1.5px solid rgba(255,255,255,0.4);color:#fff;">Contact Us</a>
    </div>
  </div>
</div>

<!-- WELCOME -->
<div class="pco-welcome">
  <div class="pco-welcome-inner">
    <div class="pco-eyebrow">Join Our Team</div>
    <h2 class="pco-h2">Welcome to Premier Hematology &amp; Oncology</h2>
    <p class="pco-body" style="max-width:820px;">Welcome to Premier Hematology and Oncology, a multi-site practice committed to bringing top-tier Hematology and Oncology services directly to the community in the New York area. As an established and growing leader, we provide a unique opportunity for physicians who want to focus on quality over quantity, offering personalized, patient-centered care without the bureaucracy of large hospital systems. Whether you&rsquo;re seeking to expand your expertise, take on a leadership role, or establish long-term stability in your career, Premier Hematology &amp; Oncology provides the support and opportunities to help you thrive.</p>
    <div class="pco-pillars">
      <div class="pco-pillar">
        <div class="pco-pillar__icon">&#9650;</div>
        <h3 class="pco-pillar__h3">Empower</h3>
        <p class="pco-pillar__p">We empower our physicians with clinical autonomy, healthy work-life balance, and a collaborative work environment.</p>
      </div>
      <div class="pco-pillar">
        <div class="pco-pillar__icon">&#11088;</div>
        <h3 class="pco-pillar__h3">Elevate</h3>
        <p class="pco-pillar__p">We elevate our care quality with state-of-the-art facilities, modern infusion centers, and streamlined administrative support.</p>
      </div>
      <div class="pco-pillar">
        <div class="pco-pillar__icon">&#127807;</div>
        <h3 class="pco-pillar__h3">Grow</h3>
        <p class="pco-pillar__p">We offer a competitive financial package, comprehensive benefits, and clear pathways for professional growth and leadership.</p>
      </div>
    </div>
  </div>
</div>

<!-- BETTER PATIENT CARE — text left, image right -->
<div class="pco-split pco-split--2col">
  <div>
    <div class="pco-eyebrow">Our Mission</div>
    <h2 class="pco-h2">Better Patient Care Starts with You.</h2>
    <p class="pco-body"><strong>We are committed</strong> to recruiting physicians who embody our dedication to high-quality care and patient well-being.</p>
    <p class="pco-body"><strong>As a member of our team</strong>, you will play a crucial role in expanding access to exceptional Hematology and Oncology services, bringing compassionate, community-based care to those who need it most.</p>
    <p class="pco-body">We provide a supportive, collaborative environment that encourages professional growth, teamwork, and the delivery of meaningful patient experiences.</p>
    <p class="pco-body">Join us and be part of a group of dedicated professionals who value your expertise and are passionate about making a positive impact on patient lives.</p>
    <a href="/contact/" class="btn" style="margin-top:8px;">Contact Us &rarr;</a>
  </div>
  <div>
    <img class="pco-split__img" src="{WP_IMG}2024/04/nurse-care.webp" alt="Premier Hematology physician with patient">
  </div>
</div>

<!-- EXPERT CARE — dark bg, 9-benefit grid -->
<div class="pco-benefits-bg" id="benefits">
  <div class="pco-benefits-inner">
    <div class="pco-benefits-header">
      <div class="pco-eyebrow">Why Join Us</div>
      <h2 class="pco-h2">Expert Care Tailored to Every Patient.</h2>
      <p class="pco-body" style="color:#c9c3e0;max-width:760px;">At Premier Hematology &amp; Oncology, we invite you to redefine your clinical practice by focusing on quality over quantity. Our practice offers a unique setting designed for physicians who value a calmer work environment and a greater ability to deliver personalized, high-quality care.</p>
      <div class="pco-tagline-trio">
        <span>Quality &amp; Compassion</span>
        <span>Flexibility &amp; Independence</span>
        <span>Care that Makes a Difference</span>
      </div>
    </div>
    <div class="pco-benefits-grid">
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Patient-Centered Care</h3>
        <p class="pco-benefit-card__p">Transform patient outcomes with thorough, individualized treatment protocols.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Focused Environment</h3>
        <p class="pco-benefit-card__p">Escape high-pressure, high-volume models. A work culture where quality time with patients is prioritized over rapid throughput.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Collaborative Culture</h3>
        <p class="pco-benefit-card__p">Open communication and collaboration lead to excellence in clinical care.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Clinical Independence</h3>
        <p class="pco-benefit-card__p">Deliver patient-centered care guided by your expertise &mdash; free from the constraints and pressures of larger systems.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Telehealth Integration</h3>
        <p class="pco-benefit-card__p">Leverage telehealth tools that empower you to see patients remotely, offering flexibility that fits your lifestyle and enhances patient access.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Work-Life Balance</h3>
        <p class="pco-benefit-card__p">Enjoy a predictable schedule with fewer administrative burdens, allowing you to focus on patient care while maintaining personal time and well-being.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">Quality Over Quantity</h3>
        <p class="pco-benefit-card__p">Enjoy meaningful patient encounters, allowing stronger doctor&ndash;patient relationships and delivering comprehensive care.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">State-of-the-Art Facilities</h3>
        <p class="pco-benefit-card__p">Work in modern, purpose-built facilities designed to support advanced diagnostic and treatment services.</p>
      </div>
      <div class="pco-benefit-card">
        <h3 class="pco-benefit-card__h3">No Red Tape</h3>
        <p class="pco-benefit-card__p">Experience streamlined processes and integrated technologies that let you concentrate on what truly matters &mdash; patient care.</p>
      </div>
    </div>
  </div>
</div>

<!-- COMMUNITY CARE -->
<div class="pco-community-bg">
  <div class="pco-community-inner">
    <div class="pco-community-intro">
      <div>
        <div class="pco-eyebrow">Community Practice</div>
        <h2 class="pco-h2">The Benefits of Community Care</h2>
        <p class="pco-body">Practicing in the community gives physicians the freedom to practice medicine without hospital bureaucracy. With full clinical autonomy, seamless specialist collaboration, and fewer administrative burdens, you can focus on patient care &mdash; not quotas.</p>
      </div>
      <div>
        <img src="{WP_IMG}2024/04/care.webp" alt="Healthcare provider with patient" style="width:100%;border-radius:20px;height:340px;object-fit:cover;display:block;">
      </div>
    </div>
    <div class="pco-community-cards">
      <div class="pco-community-card">
        <img class="pco-community-card__img" src="{WP_IMG}2024/04/experience.webp" alt="Hematology lab">
        <div class="pco-community-card__body">
          <h3 class="pco-community-card__h3">Clinical Autonomy</h3>
          <p class="pco-community-card__p">Practicing in the community offers more personalized, continuous care and stronger patient relationships, unhindered by the fast-paced and often fragmented environment of a hospital.</p>
        </div>
      </div>
      <div class="pco-community-card">
        <img class="pco-community-card__img" src="{WP_IMG}2024/04/nurse.webp" alt="Nurse with patient">
        <div class="pco-community-card__body">
          <h3 class="pco-community-card__h3">Professional Connections</h3>
          <p class="pco-community-card__p">Be a part of a local network of physicians building strong, collaborative relationships, fostering camaraderie and facilitating open communication, referrals, and shared knowledge that enhances patient care.</p>
        </div>
      </div>
      <div class="pco-community-card">
        <img class="pco-community-card__img" src="{WP_IMG}2024/04/consult-1.png" alt="Physician consultation">
        <div class="pco-community-card__body">
          <h3 class="pco-community-card__h3">Patient Relationships</h3>
          <p class="pco-community-card__p">Natural collaboration streamlines patient management while fostering meaningful professional relationships that enhance your practice.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- BENEFITS + LEADERSHIP — 2 col -->
<div class="pco-info-grid">
  <div class="pco-info-col">
    <h2 class="pco-info-col__h2">Competitive &amp; Comprehensive Benefits Package</h2>
    <p class="pco-info-col__lead">Our compensation structure is designed to acknowledge your expertise, experience, and the passion you bring to patient care. Along with competitive pay, we offer a range of benefits tailored to your personal and professional needs.</p>
    <ul class="pco-bullets">
      <li>
        <span>
          <strong>Comprehensive Coverage</strong>
          Medical, dental, and vision plans to safeguard your health and well-being.
        </span>
      </li>
      <li>
        <span>
          <strong>Retirement Savings</strong>
          Access to retirement programs that help build a solid financial future.
        </span>
      </li>
      <li>
        <span>
          <strong>Wellness Benefits</strong>
          Additional perks focused on work-life balance and overall personal wellness.
        </span>
      </li>
    </ul>
  </div>
  <div class="pco-info-col">
    <h2 class="pco-info-col__h2">Leadership &amp; Growth Opportunities</h2>
    <p class="pco-info-col__lead">We encourage leadership development and provide clear pathways for those looking to expand their skills, grow within the organization, and make a lasting impact on our practice and the patients we serve.</p>
    <ul class="pco-bullets">
      <li>
        <span>
          <strong>Practice Expansion</strong>
          A growing network that creates new avenues for patient care and physician collaboration.
        </span>
      </li>
      <li>
        <span>
          <strong>Personalized Development</strong>
          Ongoing support for continued education and skill enhancement.
        </span>
      </li>
      <li>
        <span>
          <strong>Long-Term Investment</strong>
          Our practice recognizes your contributions and invests in your sustained growth.
        </span>
      </li>
    </ul>
  </div>
</div>

<!-- FINAL CTA BAND -->
<div class="pco-cta-band">
  <div class="pco-cta-band__inner">
    <h2 class="pco-cta-band__h2">Ready to Reenvision Your Career? Let&rsquo;s Talk.</h2>
    <a href="/contact/" class="btn btn--white btn--lg">Contact Us &rarr;</a>
  </div>
</div>

{FOOTER}
</body>
</html>""")

# Infusion Suites
write("infusions-suites/index.html", service_page(
    slug="infusions-suites",
    title="Infusion Suites | Premier Hematology",
    yoast_title="Infusion Suites | Premier Hematology & Oncology",
    meta_desc="Premier Hematology offers state-of-the-art infusion suites designed for comfort and efficiency.",
    eyebrow="Your Hematology Care Experts",
    h1="Infusion Suites",
    lead="Better treatment options to fit your lifestyle.",
    body_paras=[
        "Patients who need ongoing infusion or injection treatment deserve better options for when, where and how they receive care. Visit any of our conveniently located infusion centers to receive expert care from our board-certified physicians and registered nurses.",
        "<strong>Drugs Available:</strong> Actemra, Benlysta, Cerezyme, Cimzia, Cinqair, Crysvita, Entyvio, Fabrazyme, Fasenra, Feraheme, Ilumya, Inflectra, Injectafer, IVIG, Krystexxa, Lemtrada, Lumizyme, Nucala, Nulojix, Orencia, Prolastin-C, Remicade, Renflexis, Rituxan, Simponi Aria, Soliris, Solu-Medrol, Stelara IV, Stelara SQ, Tepezza, Thyrogen, Tysabri, Venofer, Vyepti",
        "<strong>Custom-Tailored Experience</strong><br>Our center is comfortable, private and flexible so you can heal on your own terms and availability. From the moment you enter our doors, you'll be greeted with a warm smile from a caring team that will work to understand your needs, answer all your questions, and connect you with the right care.",
        "<strong>Convenient Locations</strong><br>Located in the communities where people live and work, Premier Hematology serves those with complex chronic conditions by delivering high-quality, personalized care in a private, comfortable setting so patients can access the care they need.",
        "Patients are our number one priority. Premier Hematology was founded on the premise that optimizing infusion site of care is more effective, less expensive, easier for physicians, and most importantly, better for patients.",
    ],
    bullets=["Private infusion bays", "Comfortable recliners and entertainment", "Attentive RN staff at all times", "On-site lab for real-time monitoring", "Next-day appointment availability"],
    facts=[("Locations", "a broad network of convenient locations throughout NY"), ("Privacy", "Private bays"), ("Appointments", "Next-day")],
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
    meta_desc="Review Premier Hematology's HIPAA Privacy Policy — how we use, disclose, and protect your protected health information.",
    h1="Privacy Policy",
    lead="This notice describes how medical information about you may be used and disclosed and how you can get access to this information. Please review it carefully.",
    body_html="""    <div style="max-width:760px;font-size:16px;line-height:1.8;color:#43405a;">

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Our Commitment to Your Privacy</h2>
      <p style="margin-bottom:16px;">It is our duty to maintain the privacy and confidentiality of your protected health information (PHI). We will create records regarding you and the treatment and services we provide to you. We are required by law to maintain the privacy of your PHI, which includes any individually identifiable information that we obtain from you or others that relates to your past, present or future physical or mental health, the health care you have received, or payment for your health care. We will share protected health information with one another, as necessary, to carry out treatment, payment or health care operations relating to the services to be rendered at the company.</p>
      <p style="margin-bottom:16px;">As required by law, this notice provides you with information about your rights and our legal duties and privacy practices with respect to the privacy of PHI. This notice also discusses the uses and disclosures we will make of your PHI. We must comply with the provisions of this notice as currently in effect, although we reserve the right to change the terms of this notice from time to time and to make the revised notice effective for all PHI we maintain. You can always request a written copy of our most current privacy notice from our Privacy Officer.</p>

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Permitted Uses and Disclosures</h2>
      <p style="margin-bottom:16px;">We can use or disclose your PHI for purposes of treatment, payment and health care operations. For each of these categories of uses and disclosures, we have provided a description and an example below. However, not every particular use or disclosure in every category will be listed.</p>
      <p style="margin-bottom:16px;"><strong style="color:#1C1633;">Treatment</strong> means providing services as ordered by your physician. Treatment also includes coordination and consultations with other health care providers relating to your care and referrals for health care from one health care provider to another. We may also disclose PHI to outside entities performing other services related to your treatment such as hospital, diagnostic laboratories, home health or hospice agencies, etc.</p>
      <p style="margin-bottom:16px;"><strong style="color:#1C1633;">Payment</strong> means the activities we undertake to obtain reimbursement for the health care provided to you, including billing, collections, claims management, prior approval, determinations of eligibility and coverage and other utilization review activities. Federal or state law may require us to obtain a written release from you prior to disclosing certain specially protected PHI for payment purposes, and we will ask you to sign a release when necessary under applicable law.</p>
      <p style="margin-bottom:16px;"><strong style="color:#1C1633;">Health care operations</strong> means the support functions of the company, related to treatment and payment, such as quality assurance activities, case management, receiving and responding to patient comments and complaints, physician reviews, compliance programs, audits, business planning, development, management and administrative activities. We may use your PHI to evaluate the performance of our staff when caring for you. We may also combine PHI about many patients to decide what additional services we should offer, what services are not needed, and whether certain new treatments are effective. We may also disclose PHI for review and learning purposes. In addition, we may remove information that identifies you so that others can use the de-identified information to study health care and health care delivery without learning who you are.</p>

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Other Uses and Disclosures of Protected Health Information</h2>
      <p style="margin-bottom:12px;">We may also use your PHI in the following ways:</p>
      <ul style="margin:0 0 16px 24px;display:flex;flex-direction:column;gap:10px;">
        <li>To provide appointment reminders for treatment or medical care.</li>
        <li>To tell you about or recommend possible treatment alternatives or other health-related benefits and services that may be of interest to you.</li>
        <li>To disclose to your family or friends or any other individual identified by you to the extent directly related to such person's involvement in your care or the payment for your care. We may use or disclose your PHI to notify, or assist in the notification of, a family member, a personal representative, or another person responsible for your care, of your location, general condition or death. If you are available, we will give you an opportunity to object to these disclosures, and we will not make these disclosures if you object. If you are not available, we will determine whether a disclosure to your family or friends is in your best interest, taking into account the circumstances and based upon our professional judgment.</li>
        <li>When permitted by law, we may coordinate our uses and disclosures of PHI with public or private entities authorized by law or by charter to assist in disaster relief efforts.</li>
      </ul>
      <p style="margin-bottom:16px;">We will allow your family and friends to act on your behalf to pick up filled prescriptions, medical supplies, X-rays, and similar forms of PHI, when we determine, in our professional judgment that it is in your best interest to make such disclosures.</p>
      <p style="margin-bottom:16px;">We may contact you as part of our fundraising and marketing efforts as permitted by applicable law. You have the right to opt out of receiving such fundraising communications.</p>
      <p style="margin-bottom:16px;">We may use or disclose your PHI for research purposes, subject to the requirements of applicable law. For example, a research project may involve comparisons of the health and recovery of all patients who received a particular medication. All research projects are subject to a special approval process which balances research needs with a patient's need for privacy. When required, we will obtain a written authorization from you prior to using your health information for research.</p>
      <p style="margin-bottom:16px;">We will use or disclose PHI about you when required to do so by applicable law.</p>
      <p style="margin-bottom:16px;">In accordance with applicable law, we may disclose your PHI to your employer if we are retained to conduct an evaluation relating to medical surveillance of your workplace or to evaluate whether you have a work-related illness or injury. You will be notified of these disclosures by your employer or the company as required by applicable law.</p>
      <p style="margin-bottom:16px;padding:16px 20px;background:#f7f5fc;border-left:3px solid var(--purple);border-radius:6px;"><em>Note: incidental uses and disclosures of PHI sometimes occur and are not considered to be a violation of your rights. Incidental uses and disclosures are by-products of otherwise permitted uses or disclosures which are limited in nature and cannot be reasonably prevented.</em></p>

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Special Situations</h2>
      <p style="margin-bottom:16px;">Subject to the requirements of applicable law, we will make the following uses and disclosures of your PHI:</p>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Organ and Tissue Donation.</strong> If you are an organ donor, we may release PHI to organizations that handle organ procurement or transplantation as necessary to facilitate organ or tissue donation and transplantation.</p>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Military and Veterans.</strong> If you are a member of the Armed Forces, we may release PHI about you as required by military command authorities. We may also release PHI about foreign military personnel to the appropriate foreign military authority.</p>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Worker's Compensation.</strong> We may release PHI about you for programs that provide benefits for work-related injuries or illnesses.</p>
      <p style="margin-bottom:8px;"><strong style="color:#1C1633;">Public Health Activities.</strong> We may disclose PHI about you for public health activities, including disclosures:</p>
      <ul style="margin:0 0 16px 24px;display:flex;flex-direction:column;gap:8px;">
        <li>to prevent or control disease, injury or disability;</li>
        <li>to report births and deaths;</li>
        <li>to report child abuse or neglect;</li>
        <li>to persons subject to the jurisdiction of the Food and Drug Administration (FDA) for activities related to the quality, safety, or effectiveness of FDA-regulated products or services and to report reactions to medications or problems with products;</li>
        <li>to notify a person who may have been exposed to a disease or may be at risk for contracting or spreading a disease or condition;</li>
        <li>to notify the appropriate government authority if we believe that an adult patient has been the victim of abuse, neglect or domestic violence. We will only make this disclosure if the patient agrees or when required or authorized by law.</li>
      </ul>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Health Oversight Activities.</strong> We may disclose PHI to federal or state agencies that oversee our activities (e.g., providing health care, seeking payment, and civil rights).</p>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Lawsuits and Disputes.</strong> If you are involved in a lawsuit or a dispute, we may disclose PHI subject to certain limitations.</p>
      <p style="margin-bottom:8px;"><strong style="color:#1C1633;">Law Enforcement.</strong> We may release PHI if asked to do so by a law enforcement official:</p>
      <ul style="margin:0 0 16px 24px;display:flex;flex-direction:column;gap:8px;">
        <li>In response to a court order, warrant, summons or similar process;</li>
        <li>To identify or locate a suspect, fugitive, material witness, or missing person;</li>
        <li>About the victim of a crime under certain limited circumstances;</li>
        <li>About a death we believe may be the result of criminal conduct;</li>
        <li>About criminal conduct on our premises; or</li>
        <li>In emergency circumstances, to report a crime, the location of the crime or the victims, or the identity, description or location of the person who committed the crime.</li>
      </ul>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Coroners, Medical Examiners and Funeral Directors.</strong> We may release PHI to a coroner or medical examiner. We may also release PHI about patients to funeral directors as necessary to carry out their duties.</p>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">National Security and Intelligence Activities.</strong> We may release PHI about you to authorized federal officials for intelligence, counterintelligence, other national security activities authorized by law or to authorized federal officials so they may provide protection to the President or foreign heads of state.</p>
      <p style="margin-bottom:12px;"><strong style="color:#1C1633;">Inmates.</strong> If you are an inmate of a correctional institution or under the custody of a law enforcement official, we may release PHI about you to the correctional institution or law enforcement official. This release would be necessary (1) to provide you with health care; (2) to protect your health and safety or the health and safety of others; or (3) for the safety and security of the correctional institution.</p>
      <p style="margin-bottom:16px;"><strong style="color:#1C1633;">Serious Threats.</strong> As permitted by applicable law and standards of ethical conduct, we may use and disclose PHI if we, in good faith, believe that the use or disclosure is necessary to prevent or lessen a serious and imminent threat to the health or safety of a person or the public or is necessary for law enforcement authorities to identify or apprehend an individual.</p>
      <p style="margin-bottom:16px;padding:16px 20px;background:#f7f5fc;border-left:3px solid var(--purple);border-radius:6px;"><em>Note: HIV-related information, genetic information, alcohol and/or substance abuse records, mental health records and other specially protected health information may enjoy certain special confidentiality protections under applicable state and federal law. Any disclosures of these types of records will be subject to these special protections.</em></p>

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Other Uses of Your Health Information</h2>
      <p style="margin-bottom:16px;">Certain uses and disclosures of PHI will be made only with your written authorization, including uses and/or disclosures: (a) of psychotherapy notes (where appropriate); (b) for marketing purposes; and (c) that constitute a sale of PHI under the Privacy Rule. Other uses and disclosures of PHI not covered by this notice or the laws that apply to us will be made only with your written authorization. You have the right to revoke that authorization at any time, provided that the revocation is in writing, except to the extent that we already have taken action in reliance on your authorization.</p>

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Your Rights</h2>
      <p style="margin-bottom:16px;">You have the right to request restrictions on our uses and disclosures of PHI for treatment, payment and health care operations. However, we are not required to agree to your request unless the disclosure is to a health plan in order to receive payment, the PHI pertains solely to your health care items or services for which you have paid the bill in full, and the disclosure is not otherwise required by law. To request a restriction, you may make your request in writing to the Privacy Officer.</p>
      <p style="margin-bottom:16px;">You have the right to reasonably request to receive confidential communications of your PHI by alternative means or at alternative locations. To make such a request, you may submit your request in writing to the Privacy Officer.</p>
      <p style="margin-bottom:8px;">You have the right to inspect and copy the PHI contained in our company records, except:</p>
      <ul style="margin:0 0 16px 24px;display:flex;flex-direction:column;gap:8px;">
        <li>for psychotherapy notes, (i.e., notes that have been recorded by a mental health professional documenting counseling sessions and have been separated from the rest of your medical record);</li>
        <li>for information compiled in reasonable anticipation of, or for use in, a civil, criminal, or administrative action or proceeding;</li>
        <li>for PHI involving laboratory tests when your access is restricted by law;</li>
        <li>if you are a prison inmate, and access would jeopardize your health, safety, security, custody, or rehabilitation or that of other inmates, any officer, employee, or other person at the correctional institution or person responsible for transporting you;</li>
        <li>if we obtained or created PHI as part of a research study, your access to the PHI may be restricted for as long as the research is in progress, provided that you agreed to the temporary denial of access when consenting to participate in the research;</li>
        <li>for PHI contained in records kept by a federal agency or contractor when your access is restricted by law; and</li>
        <li>for PHI obtained from someone other than us under a promise of confidentiality when the access requested would be reasonably likely to reveal the source of the information.</li>
      </ul>
      <p style="margin-bottom:16px;">In order to inspect or obtain a copy of your PHI, you may submit your request in writing to the Medical Records Custodian. If you request a copy, we may charge you a fee for the costs of copying and mailing your records, as well as other costs associated with your request.</p>
      <p style="margin-bottom:16px;">We may also deny a request for access to PHI under certain circumstances if there is a potential for harm to yourself or others. If we deny a request for access for this purpose, you have the right to have our denial reviewed in accordance with the requirements of applicable law.</p>
      <p style="margin-bottom:8px;">You have the right to request an amendment to your PHI but we may deny your request for amendment, if we determine that the PHI or record that is the subject of the request:</p>
      <ul style="margin:0 0 16px 24px;display:flex;flex-direction:column;gap:8px;">
        <li>was not created by us, unless you provide a reasonable basis to believe that the originator of PHI is no longer available to act on the requested amendment;</li>
        <li>is not part of your medical or billing records or other records used to make decisions about you;</li>
        <li>is not available for inspection as set forth above; or</li>
        <li>is accurate and complete.</li>
      </ul>
      <p style="margin-bottom:16px;">In any event, any agreed upon amendment will be included as an addition to, and not a replacement of, already existing records. In order to request an amendment to your PHI, you must submit your request in writing to the Medical Record Custodian at our company, along with a description of the reason for your request.</p>
      <p style="margin-bottom:8px;">You have the right to receive an accounting of disclosures of PHI made by us to individuals or entities other than to you for the six years prior to your request, except for disclosures:</p>
      <ul style="margin:0 0 16px 24px;display:flex;flex-direction:column;gap:8px;">
        <li>to carry out treatment, payment and health care operations as provided above;</li>
        <li>incidental to a use or disclosure otherwise permitted or required by applicable law;</li>
        <li>pursuant to your written authorization;</li>
        <li>to persons involved in your care or for other notification purposes as provided by law;</li>
        <li>for national security or intelligence purposes as provided by law;</li>
        <li>to correctional institutions or law enforcement officials as provided by law;</li>
        <li>as part of a limited data set as provided by law.</li>
      </ul>
      <p style="margin-bottom:16px;">To request an accounting of disclosures of your PHI, you must submit your request in writing to the Privacy Officer at our company. Your request must state a specific time period for the accounting (e.g., the past three months). The first accounting you request within a twelve (12) month period will be free. For additional accountings, we may charge you for the costs of providing the list. We will notify you of the costs involved, and you may choose to withdraw or modify your request at that time before any costs are incurred.</p>
      <p style="margin-bottom:16px;">You have the right to receive a notification, in the event that there is a breach of your unsecured PHI, which requires notification under the Privacy Rule.</p>

      <h2 style="font-family:'Newsreader',serif;font-size:24px;color:#1C1633;margin:40px 0 12px;letter-spacing:-.01em;">Complaints</h2>
      <p style="margin-bottom:16px;">If you believe that your privacy rights have been violated, you should immediately contact the company's Privacy Officer. We will not take action against you for filing a complaint. You also may file a complaint with the Secretary of the U.S. Department of Health and Human Services, 200 Independence Ave. S.W., Washington DC, 20201.</p>

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

# ---------------------------------------------------------------------------
# energy-boost-heavy-periods — full content page matching WP original
# ---------------------------------------------------------------------------
write("energy-boost-heavy-periods/index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Heavy Periods & Iron Deficiency | Premier Hematology", "Heavy periods are the leading cause of iron deficiency. Premier Hematology offers next-day consultations and personalized iron infusion therapy covered by most insurance plans.")}
<style>
  .eb-insurance-bar {{
    background: var(--purple); color: #fff;
    text-align: center; padding: 11px 20px;
    font-size: 13.5px; font-weight: 600; letter-spacing: 0.06em;
  }}
  .eb-hero {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px 72px;
    display: grid; grid-template-columns: 1.1fr 1fr; gap: 64px; align-items: center;
  }}
  .eb-hero__h1 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 48px;
    line-height: 1.06; letter-spacing: -0.02em; color: var(--ink); margin-bottom: 20px;
  }}
  .eb-hero__lead {{
    font-size: 17px; line-height: 1.7; color: var(--body); margin-bottom: 26px; max-width: 480px;
  }}
  .eb-hero__imgs {{ display: flex; flex-direction: column; gap: 14px; }}
  .eb-hero__img {{ width: 100%; border-radius: 18px; object-fit: cover; display: block; }}
  .eb-hero__img--top {{ height: 260px; }}
  .eb-hero__img--bottom {{ height: 220px; }}
  .eb-hero__testimonial {{
    margin-top: 28px; padding: 18px 22px;
    background: var(--lavender-bg); border-radius: 14px;
    border-left: 3px solid var(--purple);
  }}
  .eb-hero__testimonial p {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 15.5px; line-height: 1.55; color: var(--ink); margin-bottom: 8px;
  }}
  .eb-hero__testimonial cite {{ font-size: 13px; font-weight: 600; color: var(--purple); font-style: normal; }}
  .eb-split {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px;
    display: grid; gap: 64px; align-items: center;
  }}
  .eb-split--img-right {{ grid-template-columns: 1fr 1fr; }}
  .eb-split--img-left  {{ grid-template-columns: 1fr 1fr; }}
  .eb-split__img {{ width: 100%; border-radius: 20px; object-fit: cover; display: block; height: 440px; }}
  .eb-split__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 38px;
    line-height: 1.12; letter-spacing: -0.015em; color: var(--ink); margin-bottom: 18px;
  }}
  .eb-split__body {{ font-size: 16.5px; line-height: 1.75; color: var(--body); margin-bottom: 18px; }}
  .eb-dark {{ background: var(--ink); }}
  .eb-dark__inner {{
    max-width: 1200px; margin: 0 auto; padding: 80px 40px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
  }}
  .eb-dark__img {{ width: 100%; border-radius: 20px; object-fit: cover; display: block; height: 440px; }}
  .eb-dark__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 38px;
    line-height: 1.12; color: #fff; margin-bottom: 18px;
  }}
  .eb-dark__body {{ font-size: 16px; line-height: 1.75; color: #c9c3e0; margin-bottom: 24px; }}
  .eb-dark .checklist__check {{ background: rgba(255,255,255,0.12); color: #fff; border: none; }}
  .eb-dark .checklist__text {{ color: #c9c3e0; }}
  .eb-how {{ background: var(--off-white); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
  .eb-how__inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-how__header {{ text-align: center; margin-bottom: 56px; }}
  .eb-how__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 14px;
  }}
  .eb-how__lead {{ font-size: 17px; line-height: 1.65; color: var(--body); max-width: 560px; margin: 0 auto; }}
  .eb-how__grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 28px; margin-bottom: 44px; }}
  .eb-step-card {{ background: #fff; border: 1px solid var(--border-card); border-radius: 20px; overflow: hidden; }}
  .eb-step-card__img {{ width: 100%; height: 190px; object-fit: cover; display: block; }}
  .eb-step-card__body {{ padding: 28px 26px 30px; }}
  .eb-step-card__num {{
    font-family: 'Newsreader', serif; font-style: italic; font-size: 28px;
    color: var(--step-numeral); margin-bottom: 8px; line-height: 1;
  }}
  .eb-step-card__title {{ font-family: 'Newsreader', serif; font-weight: 600; font-size: 20px; color: var(--ink); margin-bottom: 10px; }}
  .eb-step-card__desc {{ font-size: 14.5px; line-height: 1.65; color: var(--body-muted); }}
  .eb-cta-band {{ max-width: 1200px; margin: 0 auto; padding: 80px 40px; }}
  .eb-cta-band__inner {{
    background: linear-gradient(110deg, var(--purple), var(--purple-deep));
    border-radius: 22px; padding: 52px 56px;
    display: flex; align-items: center; justify-content: space-between; gap: 32px;
  }}
  .eb-cta-band__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 36px;
    line-height: 1.2; color: #fff; max-width: 560px;
  }}
  .eb-reviews {{ background: var(--off-white); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
  .eb-reviews__inner {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-reviews__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 40px; text-align: center;
  }}
  .eb-reviews__grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }}
  .eb-review-card {{ background: #fff; border: 1px solid var(--border-card); border-radius: 18px; padding: 28px 26px; }}
  .eb-review-card__stars {{ color: #f59e0b; font-size: 17px; margin-bottom: 14px; letter-spacing: 2px; }}
  .eb-review-card__quote {{
    font-family: 'Newsreader', serif; font-style: italic;
    font-size: 16px; line-height: 1.65; color: var(--ink); margin-bottom: 18px;
  }}
  .eb-review-card__name {{ font-size: 13.5px; font-weight: 600; color: var(--purple); }}
  .eb-faq {{ max-width: 1200px; margin: 0 auto; padding: 88px 40px; }}
  .eb-faq__grid {{ display: grid; grid-template-columns: 360px 1fr; gap: 72px; align-items: start; }}
  .eb-faq__h2 {{
    font-family: 'Newsreader', serif; font-weight: 500; font-size: 40px;
    letter-spacing: -0.015em; color: var(--ink); margin-bottom: 28px;
  }}
  .eb-faq__img {{ width: 100%; border-radius: 18px; object-fit: cover; height: 320px; display: block; }}
  .eb-faq__item {{ padding: 22px 0; border-bottom: 1px solid var(--border); }}
  .eb-faq__item:first-child {{ padding-top: 0; }}
  .eb-faq__q {{ font-family: 'Newsreader', serif; font-weight: 600; font-size: 18px; color: var(--ink); margin-bottom: 9px; }}
  .eb-faq__a {{ font-size: 15.5px; line-height: 1.72; color: var(--body); }}
  @media (max-width: 900px) {{
    .eb-hero, .eb-split--img-right, .eb-split--img-left,
    .eb-dark__inner, .eb-faq__grid {{ grid-template-columns: 1fr; gap: 36px; }}
    .eb-hero {{ padding: 48px 24px; }}
    .eb-hero__h1 {{ font-size: 36px; }}
    .eb-split {{ padding: 56px 24px; }}
    .eb-dark__inner {{ padding: 56px 24px; }}
    .eb-how__grid {{ grid-template-columns: 1fr; }}
    .eb-reviews__grid {{ grid-template-columns: 1fr; }}
    .eb-cta-band__inner {{ flex-direction: column; text-align: center; padding: 40px 32px; }}
    .eb-how__inner, .eb-reviews__inner, .eb-faq {{ padding: 56px 24px; }}
    .eb-cta-band {{ padding: 48px 24px; }}
    .eb-split__img, .eb-dark__img {{ height: 300px; }}
  }}
</style>
</head>
<body>

{HEADER}

  <div class="eb-insurance-bar">We Accept Most Major Insurances &mdash; Get Approved Today</div>

  <!-- HERO -->
  <section class="eb-hero">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:16px;">Hematology Consults and Iron Infusions</div>
      <h1 class="eb-hero__h1">Your Heavy Periods Are Draining Your Iron. And Your Iron Is Draining <em>You</em>.</h1>
      <p class="eb-hero__lead">Heavy periods are the leading cause of iron deficiency &mdash; and oral supplements can&rsquo;t keep pace with that level of blood loss.</p>
      <div class="checklist" style="margin-bottom:28px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Board-certified hematologist consultation within 24 hours</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Fast iron recovery via personalized infusions</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Insurance-covered treatment options</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">10 NYC-area locations with same-week availability</span></div>
      </div>
      <a href="/contact-confirmation-energyboost/" class="btn btn--lg">Schedule an Appointment &rarr;</a>
      <div class="eb-hero__testimonial">
        <p>&ldquo;The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo;</p>
        <cite>&mdash; Anastasia M., &#9733;&#9733;&#9733;&#9733;&#9733; Google</cite>
      </div>
    </div>
    <div class="eb-hero__imgs">
      <img class="eb-hero__img eb-hero__img--top" src="{WP_IMG}2024/04/0_0.webp" alt="Women&apos;s iron infusion care">
      <img class="eb-hero__img eb-hero__img--bottom" src="{WP_IMG}2025/02/yonah0704_15145_headshot._smiling_latina_physician._purple_blou_6043a991-d6fd-41e8-ae2f-4ce291077430.png" alt="Premier Hematology physician">
    </div>
  </section>

  <!-- Real Reason — text left, image right -->
  <section class="eb-split eb-split--img-right" style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">Why Supplements Fail</div>
      <h2 class="eb-split__h2">The Real Reason You&rsquo;re Still Tired</h2>
      <p class="eb-split__body">Most women with heavy periods are told to &ldquo;take supplements&rdquo; and wait. But pills fail up to <strong>67% of the time</strong> &mdash; and simply can&rsquo;t replace iron fast enough when you&rsquo;re losing it every month.</p>
      <p class="eb-split__body">You&rsquo;ve tried the iron pills. You&rsquo;ve blamed stress, hormones, age. But the real reason you&rsquo;re exhausted might be right there in your bloodwork &mdash; if someone would just look.</p>
      <blockquote style="margin:24px 0;padding:16px 20px;border-left:3px solid var(--purple);background:var(--lavender-bg);border-radius:0 12px 12px 0;">
        <p style="font-family:'Newsreader',serif;font-style:italic;font-size:16px;color:var(--ink);margin:0;">&ldquo;I&rsquo;m tired of being tired. And I just want to feel normal again.&rdquo;</p>
      </blockquote>
      <a href="/contact-confirmation-energyboost/" class="btn" style="margin-top:8px;">Find Out What&rsquo;s Really Going On &rarr;</a>
    </div>
    <div>
      <img class="eb-split__img" src="{WP_IMG}2025/07/questions.png" alt="Iron deficiency questions">
    </div>
  </section>

  <!-- Hidden Crisis — dark band -->
  <section class="eb-dark">
    <div class="eb-dark__inner">
      <div>
        <img class="eb-dark__img" src="{WP_IMG}2025/07/aging-2-1.png" alt="Iron deficiency in women">
      </div>
      <div>
        <div class="eyebrow-sans" style="color:#c3aef0;margin-bottom:14px;">The Overlooked Epidemic</div>
        <h2 class="eb-dark__h2">The Hidden Crisis That Impacts 1 in 5 Women</h2>
        <p class="eb-dark__body">Anemia affects 20% of women &mdash; but most are misdiagnosed, dismissed, or ignored. Here&rsquo;s what your doctor might not tell you:</p>
        <div class="checklist">
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Iron supplements don&rsquo;t work for everyone &mdash; especially with ongoing blood loss</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Basic labs can miss low ferritin &mdash; the protein that fuels your energy</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Symptoms are often misattributed to anxiety, depression, or burnout</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">If severely deficient, supplements take 6&ndash;12 months &mdash; infusions work in days</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- How the Program Works -->
  <section class="eb-how">
    <div class="eb-how__inner">
      <div class="eb-how__header">
        <div class="eyebrow-sans" style="margin-bottom:12px;">Fast, Personalized &amp; Proven</div>
        <h2 class="eb-how__h2">How the EnergyBoost Iron Care Program&#8482; Works</h2>
        <p class="eb-how__lead">A 3-part protocol designed to identify the real problem and treat it fast. No more guessing. No more waiting.</p>
      </div>
      <div class="eb-how__grid">
        <div class="eb-step-card">
          <img class="eb-step-card__img" src="{WP_IMG}2025/07/womens-infusion.png" alt="Lab-guided diagnosis">
          <div class="eb-step-card__body">
            <div class="eb-step-card__num">01</div>
            <h3 class="eb-step-card__title">Lab-Guided Diagnosis</h3>
            <p class="eb-step-card__desc">Comprehensive bloodwork &mdash; ferritin, hemoglobin, B12, folate &mdash; to find the real root of your fatigue. We analyze your existing labs too.</p>
          </div>
        </div>
        <div class="eb-step-card">
          <img class="eb-step-card__img" src="{WP_IMG}2024/04/0_0.webp" alt="Personalized infusion protocol">
          <div class="eb-step-card__body">
            <div class="eb-step-card__num">02</div>
            <h3 class="eb-step-card__title">Personalized Infusion Protocol</h3>
            <p class="eb-step-card__desc">A custom treatment plan built around your labs, symptoms, and history. Administered at one of our 10 comfortable NYC infusion centers.</p>
          </div>
        </div>
        <div class="eb-step-card">
          <img class="eb-step-card__img" src="{WP_IMG}2024/04/care.webp" alt="Track and support recovery">
          <div class="eb-step-card__body">
            <div class="eb-step-card__num">03</div>
            <h3 class="eb-step-card__title">Track + Support Your Recovery</h3>
            <p class="eb-step-card__desc">Most patients feel improvement within 5&ndash;10 days. We monitor your levels and adjust your plan for lasting results.</p>
          </div>
        </div>
      </div>
      <div style="text-align:center;">
        <a href="/contact-confirmation-energyboost/" class="btn btn--lg">Take the First Step &rarr;</a>
      </div>
    </div>
  </section>

  <!-- Symptoms — text left, image right -->
  <section class="eb-split eb-split--img-right">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">Recognize the Signs</div>
      <h2 class="eb-split__h2">Your Body Is Trying to Tell You Something.</h2>
      <p class="eb-split__body">Do any of these sound familiar?</p>
      <div class="checklist" style="margin-bottom:12px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Chronic fatigue &mdash; even after a full night&rsquo;s sleep</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Heavy or prolonged menstrual bleeding</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Brain fog or difficulty concentrating</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Hair loss or weak, brittle nails</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Shortness of breath or dizziness</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Restless legs or cold hands and feet</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Mood changes or general irritability</span></div>
      </div>
      <p style="font-size:15px;font-weight:600;color:var(--purple);margin:16px 0 24px;">If you checked 2 or more &mdash; you may be iron deficient, and we can help.</p>
      <a href="/contact-confirmation-energyboost/" class="btn">Book Your Appointment Now &rarr;</a>
    </div>
    <div>
      <img class="eb-split__img" src="{WP_IMG}2024/04/fatigue.webp" alt="Woman experiencing fatigue from iron deficiency">
    </div>
  </section>

  <!-- Everything in One Location — image left, text right -->
  <section class="eb-split eb-split--img-left" style="background:var(--off-white);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
    <div>
      <img class="eb-split__img" src="{WP_IMG}2025/07/smiling.png" alt="Happy patient after treatment">
    </div>
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">10 NYC Locations</div>
      <h2 class="eb-split__h2">Everything You Need. All in One Location.</h2>
      <div class="checklist" style="margin-bottom:32px;">
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day consultation availability</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Most major insurance accepted</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Medically supervised infusion administration</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">In-house lab &mdash; faster, more accurate results</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Women-centered care environment</span></div>
        <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Telehealth consultation options available</span></div>
      </div>
      <a href="/contact-confirmation-energyboost/" class="btn">Get Started Today &rarr;</a>
    </div>
  </section>

  <!-- Why Choose Premier — dark band -->
  <section class="eb-dark">
    <div class="eb-dark__inner">
      <div>
        <div class="eyebrow-sans" style="color:#c3aef0;margin-bottom:14px;">Thousands Helped Across New York</div>
        <h2 class="eb-dark__h2">Why Women Who&rsquo;ve Tried Everything Else Are Choosing Premier Hematology</h2>
        <p class="eb-dark__body">Tired of being told &ldquo;you&rsquo;re fine&rdquo; when you feel anything but? No more long waits. No more generic supplement recommendations. No cookie-cutter treatment plans.</p>
        <div class="checklist">
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Board-certified hematologists specializing in women&rsquo;s iron health</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Women-prioritized, physician-led approach</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Trusted and referred by OBGYNs and PCPs across New York</span></div>
          <div class="checklist__item"><span class="checklist__check" style="background:rgba(195,174,240,0.2);color:#c3aef0;">&#10003;</span><span class="checklist__text" style="color:#c9c3e0;">Rapid outcomes across 10 NYC locations</span></div>
        </div>
        <a href="/contact-confirmation-energyboost/" class="btn btn--white" style="margin-top:28px;">Get Started &rarr;</a>
      </div>
      <div>
        <img class="eb-dark__img" src="{WP_IMG}2025/07/premier-team.png" alt="Premier Hematology care team">
      </div>
    </div>
  </section>

  <!-- Meet the Experts — light split -->
  <section class="eb-split eb-split--img-right">
    <div>
      <div class="eyebrow-sans" style="margin-bottom:14px;">Premier Hematology &amp; Oncology</div>
      <h2 class="eb-split__h2">Meet New York&rsquo;s Women&rsquo;s Iron Health Experts</h2>
      <p class="eb-split__body">Premier Hematology &amp; Oncology is New York&rsquo;s leading center for personalized iron deficiency care. Led by board-certified hematologists with women&rsquo;s health specialization, our mission is simple: help you feel like yourself again.</p>
      <p class="eb-split__body">We&rsquo;ve helped thousands of women across New York reclaim their energy, their mental clarity, and their quality of life &mdash; quickly and sustainably.</p>
      <a href="/contact-confirmation-energyboost/" class="btn">Book a Consultation &rarr;</a>
    </div>
    <div>
      <img class="eb-split__img" src="{WP_IMG}2024/04/nurse-care.webp" alt="Premier Hematology care team">
    </div>
  </section>

  <!-- Reviews -->
  <section class="eb-reviews">
    <div class="eb-reviews__inner">
      <div class="eyebrow-sans" style="text-align:center;margin-bottom:12px;">Patient Stories</div>
      <h2 class="eb-reviews__h2">Don&rsquo;t Take Our Word For It</h2>
      <div class="eb-reviews__grid">
        <div class="eb-review-card">
          <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="eb-review-card__quote">&ldquo;The service was top-notch from start to finish. Can&rsquo;t recommend it enough. I&rsquo;ll definitely be back!&rdquo;</p>
          <div class="eb-review-card__name">&mdash; Anastasia Hing Mackay</div>
        </div>
        <div class="eb-review-card">
          <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="eb-review-card__quote">&ldquo;Very professional and responsive. The quality of the space and the staff made this unlike any medical experience I&rsquo;ve had before.&rdquo;</p>
          <div class="eb-review-card__name">&mdash; Chani Shalmoni</div>
        </div>
        <div class="eb-review-card">
          <div class="eb-review-card__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="eb-review-card__quote">&ldquo;I noticed real improvements in my health after treatment. Professional environment, great amenities, and a team that truly cares.&rdquo;</p>
          <div class="eb-review-card__name">&mdash; Karla Ximena V&aacute;zquez Prada</div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Band -->
  <div class="eb-cta-band">
    <div class="eb-cta-band__inner">
      <h2 class="eb-cta-band__h2">Feeling Tired All the Time Isn&rsquo;t Normal. Let&rsquo;s Fix It.</h2>
      <a href="#bottom_form" class="btn btn--white btn--lg">Book Your Appointment Now &rarr;</a>
    </div>
  </div>

  <!-- FAQ -->
  <section class="eb-faq">
    <div class="eb-faq__grid">
      <div>
        <h2 class="eb-faq__h2">Frequently Asked Questions</h2>
        <img class="eb-faq__img" src="{WP_IMG}2024/04/care.webp" alt="Premier Hematology infusion care">
      </div>
      <div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">What causes anemia in women?</h3>
          <p class="eb-faq__a">Anemia in women is most commonly caused by iron deficiency, often driven by heavy menstrual bleeding. Other causes include vitamin deficiencies, chronic disease, and pregnancy.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">How does anemia cause fatigue?</h3>
          <p class="eb-faq__a">Anemia reduces the number of red blood cells available to carry oxygen, leaving your muscles and organs energy-deprived even after a full night&rsquo;s sleep.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">How is anemia diagnosed?</h3>
          <p class="eb-faq__a">Through a Complete Blood Count (CBC) plus ferritin and iron panel. Our in-house lab delivers results quickly so treatment can begin fast.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">Are iron infusions safe?</h3>
          <p class="eb-faq__a">Yes. IV iron is FDA-approved and administered by our clinical team in a monitored setting. Most patients tolerate it very well with minimal side effects.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">How long does it take to feel better after an iron infusion?</h3>
          <p class="eb-faq__a">Many patients start to feel better within a few days to a week after the infusion, with significant improvements in energy and a reduction in fatigue.</p>
        </div>
        <div class="eb-faq__item">
          <h3 class="eb-faq__q">Can I prevent anemia from heavy periods?</h3>
          <p class="eb-faq__a">Managing the underlying menstrual condition helps, but iron infusions are often the fastest way to restore depleted levels. We also work with your OBGYN as needed.</p>
        </div>
      </div>
    </div>
  </section>

<div><!-- form injected by build_forms.py --></div>

{FOOTER}
</body>
</html>""")

# ---------------------------------------------------------------------------
# 404 — Custom error page
# ---------------------------------------------------------------------------
write("404.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD("Page Not Found | Premier Hematology & Oncology", "The page you were looking for may have moved or no longer exists. Find what you need at Premier Hematology.")}
<style>
  .err-wrap {{
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 80px 24px;
  }}
  .err-inner {{
    max-width: 560px;
    text-align: center;
  }}
  .err-code {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 100px;
    font-weight: 400;
    line-height: 1;
    color: #E8E4F4;
    letter-spacing: -0.04em;
    margin-bottom: 8px;
  }}
  .err-h1 {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 34px;
    font-weight: 500;
    color: #1C1633;
    letter-spacing: -0.02em;
    margin-bottom: 14px;
  }}
  .err-body {{
    font-size: 16.5px;
    line-height: 1.75;
    color: #56526A;
    margin-bottom: 36px;
  }}
  .err-links {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin-bottom: 48px;
  }}
  .err-links a {{
    display: inline-block;
    padding: 9px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    border: 1.5px solid #DDD8F0;
    color: #1C1633;
    transition: border-color 0.15s, background 0.15s;
  }}
  .err-links a:hover {{ background: #EDE9F8; border-color: #5B4FCF; color: #5B4FCF; }}
  .err-divider {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
    color: #a89ecf;
    font-size: 13px;
  }}
  .err-divider::before, .err-divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: #DDD8F0;
  }}
</style>
</head>
<body>
{HEADER}

<div class="err-wrap">
  <div class="err-inner">
    <div class="err-code">404</div>
    <h1 class="err-h1">This page may have moved.</h1>
    <p class="err-body">Sorry about that — we recently updated our site and some pages have new addresses. Try one of the links below, or search for what you need.</p>

    <div class="err-links">
      <a href="/">Home</a>
      <a href="/anemia-iron-deficiency-consultation/">Book a Consultation</a>
      <a href="/locations/">Find a Location</a>
      <a href="/care-team/">Care Team</a>
      <a href="/cancers-and-conditions-we-treat/">Conditions We Treat</a>
      <a href="/contact/">Contact Us</a>
    </div>

    <div class="err-divider">or call us directly</div>

    <p style="font-size:15px;color:#56526A;">
      <strong>New York:</strong> <a href="tel:7188663037" style="color:var(--purple);text-decoration:none;">718-866-3037</a>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>Atlanta:</strong> <a href="tel:7705883530" style="color:var(--purple);text-decoration:none;">(770) 588-3530</a>
    </p>
  </div>
</div>

<!-- FOOTER -->
{FOOTER}
</body>
</html>""")

print(f"\n✅ Done! Site generated in {ROOT}")

# Always inject forms immediately after generation so they're never accidentally omitted
import subprocess as _sp
print("\n⚙️  Injecting forms via build_forms.py...")
_sp.run(["python3", os.path.join(ROOT, "build_forms.py")], check=True)

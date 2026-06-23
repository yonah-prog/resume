#!/usr/bin/env python3
"""
Injects real HTML forms into every lead-gen / contact page.
All forms POST to /.netlify/functions/submit which handles:
  - Staff email notifications (Resend)
  - Patient confirmation email (Resend)
  - Zapier webhook forwarding → GHL

Run: python3 build_forms.py
"""
import os, re

ROOT     = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = "/api/submit"

# ---------------------------------------------------------------------------
# Form HTML builders
# Each form includes a hidden form_type field for server-side routing.
# ---------------------------------------------------------------------------

def general_form(form_type, redirect, title="Request a Consultation",
                 sub="Our team will reach out within 24 hours."):
    return f"""
  <section class="form-section">
    <div class="form-layout">
      <div class="form-layout__trust">
        <div class="eyebrow-serif" style="margin-bottom:14px;">Premier Hematology &amp; Oncology</div>
        <h2>Expert care, next-day appointments.</h2>
        <p>Our board-certified specialists provide personalized treatment plans — whether you need an iron infusion, a consultation, or ongoing management. We work around your schedule.</p>
        <div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Board-certified hematology &amp; oncology specialists</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">In-house lab — faster results, no extra trips</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">13 convenient locations across NY metro + Atlanta</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Most major insurance plans accepted</span></div>
        </div>
      </div>
      <div class="form-card">
        <div class="form-card__title">{title}</div>
        <div class="form-card__sub">{sub}</div>
        <form data-webhook="{ENDPOINT}" data-redirect="{redirect}" novalidate>
          <input type="hidden" name="form_type" value="{form_type}">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">First Name <span class="req">*</span></label>
              <input type="text" id="first_name" name="first_name" required autocomplete="given-name">
            </div>
            <div class="form-group">
              <label for="last_name">Last Name <span class="req">*</span></label>
              <input type="text" id="last_name" name="last_name" required autocomplete="family-name">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="email">Email <span class="req">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="phone">Phone <span class="req">*</span></label>
              <input type="tel" id="phone" name="phone" required autocomplete="tel">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="message">Message <span class="req">*</span></label>
              <textarea id="message" name="message" rows="4" required placeholder="Tell us briefly what you're experiencing…"></textarea>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="insurance_provider">Insurance Provider <span class="req">*</span></label>
              <input type="text" id="insurance_provider" name="insurance_provider" required>
            </div>
            <div class="form-group">
              <label for="insurance_id">Insurance ID # <span class="req">*</span></label>
              <input type="text" id="insurance_id" name="insurance_id" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="files">Upload Documents (optional)</label>
              <input type="file" id="files" name="files" multiple accept=".pdf,.jpg,.jpeg,.png">
            </div>
          </div>
          <input class="form-hp" type="text" name="website" tabindex="-1" autocomplete="off">
          <div class="form-submit">
            <button type="submit" class="btn btn--lg">Request Consultation &rarr;</button>
          </div>
          <div class="form-msg" role="alert"></div>
        </form>
      </div>
    </div>
  </section>"""


def iron_infusions_form(form_type, redirect, title="Request an Iron Infusion Appointment",
                        sub="Our team will confirm your appointment within 24 hours."):
    return f"""
  <section class="form-section">
    <div class="form-layout">
      <div class="form-layout__trust">
        <div class="eyebrow-serif" style="margin-bottom:14px;">Iron Infusion Therapy</div>
        <h2>Get the iron infusion treatment you need.</h2>
        <p>Premier Hematology administers IV iron infusions at 13 locations across the New York metro area and Atlanta. Most major insurance plans accepted — our team will verify your benefits before your first visit.</p>
        <div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">FDA-approved IV iron formulations</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Board-certified hematology supervision</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Most major insurance accepted</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day appointments available</span></div>
        </div>
      </div>
      <div class="form-card">
        <div class="form-card__title">{title}</div>
        <div class="form-card__sub">{sub}</div>
        <form data-webhook="{ENDPOINT}" data-redirect="{redirect}" novalidate>
          <input type="hidden" name="form_type" value="{form_type}">
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="full_name">Full Name <span class="req">*</span></label>
              <input type="text" id="full_name" name="full_name" required autocomplete="name">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="email">Email <span class="req">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="phone">Phone <span class="req">*</span></label>
              <input type="tel" id="phone" name="phone" required autocomplete="tel">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="current_healthcare">Current Healthcare Provider <span class="req">*</span></label>
              <input type="text" id="current_healthcare" name="current_healthcare" required placeholder="Your primary care doctor or specialist">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="insurance_provider">Insurance Provider <span class="req">*</span></label>
              <input type="text" id="insurance_provider" name="insurance_provider" required>
            </div>
            <div class="form-group">
              <label for="insurance_id">Insurance ID # <span class="req">*</span></label>
              <input type="text" id="insurance_id" name="insurance_id" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="reason">Reason for Appointment <span class="req">*</span></label>
              <select id="reason" name="reason" required>
                <option value="">— Select a reason —</option>
                <option value="I have an Iron IV Referral">I have an Iron IV Referral</option>
                <option value="I would like to speak with a physician">I would like to speak with a physician</option>
                <option value="Other / Reason for Appointment">Other / Reason for Appointment</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="message">How can we help? (optional)</label>
              <input type="text" id="message" name="message" placeholder="Any additional details…">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="files">Upload Files (optional)</label>
              <input type="file" id="files" name="files" multiple accept=".pdf,.jpg,.jpeg,.png">
            </div>
          </div>
          <div class="form-submit">
            <button type="submit" class="btn btn--lg">Request Appointment &rarr;</button>
          </div>
          <div class="form-msg" role="alert"></div>
        </form>
      </div>
    </div>
  </section>"""


def energyboost_form(form_type, redirect, title="Request a Free Consultation",
                     sub="Tell us about your symptoms and we'll connect you with a specialist."):
    return f"""
  <section class="form-section">
    <div class="form-layout">
      <div class="form-layout__trust">
        <div class="eyebrow-serif" style="margin-bottom:14px;">Energy &amp; Wellness</div>
        <h2>Feel like yourself again.</h2>
        <p>Iron deficiency is one of the most under-diagnosed causes of fatigue, brain fog, and low energy. Our specialists can identify the root cause and create a personalized treatment plan — often starting with a single infusion.</p>
        <div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Rapid infusion — most patients feel better within days</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Next-day consultations available</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Most major insurance plans accepted</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Telehealth options available</span></div>
        </div>
      </div>
      <div class="form-card">
        <div class="form-card__title">{title}</div>
        <div class="form-card__sub">{sub}</div>
        <form data-webhook="{ENDPOINT}" data-redirect="{redirect}" novalidate>
          <input type="hidden" name="form_type" value="{form_type}">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">First Name <span class="req">*</span></label>
              <input type="text" id="first_name" name="first_name" required autocomplete="given-name">
            </div>
            <div class="form-group">
              <label for="last_name">Last Name <span class="req">*</span></label>
              <input type="text" id="last_name" name="last_name" required autocomplete="family-name">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="email">Email <span class="req">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="phone">Phone <span class="req">*</span></label>
              <input type="tel" id="phone" name="phone" required autocomplete="tel">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="insurance_provider">Insurance Provider <span class="req">*</span></label>
              <input type="text" id="insurance_provider" name="insurance_provider" required>
            </div>
            <div class="form-group">
              <label for="insurance_id">Insurance ID # <span class="req">*</span></label>
              <input type="text" id="insurance_id" name="insurance_id" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="documents">Upload Documents (optional)</label>
              <input type="file" id="documents" name="documents" multiple accept=".pdf,.jpg,.jpeg,.png">
            </div>
          </div>
          <div class="form-section__divider">Which symptoms are you experiencing?</div>
          <div class="form-row">
            <fieldset class="form-group form-group--check form-group--full" style="border:none;padding:0;margin:0;">
              <legend>Symptoms</legend>
              <div class="check-grid">
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Fatigue / Low energy"> Fatigue / Low energy</label>
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Heavy or long periods"> Heavy or long periods</label>
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Brain fog"> Brain fog</label>
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Shortness of breath"> Shortness of breath</label>
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Hair loss / brittle nails"> Hair loss / brittle nails</label>
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Restless legs / cold hands &amp; feet"> Restless legs / cold hands &amp; feet</label>
                <label class="check-opt"><input type="checkbox" name="symptoms" value="Low mood / irritability"> Low mood / irritability</label>
              </div>
            </fieldset>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="duration">How long have you been experiencing these symptoms? <span class="req">*</span></label>
              <select id="duration" name="duration" required>
                <option value="">— Select duration —</option>
                <option value="Less than 1 month">Less than 1 month</option>
                <option value="1–3 months">1–3 months</option>
                <option value="3–6 months">3–6 months</option>
                <option value="Over 6 months">Over 6 months</option>
              </select>
            </div>
          </div>
          <div class="form-submit">
            <button type="submit" class="btn btn--lg">Request My Free Consultation &rarr;</button>
          </div>
          <div class="form-msg" role="alert"></div>
        </form>
      </div>
    </div>
  </section>"""


def physician_referral_form(form_type, redirect, location=""):
    loc_label = f" — {location}" if location else ""
    return f"""
  <section class="form-section">
    <div class="form-layout">
      <div class="form-layout__trust">
        <div class="eyebrow-serif" style="margin-bottom:14px;">Physician Referrals{loc_label}</div>
        <h2>Refer your patient to Premier Hematology.</h2>
        <p>Our team reviews all referrals within one business day. We coordinate directly with your office to ensure a seamless transition of care and will send a full report after the patient's visit.</p>
        <div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Specialist response within 1 business day</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Full report sent after patient visit</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Direct fax line available</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">13 locations for patient convenience</span></div>
        </div>
      </div>
      <div class="form-card">
        <div class="form-card__title">Physician Referral Form{loc_label}</div>
        <div class="form-card__sub">Complete all fields. Chart notes can be uploaded or faxed to 718-866-3037.</div>
        <form data-webhook="{ENDPOINT}" data-redirect="{redirect}" novalidate>
          <input type="hidden" name="form_type" value="{form_type}">
          <div class="form-section__divider" style="margin-top:0;padding-top:0;border-top:none;">Referring Physician</div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="referring_doctor">Referring Doctor / Practice Name <span class="req">*</span></label>
              <input type="text" id="referring_doctor" name="referring_doctor" required>
            </div>
          </div>
          <div class="form-row form-row--half">
            <div class="form-group">
              <label for="office_phone">Office Phone <span class="req">*</span></label>
              <input type="tel" id="office_phone" name="office_phone" required>
            </div>
            <div class="form-group">
              <label for="office_fax">Office Fax</label>
              <input type="tel" id="office_fax" name="office_fax">
            </div>
          </div>
          <div class="form-section__divider">Patient Information</div>
          <div class="form-row form-row--half">
            <div class="form-group">
              <label for="patient_first">Patient First Name <span class="req">*</span></label>
              <input type="text" id="patient_first" name="patient_first" required>
            </div>
            <div class="form-group">
              <label for="patient_last">Patient Last Name <span class="req">*</span></label>
              <input type="text" id="patient_last" name="patient_last" required>
            </div>
          </div>
          <div class="form-row form-row--half">
            <div class="form-group">
              <label for="patient_dob">Date of Birth <span class="req">*</span></label>
              <input type="date" id="patient_dob" name="patient_dob" required>
            </div>
            <div class="form-group">
              <label for="patient_phone">Patient Phone <span class="req">*</span></label>
              <input type="tel" id="patient_phone" name="patient_phone" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="patient_address">Patient Address</label>
              <input type="text" id="patient_address" name="patient_address" autocomplete="street-address">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="patient_email">Patient Email</label>
              <input type="email" id="patient_email" name="patient_email">
            </div>
          </div>
          <div class="form-row form-row--half">
            <div class="form-group">
              <label for="patient_insurance">Patient Insurance <span class="req">*</span></label>
              <input type="text" id="patient_insurance" name="patient_insurance" required>
            </div>
            <div class="form-group">
              <label for="patient_insurance_id">Insurance ID # <span class="req">*</span></label>
              <input type="text" id="patient_insurance_id" name="patient_insurance_id" required>
            </div>
          </div>
          <div class="form-section__divider">Referral Details</div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="reason_for_referral">Reason for Referral <span class="req">*</span></label>
              <textarea id="reason_for_referral" name="reason_for_referral" rows="4" required placeholder="Diagnosis, clinical notes, or reason for referral…"></textarea>
            </div>
          </div>
          <div class="form-row form-row--half">
            <div class="form-group">
              <label for="chart_note">Upload Chart Note (PDF/image)</label>
              <input type="file" id="chart_note" name="chart_note" multiple accept=".pdf,.jpg,.jpeg,.png">
            </div>
            <div class="form-group">
              <label for="referral_priority">Referral Priority <span class="req">*</span></label>
              <select id="referral_priority" name="referral_priority" required>
                <option value="">— Select —</option>
                <option value="High">High — urgent</option>
                <option value="Medium">Medium — routine</option>
                <option value="Low">Low — follow-up</option>
              </select>
            </div>
          </div>
          <input class="form-hp" type="text" name="website" tabindex="-1" autocomplete="off">
          <div class="form-submit">
            <button type="submit" class="btn btn--lg">Submit Referral &rarr;</button>
          </div>
          <div class="form-msg" role="alert"></div>
        </form>
      </div>
    </div>
  </section>"""


def billing_form(redirect="/contact-confirmation/"):
    return f"""
  <section class="form-section">
    <div class="form-layout">
      <div class="form-layout__trust">
        <div class="eyebrow-serif" style="margin-bottom:14px;">Billing &amp; Insurance</div>
        <h2>Billing questions? We're here to help.</h2>
        <p>Our billing team is available Monday–Friday, 9 am–5 pm. For urgent billing matters, call us at <a href="tel:7189972281" style="color:var(--purple);">718-997-2281</a>.</p>
        <div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Response within 1–2 business days</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Assistance with insurance claims</span></div>
          <div class="checklist__item"><span class="checklist__check">&#10003;</span><span class="checklist__text">Payment plan options available</span></div>
        </div>
      </div>
      <div class="form-card">
        <div class="form-card__title">Billing Inquiry</div>
        <div class="form-card__sub">Fill out the form and our billing team will follow up within 1–2 business days.</div>
        <form data-webhook="{ENDPOINT}" data-redirect="{redirect}" novalidate>
          <input type="hidden" name="form_type" value="billing">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name">First Name <span class="req">*</span></label>
              <input type="text" id="first_name" name="first_name" required autocomplete="given-name">
            </div>
            <div class="form-group">
              <label for="last_name">Last Name <span class="req">*</span></label>
              <input type="text" id="last_name" name="last_name" required autocomplete="family-name">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="email">Email <span class="req">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="phone">Phone</label>
              <input type="tel" id="phone" name="phone" autocomplete="tel">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="subject">Subject <span class="req">*</span></label>
              <input type="text" id="subject" name="subject" required placeholder="e.g. Insurance claim question">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group form-group--full">
              <label for="message">Message <span class="req">*</span></label>
              <textarea id="message" name="message" rows="5" required placeholder="Please describe your billing question or concern…"></textarea>
            </div>
          </div>
          <div class="form-submit">
            <button type="submit" class="btn btn--lg">Send Inquiry &rarr;</button>
          </div>
          <div class="form-msg" role="alert"></div>
        </form>
      </div>
    </div>
  </section>"""


# ---------------------------------------------------------------------------
# Page → form mapping
# form_type values match the routing keys in netlify/functions/submit.js
# ---------------------------------------------------------------------------

REFERRAL_RD      = "/welcome/?firstname={first}&lastname={last}"

PAGES = {
    "anemia-iron-deficiency-consultation":
        general_form("general", "/contact-confirmation-iron-request/",
                     title="Request an Anemia Consultation",
                     sub="Our specialist team will reach out within 24 hours."),

    "hematology-and-iron-infusion-appointments":
        general_form("general", "/contact-confirmation-iron-request/",
                     title="Schedule Your Appointment",
                     sub="Fill out the form and our team will confirm your visit within 24 hours."),

    "contact":
        general_form("general", "/contact-confirmation-iron-request/",
                     title="Contact Premier Hematology",
                     sub="Fill out the form below and our team will be in touch within 24 hours."),

    "consulta-sobre-anemia-y-deficiencia-de-hierro":
        general_form("general", "/contact-confirmation-iron-request/",
                     title="Solicitar una Consulta",
                     sub="Nuestro equipo se comunicará con usted en menos de 24 horas."),

    "anemia-iron-deficiency-consultation-for-aging-symptoms":
        general_form("general", "/contact-confirmation-iron-request/",
                     title="Request a Consultation",
                     sub="Our specialist team will reach out within 24 hours."),

    "iron-infusions-request":
        iron_infusions_form("iron-infusions", "/contact-confirmation/"),

    "bariatric-iron-infusions":
        iron_infusions_form("iron-infusions", "/contact-confirmation/",
                            title="Request a Bariatric Iron Infusion Appointment"),

    "consultation-request":
        energyboost_form("energyboost", "/contact-confirmation-energyboost/"),

    "energy-boost":
        energyboost_form("energyboost", "/contact-confirmation-energyboost/",
                         title="Reclaim Your Energy",
                         sub="Tell us your symptoms and we'll connect you with a specialist."),

    "chronic-heart-failure":
        iron_infusions_form("iron-infusions", "/contact-confirmation/",
                            title="Request a Consultation"),

    "physician-referal":
        physician_referral_form("physician-referral", REFERRAL_RD),

    "physician-referal-atlanta":
        physician_referral_form("physician-referral-atlanta", REFERRAL_RD, location="Atlanta"),

    "contact-atlanta-center":
        general_form("atlanta-contact", "/contact-confirmation-iron-request/",
                     title="Contact Our Atlanta Center",
                     sub="Our Atlanta team will reach out within 24 hours."),

    "atlanta-anemia-iron-deficiency-consultation":
        general_form("atlanta-contact", "/contact-confirmation-iron-request/",
                     title="Atlanta: Request an Anemia Consultation",
                     sub="Our Atlanta specialist team will reach out within 24 hours."),

    "billing-inquiries":
        billing_form(),
}

# ---------------------------------------------------------------------------
# Inject into HTML files
# ---------------------------------------------------------------------------

SECTION_PATTERN = re.compile(
    r'\s*<section[^>]*>.*?<div class="sidebar-cta".*?</section>',
    re.DOTALL
)

SCRIPT_INCLUDE = '<script src="/assets/js/form-handler.js" defer></script>'

updated = 0
skipped = []

for slug, form_html in PAGES.items():
    path = os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(path):
        skipped.append(f"{slug} — file not found")
        continue

    with open(path) as f:
        html = f.read()

    if SCRIPT_INCLUDE not in html:
        html = html.replace('</head>', f'  {SCRIPT_INCLUDE}\n</head>', 1)

    if SECTION_PATTERN.search(html):
        html = SECTION_PATTERN.sub(form_html, html, count=1)
        with open(path, "w") as f:
            f.write(html)
        updated += 1
        print(f"  ✓ {slug}")
        continue

    if "<!-- FOOTER -->" in html:
        html = html.replace("<!-- FOOTER -->", form_html + "\n\n  <!-- FOOTER -->", 1)
        with open(path, "w") as f:
            f.write(html)
        updated += 1
        print(f"  ✓ {slug}")
        continue

    skipped.append(f"{slug} — no insertion point found")
    print(f"  ✗ {slug} — no insertion point found")

print(f"\n✅ Done. Updated {updated} pages, skipped {len(skipped)}.")
for s in skipped:
    print(f"   ⚠ {s}")

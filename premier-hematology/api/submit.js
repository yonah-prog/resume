/**
 * Premier Hematology — Form submission handler (Vercel Serverless Function)
 *
 * For each submission:
 *   1. Sends staff notification email via SendGrid
 *   2. Sends patient confirmation email via SendGrid
 *   3. Forwards full payload to the correct Zapier webhook → GHL
 *
 * Required env var (Vercel dashboard → Settings → Environment Variables):
 *   SENDGRID_API_KEY
 */

const SENDGRID_URL = 'https://api.sendgrid.com/v3/mail/send';
const FROM_EMAIL   = 'noreply@premierhematology.com';
const FROM_NAME    = 'Premier Hematology & Oncology';
const PHONE        = '718-866-3037';

// ---------------------------------------------------------------------------
// Staff notification lists by form type
// ---------------------------------------------------------------------------
const STAFF = {
  'general': [
    'DReich@premierhematology.com',
    'emaharajh@premierhematology.com',
    'yonah@premierhealthalliance.com',
    'zev@primeinfusions.com',
    'ybrazil@premierhematology.com',
    'ndiaz@premierhematology.com',
    'ARoshandatt@premierhematology.com',
  ],
  'iron-infusions': [
    'emaharajh@premierhematology.com',
    'yonah@premierhealthalliance.com',
    'zev@primeinfusions.com',
    'ybrazil@premierhematology.com',
    'ndiaz@premierhematology.com',
    'dapplebaum@premierhematology.com',
  ],
  'energyboost': [
    'yonah@premierhealthalliance.com',
    'emaharajh@premierhematology.com',
    'ndiaz@premierhematology.com',
  ],
  'physician-referral': [
    'DReich@premierhematology.com',
    'emaharajh@premierhematology.com',
    'yonah@premierhealthalliance.com',
    'zev@primeinfusions.com',
    'ybrazil@premierhematology.com',
    'ndiaz@premierhematology.com',
    'Aroshandatt@premierhematology.com',
    'jlunior@premierhematology.com',
    'asilberberg@premierhematology.com',
    'tshawel@premierhematology.com',
  ],
  'physician-referral-atlanta': [
    'bdavidson@premierhematology.com',
    'atlanta@premierhematology.com',
    'zev@primeinfusions.com',
    'yonah@premierhealthalliance.com',
    'asilberberg@premierhematology.com',
  ],
  'atlanta-contact': [
    'bdavidson@premierhematology.com',
    'yonah@premierhealthalliance.com',
    'zev@primeinfusions.com',
    'asilberberg@premierhematology.com',
  ],
  'atlanta-anemia': [
    'bdavidson@premierhematology.com',
    'yonah@premierhealthalliance.com',
    'asilberberg@premierhematology.com',
    'emaharajh@premierhematology.com',
  ],
  'atlanta-energyboost': [
    'bdavidson@premierhematology.com',
    'yonah@premierhealthalliance.com',
    'asilberberg@premierhematology.com',
  ],
  'billing': [
    'BillingInquiries@premierhematology.com',
  ],
  'iron-score-quiz': [
    'yonah@premierhealthalliance.com',
    'emaharajh@premierhematology.com',
    'ndiaz@premierhematology.com',
  ],
};

// ---------------------------------------------------------------------------
// Zapier webhooks by form type → GHL / CRM
// ---------------------------------------------------------------------------
const ZAPIER = {
  'general':                    'https://hooks.zapier.com/hooks/catch/18791657/4bysijr/',
  'iron-infusions':             'https://hooks.zapier.com/hooks/catch/18791657/23plldz/',
  'energyboost':                'https://hooks.zapier.com/hooks/catch/18791657/uubv670/',
  'physician-referral':         'https://hooks.zapier.com/hooks/catch/18791657/4bdp4dz/',
  'physician-referral-atlanta': 'https://hooks.zapier.com/hooks/catch/18791657/23wcu5s/',
  'atlanta-contact':            'https://hooks.zapier.com/hooks/catch/18791657/4o4yg90/',
  'atlanta-anemia':             'https://hooks.zapier.com/hooks/catch/18791657/4o4o3n6/',
  'atlanta-energyboost':        'https://hooks.zapier.com/hooks/catch/18791657/uj8me0c/',
};

// ---------------------------------------------------------------------------
// Email helpers
// ---------------------------------------------------------------------------
function patientName(data) {
  return data.first_name
    ? `${data.first_name} ${data.last_name || ''}`.trim()
    : data.full_name || data.patient_first || 'there';
}

function staffSubject(formType, data) {
  const name = patientName(data);
  const map = {
    'general':                    `New Consultation Request — ${name}`,
    'iron-infusions':             `New Iron Infusion Request — ${name}`,
    'energyboost':                `New Energy Consultation Request — ${name}`,
    'physician-referral':         `Physician Referral — ${data.patient_first || ''} ${data.patient_last || ''}`.trim(),
    'physician-referral-atlanta': `Atlanta Physician Referral — ${data.patient_first || ''} ${data.patient_last || ''}`.trim(),
    'atlanta-contact':            `New Atlanta Contact Request — ${name}`,
    'atlanta-anemia':             `New Atlanta Anemia Consultation — ${name}`,
    'atlanta-energyboost':        `New Atlanta Energy Consultation — ${name}`,
    'billing':                    `Billing Inquiry — ${name}`,
    'iron-score-quiz':            `Iron Score Lead — ${name} (Score: ${data.iron_score || '?'}/30)`,
  };
  return map[formType] || `New Form Submission — ${name}`;
}

function staffHtml(formType, data) {
  const SKIP = new Set(['website', 'answers']); // skip honeypot and verbose arrays
  const rows = Object.entries(data)
    .filter(([k]) => !k.startsWith('_') && !SKIP.has(k))
    .map(([k, v]) => {
      const label = k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      const val   = Array.isArray(v) ? v.join(', ') : (typeof v === 'object' ? JSON.stringify(v) : String(v || '—'));
      return `<tr>
        <td style="padding:7px 14px;font-weight:600;color:#3E2A6E;white-space:nowrap;font-size:14px;">${label}</td>
        <td style="padding:7px 14px;color:#1C1633;font-size:14px;">${val}</td>
      </tr>`;
    }).join('');

  const source = data._source_url ? `<a href="${data._source_url}" style="color:#7c5fa9;">${data._source_url}</a>` : '';

  return `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:620px;margin:0 auto;border:1px solid #e0d8f5;border-radius:12px;overflow:hidden;">
  <div style="background:#5B3FA0;padding:20px 28px;display:flex;align-items:center;">
    <div>
      <div style="color:#fff;font-size:18px;font-weight:700;">Premier Hematology &amp; Oncology</div>
      <div style="color:#c9b8f5;font-size:13px;margin-top:2px;">New form submission · ${staffSubject(formType, data)}</div>
    </div>
  </div>
  <div style="background:#faf8fd;padding:8px 0;">
    <table style="width:100%;border-collapse:collapse;">${rows}</table>
  </div>
  <div style="background:#f0ecfb;padding:12px 28px;font-size:12px;color:#56526A;">
    Submitted ${data._submitted_at || new Date().toISOString()} &nbsp;·&nbsp; ${source}
  </div>
</div>`;
}

function confirmationHtml(formType, data) {
  const name = data.first_name || data.full_name || 'there';

  const isAtlanta = formType.startsWith('atlanta');
  const isBilling = formType === 'billing';
  const isReferral = formType.startsWith('physician-referral');
  const isIronScore = formType === 'iron-score-quiz';

  let bodyText, ctaHref, ctaLabel;

  if (isIronScore) {
    const score = data.iron_score_pct || Math.round((data.iron_score / 30) * 100) || '';
    bodyText = `Your Iron Score of <strong>${score}/100</strong> has been received. One of our specialists will review your results and reach out within <strong>24 hours</strong> to discuss next steps. Iron deficiency is highly treatable — most patients feel noticeably better within days of their first infusion.`;
    ctaHref  = 'https://www.premierhematology.com/anemia-iron-deficiency-consultation/';
    ctaLabel = 'Learn About Iron Infusion Therapy →';
  } else if (isBilling) {
    bodyText = `We received your billing inquiry and our billing team will follow up within <strong>1–2 business days</strong>. For urgent matters, please call us at <a href="tel:7188663037" style="color:#5B3FA0;">${PHONE}</a>.`;
    ctaHref  = 'https://www.premierhematology.com/billing-inquiries/';
    ctaLabel = 'Visit Billing Page →';
  } else if (isReferral) {
    const patient = `${data.patient_first || ''} ${data.patient_last || ''}`.trim();
    bodyText = `We received your referral${patient ? ` for <strong>${patient}</strong>` : ''}. Our team reviews all referrals within <strong>one business day</strong> and will coordinate directly with your office. A full report will be sent after the patient's visit.`;
    ctaHref  = 'https://www.premierhematology.com/physician-referal/';
    ctaLabel = 'Visit Referral Page →';
  } else if (isAtlanta) {
    bodyText = `Thank you for reaching out to Premier Hematology &amp; Oncology — Atlanta. Our Atlanta specialist team will be in touch within <strong>24 hours</strong> to confirm your appointment. No referral is needed.`;
    ctaHref  = 'https://www.premierhematology.com/atlanta/';
    ctaLabel = 'Learn About Our Atlanta Center →';
  } else {
    bodyText = `Thank you for reaching out to Premier Hematology &amp; Oncology. We received your request and our team will be in touch within <strong>24 hours</strong> to confirm your appointment. No referral is needed — most patients are seen within 24 hours.`;
    ctaHref  = 'https://www.premierhematology.com/';
    ctaLabel = 'Visit Premier Hematology →';
  }

  return `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:600px;margin:0 auto;border:1px solid #e0d8f5;border-radius:12px;overflow:hidden;">
  <div style="background:#5B3FA0;padding:28px 32px;">
    <div style="color:#fff;font-size:20px;font-weight:700;">Premier Hematology &amp; Oncology</div>
    <div style="color:#c9b8f5;font-size:13px;margin-top:4px;">We received your request</div>
  </div>
  <div style="padding:36px 32px;background:#fff;">
    <p style="font-size:19px;color:#1C1633;margin:0 0 18px;font-weight:600;">Hi ${name},</p>
    <p style="font-size:15px;color:#56526A;line-height:1.75;margin:0 0 28px;">${bodyText}</p>
    <a href="${ctaHref}" style="display:inline-block;background:#5B3FA0;color:#fff;padding:13px 26px;border-radius:9px;text-decoration:none;font-weight:600;font-size:14px;">${ctaLabel}</a>
  </div>
  <div style="padding:18px 32px;background:#f0ecfb;font-size:12px;color:#56526A;line-height:1.7;">
    Premier Hematology &amp; Oncology &nbsp;·&nbsp; <a href="tel:7188663037" style="color:#7c5fa9;">${PHONE}</a> &nbsp;·&nbsp; <a href="https://www.premierhematology.com" style="color:#7c5fa9;">premierhematology.com</a><br>
    <span style="color:#aaa;">You received this email because you submitted a form on our website.</span>
  </div>
</div>`;
}

// ---------------------------------------------------------------------------
// SendGrid sender
// ---------------------------------------------------------------------------
async function sendEmail(toAddresses, subject, html) {
  const key = process.env.SENDGRID_API_KEY;
  if (!key) {
    console.warn('SENDGRID_API_KEY not set — skipping email');
    return;
  }

  const toList = (Array.isArray(toAddresses) ? toAddresses : [toAddresses])
    .filter(Boolean)
    .map(email => ({ email }));

  if (!toList.length) return;

  const body = {
    personalizations: [{ to: toList }],
    from: { email: FROM_EMAIL, name: FROM_NAME },
    subject,
    content: [{ type: 'text/html', value: html }],
  };

  const res = await fetch(SENDGRID_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${key}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error('SendGrid error:', res.status, text);
  }
}

// ---------------------------------------------------------------------------
// Zapier forward
// ---------------------------------------------------------------------------
async function forwardToZapier(url, data) {
  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  } catch (err) {
    console.error('Zapier forward error:', err);
  }
}

// ---------------------------------------------------------------------------
// Handler
// ---------------------------------------------------------------------------
module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).end('Method Not Allowed');

  const data = req.body;
  if (!data) return res.status(400).json({ error: 'No body' });

  // Honeypot
  if (data.website) return res.status(200).json({ ok: true });

  const formType     = (data.form_type || 'general').toLowerCase();
  const staffList    = STAFF[formType] || STAFF['general'];
  const zapierUrl    = ZAPIER[formType];
  const patientEmail = data.email || data.patient_email;

  await Promise.allSettled([
    sendEmail(staffList, staffSubject(formType, data), staffHtml(formType, data)),
    patientEmail
      ? sendEmail(
          patientEmail,
          'We received your request — Premier Hematology & Oncology',
          confirmationHtml(formType, data)
        )
      : Promise.resolve(),
    zapierUrl ? forwardToZapier(zapierUrl, data) : Promise.resolve(),
  ]);

  return res.status(200).json({ ok: true });
};

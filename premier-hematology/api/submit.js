/**
 * Premier Hematology — Form submission handler (Vercel Serverless Function)
 *
 * For each submission:
 *   1. Sends staff notification email via Resend
 *   2. Sends patient confirmation email via Resend
 *   3. Forwards full payload to the correct Zapier webhook → GHL
 *
 * Required env var (Vercel dashboard → Settings → Environment Variables):
 *   RESEND_API_KEY
 */

const RESEND_URL = 'https://api.resend.com/emails';
const FROM       = 'Premier Hematology <noreply@premierhematology.com>';
const PHONE      = '718-866-3037';

const STAFF = {
  'general':                   ['DReich@premierhematology.com','emaharajh@premierhematology.com','yonah@premierhealthalliance.com','zev@primeinfusions.com','ybrazil@premierhematology.com','ndiaz@premierhematology.com','ARoshandatt@premierhematology.com'],
  'iron-infusions':            ['emaharajh@premierhematology.com','yonah@premierhealthalliance.com','zev@primeinfusions.com','ybrazil@premierhematology.com','ndiaz@premierhematology.com','dapplebaum@premierhematology.com'],
  'energyboost':               ['yonah@premierhealthalliance.com'],
  'physician-referral':        ['DReich@premierhematology.com','emaharajh@premierhematology.com','yonah@premierhealthalliance.com','zev@primeinfusions.com','ybrazil@premierhematology.com','ndiaz@premierhematology.com','Aroshandatt@premierhematology.com','jlunior@premierhematology.com','asilberberg@premierhematology.com','tshawel@premierhematology.com'],
  'physician-referral-atlanta':['bdavidson@premierhematology.com','atlanta@premierhematology.com','zev@primeinfusions.com','yonah@premierhealthalliance.com','asilberberg@premierhematology.com'],
  'atlanta-contact':           ['bdavidson@premierhematology.com','yonah@premierhealthalliance.com','zev@primeinfusions.com','asilberberg@premierhematology.com'],
  'billing':                   ['BillingInquiries@premierhematology.com'],
};

const ZAPIER = {
  'general':                   'https://hooks.zapier.com/hooks/catch/18791657/4bysijr/',
  'iron-infusions':            'https://hooks.zapier.com/hooks/catch/18791657/23plldz/',
  'energyboost':               'https://hooks.zapier.com/hooks/catch/18791657/uubv670/',
  'physician-referral':        'https://hooks.zapier.com/hooks/catch/18791657/4bdp4dz/',
  'physician-referral-atlanta':'https://hooks.zapier.com/hooks/catch/18791657/23wcu5s/',
  'atlanta-contact':           'https://hooks.zapier.com/hooks/catch/18791657/4o4o3n6/',
};

function patientName(data) {
  return data.first_name
    ? `${data.first_name} ${data.last_name || ''}`.trim()
    : data.full_name || data.patient_first || 'Patient';
}

function staffSubject(formType, data) {
  const map = {
    'general':                   'New Consultation Request — Iron Deficiency & Anemia',
    'iron-infusions':            'New Iron Infusion Appointment Request',
    'energyboost':               'New Energy / Wellness Consultation Request',
    'physician-referral':        `Physician Referral — ${data.patient_first || ''} ${data.patient_last || ''}`.trim(),
    'physician-referral-atlanta':`Atlanta Physician Referral — ${data.patient_first || ''} ${data.patient_last || ''}`.trim(),
    'atlanta-contact':           'New Atlanta Contact / Consultation Request',
    'billing':                   `Billing Inquiry — ${patientName(data)}`,
  };
  return map[formType] || 'New Form Submission — Premier Hematology';
}

function staffHtml(formType, data) {
  const rows = Object.entries(data)
    .filter(([k]) => !k.startsWith('_') && k !== 'website')
    .map(([k, v]) => {
      const label = k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      const val   = Array.isArray(v) ? v.join(', ') : (typeof v === 'object' ? JSON.stringify(v) : v);
      return `<tr><td style="padding:6px 12px;font-weight:600;color:#3E2A6E;white-space:nowrap;">${label}</td><td style="padding:6px 12px;color:#1C1633;">${val || '—'}</td></tr>`;
    }).join('');

  return `<div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
  <div style="background:#5B3FA0;padding:24px 32px;">
    <div style="color:#fff;font-size:20px;font-weight:700;">Premier Hematology &amp; Oncology</div>
    <div style="color:#c9b8f5;font-size:14px;margin-top:4px;">New form submission</div>
  </div>
  <div style="padding:24px 32px;background:#faf8fd;border:1px solid #efeaf8;">
    <table style="width:100%;border-collapse:collapse;">${rows}</table>
  </div>
  <div style="padding:16px 32px;background:#f0ecfb;font-size:12px;color:#56526A;">
    Submitted ${data._submitted_at || ''} · ${data._source_url || ''}
  </div>
</div>`;
}

function confirmationHtml(data) {
  const name = data.first_name || data.full_name || 'there';
  return `<div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
  <div style="background:#5B3FA0;padding:24px 32px;">
    <div style="color:#fff;font-size:20px;font-weight:700;">Premier Hematology &amp; Oncology</div>
  </div>
  <div style="padding:32px;background:#fff;border:1px solid #efeaf8;">
    <p style="font-size:18px;color:#1C1633;margin:0 0 16px;">Hi ${name},</p>
    <p style="font-size:15px;color:#56526A;line-height:1.7;margin:0 0 16px;">
      Thank you for reaching out to Premier Hematology &amp; Oncology. We received your request and our team will be in touch within <strong>24 hours</strong> to confirm your appointment.
    </p>
    <p style="font-size:15px;color:#56526A;line-height:1.7;margin:0 0 24px;">
      Need something sooner? Call us at <a href="tel:7188663037" style="color:#5B3FA0;">${PHONE}</a>.
    </p>
    <a href="https://www.premierhematology.com" style="display:inline-block;background:#5B3FA0;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">Visit premierhematology.com</a>
  </div>
  <div style="padding:16px 32px;background:#f0ecfb;font-size:12px;color:#56526A;">
    Premier Hematology &amp; Oncology · ${PHONE} · premierhematology.com
  </div>
</div>`;
}

async function sendEmail(to, subject, html) {
  const key = process.env.RESEND_API_KEY;
  if (!key) { console.warn('RESEND_API_KEY not set'); return; }
  const res = await fetch(RESEND_URL, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: Array.isArray(to) ? to : [to], subject, html }),
  });
  if (!res.ok) console.error('Resend error:', res.status, await res.text());
}

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

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end('Method Not Allowed');

  const data = req.body;
  if (!data) return res.status(400).json({ error: 'No body' });

  // Honeypot
  if (data.website) return res.status(200).json({ ok: true });

  const formType    = (data.form_type || 'general').toLowerCase();
  const staffList   = STAFF[formType] || STAFF['general'];
  const zapierUrl   = ZAPIER[formType];
  const patientEmail = data.email;

  await Promise.allSettled([
    sendEmail(staffList, staffSubject(formType, data), staffHtml(formType, data)),
    patientEmail
      ? sendEmail(patientEmail, 'We received your request — Premier Hematology & Oncology', confirmationHtml(data))
      : Promise.resolve(),
    zapierUrl ? forwardToZapier(zapierUrl, data) : Promise.resolve(),
  ]);

  return res.status(200).json({ ok: true });
};

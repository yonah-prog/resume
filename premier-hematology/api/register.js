/**
 * Premier Hematology — New Patient Registration handler (Vercel Serverless Function)
 *
 * Receives the full registration payload from /patient-registration/:
 *   { fields: {...}, signature: dataURL(png), uploads: { key: { dataUrl, label } } }
 *
 * For each submission:
 *   1. Sends staff notification email via Resend with the full registration,
 *      signature embedded, and insurance card / photo ID images attached
 *   2. Sends the patient a confirmation email
 *
 * Required env var: RESEND_API_KEY
 */

const RESEND_URL = 'https://api.resend.com/emails';
const FROM       = 'Premier Hematology <noreply@premierhematology.com>';
const PHONE      = '718-866-3037';

// Staff who receive completed registrations — edit as needed
const STAFF = [
  'DReich@premierhematology.com',
  'emaharajh@premierhematology.com',
  'yonah@premierhealthalliance.com',
  'ybrazil@premierhematology.com',
  'ndiaz@premierhematology.com',
  'ARoshandatt@premierhematology.com',
];

// ---------------------------------------------------------------------------
// Email layout — fields grouped into the same sections as the paper packet
// ---------------------------------------------------------------------------
const SECTIONS = [
  ['Patient Information', [
    'first_name', 'middle_name', 'last_name', 'date_of_birth', 'birth_gender', 'marital_status',
    'address', 'apt', 'city', 'state', 'zip',
    'email', 'phone', 'phone_type', 'ok_to_leave_message', 'preferred_communication',
    'gender_identity', 'gender_identity_other', 'sexual_orientation', 'sexual_orientation_other',
    'race', 'ethnicity', 'preferred_language', 'how_did_you_hear', 'pcp_name', 'pcp_phone',
  ]],
  ['Emergency Contact', [
    'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
  ]],
  ['Guarantor / Responsible Party', [
    'responsible_party', 'guarantor_name', 'guarantor_dob', 'guarantor_address',
  ]],
  ['Preferred Pharmacy', ['pharmacy_name', 'pharmacy_location']],
  ['Primary Insurance', [
    'primary_insurance_company', 'primary_policy_number', 'primary_group_number',
    'primary_insurance_phone', 'primary_insurance_address',
    'primary_relationship_to_insured', 'primary_insured_name', 'primary_insured_dob',
  ]],
  ['Secondary Insurance', [
    'has_secondary_insurance', 'secondary_insurance_company', 'secondary_policy_number',
    'secondary_group_number', 'secondary_insurance_phone', 'secondary_insurance_address',
    'secondary_relationship_to_insured', 'secondary_insured_name', 'secondary_insured_dob',
  ]],
  ['Care Contacts', [
    'care_contacts_choice',
    'care_contact_1_name', 'care_contact_1_relationship', 'care_contact_1_phone',
    'care_contact_2_name', 'care_contact_2_relationship', 'care_contact_2_phone',
    'care_contact_3_name', 'care_contact_3_relationship', 'care_contact_3_phone',
  ]],
  ['Consents & Acknowledgements', [
    'consent_care_contacts', 'consent_treatment_aob', 'consent_bill_of_rights', 'consent_telehealth',
  ]],
  ['Authorization to Release Medical Information', [
    'wants_records_release', 'release_from', 'release_to_choice', 'release_to_other',
    'release_purpose', 'release_purpose_other', 'release_phi_types',
    'release_records_from_date', 'release_records_to_date', 'release_phi_other',
    'release_format', 'release_expiration', 'consent_records_release',
  ]],
  ['Iron Screening', [
    'iron_screening_applicable', 'iron_tried_oral', 'iron_prenatal',
    'iron_medication_details', 'iron_discontinuation_reason',
    'iron_has_gi_doctor', 'iron_gi_doctor_info', 'iron_intolerant', 'iron_intolerance_description',
    'iron_gi_disorder', 'iron_gi_disorder_description', 'iron_gastric_bypass', 'iron_gastric_bypass_details',
    'iron_heavy_bleed', 'iron_pads_per_12hr', 'iron_fibroids', 'iron_pregnant',
    'iron_pregnancy_weeks', 'iron_weeks_when_anemic', 'iron_anemia_before_pregnancy',
    'iron_ckd', 'iron_heart_failure', 'iron_other_notes',
  ]],
  ['Signature', ['signer_type', 'signer_printed_name', 'signer_authority', 'signature_date']],
];

function esc(s) {
  return String(s).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function labelize(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function fieldRows(fields, keys) {
  return keys
    .filter(k => fields[k] !== undefined && fields[k] !== '')
    .map(k => {
      const v = Array.isArray(fields[k]) ? fields[k].join(', ') : fields[k];
      return `<tr>
        <td style="padding:6px 12px;font-weight:600;color:#3E2A6E;white-space:nowrap;vertical-align:top;">${esc(labelize(k))}</td>
        <td style="padding:6px 12px;color:#1C1633;">${esc(v)}</td>
      </tr>`;
    }).join('');
}

function staffHtml(fields, uploadKeys, hasSignature) {
  const sections = SECTIONS.map(([title, keys]) => {
    const rows = fieldRows(fields, keys);
    if (!rows) return '';
    return `<h3 style="font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5B3FA0;margin:26px 0 6px;">${esc(title)}</h3>
      <table style="width:100%;border-collapse:collapse;background:#fff;border:1px solid #efeaf8;border-radius:8px;">${rows}</table>`;
  }).join('');

  const docsList = uploadKeys.length
    ? `<ul style="margin:6px 0 0;padding-left:20px;color:#1C1633;font-size:14px;">${uploadKeys.map(k => `<li>${esc(labelize(k))} — attached</li>`).join('')}</ul>`
    : '<p style="color:#A93226;font-size:14px;">No documents were attached.</p>';

  const sigBlock = hasSignature
    ? `<p style="font-size:14px;color:#1C1633;margin:6px 0;">Signed electronically by <strong>${esc(fields.signer_printed_name || '')}</strong> (${esc(fields.signer_type || 'Patient')}) on ${esc(fields.signature_date || '')}. Signature image attached (<em>signature.png</em>).</p>`
    : '<p style="color:#A93226;">No signature received.</p>';

  return `<div style="font-family:sans-serif;max-width:640px;margin:0 auto;">
  <div style="background:#5B3FA0;padding:24px 32px;">
    <div style="color:#fff;font-size:20px;font-weight:700;">Premier Hematology &amp; Oncology</div>
    <div style="color:#c9b8f5;font-size:14px;margin-top:4px;">New Patient Registration — completed online</div>
  </div>
  <div style="padding:8px 32px 24px;background:#faf8fd;border:1px solid #efeaf8;">
    ${sections}
    <h3 style="font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5B3FA0;margin:26px 0 6px;">Uploaded Documents</h3>
    ${docsList}
    <h3 style="font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5B3FA0;margin:26px 0 6px;">Electronic Signature</h3>
    ${sigBlock}
  </div>
  <div style="padding:16px 32px;background:#f0ecfb;font-size:12px;color:#56526A;">
    Submitted ${esc(fields._submitted_at || '')} &middot; ${esc(fields._source_url || '')}
  </div>
</div>`;
}

function confirmationHtml(fields) {
  const name = fields.first_name || 'there';
  return `<div style="font-family:sans-serif;max-width:600px;margin:0 auto;">
  <div style="background:#5B3FA0;padding:24px 32px;">
    <div style="color:#fff;font-size:20px;font-weight:700;">Premier Hematology &amp; Oncology</div>
  </div>
  <div style="padding:32px;background:#fff;border:1px solid #efeaf8;">
    <p style="font-size:18px;color:#1C1633;margin:0 0 16px;">Hi ${esc(name)},</p>
    <p style="font-size:15px;color:#56526A;line-height:1.7;margin:0 0 16px;">
      Thank you — we received your completed <strong>new patient registration</strong>, including your consents,
      insurance information, and uploaded documents. Our team will review everything before your visit.
    </p>
    <p style="font-size:15px;color:#56526A;line-height:1.7;margin:0 0 24px;">
      If anything is missing we'll reach out. Questions in the meantime? Call us at
      <a href="tel:7188663037" style="color:#5B3FA0;">${PHONE}</a>.
    </p>
    <a href="https://www.premierhematology.com" style="display:inline-block;background:#5B3FA0;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">Visit premierhematology.com</a>
  </div>
  <div style="padding:16px 32px;background:#f0ecfb;font-size:12px;color:#56526A;">
    Premier Hematology &amp; Oncology &middot; ${PHONE} &middot; premierhematology.com
  </div>
</div>`;
}

// ---------------------------------------------------------------------------

function dataUrlToAttachment(dataUrl, filename) {
  const m = /^data:(image\/\w+);base64,(.+)$/.exec(dataUrl || '');
  if (!m) return null;
  return { filename, content: m[2] };
}

async function sendEmail(to, subject, html, attachments) {
  const key = process.env.RESEND_API_KEY;
  if (!key) { console.warn('RESEND_API_KEY not set'); return; }
  const body = { from: FROM, to: Array.isArray(to) ? to : [to], subject, html };
  if (attachments && attachments.length) body.attachments = attachments;
  const res = await fetch(RESEND_URL, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) console.error('Resend error:', res.status, await res.text());
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end('Method Not Allowed');

  const payload = req.body;
  if (!payload || !payload.fields) return res.status(400).json({ error: 'No body' });

  const fields = payload.fields;

  // Honeypot
  if (fields.website) return res.status(200).json({ ok: true });

  const uploads    = payload.uploads || {};
  const uploadKeys = Object.keys(uploads);

  const attachments = [];
  for (const key of uploadKeys) {
    const att = dataUrlToAttachment(uploads[key].dataUrl, `${key}.jpg`);
    if (att) attachments.push(att);
  }
  const sigAtt = dataUrlToAttachment(payload.signature, 'signature.png');
  if (sigAtt) attachments.push(sigAtt);

  const patientName = `${fields.first_name || ''} ${fields.last_name || ''}`.trim() || 'Unknown Patient';
  const subject = `New Patient Registration — ${patientName} (DOB ${fields.date_of_birth || 'n/a'})`;

  await Promise.allSettled([
    sendEmail(STAFF, subject, staffHtml(fields, uploadKeys, !!sigAtt), attachments),
    fields.email
      ? sendEmail(fields.email, 'Registration received — Premier Hematology & Oncology', confirmationHtml(fields))
      : Promise.resolve(),
  ]);

  return res.status(200).json({ ok: true });
};

/**
 * Premier Hematology — Form submission handler
 * Posts directly to Zapier catch webhooks, then redirects to confirmation page.
 * File uploads are base64-encoded and included in the JSON payload.
 */
(function () {
  'use strict';

  async function fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve({ name: file.name, size: file.size, type: file.type, data: reader.result });
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const webhook = form.dataset.webhook;
    const redirect = form.dataset.redirect;
    const btn = form.querySelector('[type="submit"]');
    const msgEl = form.querySelector('.form-msg');

    // Honeypot check
    const honeypot = form.querySelector('.form-hp');
    if (honeypot && honeypot.value) return;

    // UI: loading state
    if (btn) { btn.disabled = true; btn.dataset.orig = btn.textContent; btn.textContent = 'Sending…'; }

    try {
      const payload = {};
      const elements = Array.from(form.elements);
      const fileFields = [];

      for (const el of elements) {
        if (!el.name || el.type === 'submit' || el.classList.contains('form-hp')) continue;

        if (el.type === 'file') {
          const files = Array.from(el.files);
          if (files.length > 0) {
            fileFields.push({ name: el.name, files });
          }
          continue;
        }

        if (el.type === 'checkbox') {
          if (!payload[el.name]) payload[el.name] = [];
          if (el.checked) payload[el.name].push(el.value);
          continue;
        }

        if (el.type === 'radio') {
          if (el.checked) payload[el.name] = el.value;
          continue;
        }

        payload[el.name] = el.value;
      }

      // Encode file uploads
      for (const field of fileFields) {
        const encoded = await Promise.all(field.files.map(fileToBase64));
        payload[field.name] = encoded;
      }

      // Always include source metadata for the master sheet
      payload._source_url  = window.location.href;
      payload._submitted_at = new Date().toISOString();

      const resp = await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) throw new Error('Network response ' + resp.status);

      // Build redirect URL — physician referral passes first/last name as query params
      let target = redirect || '/contact-confirmation/';
      if (target.includes('{first}')) target = target.replace('{first}', encodeURIComponent(payload['patient_first'] || payload['first_name'] || ''));
      if (target.includes('{last}'))  target = target.replace('{last}',  encodeURIComponent(payload['patient_last']  || payload['last_name']  || ''));

      window.location.href = target;

    } catch (err) {
      if (btn) { btn.disabled = false; btn.textContent = btn.dataset.orig || 'Submit'; }
      if (msgEl) { msgEl.textContent = 'Something went wrong — please call us at 718-866-3037 or try again.'; msgEl.classList.add('form-msg--error'); }
      console.error('Form error:', err);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[data-webhook]').forEach(function (form) {
      form.addEventListener('submit', handleSubmit);
    });
  });
})();

import { BRAND } from './product';

// Transactional email through Resend's HTTP API (free tier: 3,000/month).
// If RESEND_API_KEY is missing, emails are skipped and logged instead.
export async function sendEmail({ to, subject, text }) {
  if (!process.env.RESEND_API_KEY) {
    console.log('[email skipped: no RESEND_API_KEY]', to, subject);
    return;
  }
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: process.env.EMAIL_FROM || `${BRAND.name} <onboarding@resend.dev>`,
      to,
      subject,
      text: `${text}\n\n— ${BRAND.name}\nQuestions? Reply or write to ${BRAND.supportEmail}\n${BRAND.address}`,
    }),
  });
  if (!res.ok) console.error('Email failed', res.status, await res.text());
}

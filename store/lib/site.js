// Canonical site URL. Set SITE_URL in Vercel once the domain is connected.
export const SITE_URL = (
  process.env.SITE_URL ||
  (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : 'http://localhost:3000')
).replace(/\/$/, '');

export const abs = (path = '/') => `${SITE_URL}${path.startsWith('/') ? path : `/${path}`}`;

// Date the site content was last reviewed (shown on guides, used in sitemap).
export const CONTENT_UPDATED = '2026-11-24';

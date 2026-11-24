// Admin session: a cookie holding "<expiry>.<hmac>" signed with ADMIN_SECRET
// (falls back to ADMIN_PASSWORD). Uses Web Crypto, so it works in middleware
// (edge) and in server actions (Node).

export const COOKIE = 'ih_admin';
const MAX_AGE = 60 * 60 * 24 * 7; // 7 days

const secret = () => process.env.ADMIN_SECRET || process.env.ADMIN_PASSWORD || '';

async function hmac(data) {
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret()),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return Array.from(new Uint8Array(sig), (b) => b.toString(16).padStart(2, '0')).join('');
}

function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export async function createSessionToken() {
  const expiry = Math.floor(Date.now() / 1000) + MAX_AGE;
  return { token: `${expiry}.${await hmac(String(expiry))}`, maxAge: MAX_AGE };
}

export async function verifySessionToken(token) {
  if (!secret() || !token) return false;
  const [expiry, sig] = String(token).split('.');
  if (!expiry || !sig || Number(expiry) < Date.now() / 1000) return false;
  return safeEqual(sig, await hmac(expiry));
}

export async function checkPassword(input) {
  const expected = process.env.ADMIN_PASSWORD;
  if (!expected || !input) return false;
  // Compare HMACs so the comparison time doesn't depend on the password.
  return safeEqual(await hmac(`pw:${input}`), await hmac(`pw:${expected}`));
}

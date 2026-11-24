// CJ Dropshipping API v2 client (https://developers.cjdropshipping.com).
// Verify endpoint fields against CJ's current docs when the account is
// connected; values that tend to vary are configurable through env vars.

const BASE = 'https://developers.cjdropshipping.com/api2.0/v1';
let cached = { token: process.env.CJ_ACCESS_TOKEN || null, expires: 0 };

async function token() {
  if (cached.token && (cached.expires === 0 || Date.now() < cached.expires)) return cached.token;
  if (!process.env.CJ_API_KEY) throw new Error('CJ_API_KEY is not set');
  const res = await fetch(`${BASE}/authentication/getAccessToken`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ apiKey: process.env.CJ_API_KEY }),
  });
  const json = await res.json();
  if (!json.result) throw new Error(`CJ auth failed: ${json.message}`);
  cached = {
    token: json.data.accessToken,
    expires: new Date(json.data.accessTokenExpiryDate).getTime() - 60_000,
  };
  return cached.token;
}

async function call(path, { method = 'GET', body } = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: { 'Content-Type': 'application/json', 'CJ-Access-Token': await token() },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json();
  if (!json.result) throw new Error(`CJ ${path} failed: ${json.message}`);
  return json.data;
}

// Creates the order at CJ, shipping from its US warehouse.
// `items` = [{ vid, quantity }]. `orderNumber` must be unique (we use the
// Stripe Checkout Session ID, so a retried webhook can't double-order).
export async function createOrder({ orderNumber, address, name, phone, email, items }) {
  const data = await call('/shopping/order/createOrderV2', {
    method: 'POST',
    body: {
      orderNumber,
      shippingCountryCode: 'US',
      shippingCountry: 'United States',
      shippingProvince: address.state,
      shippingCity: address.city,
      shippingZip: address.postal_code,
      shippingAddress: address.line1,
      shippingAddress2: address.line2 || '',
      shippingCustomerName: name,
      shippingPhone: phone || '',
      email,
      fromCountryCode: 'US',
      logisticName: process.env.CJ_LOGISTIC_NAME || 'USPS+',
      // 2 = pay from CJ wallet balance automatically. Keep the wallet topped up.
      payType: Number(process.env.CJ_PAY_TYPE || 2),
      products: items,
    },
  });
  return data.orderId || data;
}

export async function getOrder(orderId) {
  return call(`/shopping/order/getOrderDetail?orderId=${encodeURIComponent(orderId)}`);
}

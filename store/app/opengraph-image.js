import { ImageResponse } from 'next/og';
import { BRAND, PRODUCT } from '@/lib/product';

export const alt = `${BRAND.name}: ${PRODUCT.short}`;
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

// Share image for links on Facebook, iMessage, X, Slack, WhatsApp, LinkedIn, etc.
export default function OgImage() {
  return new ImageResponse(
    (
      <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: 80, background: '#fbf8f3', color: '#1f2a2e' }}>
        <div style={{ fontSize: 30, color: '#e2673a', fontWeight: 700, letterSpacing: 2 }}>{BRAND.name.toUpperCase()}</div>
        <div style={{ fontSize: 76, fontWeight: 800, lineHeight: 1.05, marginTop: 20 }}>{BRAND.tagline}</div>
        <div style={{ fontSize: 32, color: '#5d6b70', marginTop: 28 }}>{PRODUCT.short}</div>
        <div style={{ display: 'flex', marginTop: 40, fontSize: 28, color: '#fff' }}>
          <div style={{ background: '#e2673a', padding: '12px 24px', borderRadius: 12 }}>Ships from the US · Free shipping over $29</div>
        </div>
      </div>
    ),
    size
  );
}

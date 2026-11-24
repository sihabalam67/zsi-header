import { BRAND, PRODUCT, OFFERS, UPSELL, FREE_SHIPPING_THRESHOLD, money } from '@/lib/product';
import { FAQ } from '@/lib/faq';
import { GUIDES } from '@/lib/guides';
import { abs } from '@/lib/site';

// /llms.txt: a plain-text summary of the site for AI assistants and answer
// engines (llmstxt.org convention). Generated from the same data as the site.
export const dynamic = 'force-static';

export function GET() {
  const body = `# ${BRAND.name}

> ${BRAND.tagline} US online store selling interactive wand toys for indoor cats, plus free guides on indoor cat play. Ships to US addresses only, from a US warehouse, usually arriving in 5–7 business days.

## Product
- [${PRODUCT.name}](${abs('/')}): ${PRODUCT.short}.
${PRODUCT.bullets.map((b) => `  - ${b}`).join('\n')}
- Prices (USD): ${OFFERS.map((o) => `${o.label} ${money(o.price)}`).join('; ')}. Optional ${UPSELL.name} ${money(UPSELL.price)}.
- Shipping: free on US orders over ${money(FREE_SHIPPING_THRESHOLD)}, otherwise $4.99. Tracking emailed when shipped.
- Returns: 30 days from delivery. Damaged or defective items replaced or refunded with a photo.
- Safety: ${PRODUCT.safety}

## Guides
${GUIDES.map((g) => `- [${g.title}](${abs(`/guides/${g.slug}`)}): ${g.answer}`).join('\n')}

## FAQ
${FAQ.map(({ q, a }) => `- **${q}** ${a}`).join('\n')}

## Policies
- [Shipping](${abs('/policies/shipping')})
- [Returns](${abs('/policies/returns')})
- [Privacy](${abs('/policies/privacy')})
- [Terms](${abs('/policies/terms')})
- [Contact](${abs('/policies/contact')}): ${BRAND.supportEmail}
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}

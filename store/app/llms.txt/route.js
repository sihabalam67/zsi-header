import { BRAND, PRODUCTS, FREE_SHIPPING_THRESHOLD, RETURN_DAYS, money } from '@/lib/product';
import { FAQ } from '@/lib/faq';
import { GUIDES } from '@/lib/guides';
import { abs } from '@/lib/site';

// /llms.txt: a plain-text summary of the site for AI assistants and answer
// engines (llmstxt.org convention). Generated from the same data as the site.
export const dynamic = 'force-static';

export function GET() {
  const body = `# ${BRAND.name}

> ${BRAND.promise} US online store for indoor cat play: interactive wand toys, window bird feeders, lure refills and silvervine, plus free guides on playing with indoor cats. Ships to US addresses only, from a US warehouse, usually arriving in 5–7 business days.

## Products
${PRODUCTS.map((p) => `- [${p.name}](${abs(`/products/${p.slug}`)}): ${p.tagline}. Prices (USD): ${p.bundles.map((b) => `${b.label} ${money(b.price)}`).join('; ')}.
${p.bullets.map((b) => `  - ${b}`).join('\n')}`).join('\n')}

## Shipping and returns
- Free shipping on US orders over ${money(FREE_SHIPPING_THRESHOLD)}, otherwise $4.99. Tracking emailed when shipped.
- Returns: ${RETURN_DAYS} days from delivery. Damaged or defective items replaced or refunded with a photo.

## Guides
${GUIDES.map((g) => `- [${g.title}](${abs(`/guides/${g.slug}`)}): ${g.answer}`).join('\n')}

## FAQ
${FAQ.map(({ q, a }) => `- **${q}** ${a}`).join('\n')}

## Pages
- [Shop all](${abs('/shop')})
- [Our story](${abs('/about')})
- [Shipping](${abs('/policies/shipping')}) · [Returns](${abs('/policies/returns')}) · [Privacy](${abs('/policies/privacy')}) · [Terms](${abs('/policies/terms')})
- [Contact](${abs('/policies/contact')}): ${BRAND.supportEmail}
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}

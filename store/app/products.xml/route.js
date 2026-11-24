import { BRAND, PRODUCTS, FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING } from '@/lib/product';
import { abs } from '@/lib/site';

// Product feed for Google Merchant Center (free Shopping listings) and
// Microsoft Merchant Center (Bing Shopping). Submit https://YOUR-DOMAIN/products.xml there.
export const dynamic = 'force-static';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function GET() {
  const items = PRODUCTS.flatMap((p) =>
    p.bundles.map((b) => {
      const shipping = b.price >= FREE_SHIPPING_THRESHOLD ? 0 : STANDARD_SHIPPING;
      return `    <item>
      <g:id>${esc(`${p.slug}-${b.id}`)}</g:id>
      <g:item_group_id>${esc(p.slug)}</g:item_group_id>
      <title>${esc(`${p.name} (${b.label}): ${p.tagline}`)}</title>
      <description>${esc(`${p.tagline}. ${p.bullets.join('. ')}.`)}</description>
      <link>${esc(abs(`/products/${p.slug}?offer=${b.id}`))}</link>
      <g:image_link>${esc(abs(p.images[0]))}</g:image_link>
${p.images.slice(1, 10).map((i) => `      <g:additional_image_link>${esc(abs(i))}</g:additional_image_link>\n`).join('')}      <g:availability>in_stock</g:availability>
      <g:condition>new</g:condition>
      <g:price>${(b.price / 100).toFixed(2)} USD</g:price>
      <g:brand>${esc(BRAND.name)}</g:brand>
      <g:identifier_exists>no</g:identifier_exists>
      <g:google_product_category>Animals &amp; Pet Supplies &gt; Pet Supplies &gt; Cat Supplies &gt; Cat Toys</g:google_product_category>
      <g:product_type>${esc(`Cat Supplies > ${p.category}`)}</g:product_type>
${b.units > 1 ? `      <g:multipack>${b.units}</g:multipack>\n` : ''}      <g:shipping>
        <g:country>US</g:country>
        <g:price>${(shipping / 100).toFixed(2)} USD</g:price>
      </g:shipping>
    </item>`;
    })
  ).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>${esc(BRAND.name)}</title>
    <link>${esc(abs('/'))}</link>
    <description>${esc(BRAND.promise)}</description>
${items}
  </channel>
</rss>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}

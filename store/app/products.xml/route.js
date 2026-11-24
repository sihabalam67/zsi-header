import { BRAND, PRODUCT, OFFERS, FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING } from '@/lib/product';
import { abs } from '@/lib/site';

// Product feed for Google Merchant Center (free Shopping listings) and
// Microsoft Merchant Center (Bing Shopping). Submit https://YOUR-DOMAIN/products.xml there.
export const dynamic = 'force-static';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function GET() {
  const items = OFFERS.map((o) => {
    const shipping = o.price >= FREE_SHIPPING_THRESHOLD ? 0 : STANDARD_SHIPPING;
    return `    <item>
      <g:id>${esc(`${PRODUCT.slug}-${o.id}`)}</g:id>
      <g:item_group_id>${esc(PRODUCT.slug)}</g:item_group_id>
      <title>${esc(`${PRODUCT.name} (${o.label}): ${PRODUCT.short}`)}</title>
      <description>${esc(`${PRODUCT.short}. ${PRODUCT.bullets.join('. ')}. ${PRODUCT.safety}`)}</description>
      <link>${esc(abs(`/?offer=${o.id}`))}</link>
      <g:image_link>${esc(abs(PRODUCT.images[0]))}</g:image_link>
      <g:availability>in_stock</g:availability>
      <g:condition>new</g:condition>
      <g:price>${(o.price / 100).toFixed(2)} USD</g:price>
      <g:brand>${esc(BRAND.name)}</g:brand>
      <g:identifier_exists>no</g:identifier_exists>
      <g:google_product_category>Animals &amp; Pet Supplies &gt; Pet Supplies &gt; Cat Supplies &gt; Cat Toys</g:google_product_category>
      <g:product_type>Cat Toys &gt; Wand Toys</g:product_type>
${o.units > 1 ? `      <g:multipack>${o.units}</g:multipack>\n` : ''}      <g:shipping>
        <g:country>US</g:country>
        <g:price>${(shipping / 100).toFixed(2)} USD</g:price>
      </g:shipping>
    </item>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>${esc(BRAND.name)}</title>
    <link>${esc(abs('/'))}</link>
    <description>${esc(BRAND.tagline)}</description>
${items}
  </channel>
</rss>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}

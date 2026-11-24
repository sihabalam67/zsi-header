import { abs, CONTENT_UPDATED } from '@/lib/site';
import { GUIDES } from '@/lib/guides';
import { PRODUCTS } from '@/lib/product';

export default function sitemap() {
  const lastModified = new Date(CONTENT_UPDATED);
  const page = (path, priority, changeFrequency = 'monthly') => ({ url: abs(path), lastModified, changeFrequency, priority });
  return [
    page('/', 1.0, 'weekly'),
    page('/shop', 0.9, 'weekly'),
    ...PRODUCTS.map((p) => page(`/products/${p.slug}`, 0.9, 'weekly')),
    page('/guides', 0.8, 'weekly'),
    ...GUIDES.map((g) => page(`/guides/${g.slug}`, 0.7)),
    page('/faq', 0.6),
    page('/about', 0.5),
    ...['shipping', 'returns', 'contact', 'privacy', 'terms'].map((p) => page(`/policies/${p}`, 0.3, 'yearly')),
  ];
}

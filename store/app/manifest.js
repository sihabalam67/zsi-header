import { BRAND } from '@/lib/product';

export default function manifest() {
  return {
    name: BRAND.name,
    short_name: 'Indoor Hunt',
    description: BRAND.tagline,
    start_url: '/',
    display: 'standalone',
    background_color: '#fbf8f3',
    theme_color: '#e2673a',
    icons: [
      { src: '/icon.svg', sizes: 'any', type: 'image/svg+xml' },
      { src: '/apple-icon', sizes: '180x180', type: 'image/png' },
    ],
  };
}

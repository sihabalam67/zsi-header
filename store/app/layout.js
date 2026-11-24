import './globals.css';
import Link from 'next/link';
import { BRAND } from '@/lib/product';
import { SITE_URL } from '@/lib/site';
import { JsonLd, organizationLd, websiteLd } from '@/lib/seo';

export const metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${BRAND.name} | Interactive Toys for Indoor Cats`,
    template: `%s | ${BRAND.name}`,
  },
  description:
    'Interactive wand toys and play guides for indoor cats. Ships from a US warehouse in 5–7 business days. Free US shipping over $29, 30-day returns.',
  applicationName: BRAND.name,
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    siteName: BRAND.name,
    locale: 'en_US',
    url: '/',
  },
  twitter: { card: 'summary_large_image' },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, 'max-image-preview': 'large', 'max-snippet': -1, 'max-video-preview': -1 },
  },
  verification: {
    google: process.env.GOOGLE_SITE_VERIFICATION || undefined,
    other: process.env.BING_SITE_VERIFICATION ? { 'msvalidate.01': process.env.BING_SITE_VERIFICATION } : undefined,
  },
  category: 'pet supplies',
};

export const viewport = {
  themeColor: '#e2673a',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en-US">
      <body>
        <a href="#main" className="skip">Skip to content</a>
        <header className="top">
          <Link href="/" className="logo">{BRAND.name}</Link>
          <nav aria-label="Main" className="mainnav">
            <Link href="/">Shop</Link>
            <Link href="/guides">Guides</Link>
            <Link href="/faq">FAQ</Link>
            <Link href="/about">About</Link>
          </nav>
        </header>
        <main id="main">{children}</main>
        <footer className="foot">
          <nav aria-label="Footer">
            <Link href="/policies/shipping">Shipping</Link>
            <Link href="/policies/returns">Returns</Link>
            <Link href="/policies/privacy">Privacy</Link>
            <Link href="/policies/terms">Terms</Link>
            <Link href="/policies/contact">Contact</Link>
          </nav>
          <p>Free US shipping over $29 · Ships from a US warehouse · 30-day returns</p>
          <p>© {new Date().getFullYear()} {BRAND.name}</p>
        </footer>
        <JsonLd data={organizationLd()} />
        <JsonLd data={websiteLd()} />
      </body>
    </html>
  );
}

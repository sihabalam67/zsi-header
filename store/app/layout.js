import './globals.css';
import Link from 'next/link';
import { Fraunces, Inter } from 'next/font/google';
import { BRAND, PRODUCTS, money, FREE_SHIPPING_THRESHOLD } from '@/lib/product';
import { SITE_URL } from '@/lib/site';
import { JsonLd, organizationLd, websiteLd } from '@/lib/seo';
import { CartProvider } from './components/cart';
import { CartButton, CartDrawer } from './components/CartDrawer';
import Motion from './components/Motion';

// Fonts are downloaded at build time and served from our own domain (no runtime dependency).
const display = Fraunces({ subsets: ['latin'], variable: '--font-display', display: 'swap', axes: ['opsz'] });
const sans = Inter({ subsets: ['latin'], variable: '--font-sans', display: 'swap' });

export const metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${BRAND.name} | Interactive Toys for Indoor Cats`,
    template: `%s | ${BRAND.name}`,
  },
  description:
    'Interactive wand toys, window bird feeders and play guides for indoor cats. Ships from a US warehouse in 5–7 business days. Free US shipping over $29, 30-day returns.',
  applicationName: BRAND.name,
  alternates: { canonical: '/' },
  openGraph: { type: 'website', siteName: BRAND.name, locale: 'en_US', url: '/' },
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

export const viewport = { themeColor: '#1f2a2e', width: 'device-width', initialScale: 1 };

export default function RootLayout({ children }) {
  return (
    <html lang="en-US" className={`${display.variable} ${sans.variable}`}>
      <body>
        <CartProvider>
          <a href="#main" className="skip">Skip to content</a>
          <div className="announce" aria-label="Store benefits">
            <div className="marquee">
              {[0, 1].map((n) => (
                <div className="marquee-row" key={n} aria-hidden={n === 1}>
                  <span>Free US shipping over {money(FREE_SHIPPING_THRESHOLD)}</span><span>Ships from a US warehouse</span><span>Arrives in 5–7 business days</span><span>30-day returns</span><span>Secure checkout by Stripe</span>
                </div>
              ))}
            </div>
          </div>
          <header className="site-head">
            <div className="wrap head-row">
              <Link href="/" className="logo" aria-label={`${BRAND.name} home`}>
                <svg width="30" height="30" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#e2673a" /><path d="M16 50 L46 16" stroke="#fff" strokeWidth="5" strokeLinecap="round" /><circle cx="21" cy="44" r="5" fill="#1f2a2e" /><path d="M46 16 Q56 28 52 40" stroke="#fff" strokeWidth="2" fill="none" /></svg>
                <span>{BRAND.name}</span>
              </Link>
              <nav aria-label="Main" className="mainnav">
                {[['/shop', 'Shop'], ['/guides', 'Play guides'], ['/about', 'Our story'], ['/faq', 'Help']].map(([href, label]) => (
                  <Link key={href} href={href} className="roll" data-text={label}><span>{label}</span></Link>
                ))}
              </nav>
              <CartButton />
            </div>
          </header>

          <main id="main">{children}</main>

          <footer className="site-foot">
            <div className="wrap foot-grid">
              <div>
                <b className="foot-brand">{BRAND.name}</b>
                <p>{BRAND.promise}</p>
                <p className="muted">Questions? <a href={`mailto:${BRAND.supportEmail}`}>{BRAND.supportEmail}</a></p>
              </div>
              <div>
                <h3>Shop</h3>
                <ul>{PRODUCTS.map((p) => <li key={p.slug}><Link href={`/products/${p.slug}`}>{p.name}</Link></li>)}</ul>
              </div>
              <div>
                <h3>Learn</h3>
                <ul>
                  <li><Link href="/guides">Play guides</Link></li>
                  <li><Link href="/about">Our story</Link></li>
                  <li><Link href="/faq">FAQ</Link></li>
                </ul>
              </div>
              <div>
                <h3>Help</h3>
                <ul>
                  <li><Link href="/policies/shipping">Shipping</Link></li>
                  <li><Link href="/policies/returns">Returns &amp; refunds</Link></li>
                  <li><Link href="/policies/contact">Contact us</Link></li>
                  <li><Link href="/policies/privacy">Privacy</Link></li>
                  <li><Link href="/policies/terms">Terms</Link></li>
                </ul>
              </div>
            </div>
            <div className="wrap foot-bottom">
              <span>© {new Date().getFullYear()} {BRAND.name}. All rights reserved.</span>
              <span className="pay-note">Secure payments by Stripe · Cards, Apple Pay &amp; Google Pay where available</span>
            </div>
          </footer>
          <CartDrawer />
          <Motion />
        </CartProvider>
        <JsonLd data={organizationLd()} />
        <JsonLd data={websiteLd()} />
      </body>
    </html>
  );
}

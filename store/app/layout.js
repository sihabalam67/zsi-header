import './globals.css';
import Link from 'next/link';
import { BRAND } from '@/lib/product';

export const metadata = {
  title: `${BRAND.name} | Play toys for indoor cats`,
  description: BRAND.tagline,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="top">
          <Link href="/" className="logo">{BRAND.name}</Link>
          <span className="ship-note">Free US shipping over $29</span>
        </header>
        <main>{children}</main>
        <footer className="foot">
          <nav>
            <Link href="/policies/shipping">Shipping</Link>
            <Link href="/policies/returns">Returns</Link>
            <Link href="/policies/privacy">Privacy</Link>
            <Link href="/policies/terms">Terms</Link>
            <Link href="/policies/contact">Contact</Link>
          </nav>
          <p>© {new Date().getFullYear()} {BRAND.name}</p>
        </footer>
      </body>
    </html>
  );
}

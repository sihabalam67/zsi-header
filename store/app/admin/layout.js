export const metadata = {
  title: 'Admin',
  robots: { index: false, follow: false },
};

export const dynamic = 'force-dynamic';

export default function AdminLayout({ children }) {
  return <div className="admin">{children}</div>;
}

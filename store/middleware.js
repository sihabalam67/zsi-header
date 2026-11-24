import { NextResponse } from 'next/server';
import { COOKIE, verifySessionToken } from '@/lib/auth';

// Protects every /admin page (except the login page).
export async function middleware(req) {
  const { pathname } = req.nextUrl;
  if (pathname === '/admin/login') return NextResponse.next();
  if (await verifySessionToken(req.cookies.get(COOKIE)?.value)) return NextResponse.next();
  const url = req.nextUrl.clone();
  url.pathname = '/admin/login';
  url.search = '';
  return NextResponse.redirect(url);
}

export const config = { matcher: ['/admin', '/admin/:path*'] };

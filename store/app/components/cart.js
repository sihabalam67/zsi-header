'use client';
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { getProduct, getBundle, FREE_SHIPPING_THRESHOLD } from '@/lib/product';

// Cart lives in the browser (localStorage). Prices are re-checked on the server at checkout.
const CartContext = createContext(null);
const KEY = 'ih_cart_v1';

export function CartProvider({ children }) {
  const [items, setItems] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(KEY) || '[]');
      setItems(saved.filter((i) => getBundle(getProduct(i.slug), i.bundle)));
    } catch {}
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(KEY, JSON.stringify(items));
    } catch {}
  }, [items]);

  const add = useCallback((slug, bundle, qty = 1) => {
    setItems((cur) => {
      const found = cur.find((i) => i.slug === slug && i.bundle === bundle);
      if (found) return cur.map((i) => (i === found ? { ...i, qty: Math.min(i.qty + qty, 10) } : i));
      return [...cur, { slug, bundle, qty }];
    });
    setOpen(true);
  }, []);

  const setQty = useCallback((slug, bundle, qty) => {
    setItems((cur) => (qty <= 0 ? cur.filter((i) => !(i.slug === slug && i.bundle === bundle)) : cur.map((i) => (i.slug === slug && i.bundle === bundle ? { ...i, qty: Math.min(qty, 10) } : i))));
  }, []);

  const lines = useMemo(
    () =>
      items
        .map((i) => {
          const product = getProduct(i.slug);
          const bundle = getBundle(product, i.bundle);
          return product && bundle ? { ...i, product, bundle, total: bundle.price * i.qty } : null;
        })
        .filter(Boolean),
    [items]
  );
  const subtotal = lines.reduce((s, l) => s + l.total, 0);
  const count = lines.reduce((s, l) => s + l.qty, 0);
  const toFreeShipping = Math.max(FREE_SHIPPING_THRESHOLD - subtotal, 0);

  const value = { items, lines, subtotal, count, toFreeShipping, add, setQty, open, setOpen, clear: () => setItems([]) };
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export const useCart = () => useContext(CartContext);

export async function startCheckout(items) {
  const res = await fetch('/api/checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items: items.map(({ slug, bundle, qty }) => ({ slug, bundle, qty })) }),
  });
  const data = await res.json().catch(() => ({}));
  if (!data.url) throw new Error(data.error || 'Checkout unavailable');
  window.location.href = data.url;
}

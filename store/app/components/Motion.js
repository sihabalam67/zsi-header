'use client';
import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(ScrollTrigger, SplitText);

// Conversion-safe motion only:
// - no intro/preloader (never make a shopper wait)
// - no smooth-scroll library or scroll-jacking (native scrolling stays native)
// - short, one-time entrance reveals on [data-split], [data-reveal], [data-stagger]
// - magnetic pull on [data-magnetic] buttons for mouse users
// Content is fully visible without JS, and reduced-motion users see final states.
export default function Motion() {
  const pathname = usePathname();

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const ctx = gsap.context(() => {
      const inView = (el) => el.getBoundingClientRect().top < window.innerHeight * 0.9;

      gsap.utils.toArray('[data-split]').forEach((el) => {
        if (inView(el)) return; // above-the-fold text shows instantly (no LCP delay)
        SplitText.create(el, {
          type: 'lines',
          mask: 'lines',
          autoSplit: true,
          onSplit: (s) =>
            gsap.from(s.lines, { yPercent: 105, duration: 0.8, ease: 'expo.out', stagger: 0.06, scrollTrigger: { trigger: el, start: 'top 90%', once: true } }),
        });
      });

      gsap.utils.toArray('[data-reveal]').forEach((fig) => {
        if (inView(fig)) return;
        const img = fig.querySelector('img');
        gsap
          .timeline({ scrollTrigger: { trigger: fig, start: 'top 88%', once: true } })
          .fromTo(fig, { clipPath: 'inset(12% 0% 0% 0%)', opacity: 0.4 }, { clipPath: 'inset(0% 0% 0% 0%)', opacity: 1, duration: 0.9, ease: 'power3.out' })
          .from(img, { scale: 1.08, duration: 1.2, ease: 'expo.out' }, '<');
      });

      gsap.utils.toArray('[data-stagger]').forEach((list) => {
        if (inView(list)) return;
        gsap.from(list.children, { y: 24, opacity: 0, duration: 0.6, ease: 'power3.out', stagger: 0.06, scrollTrigger: { trigger: list, start: 'top 90%', once: true } });
      });

      gsap.matchMedia().add('(pointer: fine)', () => {
        const cleanups = gsap.utils.toArray('[data-magnetic]').map((btn) => {
          const xTo = gsap.quickTo(btn, 'x', { duration: 0.5, ease: 'power3' });
          const yTo = gsap.quickTo(btn, 'y', { duration: 0.5, ease: 'power3' });
          const move = (e) => {
            const r = btn.getBoundingClientRect();
            xTo((e.clientX - r.left - r.width / 2) * 0.25);
            yTo((e.clientY - r.top - r.height / 2) * 0.25);
          };
          const leave = () => { xTo(0); yTo(0); };
          btn.addEventListener('pointermove', move);
          btn.addEventListener('pointerleave', leave);
          return () => { btn.removeEventListener('pointermove', move); btn.removeEventListener('pointerleave', leave); };
        });
        return () => cleanups.forEach((c) => c());
      });
    });
    const refresh = () => ScrollTrigger.refresh();
    window.addEventListener('load', refresh, { once: true });
    return () => {
      window.removeEventListener('load', refresh);
      ctx.revert();
    };
  }, [pathname]);

  return null;
}

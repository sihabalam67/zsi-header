'use client';
import { useEffect, useRef } from 'react';
import { usePathname } from 'next/navigation';
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(ScrollTrigger, SplitText);

const reduced = () => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// One motion engine for the whole site (awwwards-playbook R1/R3/R4/R5/R8):
// - Lenis smooth scroll driven by the GSAP ticker
// - [data-split] headings: masked line reveals
// - [data-reveal] figures: clip-path reveal with inner image settle
// - [data-stagger] lists: children rise in sequence
// - [data-hunt-track]: pinned horizontal scroll on desktop
// - [data-magnetic] buttons: pointer-follow on fine pointers
// Everything renders complete without JS; reduced-motion users get final states.
export default function Motion() {
  const pathname = usePathname();
  const lenisRef = useRef(null);

  // Smooth scroll (not on admin pages).
  useEffect(() => {
    if (reduced() || pathname.startsWith('/admin')) return;
    const lenis = new Lenis({ autoRaf: false, lerp: 0.1 });
    lenisRef.current = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    const tick = (t) => lenis.raf(t * 1000);
    gsap.ticker.add(tick);
    gsap.ticker.lagSmoothing(0);
    return () => {
      gsap.ticker.remove(tick);
      lenis.destroy();
      lenisRef.current = null;
    };
  }, [pathname]);

  // Lock smooth scroll while the cart drawer is open.
  useEffect(() => {
    const obs = new MutationObserver(() => {
      const open = document.body.style.overflow === 'hidden';
      if (lenisRef.current) open ? lenisRef.current.stop() : lenisRef.current.start();
    });
    obs.observe(document.body, { attributes: true, attributeFilter: ['style'] });
    return () => obs.disconnect();
  }, []);

  // Per-page choreography; re-run on every route change.
  useEffect(() => {
    if (reduced()) {
      document.documentElement.classList.remove('intro');
      return;
    }
    const ctx = gsap.context(() => {
      introTimeline();

      gsap.utils.toArray('[data-split]').forEach((el) => {
        if (el.closest('[data-intro]')) return; // handled by the intro
        SplitText.create(el, {
          type: 'lines',
          mask: 'lines',
          autoSplit: true,
          onSplit: (s) =>
            gsap.from(s.lines, { yPercent: 105, duration: 1.1, ease: 'expo.out', stagger: 0.08, scrollTrigger: { trigger: el, start: 'top 88%', once: true } }),
        });
      });

      gsap.utils.toArray('[data-reveal]').forEach((fig) => {
        const img = fig.querySelector('img, video');
        gsap
          .timeline({ scrollTrigger: { trigger: fig, start: 'top 85%', once: true } })
          .fromTo(fig, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.2, ease: 'power4.inOut' })
          .from(img, { scale: 1.25, duration: 1.6, ease: 'expo.out' }, '<');
      });

      gsap.utils.toArray('[data-stagger]').forEach((list) => {
        gsap.from(list.children, { y: 32, opacity: 0, duration: 0.9, ease: 'expo.out', stagger: 0.08, scrollTrigger: { trigger: list, start: 'top 88%', once: true } });
      });

      const mm = gsap.matchMedia();
      mm.add('(min-width: 821px)', () => {
        gsap.utils.toArray('[data-hunt]').forEach((section) => {
          const track = section.querySelector('[data-hunt-track]');
          if (!track) return;
          const dist = () => track.scrollWidth - window.innerWidth;
          gsap.to(track, {
            x: () => -dist(),
            ease: 'none',
            scrollTrigger: { trigger: section, pin: true, scrub: 1, end: () => `+=${dist()}`, invalidateOnRefresh: true },
          });
        });
      });

      mm.add('(pointer: fine)', () => {
        const cleanups = gsap.utils.toArray('[data-magnetic]').map((btn) => {
          const xTo = gsap.quickTo(btn, 'x', { duration: 0.6, ease: 'power3' });
          const yTo = gsap.quickTo(btn, 'y', { duration: 0.6, ease: 'power3' });
          const move = (e) => {
            const r = btn.getBoundingClientRect();
            xTo((e.clientX - r.left - r.width / 2) * 0.3);
            yTo((e.clientY - r.top - r.height / 2) * 0.3);
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
    requestAnimationFrame(refresh);
    window.addEventListener('load', refresh, { once: true });
    return () => {
      window.removeEventListener('load', refresh);
      ctx.revert();
    };
  }, [pathname]);

  return null;
}

// Home intro: curtain lifts, hero image settles, headline lines rise, meta follows.
// Shown once per browser session; skipped entirely if the page has no [data-intro].
function introTimeline() {
  const root = document.querySelector('[data-intro]');
  const html = document.documentElement;
  if (!root) { html.classList.remove('intro'); return; }
  const title = root.querySelector('[data-split]');
  const split = title ? SplitText.create(title, { type: 'lines', mask: 'lines' }) : null;
  const playCurtain = html.classList.contains('intro');
  const tl = gsap.timeline({ defaults: { ease: 'expo.out' }, onComplete: () => html.classList.remove('intro') });
  if (playCurtain) {
    const counter = { v: 0 };
    const out = document.querySelector('.loader-count');
    tl.to(counter, { v: 100, duration: 0.9, ease: 'power2.inOut', onUpdate: () => out && (out.textContent = String(Math.round(counter.v))) })
      .to('.loader', { clipPath: 'inset(0% 0% 100% 0%)', duration: 0.9, ease: 'power4.inOut' });
    try { sessionStorage.setItem('ih_intro', '1'); } catch {}
  }
  tl.from(root.querySelector('.hero-photo img'), { scale: 1.18, duration: 1.6 }, playCurtain ? '<' : 0);
  if (split) tl.from(split.lines, { yPercent: 105, duration: 1.1, stagger: 0.08 }, '<0.15');
  tl.from(root.querySelectorAll('[data-intro-meta] > *'), { y: 20, opacity: 0, duration: 0.8, stagger: 0.06 }, '<0.3');
}

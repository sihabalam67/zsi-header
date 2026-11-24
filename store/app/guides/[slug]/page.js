import Link from 'next/link';
import { notFound } from 'next/navigation';
import { GUIDES, getGuide } from '@/lib/guides';
import { PRODUCT } from '@/lib/product';
import { CONTENT_UPDATED } from '@/lib/site';
import { JsonLd, articleLd, faqLd, breadcrumbLd } from '@/lib/seo';

export function generateStaticParams() {
  return GUIDES.map((g) => ({ slug: g.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const g = getGuide(slug);
  if (!g) return {};
  return {
    title: g.title,
    description: g.description,
    alternates: { canonical: `/guides/${g.slug}` },
    openGraph: { type: 'article', title: g.title, description: g.description, url: `/guides/${g.slug}` },
  };
}

export default async function Guide({ params }) {
  const { slug } = await params;
  const g = getGuide(slug);
  if (!g) notFound();
  const others = GUIDES.filter((x) => x.slug !== g.slug).slice(0, 3);

  return (
    <article className="article">
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link href="/">Home</Link> › <Link href="/guides">Guides</Link> › {g.title}
      </nav>
      <h1>{g.title}</h1>
      <p className="meta">By the Indoor Hunt Co. team · Updated <time dateTime={CONTENT_UPDATED}>{new Date(CONTENT_UPDATED).toLocaleDateString('en-US', { dateStyle: 'long', timeZone: 'UTC' })}</time></p>

      <div className="answer" role="note" aria-label="Short answer">
        <b>Short answer</b>
        <p>{g.answer}</p>
      </div>

      {g.sections.map((s) => (
        <section key={s.h}>
          <h2>{s.h}</h2>
          {s.list && (
            <ol>
              {s.list.map((li) => (
                <li key={li}>{li}</li>
              ))}
            </ol>
          )}
          {s.p?.map((t) => (
            <p key={t}>{t}</p>
          ))}
        </section>
      ))}

      <section>
        <h2>Frequently asked questions</h2>
        {g.faq.map(({ q, a }) => (
          <div key={q} className="qa">
            <h3>{q}</h3>
            <p>{a}</p>
          </div>
        ))}
      </section>

      <aside className="cta-box">
        <b>Make the nightly hunt easy</b>
        <p>{PRODUCT.short}. Ships from a US warehouse.</p>
        <Link href="/" className="cta inline">See the {PRODUCT.name}</Link>
      </aside>

      <section>
        <h2>More guides</h2>
        <ul className="cards">
          {others.map((o) => (
            <li key={o.slug}>
              <Link href={`/guides/${o.slug}`}><b>{o.title}</b><span>{o.description}</span></Link>
            </li>
          ))}
        </ul>
      </section>

      <p className="fine">General information only, not veterinary advice. If your cat’s behaviour or health changes, talk to your vet.</p>

      <JsonLd data={articleLd(g)} />
      <JsonLd data={faqLd(g.faq)} />
      <JsonLd data={breadcrumbLd([['Home', '/'], ['Guides', '/guides'], [g.title, `/guides/${g.slug}`]])} />
    </article>
  );
}

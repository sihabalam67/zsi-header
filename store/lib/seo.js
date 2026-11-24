import { BRAND, PRODUCT, OFFERS, CURRENCY, FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING } from './product';
import { SITE_URL, abs, CONTENT_UPDATED } from './site';

// schema.org structured data (JSON-LD) used by Google, Bing, Apple and AI answer engines.
// Only facts we can back up: no invented ratings or reviews.

const ORG_ID = `${SITE_URL}/#organization`;

export function organizationLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': ORG_ID,
    name: BRAND.name,
    url: SITE_URL,
    logo: abs('/icon.svg'),
    description: BRAND.tagline,
    email: BRAND.supportEmail,
    sameAs: [process.env.SOCIAL_INSTAGRAM, process.env.SOCIAL_TIKTOK].filter(Boolean),
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'customer support',
      email: BRAND.supportEmail,
      areaServed: 'US',
      availableLanguage: 'en',
    },
  };
}

export function websiteLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${SITE_URL}/#website`,
    name: BRAND.name,
    url: SITE_URL,
    publisher: { '@id': ORG_ID },
    inLanguage: 'en-US',
  };
}

const shippingDetails = (price) => ({
  '@type': 'OfferShippingDetails',
  shippingRate: {
    '@type': 'MonetaryAmount',
    value: price >= FREE_SHIPPING_THRESHOLD ? 0 : STANDARD_SHIPPING / 100,
    currency: CURRENCY.toUpperCase(),
  },
  shippingDestination: { '@type': 'DefinedRegion', addressCountry: 'US' },
  deliveryTime: {
    '@type': 'ShippingDeliveryTime',
    handlingTime: { '@type': 'QuantitativeValue', minValue: 1, maxValue: 3, unitCode: 'DAY' },
    transitTime: { '@type': 'QuantitativeValue', minValue: 2, maxValue: 5, unitCode: 'DAY' },
  },
});

const returnPolicy = {
  '@type': 'MerchantReturnPolicy',
  applicableCountry: 'US',
  returnPolicyCategory: 'https://schema.org/MerchantReturnFiniteReturnWindow',
  merchantReturnDays: 30,
  returnMethod: 'https://schema.org/ReturnByMail',
  returnFees: 'https://schema.org/FreeReturn',
};

export function productLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    '@id': `${SITE_URL}/#product`,
    name: PRODUCT.name,
    description: `${PRODUCT.short}. ${PRODUCT.bullets.join('. ')}.`,
    image: PRODUCT.images.map((src) => abs(src)),
    sku: PRODUCT.slug,
    brand: { '@type': 'Brand', name: BRAND.name },
    category: 'Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Toys',
    offers: OFFERS.map((o) => ({
      '@type': 'Offer',
      name: `${PRODUCT.name}: ${o.label}`,
      sku: `${PRODUCT.slug}-${o.id}`,
      url: abs(`/?offer=${o.id}`),
      price: (o.price / 100).toFixed(2),
      priceCurrency: CURRENCY.toUpperCase(),
      availability: 'https://schema.org/InStock',
      itemCondition: 'https://schema.org/NewCondition',
      seller: { '@id': ORG_ID },
      shippingDetails: shippingDetails(o.price),
      hasMerchantReturnPolicy: returnPolicy,
    })),
  };
}

export function faqLd(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map(({ q, a }) => ({
      '@type': 'Question',
      name: q,
      acceptedAnswer: { '@type': 'Answer', text: a },
    })),
  };
}

export function breadcrumbLd(crumbs) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map(([name, path], i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name,
      item: abs(path),
    })),
  };
}

export function articleLd(guide) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: guide.title,
    description: guide.description,
    mainEntityOfPage: abs(`/guides/${guide.slug}`),
    datePublished: CONTENT_UPDATED,
    dateModified: CONTENT_UPDATED,
    author: { '@type': 'Organization', name: `${BRAND.name} team`, url: abs('/about') },
    publisher: { '@id': ORG_ID },
    image: abs('/opengraph-image'),
    inLanguage: 'en-US',
  };
}

// <script type="application/ld+json"> with safe escaping.
export function JsonLd({ data }) {
  const json = JSON.stringify(data).replace(/</g, '\\u003c');
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: json }} />;
}

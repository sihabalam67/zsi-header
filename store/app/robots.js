import { abs } from '@/lib/site';

// Everyone may crawl the public site, including AI search and answer engines
// (OpenAI, Anthropic, Perplexity, Google, Apple, Microsoft). Admin and APIs stay private.
const AI_AND_SEARCH_BOTS = [
  'Googlebot', 'Google-Extended', 'Bingbot', 'Applebot', 'Applebot-Extended', 'DuckDuckBot',
  'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
  'PerplexityBot', 'Perplexity-User', 'CCBot', 'meta-externalagent', 'YandexBot',
];

export default function robots() {
  const disallow = ['/admin', '/api/'];
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow },
      ...AI_AND_SEARCH_BOTS.map((userAgent) => ({ userAgent, allow: '/', disallow })),
    ],
    sitemap: abs('/sitemap.xml'),
  };
}

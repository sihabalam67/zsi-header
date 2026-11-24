// IndexNow key file (Bing, Yandex, Seznam, Naver). Bing's index also feeds
// ChatGPT search and Copilot. The admin "Notify search engines" button pings
// IndexNow with keyLocation pointing here.
export function GET() {
  const key = process.env.INDEXNOW_KEY;
  if (!key) return new Response('Not configured', { status: 404 });
  return new Response(key, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}

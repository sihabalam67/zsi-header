#!/usr/bin/env python3
"""Coin Theory website (free, static): home, calculators, one article page per public long video (transcript +
sources + embedded video), sitemap, robots.txt, llms.txt. Every page sends visitors to the YouTube channel.
    python3 channel/site/build.py            -> channel/site/dist/
Data: data/CPIAUCSL.csv (FRED CPI-U), data/SP500TR_daily.csv (Yahoo ^SP500TR, S&P 500 total return)."""
import csv
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(HERE)
ROOT = os.path.dirname(CH)
DIST = os.path.join(HERE, 'dist')
SITE = os.environ.get('SITE_URL', 'https://coin-theory-money.vercel.app')
YT = 'https://www.youtube.com/@cointheoryhq'
SUB = YT + '?sub_confirmation=1'
sys.path.insert(0, os.path.join(ROOT, 'youtube'))
E = html.escape

CSS = """
:root{--bg:#FFF8EC;--card:#fff;--ink:#2b1a0e;--mut:#7a6650;--gold:#E2A21F;--goldd:#B87F0E;--green:#11885A;--red:#D7261E;--line:#EBDCC2}
@media(prefers-color-scheme:dark){:root{--bg:#14110C;--card:#1E1A13;--ink:#F5EFE0;--mut:#B9AA90;--line:#3A3226}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--goldd)}header{padding:18px 16px;border-bottom:1px solid var(--line)}header .w{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:22px;color:var(--ink);text-decoration:none}
.coin{width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFF4B8,#FFD54A 45%,#D98C0C);display:inline-block;box-shadow:inset 0 -3px 0 #b8760a}
nav{display:flex;gap:16px;margin-left:auto;flex-wrap:wrap}nav a{color:var(--ink);text-decoration:none;font-weight:600}
.w{max-width:1080px;margin:0 auto;padding:0 16px}
.btn{display:inline-block;background:var(--red);color:#fff!important;text-decoration:none;font-weight:800;padding:12px 22px;border-radius:999px}
.btn.alt{background:var(--gold);color:#2b1a0e!important}
.hero{padding:44px 0 26px}.hero h1{font-size:clamp(30px,6vw,52px);line-height:1.1;margin:0 0 12px}.hero p{color:var(--mut);font-size:19px;max-width:720px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px;margin:18px 0 40px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;text-decoration:none;color:var(--ink);display:block}
.card img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}.card div{padding:12px 14px;font-weight:700}
h2{font-size:28px;margin:36px 0 6px}.mut{color:var(--mut)}
.tool{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px;margin:20px 0}
.tool label{display:block;font-weight:700;margin:10px 0 4px}.tool input,.tool select{font-size:20px;padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--ink);width:100%;max-width:320px}
.out{font-size:clamp(30px,7vw,52px);font-weight:900;color:var(--green);margin:14px 0 4px}.out.red{color:var(--red)}
.vid{position:relative;width:100%;aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:#000;margin:18px 0}.vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.note{font-size:14px;color:var(--mut)}footer{border-top:1px solid var(--line);padding:26px 0 40px;margin-top:40px;color:var(--mut);font-size:15px}
.tx{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;white-space:pre-wrap}
"""


def page(title, desc, body, path, extra_head=''):
    url = SITE + '/' + path.replace('index.html', '')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">
<meta name="google-site-verification" content="1rca9qC0icAjWlFwoUrtEcZy4N8kj7eHTteeZ8AduZE">
<style>{CSS}</style>{extra_head}</head><body>
<header><div class="w"><a class="logo" href="/"><span class="coin"></span>Coin Theory</a>
<nav><a href="/calculators/inflation.html">Inflation calculator</a><a href="/calculators/sp500.html">"What if I invested?"</a><a href="/#videos">Videos</a></nav>
<a class="btn" href="{SUB}">Subscribe on YouTube</a></div></header>
<main class="w">{body}</main>
<footer><div class="w">Coin Theory explains money with short animated stories and real data from official sources.
Education only, not financial advice. Past returns don't guarantee future results.<br>
<a href="{YT}">YouTube</a> · <a href="/llms.txt">llms.txt</a> · Data: FRED (CPI-U), Yahoo Finance (^SP500TR), BLS, Federal Reserve.</div></footer>
</body></html>"""


def series():
    cpi = {}
    rows = [r for r in csv.DictReader(open(os.path.join(CH, 'data', 'CPIAUCSL.csv'))) if r['CPIAUCSL'].strip()]
    for r in rows:
        cpi.setdefault(r['observation_date'][:4], []).append(float(r['CPIAUCSL']))
    cpi = {y: round(sum(v) / len(v), 3) for y, v in cpi.items()}
    last_cpi = rows[-1]
    tr = {}
    for r in csv.DictReader(open(os.path.join(CH, 'data', 'SP500TR_daily.csv'))):
        if not r['close'].strip():
            continue
        tr.setdefault(r['date'][:4], []).append((r['date'], float(r['close'])))
    first = {y: v[0][1] for y, v in tr.items()}
    lastrow = list(tr.values())[-1][-1]
    return cpi, (last_cpi['observation_date'], float(last_cpi['CPIAUCSL'])), first, lastrow


def videos():
    """Public long videos with title/description from the API (fallback: upload kits)."""
    ids = json.load(open(os.path.join(CH, 'out', 'video_ids.json')))
    longs = {k: v for k, v in ids.items() if '_short' not in k and k != 's02_salary'}
    meta = {}
    try:
        from upload import client
        yt = client()
        vids = list(longs.values())
        for i in range(0, len(vids), 50):
            for it in yt.videos().list(part='snippet,status', id=','.join(vids[i:i + 50])).execute()['items']:
                meta[it['id']] = it
    except Exception as e:  # offline: use kits
        print('API unavailable, using kits:', str(e)[:80])
    out = []
    for name, vid in longs.items():
        it = meta.get(vid)
        if it and it['status']['privacyStatus'] != 'public':
            continue
        kit = os.path.join(CH, 'out', name + '.upload.json')
        k = json.load(open(kit)) if os.path.exists(kit) else {}
        title = it['snippet']['title'] if it else k.get('title', name)
        desc = it['snippet']['description'] if it else k.get('description', '')
        date = it['snippet']['publishedAt'][:10] if it else ''
        srt = os.path.join(CH, 'out', name + '.en.srt')
        tx = ''
        if os.path.exists(srt):
            tx = ' '.join(l.strip() for l in open(srt) if l.strip() and not l.strip().isdigit() and '-->' not in l)
        out.append(dict(name=name, id=vid, title=title, desc=desc, date=date, tx=tx))
    out.sort(key=lambda v: v['date'], reverse=True)
    return out


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:70]


def main():
    os.makedirs(os.path.join(DIST, 'calculators'), exist_ok=True)
    os.makedirs(os.path.join(DIST, 'videos'), exist_ok=True)
    cpi, (cpi_date, cpi_now), tr_first, (tr_date, tr_now) = series()
    vs = videos()
    urls = ['', 'calculators/inflation.html', 'calculators/sp500.html']
    # ---- video pages
    for v in vs:
        p = f"videos/{slug(v['title'])}.html"
        v['path'] = p
        urls.append(p)
        ld = json.dumps({"@context": "https://schema.org", "@type": "VideoObject", "name": v['title'],
                         "description": v['desc'][:300], "uploadDate": v['date'],
                         "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg",
                         "embedUrl": f"https://www.youtube.com/embed/{v['id']}", "contentUrl": f"https://youtu.be/{v['id']}"})
        desc = re.sub(r'https?://\S+', lambda m: f'<a href="{m.group(0)}">{m.group(0)}</a>', E(v['desc']))
        body = (f"<article><h1 style='margin-top:30px'>{E(v['title'])}</h1><p class='mut'>{E(v['date'])}</p>"
                f"<div class='vid'><iframe src='https://www.youtube-nocookie.com/embed/{v['id']}' title='{E(v['title'])}' allowfullscreen loading='lazy'></iframe></div>"
                f"<p><a class='btn' href='{SUB}'>Subscribe for one money story a week</a></p>"
                f"<h2>About this video</h2><div class='tx'>{desc}</div>"
                + (f"<h2>Transcript</h2><div class='tx'>{E(v['tx'])}</div>" if v['tx'] else '') + "</article>")
        open(os.path.join(DIST, p), 'w').write(page(v['title'] + ' | Coin Theory', v['desc'][:155], body, p,
                                                     f'<script type="application/ld+json">{ld}</script>'))
    # ---- calculators
    years = sorted(y for y in cpi if int(y) >= 1947 and int(y) < int(cpi_date[:4]))
    infl = f"""<h1 style="margin-top:30px">What is my old money worth today?</h1>
<p class="mut">Type an amount and a year. We use the official U.S. consumer price index (CPI-U) to show what it buys today.</p>
<div class="tool"><label>Amount</label><input id="amt" type="number" value="1000" min="1">
<label>Year</label><select id="yr">{''.join(f'<option{" selected" if y == "1996" else ""}>{y}</option>' for y in years)}</select>
<div class="out" id="o1"></div><div id="o2" class="mut"></div><div class="out red" id="o3" style="font-size:30px"></div></div>
<p class="note">CPI-U yearly average for the year you pick vs the latest month ({cpi_date[:7]}). Source: FRED series CPIAUCSL. Education only.</p>
<h2>Watch: $1,000 in a cookie jar for 30 years</h2><div class="vid"><iframe src="https://www.youtube-nocookie.com/embed/o0-ZXEnRyDg" title="Grandpa Gave 3 Kids $1,000. Who Won?" allowfullscreen loading="lazy"></iframe></div>
<script>const C={json.dumps(cpi)},NOW={cpi_now};
function go(){{const a=+amt.value||0,y=yr.value,n=a*NOW/C[y],b=a*C[y]/NOW;
o1.textContent='$'+Math.round(n).toLocaleString('en-US');o2.textContent='is what you need today to buy what $'+a.toLocaleString('en-US')+' bought in '+y+'.';
o3.textContent='Kept as cash, $'+a.toLocaleString('en-US')+' from '+y+' now buys only $'+Math.round(b).toLocaleString('en-US')+' worth.';}}
amt.oninput=yr.onchange=go;go();</script>"""
    open(os.path.join(DIST, 'calculators/inflation.html'), 'w').write(page(
        'Inflation calculator: what is my money from 1996 worth today? | Coin Theory',
        'Free inflation calculator using official CPI data: see what your money from any year since 1947 is worth today.', infl, 'calculators/inflation.html'))
    tyears = sorted(y for y in tr_first if int(y) < int(tr_date[:4]))
    sp = f"""<h1 style="margin-top:30px">What if I had invested in the S&amp;P 500?</h1>
<p class="mut">Pick an amount and a starting year. We use the S&amp;P 500 total return index (dividends reinvested) from the first trading day of that year to {tr_date}.</p>
<div class="tool"><label>Amount invested once</label><input id="amt" type="number" value="1000" min="1">
<label>Starting year</label><select id="yr">{''.join(f'<option{" selected" if y == "1996" else ""}>{y}</option>' for y in tyears)}</select>
<div class="out" id="o1"></div><div id="o2" class="mut"></div><div id="o3" class="mut"></div></div>
<p class="note">Index level on the first trading day of the year vs {tr_date}. Before fees and taxes; you can't invest in an index directly; past returns don't guarantee future results. Source: Yahoo Finance ^SP500TR. Education only, not financial advice.</p>
<h2>Watch the story behind this calculator</h2><div class="vid"><iframe src="https://www.youtube-nocookie.com/embed/o0-ZXEnRyDg" title="Grandpa Gave 3 Kids $1,000. Who Won?" allowfullscreen loading="lazy"></iframe></div>
<script>const T={json.dumps(tr_first)},NOW={tr_now};
function go(){{const a=+amt.value||0,y=yr.value,v=a*NOW/T[y],yrs=({int(tr_date[:4])}-+y)||1,cagr=Math.pow(v/a,1/yrs)-1;
o1.textContent='$'+Math.round(v).toLocaleString('en-US');o2.textContent='is what $'+a.toLocaleString('en-US')+' invested at the start of '+y+' would be worth now ('+(v/a).toFixed(1)+'x).';
o3.textContent='That is about '+(cagr*100).toFixed(1)+'% a year, with plenty of crashes along the way.';}}
amt.oninput=yr.onchange=go;go();</script>"""
    open(os.path.join(DIST, 'calculators/sp500.html'), 'w').write(page(
        'What if you invested $1,000 in the S&P 500? Calculator | Coin Theory',
        'Free calculator: what $1,000 (or any amount) invested in the S&P 500 in any year since 1988 would be worth today, dividends reinvested.', sp, 'calculators/sp500.html'))
    # ---- home
    cards = ''.join(f"<a class='card' href='/{v['path']}'><img src='https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg' alt='' loading='lazy'><div>{E(v['title'])}</div></a>" for v in vs)
    home = f"""<section class="hero"><h1>Money, explained simply.<br>Every number is real.</h1>
<p>Animated money stories and plain-English explainers about prices, saving, investing and the economy, built on official data.</p>
<p><a class="btn" href="{SUB}">Subscribe on YouTube</a> &nbsp; <a class="btn alt" href="/calculators/inflation.html">Try the inflation calculator</a></p></section>
<h2>Free money calculators</h2><div class="grid">
<a class="card" href="/calculators/inflation.html"><div>What is my old money worth today? (inflation calculator)</div></a>
<a class="card" href="/calculators/sp500.html"><div>What if I had invested in the S&amp;P 500?</div></a></div>
<h2 id="videos">Videos</h2><div class="grid">{cards}</div>"""
    open(os.path.join(DIST, 'index.html'), 'w').write(page('Coin Theory: money explained simply, with real numbers',
                                                           'Animated money stories and explainers with real data, plus free inflation and investing calculators.', home, 'index.html'))
    # ---- sitemap, robots, llms.txt
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                                       + ''.join(f'<url><loc>{SITE}/{u}</loc></url>' for u in urls) + '</urlset>')
    open(os.path.join(DIST, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    llms = [f'# Coin Theory\n\n> Money explained simply with animated stories and real, sourced data (FRED, BLS, Federal Reserve, Yahoo Finance). '
            f'YouTube: {YT}\n\n## Calculators\n- [Inflation calculator]({SITE}/calculators/inflation.html): what money from any year since 1947 is worth today (CPI-U).\n'
            f'- [S&P 500 "what if I invested" calculator]({SITE}/calculators/sp500.html): growth of a one-time investment since 1988, dividends reinvested.\n\n## Videos\n']
    llms += [f"- [{v['title']}]({SITE}/{v['path']}): {v['desc'][:160].replace(chr(10), ' ')}\n" for v in vs]
    open(os.path.join(DIST, 'llms.txt'), 'w').write(''.join(llms))
    print('built', len(vs), 'video pages ->', DIST)


if __name__ == '__main__':
    main()

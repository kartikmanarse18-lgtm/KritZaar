#!/usr/bin/env python3
"""
KritZaar static page builder.
Reads the section JSON files (stories.json, fun.json, ...) and writes real,
Google-friendly pages: about.html, stories.html, games.html, ... plus
pages.css (colors taken from the theme in _index.json) and sitemap.xml.

Usage:  python3 build_pages.py [repo_dir] [out_dir]      (both default to ".")
Sections whose JSON has no real articles yet are skipped automatically,
so empty/placeholder sections never become thin pages.
"""
import json, re, sys, os, html, datetime

REPO = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT  = sys.argv[2] if len(sys.argv) > 2 else '.'
SITE = 'https://kritzaar.online'
CONTACT_EMAIL = ''   # optional: e.g. 'hello@kritzaar.online' adds a Contact line on the About page
TODAY = datetime.date.today().isoformat()

SECTIONS = [
  dict(id='stories', file='stories.html', label='Stories', json='stories.json',
       title='Mystery Stories and Real-Life Cases | KRITZAAR',
       desc='Read mystery stories and real-life cases on KritZaar, from unsolved disappearances to ghost tales. Every story opens right on the site.',
       lead='Mystery stories and real-life cases, from unsolved disappearances to ghost tales.',
       about=['Stories on KritZaar open on their own reading page, so you can read without leaving the site.',
              'Use Save to keep a story in your Saved tab, or Share to send it to a friend.'],
       cta='Read'),
  dict(id='fun', file='games.html', label='Games', json='fun.json',
       title='Free HTML Games to Play in Your Browser | KRITZAAR',
       desc='Play free HTML games on KritZaar. They run in your browser on phone or computer, with no download or sign-up.',
       lead='Free HTML games you can play instantly in your browser, with no download or sign-up.',
       about=['Every game here runs directly in your browser, on a phone or a computer, so there is nothing to install and no account to create.',
              'Tap Play to open a game inside KritZaar, and use Fullscreen for a bigger view. If a game does not load, use Retry or open it in a new tab.'],
       cta='Play'),
  dict(id='coolstuff', file='cool-stuff.html', label='Cool Stuff', json='coolstuff.json',
       title='Free Browser Tools and Mini Projects | KRITZAAR',
       desc='Try free tools and mini projects on KritZaar, such as an image compressor, plus small games and experiments.',
       lead='Free tools and mini projects, such as an image compressor, plus small games and experiments.',
       about=['Cool Stuff collects small tools, projects and experiments you can try right in your browser.',
              'Open any item to use it inside the site.'],
       cta='Open'),
  dict(id='ai', file='ai.html', label='AI', json='ai.json',
       title='AI Articles and News | KRITZAAR',
       desc='Read articles about artificial intelligence on KritZaar: new developments, how things work and how people use them.',
       lead='Articles about artificial intelligence: what is new, how it works and how people use it.',
       about=['Each article opens on its own reading page inside KritZaar.'],
       cta='Read'),
  dict(id='interesting', file='interesting.html', label='Interesting', json='interesting.json',
       title='Interesting Finds and Discoveries | KRITZAAR',
       desc='Discoveries and curiosities worth a look, collected on KritZaar.',
       lead='Discoveries and curiosities that are worth knowing about.',
       about=['Open an item to read more about it on KritZaar.'],
       cta='Read'),
  dict(id='conflict', file='conflict.html', label='Conflict', json='conflict.json',
       title='Conflict Explainers | KRITZAAR',
       desc='Articles about conflicts and global tensions, with background so you can follow what is happening.',
       lead='Articles about conflicts and global tensions, with background so you can follow what is happening.',
       about=['Each article opens on its own reading page inside KritZaar.'], cta='Read'),
  dict(id='updates', file='updates.html', label='Updates', json='updates.json',
       title='Site Updates | KRITZAAR',
       desc='What is new on KritZaar: new sections, features and changes to the site.',
       lead='What is new on KritZaar: new sections, features and changes to the site.',
       about=['Check here to see what has changed.'], cta='Read'),
]

def slugify(s):
    s = re.sub(r'[^a-z0-9]+', '-', str(s or '').lower().strip())
    return re.sub(r'^-+|-+$', '', s)[:80]

def clean_title(t):
    t = re.sub(r'\s+', ' ', str(t or '').replace('_', ' ')).strip()
    return t.title() if t.isupper() else t

def real(c):
    t = str(c.get('title') or '')
    if len(re.findall(r'[A-Za-z0-9]', t)) < 3: return False          # placeholders like "...."
    if 'drive.google.com' in str(c.get('url') or ''): return False    # personal Drive folders
    return True

def items_for(sec):
    path = os.path.join(REPO, sec['json'])
    if not os.path.exists(path): return []
    d = json.load(open(path, encoding='utf-8'))
    out = []
    for i, c in enumerate(d.get('cards', [])):           # main cards only (sub-sections are skipped)
        if not real(c): continue
        slug = slugify(c.get('slug')) if c.get('slug') else slugify(c.get('title'))
        slug = slug or f'article-{i}'
        kind = 'game' if c.get('type') == 'game' else 'article'
        tag = re.sub(r'\s+', ' ', str(c.get('tag') or '')).strip()
        tm = str(c.get('time') or '').strip()
        meta = ' · '.join(x for x in [tag if len(tag) > 2 else '', tm if len(tm) > 2 and tm != '..' else ''] if x)
        out.append(dict(title=clean_title(c.get('title')), kind=kind, meta=meta,
                        href=f"index.html#/{kind}/{sec['id']}/{slug}"))
    return out

E = html.escape
def page(title, desc, canonical, body, ld):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="/brand/favicon.svg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/brand/icon-192.png">
<link rel="apple-touch-icon" href="/brand/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#101114">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KRITZAAR">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/brand/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/brand/og-image.png">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="pages.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4231942641082363"
     crossorigin="anonymous"></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{body}
</body>
</html>
'''

def header(live, current):
    links = ['<a href="index.html">Home</a>', '<a href="about.html"%s>About</a>' % (' aria-current="page"' if current == 'about.html' else '')]
    for s in live:
        links.append('<a href="%s"%s>%s</a>' % (s['file'], ' aria-current="page"' if current == s['file'] else '', E(s['label'])))
    return ('<header class="top"><a class="mark" href="index.html"><img class="mark-logo" src="brand/logo-emblem-white.svg" alt="" width="28" height="30">KRITZ<span>A</span>AR</a>'
            '<nav aria-label="Sections">' + ''.join(links) + '</nav></header><div class="glow" aria-hidden="true"></div>')

def footer(live):
    links = ' '.join(['<a href="index.html">Home</a>', '<a href="about.html">About</a>'] +
                     ['<a href="%s">%s</a>' % (s['file'], E(s['label'])) for s in live])
    return f'<footer class="foot"><nav aria-label="Footer">{links}</nav><p>KRITZAAR is a free content hub. No sign-up needed.</p></footer>'

def crumbs(name, file):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "KRITZAAR", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{file}"}]}

CSS_TEMPLATE = r"""/* KritZaar static pages: matches the main site's look */
:root{--bg:@BG@;--card:@CARD@;--mint:@ACCENT@;--link:@LINK@;--slate:@SLATE@;--white:@WHITE@;--mint-glow:@GLOW@;--mint-dim:@DIM@;--line:@LINE@;--line2:@LINE2@}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{color-scheme:dark;scroll-behavior:smooth}
body{background:var(--bg);color:var(--slate);font-family:'Rajdhani',system-ui,sans-serif;font-size:17px;line-height:1.65;overflow-x:hidden}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--mint);outline-offset:3px}
.top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:18px 32px;flex-wrap:wrap}
.mark{font-family:'Orbitron',sans-serif;font-weight:900;font-size:22px;letter-spacing:-1px;color:var(--white)}
.mark-logo{height:30px;width:auto;vertical-align:middle;margin:-4px 10px 0 0}
.mark:hover{text-decoration:none}
.mark span,.ac{color:var(--link);text-shadow:0 0 24px var(--mint),0 0 60px var(--mint-glow)}
.top nav{display:flex;gap:4px 18px;flex-wrap:wrap}
.top nav a{font-size:11px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;color:var(--slate);padding:6px 0;border-bottom:2px solid transparent;transition:color .2s,border-color .2s}
.top nav a:hover,.top nav a[aria-current]{color:var(--link);border-bottom-color:var(--mint);text-decoration:none}
.glow{position:relative;height:1px;background:linear-gradient(90deg,transparent,@ACCENT55@ 50%,transparent);box-shadow:0 0 14px 1px var(--mint-glow),0 0 44px 6px var(--mint-dim)}
main{max-width:860px;margin:0 auto;padding:36px 32px 72px}
.crumbs{font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px}
h1{font-family:'Orbitron',sans-serif;font-size:clamp(30px,6vw,52px);font-weight:900;color:var(--white);letter-spacing:2px;line-height:1.1}
.lead{margin-top:16px;font-size:19px;color:var(--white);max-width:60ch}
h2{margin-top:40px;font-family:'Orbitron',sans-serif;font-size:13px;letter-spacing:4px;text-transform:uppercase;color:var(--link);padding-bottom:10px;border-bottom:1px solid var(--line);box-shadow:0 10px 18px -14px var(--mint-glow)}
h2 + p,h2 + ul,h2 + .cards{margin-top:16px}
p + p{margin-top:12px}
.items{list-style:none;display:grid;gap:10px}
.item{display:flex;align-items:center;gap:6px 14px;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;color:inherit;transition:border-color .25s,box-shadow .25s,scale .3s cubic-bezier(.34,1.56,.64,1)}
.item:hover,.item:focus-visible{border-color:var(--line2);box-shadow:0 0 18px var(--mint-glow);text-decoration:none}
.item:active,.card:active,.btn:active{scale:1.05}
.item-t{color:var(--white);font-weight:600;flex:1 1 220px;min-width:0;overflow-wrap:anywhere}
.item-m{font-size:11px;letter-spacing:2px;text-transform:uppercase}
.item-go{font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--link)}
.btn{display:inline-block;margin-top:24px;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--link);border:1px solid var(--line2);padding:12px 24px;transition:background .2s,color .2s,scale .3s cubic-bezier(.34,1.56,.64,1)}
.btn:hover{background:var(--link);color:var(--bg);text-decoration:none}
.more{display:flex;gap:6px 18px;flex-wrap:wrap}
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;color:inherit;transition:border-color .25s,box-shadow .25s,scale .3s cubic-bezier(.34,1.56,.64,1)}
.card:hover{border-color:var(--line2);box-shadow:0 0 18px var(--mint-glow);text-decoration:none}
.card-n{display:block;font-family:'Orbitron',sans-serif;font-size:14px;font-weight:900;letter-spacing:2px;text-transform:uppercase;color:var(--white)}
.card-d{display:block;font-size:15px;line-height:1.5;margin-top:6px}
.list{padding-left:20px;display:grid;gap:8px}
.list b{color:var(--white);font-weight:600}
.foot{border-top:1px solid var(--line);padding:28px 32px;text-align:center;font-size:14px}
.foot nav{display:flex;gap:6px 20px;justify-content:center;flex-wrap:wrap;margin-bottom:10px}
.foot nav a{font-size:11px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;color:var(--slate)}
.foot nav a:hover{color:var(--white)}
@media(max-width:580px){.top{padding:14px 16px}main{padding:28px 18px 56px}.cards{grid-template-columns:1fr}.lead{font-size:17px}.foot{padding:24px 16px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

def _rgb(h):
    h = h.lstrip('#'); return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
def _rgba(h, a):
    r, g, b = _rgb(h); return 'rgba(%d,%d,%d,%s)' % (r, g, b, ('%.3f' % a).rstrip('0').rstrip('.'))
def _mix(h1, h2, t):
    a, b = _rgb(h1), _rgb(h2); return '#%02x%02x%02x' % tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))

def write_css():
    th = {}
    try: th = json.load(open(os.path.join(REPO, '_index.json'), encoding='utf-8')).get('_theme', {})
    except Exception: pass
    acc = th.get('accent', '#00FFC2'); white = th.get('white', '#E8ECF0')
    vals = {'@BG@': th.get('bg', '#1A1C1E'), '@CARD@': th.get('card', '#1E2124'), '@ACCENT@': acc,
            '@LINK@': _mix(acc, white, 0.55),            # lighter accent so link text stays readable
            '@SLATE@': th.get('slate', '#9BA4B0'), '@WHITE@': white,
            '@GLOW@': _rgba(acc, (th.get('glowIntensity', 28) or 28) / 100), '@DIM@': _rgba(acc, 0.07),
            '@LINE@': _rgba(acc, 0.22), '@LINE2@': _rgba(acc, 0.55), '@ACCENT55@': _rgba(acc, 0.6)}
    css = CSS_TEMPLATE
    for k, v in vals.items(): css = css.replace(k, v)
    open(os.path.join(OUT, 'pages.css'), 'w', encoding='utf-8').write(css)

def main():
    os.makedirs(OUT, exist_ok=True)
    write_css()
    live = []
    for s in SECTIONS:
        s['items'] = items_for(s)
        if s['items']: live.append(s)
    skipped = [s['label'] for s in SECTIONS if not s['items']]

    for s in live:
        cards = ''.join(
            '<li><a class="item" href="%s"><span class="item-t">%s</span>%s<span class="item-go">%s</span></a></li>' % (
                E(it['href']), E(it['title']),
                ('<span class="item-m">%s</span>' % E(it['meta'])) if it['meta'] else '',
                s['cta'] if it['kind'] == 'article' else 'Play') for it in s['items'])
        others = ' '.join('<a href="%s">%s</a>' % (o['file'], E(o['label'])) for o in live if o is not s)
        body = f'''{header(live, s['file'])}
<main>
<p class="crumbs"><a href="index.html">Home</a> / {E(s['label'])}</p>
<h1>{E(s['label'])}</h1>
<p class="lead">{E(s['lead'])}</p>
<h2>In this section</h2>
<ul class="items">{cards}</ul>
<p><a class="btn" href="index.html#/section/{s['id']}">Open {E(s['label'])} on KritZaar</a></p>
<h2>About {E(s['label'])}</h2>
{''.join('<p>%s</p>' % E(p) for p in s['about'])}
<h2>More on KritZaar</h2>
<p class="more">{others} <a href="about.html">About</a></p>
</main>
{footer(live)}'''
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "name": s['title'].split(' | ')[0], "url": f"{SITE}/{s['file']}",
             "description": s['desc'], "isPartOf": {"@type": "WebSite", "name": "KRITZAAR", "url": SITE + "/"},
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(s['items']),
                            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": it['title']} for i, it in enumerate(s['items'])]}},
            crumbs(s['label'], s['file'])]}
        open(os.path.join(OUT, s['file']), 'w', encoding='utf-8').write(
            page(s['title'], s['desc'], f"{SITE}/{s['file']}", body, ld))

    # ---------- About ----------
    sec_cards = ''.join(
        '<a class="card" href="%s"><span class="card-n">%s</span><span class="card-d">%s</span></a>' % (s['file'], E(s['label']), E(s['lead'])) for s in live)
    contact = ('<h2>Contact</h2><p>Questions or feedback? Write to <a href="mailto:%s">%s</a>.</p>' % (E(CONTACT_EMAIL), E(CONTACT_EMAIL))) if CONTACT_EMAIL else ''
    about_desc = 'KRITZAAR is a free, dark-mode content hub with stories, free HTML games, AI articles and more. Learn what it is, how to use it, and how it handles privacy and ads.'
    body = f'''{header(live, 'about.html')}
<main>
<p class="crumbs"><a href="index.html">Home</a> / About</p>
<h1>About KRITZ<span class="ac">A</span>AR</h1>
<p class="lead">KRITZAAR is a free, dark-mode content hub. Read stories, play games, follow AI topics, and find cool things, all in one place. There is no sign-up and nothing to install, and every article or game opens right inside the site.</p>
<h2>What you will find here</h2>
<div class="cards">{sec_cards}</div>
<h2>How to use it</h2>
<ul class="list">
<li><b>Browse:</b> pick a section from the bar at the top of the site, or let the preview strip show you around.</li>
<li><b>Search:</b> type in the search box to find articles and games across every section. Searching a topic such as games also shows that section and what it is about.</li>
<li><b>Save for later:</b> tap Save on an article to keep it in your Saved tab.</li>
<li><b>Share:</b> use Share on any article or section to send a link to a friend.</li>
<li><b>Play:</b> tap Play on a game card, and use Fullscreen for the best view. If a game does not load, use Retry or open it in a new tab.</li>
</ul>
<h2>Privacy and ads</h2>
<p>You do not need an account. Your Saved items and some cached content are stored only in your own browser, on your device. KRITZAAR shows ads through Google AdSense, which may use cookies or similar technology to show and measure ads. You can manage ad personalization in your Google ad settings.</p>
<h2>About political content</h2>
<p>The Political section is for information only. KRITZAAR does not promote or endorse any political party, candidate or ideology, and shows a notice before you enter it.</p>
{contact}
<p><a class="btn" href="index.html">Start exploring</a></p>
</main>
{footer(live)}'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "name": "About KRITZAAR", "url": f"{SITE}/about.html", "description": about_desc,
         "isPartOf": {"@type": "WebSite", "name": "KRITZAAR", "url": SITE + "/"}},
        crumbs('About', 'about.html')]}
    open(os.path.join(OUT, 'about.html'), 'w', encoding='utf-8').write(
        page('About KRITZAAR: a free content hub | KRITZAAR', about_desc, f"{SITE}/about.html", body, ld))

    # ---------- sitemap ----------
    urls = [('', '1.0', 'daily'), ('about.html', '0.7', 'monthly')] + [(s['file'], '0.8', 'weekly') for s in live]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr, cf in urls:
        sm.append(f'  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>')
    sm.append('</urlset>\n')
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm))

    print('pages written:', ['about.html'] + [s['file'] for s in live])
    print('skipped (no real articles yet):', skipped)
    for s in live: print(' ', s['label'], len(s['items']), 'items')

if __name__ == '__main__':
    main()

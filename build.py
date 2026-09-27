"""Baut social-media/index.html aus dem Claude-Design-Export SocialMedia.dc.html.
Jede <section> wird zu einem Akkordeon-Eintrag (<details>)."""
import re, html, sys, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
s = SRC.read_text()

head_start = s.find('<header')
header = s[head_start:s.find('</header>') + 9]
sections = re.findall(r'<section id="([^"]+)"[^>]*>(.*?)</section>', s, re.S)

def text(x):
    return html.unescape(re.sub(r'<[^>]+>', '', x)).replace('­', '').strip()

def kind(meta):
    m = meta.lower()
    for k in ('reel', 'story', 'karussell', 'einzelgrafik'):
        if k in m:
            return {'reel': 'Reel', 'story': 'Story', 'karussell': 'Karussell', 'einzelgrafik': 'Einzelgrafik'}[k]
    return 'Profil'

items = []
for sid, body in sections:
    meta_m = re.search(r'<p style="margin:0;font-size:14px;font-weight:700;color:#5C514B">(.*?)</p>\s*', body, re.S)
    h2_m = re.search(r'<h2[^>]*>(.*?)</h2>\s*', body, re.S)
    meta, title = text(meta_m.group(1)), text(h2_m.group(1))
    # Kopf aus der Seitenleiste entfernen, er steht schon in der Akkordeon-Zeile
    body = body.replace(meta_m.group(0), '', 1).replace(h2_m.group(0), '', 1)
    parts = [p.strip() for p in meta.split('·')]
    if sid == 'profil':
        num, when = '00', 'Vor dem Start'
    else:
        num = parts[0].replace('Post', '').strip()
        when = ' · '.join(parts[1:])
    items.append((sid, num, title, when, kind(meta), body))

rows = []
for sid, num, title, when, k, body in items:
    rows.append(f'''
<details class="post" id="{sid}">
  <summary>
    <span class="num" aria-hidden="true">{num}</span>
    <span class="head">
      <span class="title">{html.escape(title)}</span>
      <span class="when">{html.escape(when)}</span>
    </span>
    <span class="kind">{k}</span>
    <span class="chev" aria-hidden="true"></span>
  </summary>
  <div class="panel"><div class="sec">{body}</div></div>
</details>''')

page = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Social-Media-Kit · Stark gegen Mobbing</title>
<meta name="description" content="Alle vorbereiteten Instagram-Posts für Stark gegen Mobbing: Grafiken, Captions, Hashtags und Alt-Texte.">
<link rel="icon" href="assets/logo-mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet" crossorigin="anonymous">
<style>
@font-face {{
  font-family: "Sink";
  src: url("assets/fonts/Sink.otf") format("opentype"), url("assets/fonts/Sink.ttf") format("truetype");
  font-weight: 400 700; font-style: normal; font-display: swap;
}}
:root {{
  --ink: #1B1513; --ink-soft: #5C514B; --red: #D62F1E; --red-dark: #8E1F13;
  --sand: #E6D8CE; --cream: #FBF3EC; --paper: #FFFFFF; --butter: #F7E8C3;
  --radius: 12px; --pill: 9999px;
  --font-display: "Sink", Impact, sans-serif;
  --font-body: "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--sand); color: var(--ink); }}
body {{ font-family: var(--font-body); font-size: 17px; line-height: 1.5; -webkit-font-smoothing: antialiased; }}
a {{ color: var(--ink); }} a:hover {{ color: var(--red-dark); }}
.skip {{ position: absolute; left: 16px; top: -60px; background: var(--ink); color: #fff; padding: 10px 16px; border-radius: var(--pill); z-index: 10; }}
.skip:focus {{ top: 16px; }}
:focus-visible {{ outline: 3px solid var(--ink); outline-offset: 3px; }}

.wrap {{ max-width: 1440px; margin: 0 auto; padding: 64px 40px 96px; }}
.top {{ display: grid; gap: 12px; max-width: 760px; margin-bottom: 40px; }}
.top h1 {{ font-size: clamp(44px, 7vw, 72px) !important; }}
.tools {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 20px; }}
.btn {{ font: 700 14px/1.2 var(--font-body); border: 0; cursor: pointer; border-radius: var(--pill); padding: 10px 18px; background: var(--ink); color: #fff; }}
.btn.ghost {{ background: transparent; color: var(--ink); box-shadow: inset 0 0 0 1.5px var(--ink); }}
.btn:hover {{ background: var(--red-dark); color: #fff; box-shadow: none; }}
.count {{ font-size: 14px; font-weight: 500; color: var(--ink-soft); margin-left: auto; }}

.list {{ display: grid; grid-template-columns: minmax(0, 1fr); gap: 10px; }}
.post {{ background: var(--cream); border-radius: var(--radius); min-width: 0; }}
.post > summary {{ list-style: none; cursor: pointer; display: grid; grid-template-columns: 56px 1fr auto 28px; gap: 20px; align-items: center; padding: 18px 24px; border-radius: var(--radius); }}
.post > summary::-webkit-details-marker {{ display: none; }}
.post > summary:hover {{ background: #F3E9E1; }}
.num {{ font-family: var(--font-display); font-weight: 700; font-size: 34px; line-height: 1; color: var(--ink); }}
.post[open] .num {{ color: var(--red); }}
.head {{ display: grid; gap: 2px; min-width: 0; }}
.title {{ font-size: 19px; font-weight: 700; line-height: 1.3; }}
.when {{ font-size: 14px; font-weight: 500; color: var(--ink-soft); }}
.kind {{ font-size: 13px; font-weight: 700; padding: 6px 12px; border-radius: var(--pill); background: var(--paper); white-space: nowrap; }}
.chev {{ width: 28px; height: 28px; border-radius: 50%; background: var(--ink); position: relative; }}
.chev::before, .chev::after {{ content: ""; position: absolute; left: 50%; top: 50%; width: 12px; height: 2px; background: #fff; transform: translate(-50%, -50%); transition: transform .2s; }}
.chev::after {{ transform: translate(-50%, -50%) rotate(90deg); }}
.post[open] .chev::after {{ transform: translate(-50%, -50%) rotate(0deg); }}

.panel {{ padding: 8px 24px 28px; }}
/* Die Sektion aus dem Design: Seitenleiste links, Motive rechts in einer waagerechten Leiste */
.sec {{ display: flex; gap: 28px; align-items: flex-start; }}
.sec > aside {{ width: 380px !important; max-width: 100%; }}
.sec > div {{ flex: 1 1 0; min-width: 0; overflow-x: auto; padding-bottom: 14px; scroll-snap-type: x proximity; }}
.sec > div > div {{ scroll-snap-align: start; }}
.sec > div::-webkit-scrollbar {{ height: 10px; }}
.sec > div::-webkit-scrollbar-thumb {{ background: #CDBDB1; border-radius: 10px; }}

/* Kopieren und Export */
.copy {{ justify-self: start; font: 700 13px/1 var(--font-body); border: 0; cursor: pointer; border-radius: var(--pill); padding: 7px 12px; background: var(--sand); color: var(--ink); }}
.copy:hover {{ background: var(--ink); color: #fff; }}
.copy.done {{ background: var(--ink); color: #fff; }}
.frame-label {{ display: flex !important; align-items: center; justify-content: space-between; gap: 12px; }}
.dl {{ font: 700 12px/1 var(--font-body); border: 0; cursor: pointer; border-radius: var(--pill); padding: 6px 11px; background: var(--paper); color: var(--ink); }}
.dl:hover {{ background: var(--ink); color: #fff; }}
.note {{ font-size: 14px; color: var(--ink-soft); margin: 28px 0 0; }}

@media (max-width: 1100px) {{
  .sec {{ flex-direction: column; }}
  .sec > aside {{ width: 100% !important; max-width: 640px; }}
  .sec > div {{ width: 100%; flex: none; }}
}}
@media (max-width: 700px) {{
  .wrap {{ padding: 40px 16px 64px; }}
  .post > summary {{ grid-template-columns: 40px 1fr 28px; gap: 14px; padding: 16px; }}
  .kind {{ display: none; }}
  .num {{ font-size: 28px; }}
  .title {{ font-size: 17px; }}
  .panel {{ padding: 4px 12px 20px; }}
  .sec > aside {{ padding: 20px !important; }}
  .sec > div {{ zoom: .6; }}
  .count {{ margin-left: 0; width: 100%; }}
}}
@media (prefers-reduced-motion: reduce) {{ .chev::before, .chev::after {{ transition: none; }} }}
</style>
</head>
<body>
<a class="skip" href="#posts">Zu den Posts springen</a>
<main class="wrap">
<div class="top">{header}</div>
<div class="tools">
  <button class="btn" type="button" data-all="open">Alle öffnen</button>
  <button class="btn ghost" type="button" data-all="close">Alle schließen</button>
  <span class="count">{len(items) - 1} Posts plus Profil · Klick auf eine Zeile öffnet Grafiken und Texte</span>
</div>
<div class="list" id="posts">{''.join(rows)}
</div>
<p class="note">Export: „PNG“ unter jedem Motiv speichert es in Originalgröße (Feed 1080 × 1350, Story 1080 × 1920). Das klappt online und über einen lokalen Server, aber nicht, wenn die Datei per Doppelklick geöffnet ist.</p>
</main>
<script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js" defer></script>
<script>
(() => {{
  const list = document.getElementById('posts');
  let bulk = false;

  // Alle öffnen / schließen
  document.querySelectorAll('[data-all]').forEach(b => b.addEventListener('click', () => {{
    const open = b.dataset.all === 'open';
    bulk = true;
    list.querySelectorAll('details.post').forEach(d => d.open = open);
    setTimeout(() => {{ bulk = false; }}, 150);
    history.replaceState(null, '', location.pathname);
  }}));

  // Deep-Link: #post-05 öffnet den Post; offener Post landet in der Adresse
  const openHash = () => {{
    const d = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (d && d.matches('details.post')) {{ d.open = true; d.scrollIntoView({{ block: 'start' }}); }}
  }};
  openHash(); addEventListener('hashchange', openHash);
  list.querySelectorAll('details.post').forEach(d => d.addEventListener('toggle', () => {{
    if (d.open && !bulk) history.replaceState(null, '', '#' + d.id);
  }}));

  // Ebenen wie im Design: Text liegt vor den Deko-Formen
  document.querySelectorAll('.sec span[aria-hidden="true"]').forEach(s => {{
    if (s.style.position !== 'absolute') return;
    s.style.zIndex = s.dataset.front ? '2' : '0';
    [...s.parentElement.children].forEach(c => {{
      if (c === s || c.getAttribute('aria-hidden') === 'true') return;
      if (c.style.position === 'absolute') {{ c.style.zIndex = '1'; return; }}
      c.style.position = 'relative'; c.style.zIndex = '1';
    }});
  }});

  // Kopieren-Knöpfe für Caption, Hashtags, Alt-Text, Skript usw.
  const addCopy = (target, label) => {{
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'copy'; b.textContent = label;
    b.addEventListener('click', async () => {{
      const txt = target.innerText.trim();
      try {{ await navigator.clipboard.writeText(txt); }}
      catch {{ const t = document.createElement('textarea'); t.value = txt; document.body.append(t); t.select(); document.execCommand('copy'); t.remove(); }}
      b.textContent = 'Kopiert'; b.classList.add('done');
      setTimeout(() => {{ b.textContent = label; b.classList.remove('done'); }}, 1400);
    }});
    target.after(b);
  }};
  document.querySelectorAll('.sec > aside').forEach(a => {{
    a.querySelectorAll(':scope > div').forEach(g => {{
      const val = g.children[1];
      if (val) addCopy(val, 'Kopieren');
    }});
    a.querySelectorAll(':scope > p').forEach(p => {{
      if (p.textContent.trim().startsWith('#')) addCopy(p, 'Hashtags kopieren');
    }});
  }});

  // PNG-Export je Motiv
  const slug = t => t.toLowerCase().replace(/[^a-z0-9äöüß]+/g, '-').replace(/^-|-$/g, '');
  document.querySelectorAll('.sec > div > div').forEach(frame => {{
    const label = frame.querySelector(':scope > p');
    const art = frame.querySelector(':scope > div');
    if (!label || !art) return;
    const post = frame.closest('details').id;
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'dl'; b.textContent = 'PNG';
    b.setAttribute('aria-label', 'Motiv ' + label.textContent.trim() + ' als PNG speichern');
    label.classList.add('frame-label'); label.append(b);
    b.addEventListener('click', async () => {{
      if (!window.htmlToImage) {{ alert('Export-Bibliothek nicht geladen. Internetverbindung prüfen.'); return; }}
      b.textContent = '…';
      try {{
        const url = await htmlToImage.toPng(art, {{ pixelRatio: 2, cacheBust: true }});
        const a = document.createElement('a');
        a.href = url; a.download = post + '_' + slug(label.firstChild.textContent) + '.png'; a.click();
        b.textContent = 'PNG';
      }} catch (e) {{
        console.warn(e); b.textContent = 'PNG';
        alert('Export hat nicht geklappt. Bitte die Online-Version nutzen oder die Seite über einen lokalen Server öffnen.');
      }}
    }});
  }});
}})();
</script>
</body>
</html>
'''
OUT.write_text(page)
print('ok', len(items), 'Einträge', len(page), 'Bytes')

"""moon5h1n3.dev built from the two brand guidelines (October 2026).

Unbinge page: "Warm Broadcast" (dark default, Sage light), Fraunces italic display, Work Sans,
lowercase UI copy, the Release Ring mark and tick meter.
Last Showing page: "Auditorium" (dark default, Matinee light), Big Shoulders Display for short
uppercase marquee moments, IBM Plex Sans and Mono, amber marquee and velvet, the ticket-stub mark.

Usage: python3 build.py [OUT_DIR] [prod|preview]   (defaults: dist prod)
"""
import pathlib
import shutil
import sys

from common import (code, esc, faq_html, fill, head, install_html, jsonld_app, jsonld_site,
                    links, table_html, COPY_JS, write_extras)
from content import SITE, UNBINGE, LAST, WORTH


# ---------------------------------------------------------------- marks
def release_ring(size=28, cls="ring"):
    """Eight ticks round a clock face. The first two carry the accent, the rest fade."""
    ticks = []
    for i in range(8):
        a = i * 45
        if i < 2:
            style = 'stroke="var(--accent)"'
        else:
            style = f'stroke="var(--text-faint)" opacity="{1 - (i - 2) * 0.1:.2f}"'
        ticks.append(f'<line x1="16" y1="3.5" x2="16" y2="9.5" stroke-width="3" stroke-linecap="round" {style} transform="rotate({a} 16 16)"/>')
    return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 32 32" aria-hidden="true">{"".join(ticks)}</svg>'


def ticket_mark(size=30, fill_var="var(--marquee)", cls="stub"):
    """Ticket stub, a notch each side, three cut-out bars 20, 13 and 6 high."""
    h = size * 0.6
    return (f'<svg class="{cls}" width="{size}" height="{h:.0f}" viewBox="0 0 50 30" aria-hidden="true">'
            f'<path fill-rule="evenodd" fill="{fill_var}" d="M4 0h42a4 4 0 0 1 4 4v7a4 4 0 0 0 0 8v7a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4v-7a4 4 0 0 0 0-8V4a4 4 0 0 1 4-4z'
            f'M15 5h5v20h-5zM24 12h5v13h-5zM33 19h5v6h-5z"/></svg>')


def stamp_mark(size=34):
    """A round passport stamp: double ring and a star."""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 34 34" aria-hidden="true" fill="none" stroke="currentColor">'
            '<circle cx="17" cy="17" r="15" stroke-width="2"/><circle cx="17" cy="17" r="11" stroke-width="1" stroke-dasharray="2 2"/>'
            '<path d="M17 11.5l1.6 3.4 3.7.4-2.8 2.5.8 3.6-3.3-1.9-3.3 1.9.8-3.6-2.8-2.5 3.7-.4z" fill="currentColor" stroke="none"/></svg>')


# Ready-made apps served as they are, from apps/<folder>/. Each one is copied into the
# built site unchanged and gets a card on the home page.
EXTRA_APPS = [
    {"folder": "waystamp", "name": "Waystamp", "icon": "icons/icon-192.png",
     "summary": "Collect an illustrated stamp for every heritage place, summit and trail you visit. Works offline, installs on your phone, and keeps your stamps on your own device.",
     "cta": "Open the app", "repo": "https://github.com/MOON5H1N3/waystamp"},
]


APPS_DIR = pathlib.Path(__file__).resolve().parent / "apps"


# ---------------------------------------------------------------- Unbinge
UB_CSS = """
:root{
 --bg:#1B1815;--sidebar:#15120F;--surface:#221E19;--border:#342E26;--accent:#D98A4B;--accent-fade:#5A4530;--on-accent:#1B1815;
 --text:#F2EDE6;--text-muted:#A89C8C;--text-faint:#716A5A;--code-bg:#15120F;
 --p-drip-bg:#D98A4B;--p-drip:#1B1815;--p-cool-bg:#7A5A2E;--p-cool:#F7E3C4;--p-pause-bg:#2C2722;--p-pause:#A89C8C;
 --p-queue-bg:#2E2A40;--p-queue:#B9B0E0;--p-done-bg:#3B5734;--p-done:#D6EDC9;--p-miss-bg:#5A2A2A;--p-miss:#F0B4B4;
 --display:"Fraunces",Georgia,serif;--ui:"Work Sans",system-ui,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){
 --bg:#FAF8F3;--sidebar:#F1EEE6;--surface:#FFFFFF;--border:#E2DDD0;--accent:#5C7A5C;--accent-fade:#B7C4AE;--on-accent:#FFFFFF;
 --text:#2B2A26;--text-muted:#6F6B5A;--text-faint:#A39F8C;--code-bg:#F1EEE6;
 --p-drip-bg:#5C7A5C;--p-drip:#FFFFFF;--p-cool-bg:#EBD9B8;--p-cool:#5E4520;--p-pause-bg:#ECE8DD;--p-pause:#6F6B5A;
 --p-queue-bg:#E5E1F2;--p-queue:#463C78;--p-done-bg:#DCE8D2;--p-done:#2F4A2A;--p-miss-bg:#F3DADA;--p-miss:#7A2626;}}
:root[data-theme="light"]{--bg:#FAF8F3;--sidebar:#F1EEE6;--surface:#FFFFFF;--border:#E2DDD0;--accent:#5C7A5C;--accent-fade:#B7C4AE;--on-accent:#FFFFFF;--text:#2B2A26;--text-muted:#6F6B5A;--text-faint:#A39F8C;--code-bg:#F1EEE6}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 1.0625rem/1.65 var(--ui)}
a{color:var(--accent);text-underline-offset:.2em}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px}
.top{border-bottom:1px solid var(--border);background:var(--sidebar)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:60px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--text)}
.brand b{font:italic 600 1.35rem/1 var(--display)}
.top nav{display:flex;gap:20px;font-weight:500;font-size:.95rem}
.top nav a{color:var(--text-muted);text-decoration:none}
.top nav a:hover{color:var(--text)}
@media (max-width:640px){.top nav a.opt{display:none}}
h1,h2{font-family:var(--display);font-style:italic;font-weight:500;letter-spacing:-.01em;line-height:1.08}
h1{font-size:clamp(2.4rem,5.6vw,4.1rem);margin:0 0 18px}
h2{font-size:clamp(1.8rem,3.6vw,2.5rem);margin:0 0 14px}
h3{font:600 1.05rem/1.3 var(--ui);margin:28px 0 8px}
.kicker{font-weight:500;color:var(--text-muted);margin:0 0 12px;display:flex;align-items:center;gap:8px}
.hero{display:grid;grid-template-columns:minmax(0,1fr);gap:40px;padding:56px 0 64px;align-items:center}
@media (min-width:900px){.hero{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr)}}
.lede{font-size:1.15rem;color:var(--text-muted);max-width:56ch;margin:0}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 0}
.btn{display:inline-flex;align-items:center;min-height:42px;padding:0 18px;border-radius:7px;font:600 .98rem var(--ui);text-decoration:none;border:1px solid var(--accent)}
.btn.primary{background:var(--accent);color:var(--on-accent)}
.btn.secondary{color:var(--accent);background:transparent}
.note{margin:22px 0 0;font-size:.95rem;color:var(--text-muted);max-width:56ch;padding-left:14px;border-left:2px solid var(--accent-fade)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:22px}
.panel .label{font-size:.85rem;font-weight:500;color:var(--text-muted);display:flex;justify-content:space-between;gap:8px}
.panel .show{font:italic 600 1.9rem/1.1 var(--display);margin:10px 0 6px}
.panel .meta{color:var(--text-muted);font-size:.95rem;margin:0 0 16px}
.pill{display:inline-block;font:700 .68rem/1 var(--ui);letter-spacing:.06em;text-transform:uppercase;padding:5px 9px;border-radius:999px;vertical-align:middle}
.pill.drip{background:var(--p-drip-bg);color:var(--p-drip)}.pill.cool{background:var(--p-cool-bg);color:var(--p-cool)}
.pill.pause{background:var(--p-pause-bg);color:var(--p-pause)}.pill.queue{background:var(--p-queue-bg);color:var(--p-queue)}
.pill.done{background:var(--p-done-bg);color:var(--p-done)}.pill.miss{background:var(--p-miss-bg);color:var(--p-miss)}
.meter{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin:6px 0 6px}
.meter i{height:6px;border-radius:2px;background:var(--border)}
.meter i.on{background:var(--accent)}
.meter-cap{font-size:.85rem;color:var(--text-muted);display:flex;justify-content:space-between}
.drops{list-style:none;margin:18px 0 0;padding:14px 0 0;border-top:1px solid var(--border)}
.drops li{display:grid;grid-template-columns:7ch minmax(0,1fr) auto;gap:10px;padding:7px 0;font-size:.97rem}
.drops .d{font-weight:600}
.drops .e{color:var(--text-muted);font-family:var(--mono);font-size:.9rem}
.drops .when{color:var(--text-faint);font-size:.9rem}
.drops li.next .when{color:var(--accent)}
.fakebtns{display:flex;gap:8px;margin-top:18px}
.fakebtns span{font:600 .9rem var(--ui);padding:8px 14px;border-radius:7px;border:1px solid var(--accent)}
.fakebtns .p{background:var(--accent);color:var(--on-accent)}.fakebtns .s{color:var(--accent)}
section{padding:60px 0;border-top:1px solid var(--border)}
.prose{max-width:66ch}
.prose p{margin:0 0 14px}
.steps{list-style:none;padding:0;margin:26px 0 0;display:grid;gap:14px;grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.steps{grid-template-columns:repeat(4,minmax(0,1fr))}}
.steps li{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px}
.steps b{display:block;font:italic 600 1.35rem/1.2 var(--display);margin:12px 0 6px}
.steps p{margin:0;color:var(--text-muted);font-size:.97rem}
.table-scroll{overflow-x:auto;margin:18px 0}
table{border-collapse:collapse;width:100%;font-size:.97rem;background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--border);vertical-align:top}
th{font-weight:600;font-size:.9rem;color:var(--text-muted);background:var(--sidebar)}
tr:last-child td{border-bottom:0}
code{font-family:var(--mono);font-size:.88em;background:var(--code-bg);border:1px solid var(--border);padding:.05em .35em;border-radius:5px}
pre.code{position:relative;background:var(--code-bg);border:1px solid var(--border);border-radius:10px;padding:16px;overflow-x:auto;font-size:.86rem;line-height:1.55;margin:10px 0 16px}
pre.code code{background:none;border:0;padding:0;font-size:inherit}
.copy{position:absolute;top:8px;right:8px;font:600 .8rem var(--ui);background:var(--surface);color:var(--text);border:1px solid var(--border);border-radius:7px;padding:4px 10px;cursor:pointer}
.features{columns:1;column-gap:44px;padding-left:1.1rem;margin:18px 0 0}
@media (min-width:760px){.features{columns:2}}
.features li{break-inside:avoid;margin:0 0 10px}
.features li::marker{color:var(--accent)}
.faq details{border-bottom:1px solid var(--border)}
.faq summary{cursor:pointer;font-weight:600;padding:16px 0;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--accent);font-size:1.3rem;line-height:1}
.faq details[open] summary::after{content:"\\2212"}
.faq .a{padding:0 0 16px;color:var(--text-muted)}
.faq .a p{margin:0}
footer{border-top:1px solid var(--border);padding:32px 0 48px;color:var(--text-muted);font-size:.93rem}
footer a{color:inherit}
"""


def ub_page(L):
    app = UNBINGE
    s = [head(title=app["title"], description=app["description"], canonical=SITE["url"] + "unbinge/", L=L,
              theme="#1B1815", fonts="family=Fraunces:ital,opsz,wght@1,9..144,500;1,9..144,600&family=Work+Sans:wght@400;500;600;700",
              css=UB_CSS, extra=jsonld_app(app))]
    s.append(f'<body><header class="top"><div class="wrap"><a class="brand" href="{L["unbinge"]}">{release_ring(26)}<b>Unbinge</b></a>'
             f'<nav aria-label="Page"><a class="opt" href="#how">how it works</a><a href="#install">install</a>'
             f'<a class="opt" href="#faq">questions</a><a href="{app["repo"]}">github</a></nav></div></header>')
    s.append('<main class="wrap"><div class="hero"><div>')
    s.append(f'<p class="kicker">{release_ring(18)} unbinge for plex</p>')
    s.append(f'<h1>{app["lede"]}</h1><p class="lede">{app["intro"]}</p>')
    s.append(f'<div class="actions"><a class="btn primary" href="#install">install with docker</a><a class="btn secondary" href="{app["repo"]}">source on github</a></div>')
    s.append(f'<p class="note">Vibe coded, tested by hand. {app["honesty"]}</p></div>')
    s.append('<figure class="panel" style="margin:0" aria-label="Example: a show releasing two episodes on Tuesdays and Fridays">'
             '<div class="label"><span>now dripping</span><span class="pill drip">dripping</span></div>'
             '<p class="show">The Lighthouse Keepers</p><p class="meta">season 1 · 2 episodes, tue and fri</p>'
             '<div class="meter" aria-hidden="true">' + '<i class="on"></i>' * 3 + '<i></i>' * 5 + '</div>'
             '<div class="meter-cap"><span>6 of 16 released</span><span>vault: 10</span></div>'
             '<ul class="drops"><li class="next"><span class="d">tue</span><span class="e">s01e07–e08</span><span class="when">next drop tonight, 9:00pm</span></li>'
             '<li><span class="d">fri</span><span class="e">s01e09–e10</span><span class="when">drops fri</span></li>'
             '<li><span class="d">tue</span><span class="e">s01e11–e12</span><span class="when">drops 13 oct</span></li></ul>'
             '<div class="fakebtns" aria-hidden="true"><span class="p">drip now</span><span class="s">pause</span></div></figure></div>')
    s.append(f'<section id="why"><div class="prose"><h2>{app["why"]["h"]}</h2>' + "".join(f"<p>{p}</p>" for p in app["why"]["p"]) + "</div></section>")
    pills = [("queue", "queued"), ("drip", "dripping"), ("cool", "cooldown"), ("done", "complete")]
    s.append(f'<section id="how"><h2>{app["how"]["h"]}</h2><p class="prose" style="color:var(--text-muted)">{app["how"]["intro"]}</p><ol class="steps">')
    for (t, d), (pc, pl) in zip(app["how"]["steps"], pills):
        s.append(f'<li><span class="pill {pc}">{pl}</span><b>{t}</b><p>{d}</p></li>')
    s.append("</ol>")
    t = app["table"]
    s.append(f'<h3>{t["h"]}</h3>{table_html(t["cols"], t["rows"])}</section>')
    s.append(f'<section id="features"><h2>{app["features_h"]}</h2><ul class="features">' + "".join(f"<li>{f}</li>" for f in app["features"]) + "</ul></section>")
    ins = app["install"]
    s.append(f'<section id="install"><div class="prose"><h2>{ins["h"]}</h2><p>{ins["intro"]}</p>{install_html(app, numbered=True)}')
    o = app["options"]
    s.append(f'<h3>{o["h"]}</h3></div>{table_html(("Setting", "What it does"), o["rows"])}<p class="prose">{o["after"]}</p></section>')
    s.append(f'<section id="faq"><h2>Questions</h2><div class="prose">{faq_html(app)}</div></section></main>')
    sk, sname, sdesc = app["sibling"]
    s.append('<footer><div class="wrap">' + "".join(f"<p>{fill(f, L)}</p>" for f in app["footer"]))
    s.append(f'<p>Also by me: <a href="{L[sk]}">{sname}</a>, which {sdesc}. More at <a href="{L["home"]}">{SITE["domain"]}</a>.</p></div></footer>')
    s.append(f"<script>{COPY_JS}</script></body></html>")
    return "\n".join(s)


# ---------------------------------------------------------------- Last Showing
LS_CSS = """
:root{
 --ground:#14110f;--raised:#1f1a16;--sunk:#0d0b09;--hairline:#3b332c;--border-control:#7d7063;
 --ink:#f3ebdc;--ink-muted:#b4a896;--marquee:#f2b33d;--marquee-text:#f2b33d;--on-marquee:#1a1206;
 --velvet:#a32a3c;--on-velvet:#fbefe6;--leaving:#ff7a6b;--later:#8fbcd4;
 --s1:4px;--s2:8px;--s3:12px;--s4:16px;--s6:24px;--s8:32px;--s12:48px;
 --r-sm:4px;--r-md:8px;--r-lg:16px;
 --marq:"Big Shoulders Display",Impact,sans-serif;--sans:"IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){
 --ground:#f5efe3;--raised:#fffaf1;--sunk:#ebe3d3;--hairline:#d6cbb8;--border-control:#8f8270;
 --ink:#1c1714;--ink-muted:#5f5448;--marquee:#eaa52b;--marquee-text:#8a5600;--on-marquee:#1a1206;
 --velvet:#8c2232;--on-velvet:#fbefe6;--leaving:#b3261e;--later:#2f6a8a;}}
:root[data-theme="light"]{--ground:#f5efe3;--raised:#fffaf1;--sunk:#ebe3d3;--hairline:#d6cbb8;--border-control:#8f8270;--ink:#1c1714;--ink-muted:#5f5448;--marquee:#eaa52b;--marquee-text:#8a5600;--velvet:#8c2232;--leaving:#b3261e;--later:#2f6a8a}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ground);color:var(--ink);font:400 1rem/1.6 var(--sans)}
a{color:var(--marquee-text);text-underline-offset:.2em}
:focus-visible{outline:2px solid var(--marquee);outline-offset:2px;border-radius:2px}
.wrap{max-width:1120px;margin:0 auto;padding:0 var(--s4)}
@media (min-width:760px){.wrap{padding:0 var(--s6)}}
.top{border-bottom:1px solid var(--hairline)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);min-height:64px}
.lockup{display:flex;align-items:center;gap:var(--s3);text-decoration:none;color:var(--ink)}
.lockup b{font:800 1.5rem/1 var(--marq);text-transform:uppercase;letter-spacing:.01em}
.top nav{display:flex;gap:var(--s6);font-size:.95rem}
.top nav a{color:var(--ink-muted);text-decoration:none}
.top nav a:hover{color:var(--ink)}
@media (max-width:640px){.top nav a.opt{display:none}}
.label{font:600 .72rem/1.45 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-muted)}
.marquee-xl{font:800 clamp(3.6rem,10vw,4.5rem)/.9 var(--marq);text-transform:uppercase;margin:0}
.marquee-s{font:700 1.5rem/1.1 var(--marq);text-transform:uppercase;margin:0;letter-spacing:.01em}
h2{font:600 clamp(1.5rem,3vw,1.9rem)/1.2 var(--sans);margin:0 0 var(--s4)}
h3{font:600 1.1rem/1.3 var(--sans);margin:var(--s8) 0 var(--s2)}
.hero{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--s12);padding-top:var(--s12);padding-bottom:var(--s12);align-items:center}
@media (min-width:920px){.hero{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.lede{font:600 clamp(1.3rem,2.4vw,1.6rem)/1.3 var(--sans);margin:var(--s4) 0 var(--s3);max-width:24ch}
.intro{color:var(--ink-muted);max-width:60ch;margin:0}
.actions{display:flex;flex-wrap:wrap;gap:var(--s2);margin:var(--s6) 0 0}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 var(--s4);border-radius:var(--r-md);font:600 .97rem var(--sans);text-decoration:none;border:1px solid var(--border-control);color:var(--ink)}
.btn.primary{background:var(--marquee);border-color:var(--marquee);color:var(--on-marquee)}
.note{margin:var(--s6) 0 0;font-size:.92rem;color:var(--ink-muted);max-width:60ch}
.pills{display:flex;gap:var(--s2);margin:0 0 var(--s4)}
.pills span{font:600 .75rem var(--mono);letter-spacing:.08em;padding:6px 14px;border-radius:999px;border:1px solid var(--hairline);color:var(--ink-muted)}
.pills span.on{background:var(--marquee);border-color:var(--marquee);color:var(--on-marquee)}
.sechead{display:flex;justify-content:space-between;align-items:baseline;gap:var(--s3);margin:0 0 var(--s3)}
.sechead .label{white-space:nowrap}
.card{background:var(--raised);border:1px solid var(--hairline);border-radius:var(--r-md);padding:var(--s4)}
.tags{display:flex;gap:var(--s2);margin:0 0 var(--s3)}
.tag{font:600 .68rem/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:5px 8px;border-radius:var(--r-sm);border:1px solid currentColor}
.tag.pick{background:var(--marquee);border-color:var(--marquee);color:var(--on-marquee)}
.tag.leaving{color:var(--leaving)}.tag.later{color:var(--later)}
.film{font:600 1.15rem/1.3 var(--sans);margin:0 0 var(--s1)}
.fmeta{color:var(--ink-muted);font-size:.92rem;margin:0 0 var(--s4)}
.data{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s3);padding:var(--s3) 0;border-top:1px solid var(--hairline);border-bottom:1px solid var(--hairline)}
.data .v{font:500 1rem var(--mono);font-variant-numeric:tabular-nums;display:block;margin-top:2px}
.fakebtns{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4)}
.fakebtns span{font:600 .88rem var(--sans);padding:8px 12px;border-radius:var(--r-md);border:1px solid var(--border-control)}
.fakebtns .p{background:var(--marquee);border-color:var(--marquee);color:var(--on-marquee)}
.fakebtns .q{border-color:transparent;color:var(--ink-muted)}
.card + .card{margin-top:var(--s3)}
section{padding:var(--s12) 0;border-top:1px solid var(--hairline)}
.velvet{background:var(--velvet);color:var(--on-velvet);border:0}
.velvet .label{color:var(--on-velvet);opacity:.85}
.velvet a{color:var(--on-velvet)}
.prose{max-width:68ch}
.prose p{margin:0 0 var(--s4)}
.steps{list-style:none;padding:0;margin:var(--s6) 0 0;display:grid;gap:var(--s6) var(--s8);grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.steps{grid-template-columns:repeat(2,minmax(0,1fr))}}
.steps li{border-top:1px solid var(--hairline);padding-top:var(--s4)}
.steps .label{color:var(--marquee-text)}
.steps b{display:block;font:600 1.15rem/1.3 var(--sans);margin:var(--s1) 0 var(--s1)}
.steps p{margin:0;color:var(--ink-muted)}
.dm{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--s8);align-items:start}
@media (min-width:920px){.dm{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}}
.discord{background:var(--sunk);border:1px solid var(--hairline);border-radius:var(--r-md);padding:var(--s4)}
.who{display:flex;align-items:center;gap:var(--s3);margin:0 0 var(--s3)}
.who .av{width:36px;height:36px;border-radius:50%;background:#0d0b09;display:grid;place-items:center}
.who b{font-weight:600}.who .app{font:600 .62rem var(--mono);background:#5865f2;color:#fff;padding:2px 5px;border-radius:3px;margin-left:6px}
.who .t{color:var(--ink-muted);font-size:.8rem;margin-left:6px}
.embed{border-left:4px solid var(--velvet);background:var(--raised);border-radius:var(--r-sm);padding:var(--s3) var(--s4)}
.embed b{display:block;margin-bottom:var(--s1)}
.embed p{margin:0 0 var(--s2);color:var(--ink-muted);font-size:.93rem}
.embed ul{list-style:none;margin:0;padding:0;font-size:.93rem}
.embed li{padding:2px 0}
.embed .n{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--ink-muted)}
.table-scroll{overflow-x:auto;margin:var(--s4) 0}
table{border-collapse:collapse;width:100%;font-size:.95rem}
th,td{text-align:left;padding:var(--s3) var(--s3);border-bottom:1px solid var(--hairline);vertical-align:top}
th{font:600 .72rem var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-muted)}
td:first-child{font-weight:600;white-space:nowrap}
code{font-family:var(--mono);font-size:.86em;background:var(--sunk);padding:.1em .35em;border-radius:var(--r-sm)}
pre.code{position:relative;background:var(--sunk);border:1px solid var(--hairline);border-radius:var(--r-md);padding:var(--s4);overflow-x:auto;font-size:.85rem;line-height:1.55;margin:var(--s2) 0 var(--s4)}
pre.code code{background:none;padding:0;font-size:inherit}
.copy{position:absolute;top:8px;right:8px;font:600 .78rem var(--sans);background:var(--raised);color:var(--ink);border:1px solid var(--border-control);border-radius:var(--r-sm);padding:4px 10px;cursor:pointer}
.features{padding-left:1.1rem;columns:1;column-gap:var(--s12);margin:var(--s4) 0 0}
@media (min-width:760px){.features{columns:2}}
.features li{break-inside:avoid;margin:0 0 var(--s2)}
.features li::marker{color:var(--marquee)}
.faq details{border-bottom:1px solid var(--hairline)}
.faq summary{cursor:pointer;font-weight:600;padding:var(--s4) 0;list-style:none;display:flex;justify-content:space-between;gap:var(--s4)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--marquee-text);font-size:1.3rem;line-height:1}
.faq details[open] summary::after{content:"\\2212"}
.faq .a{padding:0 0 var(--s4);color:var(--ink-muted)}
.faq .a p{margin:0}
footer{border-top:1px solid var(--hairline);padding:var(--s8) 0 var(--s12);color:var(--ink-muted);font-size:.9rem}
footer a{color:inherit}
@media (prefers-reduced-motion:no-preference){.btn,.faq summary::after{transition:background-color .15s ease-out,color .15s ease-out}}
"""


def ls_page(L):
    app = LAST
    s = [head(title=app["title"], description=app["description"], canonical=SITE["url"] + "last-showing/", L=L,
              theme="#14110f", fonts="family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;600",
              css=LS_CSS, extra=jsonld_app(app))]
    s.append(f'<body><header class="top"><div class="wrap"><a class="lockup" href="{L["last"]}">{ticket_mark(36)}<b>Last Showing</b></a>'
             f'<nav aria-label="Page"><a class="opt" href="#how">How it decides</a><a href="#install">Install</a>'
             f'<a class="opt" href="#faq">Questions</a><a href="{app["repo"]}">GitHub</a></nav></div></header>')
    s.append('<main><div class="wrap hero"><div>')
    s.append('<p class="label">Free and self-hosted, for Vue in the UK</p><h1 class="marquee-xl">Last<br>Showing</h1>')
    s.append(f'<p class="lede">{app["lede"]}</p><p class="intro">{app["intro"]}</p>')
    s.append(f'<div class="actions"><a class="btn primary" href="#install">Install with Docker</a><a class="btn" href="{app["repo"]}">Source on GitHub</a></div>')
    s.append(f'<p class="note">Vibe coded, tested by hand. {app["honesty"]}</p></div>')
    s.append('<figure style="margin:0" aria-label="Example plan: one ticket pick leaving soon, one film to catch later at home">'
             '<div class="pills" aria-hidden="true"><span class="on">OCT</span><span>NOV</span><span>DEC</span></div>'
             '<div class="sechead"><p class="marquee-s">Your ticket picks</p><span class="label">1 of 2 tickets</span></div>'
             '<div class="card"><div class="tags"><span class="tag pick">Ticket pick</span><span class="tag leaving">Leaving soon</span></div>'
             '<p class="film">The Night Projectionist</p><p class="fmeta">Drama · 2h 14m · IMAX showings. Directed by someone you rate 0.6★ above your average.</p>'
             '<div class="data"><div><span class="label">For you</span><span class="v">4.4★</span></div><div><span class="label">On in a week</span><span class="v">38%</span></div><div><span class="label">Go by</span><span class="v">Thu 8 Oct</span></div></div>'
             '<div class="fakebtns" aria-hidden="true"><span class="p">Used a ticket</span><span>I\'m seeing this</span><span class="q">Not for me</span></div></div>'
             '<div class="card"><div class="tags"><span class="tag later">Catching later</span></div>'
             '<p class="film">A Quiet Kind of Weather</p><p class="fmeta">Drama · 1h 48m. Just as good at home.</p>'
             '<div class="data"><div><span class="label">For you</span><span class="v">4.1★</span></div><div><span class="label">On in a month</span><span class="v">81%</span></div><div><span class="label">Rent from</span><span class="v">~Dec</span></div></div></div>'
             '</figure></div>')
    s.append(f'<section id="why" class="velvet"><div class="wrap"><div class="prose"><p class="label">The problem</p><h2>{app["why"]["h"]}</h2>'
             + "".join(f"<p>{p}</p>" for p in app["why"]["p"]) + "</div></div></section>")
    s.append(f'<section id="how"><div class="wrap"><h2>{app["how"]["h"]}</h2><p class="prose" style="color:var(--ink-muted)">{app["how"]["intro"]}</p><ol class="steps">')
    for i, (t, d) in enumerate(app["how"]["steps"], 1):
        s.append(f'<li><span class="label">Step {i}</span><b>{t}</b><p>{d}</p></li>')
    s.append("</ol></div></section>")
    s.append('<section id="dm"><div class="wrap dm"><div class="prose"><p class="label">On the 1st of the month</p><h2>The plan arrives as a Discord DM</h2>'
             '<p>The decision comes first, then one line per film. Buttons under the message let you mark a ticket as used, pin a film to a month, or rule it out, without opening the dashboard.</p>'
             '<p>If something stops working, such as a rejected key or a step that fails twice in a row, it tells you in the same place, and again when it\'s fixed.</p></div>'
             '<div class="discord" aria-label="Example Discord message from Last Showing">'
             f'<div class="who"><span class="av">{ticket_mark(24)}</span><span><b>Last Showing</b><span class="app">APP</span><span class="t">Today at 09:00</span></span></div>'
             '<div class="embed"><b>Your October plan</b><p>2 tickets, 3 films worth it. Use one by Thu 8 Oct.</p><ul>'
             '<li>The Night Projectionist <span class="n">· 4.4★ · go by Thu 8 Oct</span></li>'
             '<li>Harbour Lights <span class="n">· 4.2★ · go by Sun 25 Oct</span></li>'
             '<li>A Quiet Kind of Weather <span class="n">· 4.1★ · Catching later</span></li></ul></div>'
             '<div class="fakebtns" aria-hidden="true"><span class="p">Used a ticket</span><span>I\'m seeing this</span><span class="q">Not for me</span></div>'
             '</div></div></section>')
    t = app["table"]
    s.append(f'<section id="pages"><div class="wrap"><h2>{t["h"]}</h2>{table_html(t["cols"], t["rows"])}<p class="prose">{t["after"]}</p></div></section>')
    s.append(f'<section id="features"><div class="wrap"><h2>{app["features_h"]}</h2><ul class="features">' + "".join(f"<li>{f}</li>" for f in app["features"]) + "</ul></div></section>")
    ins = app["install"]
    s.append(f'<section id="install"><div class="wrap"><div class="prose"><h2>{ins["h"]}</h2><p>{ins["intro"]}</p>{install_html(app, numbered=True)}')
    o = app["options"]
    s.append(f'<h3>{o["h"]}</h3></div>{table_html(("Setting", "What it does"), o["rows"])}<p class="prose">{o["after"]}</p></div></section>')
    s.append(f'<section id="faq"><div class="wrap"><h2>Questions</h2><div class="prose">{faq_html(app)}</div></div></section></main>')
    sk, sname, sdesc = app["sibling"]
    s.append('<footer><div class="wrap">' + "".join(f"<p>{fill(f, L)}</p>" for f in app["footer"]))
    s.append(f'<p>Also by me: <a href="{L[sk]}">{sname}</a>, which {sdesc}. More at <a href="{L["home"]}">{SITE["domain"]}</a>.</p></div></footer>')
    s.append(f"<script>{COPY_JS}</script></body></html>")
    return "\n".join(s)


# ---------------------------------------------------------------- Worth Keeping
# Same family as Last Showing (shared neutrals, type, spacing); only the brand colour
# (keeper lavender), the identity colour (cloth green) and the mark change.
def shelf_mark(size=34):
    return ('<svg width="%d" height="%d" viewBox="0 0 96 96" aria-hidden="true"><rect width="96" height="96" rx="20" fill="var(--velvet)"/>'
            '<g transform="translate(16 14)" fill="#f3ebdc"><rect x="4" y="25" width="10" height="31" rx="1.5"/><rect x="17" y="19" width="10" height="37" rx="1.5"/>'
            '<path fill-rule="evenodd" fill="#b39cf0" d="M31.5 4h11a1.5 1.5 0 0 1 1.5 1.5v49a1.5 1.5 0 0 1-1.5 1.5h-11a1.5 1.5 0 0 1-1.5-1.5v-49A1.5 1.5 0 0 1 31.5 4zM33 11v2.5h8V11zM33 45v2.5h8V45z"/>'
            '<rect x="51" y="27" width="10" height="29" rx="1.5" transform="rotate(-9 51 56)"/><rect x="2" y="58" width="60" height="4" rx="1"/></g></svg>') % (size, size)


def _wk_css():
    c = LS_CSS
    dark, light = c.split("@media (prefers-color-scheme:light)", 1)
    dark = (dark.replace("#f2b33d", "#b39cf0").replace("--on-marquee:#1a1206", "--on-marquee:#1a1030")
                .replace("#a32a3c", "#245442"))
    light = (light.replace("--marquee:#eaa52b", "--marquee:#5e3fae").replace("--marquee-text:#8a5600", "--marquee-text:#5e3fae")
                  .replace("--on-marquee:#1a1206", "--on-marquee:#fffaf1").replace("#8c2232", "#1f4a3a")
                  .replace("--marquee:#eaa52b", "--marquee:#5e3fae").replace("--marquee-text:#8a5600", "--marquee-text:#5e3fae"))
    return dark + "@media (prefers-color-scheme:light)" + light + "\n.velvet{--on-velvet:#f3ebdc}\n.lockup .mk{display:block;border-radius:8px}"


WK_CSS = _wk_css()


def wk_page(L):
    app = WORTH
    s = [head(title=app["title"], description=app["description"], canonical=SITE["url"] + "worth-keeping/", L=L,
              theme="#14110f", fonts="family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;600",
              css=WK_CSS, extra=jsonld_app(app))]
    s.append(f'<body><header class="top"><div class="wrap"><a class="lockup" href="{L["worth"]}"><span class="mk">{shelf_mark(32)}</span><b>Worth Keeping</b></a>'
             f'<nav aria-label="Page"><a class="opt" href="#how">How a scan works</a><a href="#install">Install</a>'
             f'<a class="opt" href="#faq">Questions</a><a href="{app["repo"]}">GitHub</a></nav></div></header>')
    s.append('<main><div class="wrap hero"><div>')
    s.append('<p class="label">Free and self-hosted, for physical media</p><h1 class="marquee-xl">Worth<br>Keeping</h1>')
    s.append(f'<p class="lede">{app["lede"]}</p><p class="intro">{app["intro"]}</p>')
    s.append(f'<div class="actions"><a class="btn primary" href="#install">Install with Docker</a><a class="btn" href="{app["repo"]}">Source on GitHub</a></div>')
    s.append(f'<p class="note">Vibe coded, tested by hand. {app["honesty"]}</p></div>')
    s.append('<figure style="margin:0" aria-label="Example scan: a Blu-ray that upgrades a DVD you own, at a good price">'
             '<div class="sechead"><p class="marquee-s">Just scanned</p><span class="label">5 012345 678900</span></div>'
             '<div class="card"><div class="tags"><span class="tag pick">Good find</span><span class="tag later">Upgrade</span></div>'
             '<p class="film">The Long Field</p><p class="fmeta">Blu-ray · 2019. You own this on DVD, and you rated it 4.5★ on Letterboxd.</p>'
             '<div class="data"><div><span class="label">Shop price</span><span class="v">£3.00</span></div><div><span class="label">Usually</span><span class="v">£6.50</span></div><div><span class="label">On Plex</span><span class="v">No</span></div></div>'
             '<div class="fakebtns" aria-hidden="true"><span class="p">Bought it</span><span>Replace the DVD</span><span class="q">Not today</span></div></div>'
             '<div class="card"><div class="tags"><span class="tag leaving">On your shelf</span></div>'
             '<p class="film">The Quiet Harbour</p><p class="fmeta">Paperback · added 12 March, £1.50 from the charity shop on the high street.</p></div>'
             '</figure></div>')
    s.append(f'<section id="why" class="velvet"><div class="wrap"><div class="prose"><p class="label">The problem</p><h2>{app["why"]["h"]}</h2>'
             + "".join(f"<p>{p}</p>" for p in app["why"]["p"]) + "</div></div></section>")
    s.append(f'<section id="how"><div class="wrap"><h2>{app["how"]["h"]}</h2><p class="prose" style="color:var(--ink-muted)">{app["how"]["intro"]}</p><ol class="steps">')
    for i, (t, d) in enumerate(app["how"]["steps"], 1):
        s.append(f'<li><span class="label">Step {i}</span><b>{t}</b><p>{d}</p></li>')
    s.append("</ol></div></section>")
    t = app["table"]
    s.append(f'<section id="verdicts"><div class="wrap"><h2>{t["h"]}</h2>{table_html(t["cols"], t["rows"])}<p class="prose">{t["after"]}</p></div></section>')
    s.append(f'<section id="features"><div class="wrap"><h2>{app["features_h"]}</h2><ul class="features">' + "".join(f"<li>{f}</li>" for f in app["features"]) + "</ul></div></section>")
    ins = app["install"]
    s.append(f'<section id="install"><div class="wrap"><div class="prose"><h2>{ins["h"]}</h2><p>{ins["intro"]}</p>{install_html(app, numbered=True)}')
    o = app["options"]
    s.append(f'<h3>{o["h"]}</h3></div>{table_html(("Service", "What it adds"), o["rows"])}<p class="prose">{o["after"]}</p></div></section>')
    s.append(f'<section id="faq"><div class="wrap"><h2>Questions</h2><div class="prose">{faq_html(app)}</div></div></section></main>')
    sk, sname, sdesc = app["sibling"]
    s.append('<footer><div class="wrap">' + "".join(f"<p>{fill(f, L)}</p>" for f in app["footer"]))
    s.append(f'<p>Also by me: <a href="{L[sk]}">{sname}</a>, which {sdesc}. More at <a href="{L["home"]}">{SITE["domain"]}</a>.</p></div></footer>')
    s.append(f"<script>{COPY_JS}</script></body></html>")
    return "\n".join(s)


# ---------------------------------------------------------------- home
HOME_CSS = """
:root{--ground:#14110f;--raised:#1f1a16;--hairline:#3b332c;--ink:#f3ebdc;--ink-muted:#b4a896;--accent:#D98A4B;--text-faint:#716A5A;--marquee:#f2b33d;--sans:"IBM Plex Sans",system-ui,sans-serif}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){--ground:#f5efe3;--raised:#fffaf1;--hairline:#d6cbb8;--ink:#1c1714;--ink-muted:#5f5448;--accent:#5C7A5C;--text-faint:#A39F8C;--marquee:#eaa52b}}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font:400 1.05rem/1.6 var(--sans)}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:4px}
.wrap{max-width:780px;margin:0 auto;padding:72px 16px 56px}
h1{font:600 clamp(2.2rem,6vw,3.2rem)/1.05 var(--sans);letter-spacing:-.02em;margin:0 0 16px}
.intro{color:var(--ink-muted);max-width:58ch;margin:0 0 40px}
a{color:inherit}
.app{display:grid;grid-template-columns:56px minmax(0,1fr);gap:4px 18px;align-items:start;text-decoration:none;padding:24px;border:1px solid var(--hairline);background:var(--raised);border-radius:10px;margin:0 0 14px}
.app .mk{grid-row:span 2;width:56px;height:56px;border-radius:12px;display:grid;place-items:center;border:1px solid var(--hairline);background:var(--ground)}
.app h2{margin:0;font-size:1.3rem;line-height:1.2}
.app.ub h2{font:italic 600 1.55rem/1.2 "Fraunces",Georgia,serif}
.app.wk h2{font:800 1.6rem/1.1 "Big Shoulders Display",Impact,sans-serif;text-transform:uppercase}
.app .wkmk{--velvet:#245442;border:0;overflow:hidden}
.app.ls h2{font:800 1.6rem/1.1 "Big Shoulders Display",Impact,sans-serif;text-transform:uppercase}
.app p{margin:4px 0 0;color:var(--ink-muted)}
.app.sp .mk{overflow:hidden;border:0}
.app.sp .mk img{display:block;width:56px;height:56px}
.app.sp h2{font:600 1.45rem/1.2 Georgia,serif}
.app .cta{grid-column:2;color:var(--ink);font-weight:600}
.app:hover{border-color:var(--ink-muted)}
footer{margin-top:36px;color:var(--ink-muted);font-size:.92rem}
"""


def home_page(L):
    s = [head(title=SITE["title"], description=SITE["description"], canonical=SITE["url"], L=L, theme="#14110f",
              fonts="family=Big+Shoulders+Display:wght@800&family=Fraunces:ital,opsz,wght@1,9..144,600&family=IBM+Plex+Sans:wght@400;600",
              css=HOME_CSS, extra=jsonld_site())]
    s.append(f'<body><main class="wrap"><h1>{SITE["domain"]}</h1><p class="intro">{SITE["intro"]} {SITE["honesty"]}</p>')
    s.append(f'<a class="app ub" href="{L["unbinge"]}"><span class="mk">{release_ring(32)}</span><h2>Unbinge</h2><p>{UNBINGE["summary"]}</p></a>')
    s.append(f'<a class="app ls" href="{L["last"]}"><span class="mk">{ticket_mark(36)}</span><h2>Last Showing</h2><p>{LAST["summary"]}</p></a>')
    s.append(f'<a class="app wk" href="{L["worth"]}"><span class="mk wkmk">{shelf_mark(56)}</span><h2>Worth Keeping</h2><p>{WORTH["summary"]}</p></a>')
    up = "" if L["home"] == "/" else L["home"].replace("index.html", "")
    for app in EXTRA_APPS:
        if (APPS_DIR / app["folder"] / "index.html").exists():
            href = f'/{app["folder"]}/' if L["home"] == "/" else f'{up}{app["folder"]}/index.html'
            icon = href.replace("index.html", "") + app["icon"]
            s.append(f'<a class="app sp" href="{href}"><span class="mk"><img src="{icon}" width="56" height="56" alt=""></span><h2>{app["name"]}</h2><p>{app["summary"]}</p><p class="cta">{app["cta"]}</p></a>')
    code = [f'<a href="{UNBINGE["repo"]}">Unbinge</a>', f'<a href="{LAST["repo"]}">Last Showing</a>', f'<a href="{WORTH["repo"]}">Worth Keeping</a>'] + [
        f'<a href="{a["repo"]}">{a["name"]}</a>' for a in EXTRA_APPS if (APPS_DIR / a["folder"] / "index.html").exists()]
    s.append(f'<footer>The code for each app is on GitHub: {", ".join(code[:-1])} and {code[-1]}. All are MIT licensed. Unbinge, Last Showing and Worth Keeping run in Docker on your own computer; {EXTRA_APPS[0]["name"]} runs in your browser.</footer></main></body></html>')
    return "\n".join(s)


NOT_FOUND = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>:root{--g:#14110f;--i:#f3ebdc;--m:#b4a896}@media (prefers-color-scheme:light){:root{--g:#f5efe3;--i:#1c1714;--m:#5f5448}}body{margin:0;background:var(--g);color:var(--i);font:1.05rem/1.6 system-ui,sans-serif}main{max-width:560px;margin:0 auto;padding:96px 16px}h1{font-size:1.8rem;margin:0 0 .5rem}p{color:var(--m)}a{color:inherit}</style></head>
<body><main><h1>There's no page here</h1><p>Try <a href="/unbinge/">Unbinge</a>, <a href="/last-showing/">Last Showing</a> or the <a href="/">home page</a>.</p></main></body></html>
"""


def build(out, mode):
    out = pathlib.Path(out)
    for d in ("", "unbinge", "last-showing", "worth-keeping"):
        (out / d).mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(home_page(links(0, mode)))
    (out / "unbinge/index.html").write_text(ub_page(links(1, mode)))
    (out / "last-showing/index.html").write_text(ls_page(links(1, mode)))
    (out / "worth-keeping/index.html").write_text(wk_page(links(1, mode)))
    write_extras(out, mode)
    for app in EXTRA_APPS:
        src = APPS_DIR / app["folder"]
        if src.exists():
            shutil.copytree(src, out / app["folder"], dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("README*", ".DS_Store"))
    if mode == "prod":
        (out / "404.html").write_text(NOT_FOUND)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "dist", sys.argv[2] if len(sys.argv) > 2 else "prod")

"""Helpers shared by the three design builds."""
import html as _html
import json
import re

from content import SITE, APPS

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><style>path{fill:#1D1D22}@media (prefers-color-scheme:dark){path{fill:#EDEDF0}}</style><path d="M40 6a26 26 0 1 0 18 44A22 22 0 0 1 40 6z"/></svg>\n'


def links(depth, mode):
    """Page links. prod = clean URLs for GitHub Pages; preview = relative files that work anywhere."""
    if mode == "prod":
        return {"home": "/", "unbinge": "/unbinge/", "last": "/last-showing/", "worth": "/worth-keeping/", "favicon": "/favicon.svg"}
    up = "../" * depth
    return {"home": up + "index.html", "unbinge": up + "unbinge/index.html",
            "last": up + "last-showing/index.html", "worth": up + "worth-keeping/index.html", "favicon": up + "favicon.svg"}


def fill(s, L):
    return s.replace("{home}", L["home"]).replace("{unbinge}", L["unbinge"]).replace("{last}", L["last"])


def esc(s):
    return _html.escape(s, quote=True)


def text(fragment):
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", _html.unescape(fragment)).strip()


def head(*, title, description, canonical, L, theme, fonts, css, extra=""):
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="{L['favicon']}" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['domain']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
{extra}<style>
{css}
</style>
</head>
"""


def jsonld_app(app):
    url = SITE["url"] + app["slug"] + "/"
    author = {"@type": "Person", "name": SITE["author"], "url": SITE["github"]}
    lic = app.get("license", "https://opensource.org/licenses/MIT")
    graph = [
        {"@type": "SoftwareApplication", "@id": url + "#app", "name": app["name"],
         "description": app["description"], "url": url,
         "applicationCategory": app["category"], "operatingSystem": "Docker (Linux, Windows, macOS)",
         "softwareRequirements": "Docker with Compose",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"},
         "author": author, "keywords": app["keywords"], **({} if app.get("soon") else {"sameAs": [app["repo"]]})},
        *([] if app.get("soon") else [{"@type": "SoftwareSourceCode", "name": app["name"], "codeRepository": app["repo"],
                                       "programmingLanguage": "Python", "author": author}]),
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}}
            for q, a in app["faq"]]},
    ]
    if lic:
        for g in graph[:2]:
            if g["@type"] != "FAQPage":
                g["license"] = lic
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
            + "\n</script>\n")


def jsonld_site():
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": SITE["domain"],
                          "url": SITE["url"], "author": {"@type": "Person", "name": SITE["author"], "url": SITE["github"]}})
            + "</script>\n")


def code(src, cls="code"):
    return f'<pre class="{cls}"><code>{esc(src)}</code></pre>'


def faq_html(app, cls="faq"):
    out = [f'<div class="{cls}">']
    for q, a in app["faq"]:
        out.append(f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>')
    out.append("</div>")
    return "\n".join(out)


def install_html(app, step_tag="h3", numbered=False):
    out = []
    for i, st in enumerate(app["install"]["steps"], 1):
        label = f"{i}. {st['h']}" if numbered else st["h"]
        out.append(f"<{step_tag}>{label}</{step_tag}>")
        for p in st.get("p", []):
            out.append(f"<p>{p}</p>")
        if "list" in st:
            out.append("<ul>" + "".join(f"<li>{li}</li>" for li in st["list"]) + "</ul>")
        if "code" in st:
            out.append(code(st["code"]))
        for p in st.get("after", []):
            out.append(f"<p>{p}</p>")
    return "\n".join(out)


def table_html(cols, rows, cls="tbl"):
    th = "".join(f"<th>{c}</th>" for c in cols)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


COPY_JS = """
document.querySelectorAll('pre').forEach(function(pre){
  var b=document.createElement('button');b.className='copy';b.type='button';b.textContent='Copy';
  b.addEventListener('click',function(){
    var t=pre.querySelector('code').innerText;
    (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)}).catch(function(){b.textContent='Select and copy'});
  });
  pre.appendChild(b);
});
"""


def write_extras(root, mode):
    """robots, sitemap, llms.txt, 404, favicon, CNAME: same for every design."""
    (root / "favicon.svg").write_text(FAVICON)
    if mode != "prod":
        return
    (root / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: https://moon5h1n3.dev/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{u}</loc><lastmod>2026-10-09</lastmod></url>\n"
                   for u in [SITE["url"]] + [SITE["url"] + a["slug"] + "/" for a in APPS])
    (root / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    lines = [f"# {SITE['domain']}", "",
             "> Free, open-source (MIT), self-hosted Docker apps by MOON5H1N3. Both are vibe coded (written with AI coding tools) and tested by hand.", "",
             "## Apps", ""]
    for a in APPS:
        lines.append(f"- [{a['name']}]({SITE['url']}{a['slug']}/): {a['description']} "
                     + ("Not released yet." if a.get("soon") else f"Source: {a['repo']}"))
    (root / "llms.txt").write_text("\n".join(lines) + "\n")

"""Levitt Houston: Squarespace export.
Run after build.py:  python3 squarespace.py
Writes squarespace/ with one paste-ready code block per page, plus the site-wide header and footer injection.
Images, CSS, JS and calendar files load from the GitHub Pages preview, so push the repo first."""
import os, re

ASSETS = "https://jbroadfoot.github.io/levitthouston/"   # GitHub Pages copy of this repo

# Built file -> Squarespace page URL slug
SLUGS = {
    "index.html": "/", "concerts.html": "/concerts", "march-20-2027.html": "/march-20-2027",
    "may-1-2027.html": "/may-1-2027", "musicfest.html": "/musicfest", "pavilion.html": "/pavilion",
    "levitt-network.html": "/levitt-network", "get-involved.html": "/get-involved",
    "donate.html": "/donate", "about.html": "/about", "contact.html": "/contact",
}

def convert(html):
    # internal page links -> clean Squarespace slugs, keeping ?query and #anchor
    def link(m):
        page, rest = m.group(1), m.group(2) or ""
        return f'href="{SLUGS[page]}{rest}"'
    html = re.sub(r'href="(' + "|".join(re.escape(k) for k in SLUGS) + r')([?#][^"]*)?"', link, html)
    for page, slug in SLUGS.items():
        html = html.replace(f'"href": "{page}"', f'"href": "{slug}"')
        html = html.replace(f'levitthouston.org/{page}', f'levitthouston.org{slug}')
    # same-page query links like href="?interest=volunteer#connect" stay as they are
    # assets -> absolute GitHub Pages URLs
    html = re.sub(r'(src|href)="(images/[^"]+|[^"/]+\.ics)"', lambda m: f'{m.group(1)}="{ASSETS}{m.group(2)}"', html)
    return html

os.makedirs("squarespace", exist_ok=True)
rows = []
for fname, slug in SLUGS.items():
    src = open(fname).read()
    title = re.search(r"<title>(.*?)</title>", src).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', src).group(1)
    schema = "".join(re.findall(r'<script type="application/ld\+json">.*?</script>\n?', src, re.S))
    body = re.search(r"<body>\n(.*?)<script src=\"site.js\" defer></script>", src, re.S).group(1)
    block = convert(f'<div class="lh-page">\n{body}</div>\n{schema}')
    out = "squarespace/" + ("home" if fname == "index.html" else fname.replace(".html", "")) + ".html"
    open(out, "w").write(block)
    rows.append((slug, out, title, desc))

for old in ("squarespace/header-injection.html", "squarespace/footer-injection.html"):
    if os.path.exists(old): os.remove(old)
open("squarespace/page-injection.html", "w").write(f'''<!-- Levitt Houston: paste into EACH new page > Page Settings > Advanced > Page Header Code Injection.
     Page level only, so the current live pages keep their look until cutover. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ASSETS}site.css">
<link rel="stylesheet" href="{ASSETS}squarespace/squarespace.css">
<script src="{ASSETS}site.js" defer></script>
''')
open("squarespace/squarespace.css", "w").write('''/* Levitt Houston on Squarespace: hide Squarespace's own header and footer
   and let our code block run full width. First pass; tune after a live look. */
body:has(.lh-page) #header, body:has(.lh-page) header#header,
body:has(.lh-page) #footer-sections, body:has(.lh-page) footer.sections { display: none !important; }
.page-section:has(.lh-page), .page-section:has(.lh-page) .content-wrapper,
.page-section:has(.lh-page) .content, .page-section:has(.lh-page) .fluid-engine,
.page-section:has(.lh-page) .fe-block, .page-section:has(.lh-page) .sqs-block,
.page-section:has(.lh-page) .sqs-block-content {
  padding: 0 !important; margin: 0 !important; max-width: none !important; width: 100% !important;
  min-height: 0 !important; display: block !important; grid-column: 1 / -1 !important; grid-row: auto !important;
}
.page-section:has(.lh-page) .section-background { display: none !important; }
body:has(.lh-page) #page, body:has(.lh-page) main#page, body:has(.lh-page) .sections { padding-top: 0 !important; margin-top: 0 !important; }
body:has(.lh-page) { overflow-x: clip; }
.lh-page { font-family: var(--body); color: var(--ink); background: #fff; font-size: 17px; line-height: 1.65; }
.lh-page h1, .lh-page h2, .lh-page h3, .lh-page h4 { font-family: var(--display); font-weight: 600; text-transform: none; letter-spacing: -0.01em; }
.lh-page p, .lh-page li { font-family: var(--body); }
.lh-page .btn, .lh-page .kicker, .lh-page .textlink, .lh-page .nav-links a.top { font-family: var(--display); }
.lh-page ul { margin: 0; }
.lh-page img { max-width: 100%; }
.lh-page .nextbar p, .lh-page .chips li, .lh-page .caps li, .lh-page .roster li, .lh-page .partner-tiles li, .lh-page .footer-grid h2 { font-family: var(--display); }
''')

readme = ["# Levitt Houston on Squarespace\n",
"Setup, once:",
"1. Push this whole repo to GitHub (jbroadfoot/levitthouston) and turn on GitHub Pages. Images, CSS, JS and calendar files load from there.",
"2. Open https://jbroadfoot.github.io/levitthouston/ in a browser and confirm it loads before touching Squarespace.",
"",
"Each page:",
"1. Add a blank page with the URL slug below. Keep new pages in Not Linked until cutover so the live site is untouched.",
"2. Page Settings > Advanced > Page Header Code Injection: paste squarespace/page-injection.html. Use page level, never site wide, so live pages are untouched.",
"3. Add one Code Block, turn off 'Display Source', and paste the matching file.",
"4. In the page's SEO settings, paste the title and description below.",
"",
"| Slug | File | SEO title | SEO description |", "|---|---|---|---|"]
readme += [f"| {s} | {o} | {t.replace(chr(124), chr(92)+chr(124))} | {d} |" for s, o, t, d in rows]
readme += ["",
"Cutover: point the homepage at the new Home page and make sure /donate is the new Donate page, since trifold QR codes use both.",
"Forms show an 'email us' message until Squarespace Form and Newsletter Blocks go in. That is the next round."]
open("squarespace/README.md", "w").write("\n".join(readme) + "\n")
print("squarespace export:", len(rows), "pages")

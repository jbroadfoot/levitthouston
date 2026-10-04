# levitthouston (v18)

Pages (root): index, concerts, march-20-2027, may-1-2027, musicfest, pavilion, levitt-network, get-involved, donate, about, contact, 404
Also: site.css, site.js, sitemap.xml, robots.txt, build.py, images/

Edit copy in build.py, then run `python3 build.py`.

Forms: paste a form endpoint into FORM_ENDPOINT in site.js and every form submits on the page. Until then forms show an "email us at info@levitthouston.org" message. On Squarespace, native Form and Newsletter Blocks replace these forms.
SEO: canonical URLs, Open Graph, Organization and Event structured data, sitemap. PREVIEW = True adds noindex for github.io; set False for the live site.

Levitt logo: drop a white version at images/Logos/levitt-foundation-logo.png and run build.py. The Network page picks it up automatically.

Squarespace: run `python3 squarespace.py` after build.py. See squarespace/README.md.

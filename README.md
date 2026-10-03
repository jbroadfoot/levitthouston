# levitthouston

Website for Friends of Levitt Pavilion Houston. Preview on GitHub Pages, ported to Squarespace, Netlify later.

Everything lives in the root:
- Pages: index, concerts, march-20-2027, may-1-2027, musicfest, pavilion, get-involved, donate, about
- site.css (all styling), site.js (menu, logo fallback, email signup)
- squarespace-header.html and squarespace-footer.html (for Squarespace code injection)
- images/Logos, images/photos, images/posters

Copy lives in build.py. Edit it and run `python3 build.py` to regenerate all pages with the shared header and footer.
Logo files expected: images/Logos/levitt-houston-logo.svg and levitt-houston-logo-white.svg

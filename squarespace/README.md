# Levitt Houston on Squarespace

Setup, once:
1. Push this whole repo to GitHub (jbroadfoot/levitthouston) and turn on GitHub Pages. Images, CSS, JS and calendar files load from there.
2. Open https://jbroadfoot.github.io/levitthouston/ in a browser and confirm it loads before touching Squarespace.

Each page:
1. Add a blank page with the URL slug below. Keep new pages in Not Linked until cutover so the live site is untouched.
2. Page Settings > Advanced > Page Header Code Injection: paste squarespace/page-injection.html. Use page level, never site wide, so live pages are untouched.
3. Add one Code Block, turn off 'Display Source', and paste the matching file.
4. In the page's SEO settings, paste the title and description below.

| Slug | File | SEO title | SEO description |
|---|---|---|---|
| / | squarespace/home.html | Levitt Pavilion Houston \| Free Live Music in Southwest Houston | Free outdoor concerts at Willow Waterhole in Southwest Houston. Our 2027 series opens March 20, with plans underway for a permanent Levitt Pavilion. |
| /concerts | squarespace/concerts.html | 2027 Concerts \| Levitt Pavilion Houston | Free concerts at Willow Waterhole in Southwest Houston. Saturday, March 20 and Saturday, May 1, 2027, with two more planned for fall. |
| /march-20-2027 | squarespace/march-20-2027.html | Saturday, March 20, 2027 \| Free Concert \| Levitt Pavilion Houston | Free live music at Willow Waterhole on Saturday, March 20, 2027. Free admission, all ages. Artist announcement coming soon. |
| /may-1-2027 | squarespace/may-1-2027.html | Saturday, May 1, 2027 \| Free Concert \| Levitt Pavilion Houston | Free live music at Willow Waterhole on Saturday, May 1, 2027. Free admission, all ages. Artist announcement coming soon. |
| /musicfest | squarespace/musicfest.html | MusicFest \| Levitt Pavilion Houston | MusicFest has brought free live music to Willow Waterhole since 2012. Now it grows into a recurring Levitt concert series. |
| /pavilion | squarespace/pavilion.html | The Pavilion \| Levitt Pavilion Houston | Plans are moving forward for a permanent Levitt Pavilion beside Willow Waterhole Greenway in Southwest Houston. Every show is a preview of what is coming. |
| /levitt-network | squarespace/levitt-network.html | The Levitt Network \| Levitt Pavilion Houston | Levitt Houston is part of a national network of Levitt venues and concert series in more than 100 communities, building community through free live music. |
| /get-involved | squarespace/get-involved.html | Get Involved \| Levitt Pavilion Houston | Sponsor a concert, volunteer, partner or donate. Help free live music grow at Willow Waterhole in Southwest Houston. |
| /donate | squarespace/donate.html | Donate \| Levitt Pavilion Houston | Keep free live music growing in Southwest Houston. Give to Friends of Levitt Pavilion Houston, a 501(c)(3) nonprofit. |
| /about | squarespace/about.html | About \| Levitt Pavilion Houston | Levitt Pavilion Houston is a local nonprofit building community through free live music in Southwest Houston, part of the national Levitt network. |
| /contact | squarespace/contact.html | Contact \| Levitt Pavilion Houston | Contact Levitt Pavilion Houston about concerts, volunteering, sponsorship, partnerships or the permanent pavilion. |

Cutover: point the homepage at the new Home page and make sure /donate is the new Donate page, since trifold QR codes use both.
Forms show an 'email us' message until Squarespace Form and Newsletter Blocks go in. That is the next round.

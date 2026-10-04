"""Levitt Pavilion Houston v17. Builds every page with the shared header and footer.
Edit copy below, then run: python3 build.py"""
import json

DONATE = "https://square.link/u/yzNNS96a"
EMAIL = "info@levitthouston.org"
FB = "https://www.facebook.com/LevittHouston"
LOGO = "images/Logos/levitt-houston-logo.png"
PREVIEW = False  # live: allow indexing

NAV = [
  ("Concerts", "concerts.html", [("2027 Concerts", "concerts.html"), ("March 20", "march-20-2027.html"), ("May 1", "may-1-2027.html"), ("What to expect", "concerts.html#plan"), ("MusicFest", "musicfest.html")]),
  ("The Pavilion", "pavilion.html", [("The vision", "pavilion.html"), ("The site", "pavilion.html#rooted"), ("Progress", "pavilion.html#progress"), ("Help build it", "pavilion.html#build")]),
  ("Levitt Network", "levitt-network.html", []),
  ("Get Involved", "get-involved.html", [("Sponsor", "get-involved.html#sponsor"), ("Volunteer", "get-involved.html?interest=volunteer#connect"), ("Partner with us", "get-involved.html?interest=partner#connect"), ("Donate", "donate.html")]),
  ("About", "about.html", [("Our story", "about.html"), ("Partners", "about.html#partners"), ("Leadership", "about.html#leadership"), ("Contact", "contact.html")]),
]
SECTION = {"concerts.html": "concerts.html", "march-20-2027.html": "concerts.html", "may-1-2027.html": "concerts.html",
           "musicfest.html": "concerts.html", "pavilion.html": "pavilion.html", "get-involved.html": "get-involved.html",
           "about.html": "about.html", "levitt-network.html": "levitt-network.html", "contact.html": "about.html"}
SITE = "https://www.levitthouston.org/"
# One list of upcoming concerts. The next-concert bar reads this and rolls forward on its own after each date.
EVENTS = [
    {"date": "2027-03-20", "label": "Saturday, March 20", "href": "march-20-2027.html"},
    {"date": "2027-05-01", "label": "Saturday, May 1", "href": "may-1-2027.html"},
]
EVENTS_JSON = json.dumps(EVENTS)
import os, re
from PIL import Image

def mail(subject):
    return f"mailto:{EMAIL}?subject=" + subject.replace(" ", "%20")

def header(current):
    sec = SECTION.get(current, "")
    def cur(href):
        if href == current: return ' aria-current="page"'
        if href == sec: return ' data-section="current"'
        return ""
    items = "".join(f'<a class="top" href="{href}"{cur(href)}>{label}</a>' for label, href, _ in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="nextbar" data-events='{EVENTS_JSON}'><div class="wrap"><p>Next concert: {EVENTS[0]["label"]} at Willow Waterhole. Free. <a href="{EVENTS[0]["href"]}">Details</a></p></div></div>
<header class="site-header">
  <div class="nav-inner">
    <a class="brand" href="index.html"><img data-logo src="{LOGO}" alt="Levitt Pavilion Houston home" width="900" height="666"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav-links" id="site-nav" aria-label="Main">{items}<a class="btn btn-donate" href="donate.html">Donate</a></nav>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img data-logo src="{LOGO}" alt="Levitt Pavilion Houston" width="900" height="666" loading="lazy">
        <p>Building community through music. Free live music at Willow Waterhole in Southwest Houston, with a permanent Levitt Pavilion on the way.</p>
      </div>
      <div><h2>Concerts</h2><ul>
        <li><a href="concerts.html">2027 Concerts</a></li>
        <li><a href="march-20-2027.html">March 20</a></li>
        <li><a href="may-1-2027.html">May 1</a></li>
        <li><a href="musicfest.html">MusicFest</a></li></ul></div>
      <div><h2>Explore</h2><ul>
        <li><a href="pavilion.html">The Pavilion</a></li>
        <li><a href="about.html#partners">Our Partners</a></li>
        <li><a href="levitt-network.html">Levitt Network</a></li>
        <li><a href="get-involved.html">Get Involved</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="donate.html">Donate</a></li></ul></div>
      <div><h2>Connect</h2><ul>
        <li><a href="contact.html">Contact us</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{FB}">Facebook</a></li>
        <li>5300 N. Braeswood Blvd., Suite 4&#8209;202<br>Houston, TX 77096</li></ul></div>
    </div>
    <div class="footer-legal">
      <span>&copy; 2026 Friends of Levitt Pavilion Houston, Inc. A 501(c)(3) nonprofit.</span>
      <span><a href="about.html#organization">Organization information</a></span>
    </div>
  </div>
</footer>'''

PROMPTS = {
  "home": ("Be first to know who&rsquo;s playing.", "Lineups, concert details and news from Levitt Houston. A few emails a season."),
  "concerts": ("Get the lineup first.", "Artist announcements and show day details, straight to your inbox."),
  "pavilion": ("Follow the pavilion&rsquo;s progress.", "Milestones, design updates and ways to help as the permanent home comes together."),
  "get-involved": ("Stay in the loop.", "Volunteer calls, community news and concert updates. A few emails a season."),
  "musicfest": ("Keep the music going.", "Concert news, community stories and what&rsquo;s next for free music at Willow Waterhole."),
  "contact": ("Stay connected.", "Concerts, volunteer opportunities and pavilion news from Levitt Houston."),
}
def signup(src):
    h, p = PROMPTS.get(src, ("Be first to know who&rsquo;s playing.", "Artist announcements and concert details for this show."))
    return f'''<section class="ink signup" id="updates" aria-labelledby="su-{src}">
  <div class="wrap">
    <div><h2 id="su-{src}">{h}</h2>
      <p>{p}</p></div>
    <form class="signup-form" data-source="{src}" name="signup" method="POST" data-netlify="true" netlify-honeypot="_gotcha" novalidate>
      <input type="hidden" name="form-name" value="signup">
      <input type="hidden" name="source" value="{src}"><input type="hidden" name="page"><input type="hidden" name="subject">
      <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign">
      <label for="em-{src}">Email address</label>
      <input id="em-{src}" type="email" name="email" autocomplete="email" required placeholder="you@example.com">
      <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn" type="submit">Sign up</button>
      <p class="signup-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''

ORG = {"@context": "https://schema.org", "@type": "NGO", "name": "Levitt Pavilion Houston",
       "legalName": "Friends of Levitt Pavilion Houston, Inc.", "alternateName": "Levitt Houston", "url": SITE,
       "logo": SITE + "images/Logos/levitt-houston-logo.png", "email": EMAIL, "sameAs": [FB],
       "address": {"@type": "PostalAddress", "streetAddress": "5300 N. Braeswood Blvd., Suite 4-202", "addressLocality": "Houston", "addressRegion": "TX", "postalCode": "77096", "addressCountry": "US"},
       "description": "Texas nonprofit presenting free live music at Willow Waterhole in Southwest Houston and developing a permanent Levitt Pavilion."}

def keep_sentences(html):
    """Two sentence headings break between sentences, not mid sentence."""
    def fix(m):
        inner = m.group(3)
        if "<" in inner: return m.group(0)
        parts = re.split(r"(?<=\.) (?=[A-Z])", inner)
        if len(parts) < 2: return m.group(0)
        return m.group(1) + " ".join(f'<span class="keep">{x}</span>' for x in parts) + m.group(4)
    return re.sub(r"(<(h[12])\b[^>]*>)(.*?)(</\2>)", fix, html, flags=re.S)

def add_dims(html):
    def fix(m):
        tag = m.group(0)
        if " width=" in tag: return tag
        src = re.search(r'src="([^"]+)"', tag).group(1)
        if not os.path.exists(src): return tag
        if src.endswith(".svg"):
            vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', open(src).read())
            if not vb: return tag
            w, h = round(float(vb.group(1))), round(float(vb.group(2)))
        else:
            w, h = Image.open(src).size
        return tag[:-1] + f' width="{w}" height="{h}">'
    return re.sub(r'<img [^>]*>', fix, html)

GA_ID = ""  # paste the Levitt Houston GA4 measurement ID (G-XXXXXXX) to turn on analytics
PAGES = []
def page(fname, title, desc, body, schema=None, image="images/mf-sunset-stage-perme.jpg"):
    PAGES.append(fname)
    url = SITE + ("" if fname == "index.html" else fname)
    robots = '<meta name="robots" content="noindex">\n' if (PREVIEW or fname == "404.html") else ""
    blocks = [ORG] if fname == "index.html" else []
    if schema: blocks.append(schema)
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>') if GA_ID else ""
    sch = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>\n' for x in blocks)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0044AD">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Levitt Pavilion Houston">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="images/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
{ga}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css?v=20">
{sch}</head>
<body>
{header(fname)}
<main id="main">
{body}
</main>
{footer()}
<script src="site.js?v=20" defer></script>
</body>
</html>
'''
    open(fname, "w").write(keep_sentences(add_dims(html)))

INTERESTS = [("general", "General question"), ("volunteer", "Volunteering"), ("sponsor", "Sponsoring a concert"),
             ("partner", "Community or school partnership"), ("pavilion", "Permanent pavilion"), ("media", "Media")]
def form(src, default="general", button="Send"):
    opts = "".join(f'<option value="{v}"{" selected" if v == default else ""}>{l}</option>' for v, l in INTERESTS)
    return f'''<form class="lh-form" data-source="{src}" name="inquiry" method="POST" data-netlify="true" netlify-honeypot="_gotcha" novalidate>
  <input type="hidden" name="form-name" value="inquiry">
  <input type="hidden" name="source" value="{src}"><input type="hidden" name="page"><input type="hidden" name="subject">
  <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign">
  <p class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
  <div><label for="n-{src}">Name</label><input id="n-{src}" name="name" autocomplete="name" required></div>
  <div><label for="e-{src}">Email</label><input id="e-{src}" type="email" name="email" autocomplete="email" required></div>
  <div class="full"><label for="i-{src}">I&rsquo;m interested in</label><select id="i-{src}" name="interest">{opts}</select></div>
  <div class="full"><label for="m-{src}">Message</label><textarea id="m-{src}" name="message" placeholder="Tell us a little about yourself or your organization."></textarea></div>
  <button class="btn btn-navy" type="submit">{button}</button>
  <p class="form-status full" role="status" aria-live="polite"></p>
</form>'''

def card(href, dow, day, mon):
    return f'''<a class="event" href="{href}">
  <div class="stub" aria-hidden="true"><span class="dow">{dow}</span><span class="day">{day}</span><span class="mon">{mon}</span></div>
  <div class="event-body">
    <p class="visually-hidden">Saturday, {mon.split()[0]} {day}, 2027</p>
    <h3>Free Live Music at Willow Waterhole</h3>
    <p class="status">Artist announcement coming soon</p>
    <ul class="chips"><li>Free admission</li><li>All ages</li></ul>
    <span class="go">View concert details</span>
  </div>
</a>'''
CARDS = card("march-20-2027.html", "Sat", "20", "March 2027") + card("may-1-2027.html", "Sat", "1", "May 2027")

PARTNERS = [
    ("Site and development partner", "Southwest Houston Redevelopment Authority (TIRZ 20)",
     "Acquired the Gasmer property and is leading planning and development of the broader site that will include Levitt Houston&rsquo;s future home."),
    ("National partner", "Levitt Foundation",
     "Provides the Levitt model, national expertise and ongoing support for bringing free outdoor music to Houston."),
    ("City partner", "City of Houston",
     "Longtime public partner helping advance Levitt Houston and the permanent pavilion at Willow Waterhole."),
    ("Greenway partner", "Willow Waterhole Greenspace Conservancy",
     "Steward of Willow Waterhole Greenway and longtime partner in MusicFest and community programming."),
    ("Community partner", "Brays Oaks Management District",
     "Supports the surrounding Brays Oaks community and efforts that strengthen Willow Waterhole as a regional destination."),
]
PARTNER_CARDS = "".join(f'<div class="card"><p class="role">{r}</p><h3>{n}</h3><p>{d}</p></div>' for r, n, d in PARTNERS)
PARTNER_NAMES = "".join(f"<li>{n}</li>" for _, n, _ in PARTNERS)

# ============================== HOME ==============================
home = f'''
<section class="hero hero-overlay hero-home hero-thin" aria-labelledby="h1">
  <img src="images/levitt-crowd-dancing.jpg" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="kicker">2027 Concert Series</p>
    <h1 id="h1"><span class="keep">Free live music.</span> <span class="keep">Open to all.</span></h1>
    <p class="lede" style="max-width:34em">Free concerts return to Willow Waterhole this spring. Join us Saturday, March 20 and Saturday, May 1.</p>
    <div class="btn-row"><a class="btn btn-white" href="concerts.html">2027 concerts</a><a class="btn btn-ghost-light" href="#updates">Get concert updates</a></div>
  </div>
  <span class="credit">A free Levitt concert in the national network.</span>
</section>

<section class="tint" aria-labelledby="next">
  <div class="wrap">
    <p class="kicker">Upcoming</p>
    <h2 id="next">Next on the lawn</h2>
    <p class="lede">Four free concerts in 2027. Here&rsquo;s what&rsquo;s first.</p>
    <div class="grid g2">{CARDS}</div>
    <p style="margin-top:22px">Two more concerts planned for fall. <a class="textlink" href="#updates">Get updates</a></p>
  </div>
</section>

<section aria-labelledby="exp">
  <div class="wrap split">
    <figure><img src="images/ww-picnic-blanket-cheering.jpg" alt="Friends and family on a picnic blanket enjoying a free outdoor concert" loading="lazy"></figure>
    <div>
      <p class="kicker">The experience</p>
      <h2 id="exp">Bring a chair or blanket. Bring family and friends.</h2>
      <p class="lede">Free concerts give everyone a reason to come out, spend an evening outdoors and enjoy live music together at Willow Waterhole.</p>
      <ul class="facts"><li>Free<span>No cost to attend</span></li><li>All ages<span>Kids welcome</span></li><li>Outdoors<span>On the lawn</span></li></ul>
      <div class="btn-row"><a class="textlink" href="concerts.html#plan">What to expect</a></div>
    </div>
  </div>
</section>

<section class="dark" aria-labelledby="proof">
  <div class="wrap split flip">
    <figure><img src="images/mf-aerial-2018.jpg" alt="Aerial view of the MusicFest crowd, tents and stage at Willow Waterhole in 2018" loading="lazy"><figcaption>MusicFest 2018 from above. Photo: &copy; 2018 ev1pro.com + EAMD.</figcaption></figure>
    <div>
      <p class="kicker">Proven here</p>
      <h2 id="proof">Free music at Willow Waterhole since 2012.</h2>
      <p>MusicFest has filled the lawn with local and touring artists, families and neighbors for more than a decade. Along the way, we learned how to book talent, produce a professional stage, coordinate vendors, food and beverage, parking and permits, organize volunteers, and raise local sponsorship support.</p>
      <p class="pull">MusicFest proved the audience and built the experience. The concert series is the next step.</p>
      <a class="btn btn-white" href="musicfest.html">Explore MusicFest</a>
    </div>
  </div>
</section>

<section aria-labelledby="home-pav">
  <div class="wrap split">
    <figure><img src="images/levitt-pavilion-stage.jpg" alt="A covered Levitt pavilion stage facing an open lawn" loading="lazy"><figcaption>A Levitt pavilion in the national network. A glimpse of the experience Houston is building toward.</figcaption></figure>
    <div>
      <p class="kicker">What comes next</p>
      <h2 id="home-pav">The music is here. A permanent home is next.</h2>
      <p class="lede">Plans are moving forward for a permanent Levitt Pavilion beside Willow Waterhole Greenway. It will give free concerts a home built for music and become a gathering place for artists, community partners and neighbors across Southwest Houston.</p>
      <div class="btn-row"><a class="btn btn-navy" href="pavilion.html">Explore the pavilion</a></div>
    </div>
  </div>
</section>

<section class="tint" aria-labelledby="home-net">
  <div class="wrap">
    <p class="kicker">Part of Levitt</p>
    <h2 id="home-net">Locally led. Nationally supported.</h2>
    <p class="lede">Levitt Houston is a local nonprofit working with public and community partners and backed by the experience of the national Levitt network.</p>
    <div class="proof">
      <div><h3>A proven model</h3><p>Free outdoor music, welcoming public spaces and community connection.</p></div>
      <div><h3>Built for Houston</h3><p>Local leadership and local partners are shaping Levitt around Willow Waterhole and Southwest Houston.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn-navy" href="levitt-network.html">Explore the Levitt Network</a><a class="btn btn-ghost" href="about.html#partners">Meet our partners</a></div>
  </div>
</section>

<section aria-labelledby="help">
  <div class="wrap">
    <p class="kicker">Get involved</p>
    <h2 id="help">Help keep free music growing.</h2>
    <div class="grid g3">
      <div class="card card-green"><h3>Donate</h3><p>Donations of any size help keep every concert free and open to all.</p><div class="btn-row"><a class="btn btn-navy" href="donate.html">Donate</a></div></div>
      <div class="card card-green"><h3>Volunteer</h3><p>Lend a hand on concert day and meet your neighbors doing it.</p><div class="btn-row"><a class="btn btn-ghost" href="get-involved.html?interest=volunteer#connect">Volunteer</a></div></div>
      <div class="card card-green"><h3>Sponsor</h3><p>Put your business behind free live music in Southwest Houston.</p><div class="btn-row"><a class="btn btn-ghost" href="get-involved.html#sponsor">Sponsor a concert</a></div></div>
    </div>
  </div>
</section>
{signup("home")}
'''
page("index.html", "Levitt Pavilion Houston | Free Live Music in Southwest Houston",
     "Free outdoor concerts at Willow Waterhole in Southwest Houston. Our 2027 series opens March 20, with plans underway for a permanent Levitt Pavilion.",
     home, image="images/levitt-crowd-dancing.jpg")

# ============================== CONCERTS ==============================
concerts = f'''
<section class="hero-photo" aria-labelledby="ch1">
  <img src="images/mf-sunset-stage-perme.jpg" alt="A band on the MusicFest stage at sunset, playing to a crowd on the lawn at Willow Waterhole" fetchpriority="high">
  <div class="wrap">
    <p class="kicker">2027 Concert Series</p>
    <h1 id="ch1">Meet us on the lawn.</h1>
    <p class="lede">Free concerts at Willow Waterhole begin Saturday, March 20 and Saturday, May 1, 2027.</p>
    <div class="btn-row"><a class="btn btn-white" href="#updates">Get concert updates</a></div>
  </div>
  <span class="credit">Photo: &copy; Eduardo Perme</span>
</section>

<section class="tint" id="upcoming" aria-labelledby="up">
  <div class="wrap">
    <h2 id="up">Upcoming concerts</h2>
    <p class="lede">Four free concerts are planned for 2027. March 20 and May 1 are first up, with two more concerts planned for fall.</p>
    <div class="grid g2">{CARDS}</div>
  </div>
</section>

<section id="plan" aria-labelledby="plan-h">
  <div class="wrap">
    <h2 id="plan-h">What to expect</h2>
    <p class="lede">Free. Outdoors. All ages. Bring a chair or blanket and settle in on the lawn.</p>
    <div class="grid g3">
      <div class="card"><h3>Admission</h3><p>Every concert is free and open to all.</p></div>
      <div class="card"><h3>What to bring</h3><p>Lawn chairs, blankets, sunscreen and water.</p></div>
      <div class="card"><h3>Times and location</h3><p>Start times and exact location will be posted on each concert page as the date approaches.</p></div>
      <div class="card"><h3>Parking and arrival</h3><p>Parking, entrance and arrival details will be posted before each concert.</p></div>
      <div class="card"><h3>Food and drink</h3><p>Details on food and beverage will be shared before each show.</p></div>
      <div class="card"><h3>Weather</h3><p>Weather updates will be posted here and sent to the email list.</p></div>
    </div>
  </div>
</section>

<section class="dark tight" aria-labelledby="bridge">
  <div class="wrap">
    <p class="kicker">Built on experience</p>
    <h2 id="bridge">A new series built on years of doing the work.</h2>
    <p class="lede">The 2027 series grows from more than a decade of MusicFest at Willow Waterhole, moving from a festival model to a recurring concert series.</p>
    <a class="textlink" href="musicfest.html">The MusicFest story</a>
  </div>
</section>

<section aria-labelledby="yard">
  <div class="wrap split">
    <figure><img src="images/ww-westbury-lake-aerial.jpg" alt="Aerial view of Willow Waterhole Greenway lakes, trails and a footbridge" loading="lazy"><figcaption>Willow Waterhole Greenway from above.</figcaption></figure>
    <div>
      <p class="kicker">Where</p>
      <h2 id="yard">Right in Southwest Houston&rsquo;s backyard.</h2>
      <p class="lede">Worth the trip from anywhere in Houston.</p>
      <p>Willow Waterhole Greenway is a landscape of lakes, trails, wetlands and open lawn in Southwest Houston. Come early, walk the trails, then find your spot on the lawn for free live music.</p>
    </div>
  </div>
</section>
{signup("concerts")}
'''
page("concerts.html", "2027 Concerts | Levitt Pavilion Houston",
     "Free concerts at Willow Waterhole in Southwest Houston. Saturday, March 20 and Saturday, May 1, 2027, with two more planned for fall.",
     concerts, image="images/mf-sunset-stage-perme.jpg")

# ============================== EVENTS ==============================
def event(fname, iso, day, month, other, other_label, img, alt):
    schema = {"@context": "https://schema.org", "@type": "MusicEvent", "name": "Free Live Music at Willow Waterhole",
              "startDate": iso, "eventStatus": "https://schema.org/EventScheduled",
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "isAccessibleForFree": True,
              "location": {"@type": "Place", "name": "Willow Waterhole Greenway",
                           "address": {"@type": "PostalAddress", "addressLocality": "Houston", "addressRegion": "TX", "addressCountry": "US"}},
              "organizer": {"@type": "Organization", "name": "Friends of Levitt Pavilion Houston", "url": "https://www.levitthouston.org/"},
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
              "description": "Free outdoor concert at Willow Waterhole in Southwest Houston. Artist announcement coming soon.", "image": [SITE + "images/" + img], "url": SITE + fname}
    ymd = iso.replace("-", "")
    ics = f"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Levitt Pavilion Houston//EN\r\nBEGIN:VEVENT\r\nUID:{iso}@levitthouston.org\r\nDTSTAMP:20261001T000000Z\r\nDTSTART;VALUE=DATE:{ymd}\r\nSUMMARY:Levitt Houston free concert\r\nLOCATION:Willow Waterhole Greenway, Houston, TX\r\nDESCRIPTION:Free live music at Willow Waterhole. Details at levitthouston.org\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
    body = f'''
<section class="hero event-hero">
  <div class="wrap">
    <div class="stub" aria-hidden="true"><span class="dow">Sat</span><span class="day">{day}</span><span class="mon">{month} 2027</span></div>
    <div>
      <p class="kicker">Saturday, {month} {day}, 2027</p>
      <h1>Free Live Music at Willow Waterhole</h1>
      <p class="lede">Artist announcement coming soon.</p>
      <ul class="chips"><li>Free admission</li><li>All ages welcome</li><li>Willow Waterhole Greenway</li></ul>
      <div class="btn-row"><a class="btn btn-white" href="#updates">Get concert updates</a></div>
    </div>
  </div>
</section>
<section aria-labelledby="ev">
  <div class="wrap split">
    <figure><img src="images/{img}" alt="{alt}" loading="lazy"></figure>
    <div>
      <h2 id="ev">Plan your evening</h2>
      <p class="lede">Bring a chair or blanket. Bring family and friends. We&rsquo;ll post the artist, times and arrival details here as the date gets closer.</p>
      <div class="details">
        <div class="card"><h3>Time</h3><p>Evening. Exact times to come.</p></div>
        <div class="card"><h3>Location and parking</h3><p>Willow Waterhole Greenway, Southwest Houston. Exact entrance, parking and arrival details will be posted here before the concert.</p></div>
        <div class="card"><h3>Accessibility</h3><p>Accessibility information will be posted with final event details.</p></div>
      </div>
    </div>
  </div>
</section>
<section class="tint tight"><div class="wrap"><h2 style="font-size:1.5rem">Also coming up</h2><p>Two more concerts planned for fall.</p><div class="btn-row" style="margin-top:0"><a class="textlink" href="{other}">{other_label}</a><a class="textlink" href="concerts.html">All 2027 concerts</a></div></div></section>
{signup(fname.replace(".html", ""))}
'''
    page(fname, f"Saturday, {month} {day}, 2027 | Free Concert | Levitt Pavilion Houston",
         f"Free live music at Willow Waterhole on Saturday, {month} {day}, 2027. Free admission, all ages. Artist announcement coming soon.",
         body, schema=schema, image=f"images/{img}")

event("march-20-2027.html", "2027-03-20", "20", "March", "may-1-2027.html", "Saturday, May 1, 2027",
      "ww-bluebonnets-gazebo.jpg", "Bluebonnets in bloom in front of the gazebo at Willow Waterhole at sunrise")
event("may-1-2027.html", "2027-05-01", "1", "May", "march-20-2027.html", "Saturday, March 20, 2027",
      "mf-band-stage.jpg", "A band performing on the MusicFest stage at Willow Waterhole")

# ============================== MUSICFEST ==============================
POSTERS = [("poster-2012-nov", "2012"), ("poster-2013-apr", "2013"), ("poster-2013-oct", "2013"), ("poster-2014", "2014"),
           ("poster-2015", "2015"), ("poster-2016", "2016"), ("poster-2017", "2017"), ("poster-2017-artist-village", "2017"),
           ("poster-2018", "2018"), ("poster-2019", "2019"), ("poster-2020", "2020"), ("poster-2021", "2021"),
           ("poster-2022", "2022"), ("poster-2026", "2026")]
posters = "".join(f'<figure><div class="frame"><img src="images/posters/{f}.jpg" alt="MusicFest poster, {y}" loading="lazy"></div><figcaption>{y}</figcaption></figure>' for f, y in POSTERS)

mf = f'''
<section class="hero hero-split">
  <div class="wrap">
    <div>
      <p class="kicker">MusicFest</p>
      <h1>More than a decade of free music at Willow Waterhole.</h1>
      <p class="lede">Since 2012, MusicFest and related events have brought free live music to Willow Waterhole, bringing together neighbors, families, artists, volunteers, sponsors and community partners.</p>
      <div class="btn-row"><a class="btn btn-white" href="concerts.html">2027 concerts</a></div>
    </div>
    <figure><img src="images/mf-crowd-lawn.jpg" alt="MusicFest crowd relaxing in lawn chairs under the trees at Willow Waterhole" fetchpriority="high"><figcaption>MusicFest at Willow Waterhole. Photo: &copy; Steve N. Magoon.</figcaption></figure>
  </div>
</section>

<section aria-labelledby="caps">
  <div class="wrap">
    <p class="kicker">Proven capability</p>
    <h2 id="caps">We know what it takes to put on the show.</h2>
    <p class="lede">The team behind Levitt Houston has built practical experience across every part of a free outdoor concert.</p>
    <ul class="caps"><li>Talent booking</li><li>Stage and production</li><li>Vendors, food and beverage</li><li>Parking and site logistics</li><li>Permits</li><li>Volunteers</li><li>Local sponsorship and fundraising</li><li>Local and regional artists</li><li>Community partnerships</li></ul>
  </div>
</section>

<section class="tint" aria-labelledby="shared">
  <div class="wrap split">
    <figure><img src="images/mf-brass-band.jpg" alt="A brass band performing on the MusicFest stage" loading="lazy"><figcaption>MusicFest at Willow Waterhole. Photo: &copy; Steve N. Magoon.</figcaption></figure>
    <div>
      <p class="kicker">Community</p>
      <h2 id="shared">A stage shared with the community.</h2>
      <p>MusicFest has always been about more than a headliner. Local bands, school groups, artists, vendors, volunteers, sponsors and neighborhood organizations have all helped create the day together.</p>
      <p>Student performers from local schools have shared the stage with professional musicians.</p>
      <p>That mix of professional music and local participation is what Levitt Houston can now grow into a recurring concert and community music program.</p>
    </div>
  </div>
</section>

<section aria-labelledby="post">
  <div class="wrap">
    <p class="kicker">The posters</p>
    <h2 id="post">The posters tell the story.</h2>
    <p class="lede">Across the years, MusicFest posters trace the evolution of free music at Willow Waterhole.</p>
    <div class="posters">{posters}</div>
  </div>
</section>

<section class="dark" aria-labelledby="mfnext">
  <div class="wrap">
    <p class="kicker">What&rsquo;s next</p>
    <h2 id="mfnext">From a festival model to a recurring concert series.</h2>
    <p class="lede">MusicFest proved the audience and built the experience. The next step is a recurring Levitt concert series that grows the audience, sponsors, donors and rhythm of free music at Willow Waterhole, show by show.</p>
    <div class="btn-row"><a class="btn btn-white" href="concerts.html#upcoming">Upcoming shows</a></div>
  </div>
</section>
{signup("musicfest")}
'''
page("musicfest.html", "MusicFest | Levitt Pavilion Houston",
     "MusicFest has brought free live music to Willow Waterhole since 2012. Now it grows into a recurring Levitt concert series.",
     mf, image="images/mf-crowd-lawn.jpg")

# ============================== PAVILION ==============================
POSSIBLE = [
  ("card card-green", "Artists and students", "Visiting artists can connect with young musicians through school visits, workshops and shared performance experiences."),
  ("card card-green", "Music beyond the lawn", "Pop up performances can take music into schools, neighborhoods and partner locations."),
  ("card card-green", "Local artists and cultural celebrations", "Houston musicians and community partners can help shape programs that reflect the cultures of Southwest Houston."),
  ("card card-green", "A community gathering place", "The venue can create reasons to return beyond the main concert series through partnerships and community programming."),
]
possible = "".join(f'<div class="{c}"><h3>{t}</h3><p>{d}</p></div>' for c, t, d in POSSIBLE)
def _pname(n):
    if "(TIRZ 20)" in n:
        return n.replace(" (TIRZ 20)", "") + " (TIRZ 20)"
    return n
partner_names = "".join(f'<li><span class="role">{r.replace(" partner", "")}</span>{_pname(n)}</li>' for r, n, _ in PARTNERS)

pav = f'''
<section class="hero hero-split">
  <div class="wrap">
    <div>
      <p class="kicker">Future pavilion vision</p>
      <h1>A permanent home for free live music.</h1>
      <p class="lede">The concerts begin now. The permanent Levitt Pavilion will give the music a home designed for artists, audiences and community beside Willow Waterhole Greenway in Southwest Houston.</p>
      <div class="btn-row"><a class="btn btn-white" href="#build">Help build the home for it</a><a class="btn btn-ghost-light" href="#progress">Progress</a></div>
    </div>
    <figure><img class="natural" src="images/pavilion-concept.jpg" alt="Concept illustration of a covered stage facing an open lawn filled with families at sunset" fetchpriority="high" style="max-height:560px"><figcaption>Concept illustration; design is not final.</figcaption></figure>
  </div>
</section>

<section aria-labelledby="what">
  <div class="wrap">
    <p class="kicker">What it will be</p>
    <h2 id="what">Music, nature and community together.</h2>
    <p class="lede">Levitt Pavilions pair a professional covered stage with an open lawn, built for free concerts close to home. Bring a blanket, find your spot and hear great music with your neighbors.</p>
    <div class="features">
      <div><h3>Free concerts</h3><p>Professional artists. Free admission.</p></div>
      <div><h3>Open lawn</h3><p>Room for families and friends.</p></div>
      <div><h3>Community events</h3><p>Reasons to gather beyond concert night.</p></div>
      <div><h3>Part of Levitt</h3><p>A national network of free music venues.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn-ghost" href="levitt-network.html">How Levitt venues work nationwide</a></div>
  </div>
</section>

<section class="tint" aria-labelledby="more">
  <div class="wrap">
    <p class="kicker">Beyond concert night</p>
    <h2 id="more">What a Levitt venue can make possible.</h2>
    <p class="lede">Across the Levitt network, the work extends beyond the main stage. As Levitt Houston grows, the permanent venue can create new ways for artists, students, schools and community partners to connect through music.</p>
    <div class="grid g4">{possible}</div>
    <div class="btn-row"><a class="textlink" href="levitt-network.html">See how Levitt works across the country</a></div>
  </div>
</section>

<section class="dark" aria-labelledby="preview">
  <div class="wrap">
    <p class="kicker">Starting now</p>
    <h2 id="preview">Every show is a preview of what is coming.</h2>
    <p class="lede">The 2027 concert series starts building the Levitt experience before the pavilion is built: professional music, an open lawn, neighbors together and new audiences growing show by show.</p>
    <a class="btn btn-white" href="concerts.html">2027 concert series</a>
  </div>
</section>

<section aria-labelledby="rooted">
  <div class="wrap split">
    <figure><img src="images/site-derrick-lake.jpg" alt="The historic Gasmer oil derrick seen across a lake at Willow Waterhole at dusk" loading="lazy"><figcaption>The Gasmer derrick across the water at Willow Waterhole.</figcaption></figure>
    <div>
      <p class="kicker">The site</p>
      <h2 id="rooted">A permanent home beside Willow Waterhole.</h2>
      <p class="lede">The future Levitt Pavilion will be part of the former Shell Gasmer site beside Willow Waterhole Greenway. TIRZ 20 is leading planning and development of the broader site, creating a new gateway where live music, public space and the Greenway come together.</p>
      <p>The historic oil derrick remains a landmark from the site&rsquo;s past. Levitt Houston will help define what comes next.</p>
    </div>
  </div>
</section>

<section class="tint" id="progress" aria-labelledby="prog">
  <div class="wrap">
    <p class="kicker">Progress</p>
    <h2 id="prog">Momentum, milestone by milestone.</h2>
    <ol class="timeline">
      <li><span class="yr">2012</span><h3>Willow Waterhole selected for Levitt Houston</h3><p>After a Houston site search, the Levitt Foundation and City of Houston select Willow Waterhole as the future home of a Levitt Pavilion.</p></li>
      <li><span class="yr">2019</span><h3>Gasmer becomes the future site</h3><p>The former Shell property creates a new opportunity beside the Greenway.</p></li>
      <li><span class="yr">2026</span><h3>A major public milestone</h3><p>Southwest Houston Redevelopment Authority (TIRZ 20) completes its purchase of the 17 acre Gasmer property, clearing the way for master planning and development of the broader site.</p></li>
      <li class="now"><span class="yr">2027</span><h3>The concert series begins</h3><p>Free concerts start while planning, design and fundraising continue.</p></li>
    </ol>
    <p style="margin-top:24px"><strong style="font-family:var(--display)">What comes next:</strong> master planning, design, fundraising and a growing concert series.</p>
  </div>
</section>

<section class="tight" aria-labelledby="pp">
  <div class="wrap">
    <h2 id="pp" style="font-size:1.6rem">Moving forward with strong partners.</h2>
    <ul class="partner-tiles">{partner_names}</ul>
    <div class="btn-row"><a class="btn btn-ghost" href="about.html#partners">Meet our partners</a><a class="btn btn-ghost" href="levitt-network.html">The Levitt network</a></div>
  </div>
</section>

<section class="dark" id="build" aria-labelledby="bh">
  <div class="wrap">
    <p class="kicker">Support the pavilion</p>
    <h2 id="bh">Help build the home for it.</h2>
    <p class="lede">Major gifts toward the permanent pavilion begin with a conversation. Individuals, families, foundations and companies can all be part of what comes next.</p>
    <div class="btn-row"><a class="btn btn-white" href="contact.html?interest=pavilion#connect">Talk with us about the pavilion</a><a class="btn btn-ghost-light" href="donate.html">Donate to free concerts</a></div>
  </div>
</section>
{signup("pavilion")}
'''
page("pavilion.html", "The Pavilion | Levitt Pavilion Houston",
     "Plans are moving forward for a permanent Levitt Pavilion beside Willow Waterhole Greenway in Southwest Houston. Every show is a preview of what is coming.",
     pav, image="images/pavilion-concept.jpg")

# ============================== LEVITT NETWORK ==============================
# Drop the Levitt Foundation logo (white or light version for navy) at this path and rebuild.
LEVITT_LOGO = "images/Logos/levitt-foundation-logo.png"
if os.path.exists(LEVITT_LOGO):
    LEVITT_PANEL = f'<figure class="mark-panel levitt-logo"><img src="{LEVITT_LOGO}" alt="Levitt Foundation"><figcaption>Part of the Levitt network</figcaption></figure>'
else:
    LEVITT_PANEL = '<figure class="mark-panel"><img src="images/Logos/levitt-houston-mark-concept-white.png" alt="Levitt Pavilion Houston mark"><figcaption>Part of the Levitt network</figcaption></figure>'

VENUES = [("levitt-arlington", "Levitt Pavilion Arlington", "Arlington, Texas", "Free concerts fill a downtown gathering place in North Texas.", "https://levittpavilionarlington.org"),
          ("levitt-dayton", "Levitt Pavilion Dayton", "Dayton, Ohio", "A downtown lawn where free live music brings the whole city together.", "https://levittdayton.org"),
          ("levitt-denver", "Levitt Pavilion Denver", "Denver, Colorado", "Audiences gather for free outdoor music at Ruby Hill Park.", "https://levittdenver.org"),
          ("levitt-siouxfalls", "Levitt Shell Sioux Falls", "Sioux Falls, South Dakota", "Free concerts bring the community together in the heart of Sioux Falls.", "https://www.levittsiouxfalls.org"),
          ("levitt-steelstacks", "Levitt Pavilion SteelStacks", "Bethlehem, Pennsylvania", "Free music beneath the historic blast furnaces at the SteelStacks arts campus.", "https://www.levitt.org/bethlehem"),
          ("levitt-westport", "Levitt Pavilion Westport", "Westport, Connecticut", "The original Levitt Pavilion, bringing music to the Saugatuck riverfront since 1974.", "https://levittpavilion.com")]
DEV = [("levitt-sanjose-rendering", "Levitt Pavilion San Jose", "San Jose, California", "Pop up concerts since 2022, with a permanent pavilion planned for St. James Park.", "Rendering of the future Levitt Pavilion San Jose"),
       ("levitt-neworleans", "Levitt Pavilion New Orleans", "New Orleans, Louisiana", "A future Levitt venue planned for Armstrong Park, the heart of the city&rsquo;s music heritage.", "Armstrong Park in New Orleans, future home of a Levitt venue"),
       ("pavilion-concept", "Levitt Pavilion Houston", "Houston, Texas", "Free concerts begin in 2027 at Willow Waterhole while plans for the permanent pavilion move forward.", "Concept illustration of the future Levitt Pavilion Houston")]
venues = "".join(f'<div class="venue"><img src="images/{i}.jpg" alt="{n}, free outdoor concerts on an open lawn" loading="lazy"><h3>{n}</h3><p class="where">{w}</p><p>{d}</p><a href="{u}">Official site</a></div>' for i, n, w, d, u in VENUES)
dev = "".join(f'<div class="venue dev"><img src="images/{i}.jpg" alt="{a}" loading="lazy"><h3>{n}</h3><p class="where">{w}</p><p>{d}</p>{"<a href=\"pavilion.html\">Our pavilion plans</a>" if "Houston" in n else ""}</div>' for i, n, w, d, a in DEV)

net = f'''
<section class="hero hero-split">
  <div class="wrap">
    <div>
      <p class="kicker">The Levitt network</p>
      <h1>Part of something bigger.</h1>
      <p class="lede">Across the country, Levitt venues bring people together through free outdoor concerts in welcoming public spaces. Each venue is shaped by its own city, but all share the same purpose: creating connection through music.</p>
    </div>
    <figure><img src="images/levitt-network-concert.jpg" alt="Musicians performing for a large crowd on a sloped lawn at a Levitt concert" fetchpriority="high"><figcaption>A free Levitt concert in the national network.</figcaption></figure>
  </div>
</section>

<section aria-labelledby="reach">
  <div class="wrap">
    <p class="kicker">National reach</p>
    <h2 id="reach">A movement, coast to coast.</h2>
    <div class="stats">
      <div class="stat"><div class="num">100+</div><div class="lbl">towns and cities</div></div>
      <div class="stat"><div class="num">1,000+</div><div class="lbl">free concerts each year</div></div>
      <div class="stat"><div class="num">1M+</div><div class="lbl">people reached each year</div></div>
      <div class="stat"><div class="num">1974</div><div class="lbl">first Levitt Pavilion opened in Westport</div></div>
    </div>
  </div>
</section>

<section class="tint" aria-labelledby="beyond">
  <div class="wrap">
    <p class="kicker">More than concerts</p>
    <h2 id="beyond">More than a concert series.</h2>
    <p class="lede">Across the country, Levitt organizations use free music to create stronger public spaces, support local artists and build partnerships that bring communities together.</p>
    <div class="grid g3">
      <div class="card card-green"><h3>Local artists, real stage</h3><p>Hometown musicians share the bill with touring acts.</p></div>
      <div class="card card-green"><h3>Community partnerships</h3><p>Schools, nonprofits and neighborhood organizations help shape programs.</p></div>
      <div class="card card-green"><h3>A place people return to</h3><p>Concerts and community events create repeated reasons to gather.</p></div>
    </div>
    <p class="pull">Free, live music brings friends, families, and neighbors of all ages and backgrounds together.<cite>Sharon Yazowski, President and CEO, Levitt Foundation</cite></p>
  </div>
</section>

<section aria-labelledby="econ">
  <div class="wrap">
    <p class="kicker">Public space impact</p>
    <h2 id="econ">More activity. More connection. A stronger public place.</h2>
    <p class="lede">Free, recurring programming gives people reasons to return to a public space, bringing activity, connection and a stronger sense of place over time.</p>
    <div class="grid g3">
      <div class="card card-top"><h3>An active public space</h3><p>Regular programming brings people back again and again.</p></div>
      <div class="card card-top"><h3>A stronger sense of place</h3><p>Music can help a public space become part of a community&rsquo;s identity.</p></div>
      <div class="card card-top"><h3>Built to last</h3><p>Local leadership and Levitt Foundation support help sustain the work over time.</p></div>
    </div>
  </div>
</section>

<section class="dark" aria-labelledby="hp">
  <div class="wrap split">
    {LEVITT_PANEL}
    <div>
      <p class="kicker">Houston&rsquo;s place</p>
      <h2 id="hp">Bringing the Levitt model to Houston.</h2>
      <p class="lede">Levitt Houston brings a nationally proven model for free outdoor music to Willow Waterhole, shaped by the people, music and character of Southwest Houston.</p>
      <p>We&rsquo;re starting with a recurring concert series in 2027 while continuing the work toward a permanent Levitt Pavilion. Each concert helps build the audience, partnerships and community support for what comes next.</p>
      <div class="btn-row"><a class="btn btn-white" href="pavilion.html">Explore Houston&rsquo;s pavilion plans</a></div>
    </div>
  </div>
</section>

<section aria-labelledby="venues">
  <div class="wrap">
    <p class="kicker">The venues</p>
    <h2 id="venues">Levitt venues across the country.</h2>
    <div class="grid g3">{venues}</div>
  </div>
</section>

<section class="tint" aria-labelledby="dev">
  <div class="wrap">
    <p class="kicker">In development</p>
    <h2 id="dev">Houston is not building alone.</h2>
    <p class="lede">Houston is one of several communities presenting free Levitt concerts while working toward a permanent pavilion.</p>
    <div class="grid g3">{dev}</div>
    <div class="btn-row"><a class="btn btn-navy" href="pavilion.html">Our pavilion plans</a><a class="btn btn-ghost" href="https://levitt.org">levitt.org</a></div>
  </div>
</section>
'''
page("levitt-network.html", "The Levitt Network | Levitt Pavilion Houston",
     "Levitt Houston is part of a national network of Levitt venues and concert series in more than 100 communities, building community through free live music.",
     net, image="images/levitt-network-concert.jpg")

# ============================== GET INVOLVED ==============================
gi = f'''
<section class="hero hero-overlay hero-active hero-bridge">
  <img src="images/ww-bridge-riese.jpg" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="kicker" style="color:var(--green)">Get involved</p>
    <h1>There&rsquo;s more than one way to make the music happen.</h1>
    <p class="lede">Sponsor a concert. Volunteer. Partner with us. Donate. Every one of them helps free live music grow in Southwest Houston.</p>
  </div>
</section>

<section aria-labelledby="ways">
  <div class="wrap">
    <h2 id="ways" class="visually-hidden">Ways to get involved</h2>
    <div class="grid g4" style="margin-top:0">
      <div class="card card-green"><h3>Sponsor a concert</h3><p>Put your company behind free live music and meet neighbors from across Southwest Houston.</p><div class="btn-row"><a class="btn btn-navy" href="#sponsor">Learn more</a></div></div>
      <div class="card card-green" id="volunteer"><h3>Volunteer</h3><p>Volunteer roles will grow with the series. Tell us you&rsquo;re interested and we&rsquo;ll reach out as opportunities open.</p><div class="btn-row"><a class="btn btn-ghost" href="?interest=volunteer#connect">Volunteer</a></div></div>
      <div class="card card-green" id="partner"><h3>Partner with us</h3><p>School, arts organization, neighborhood group, nonprofit or community partner? Let&rsquo;s explore how music can connect with the people you serve.</p><div class="btn-row"><a class="btn btn-ghost" href="?interest=partner#connect">Partner with us</a></div></div>
      <div class="card card-green"><h3>Donate</h3><p>Donations of any size help keep every concert free and open to all.</p><div class="btn-row"><a class="btn btn-ghost" href="donate.html">Donate</a></div></div>
    </div>
  </div>
</section>

<section class="tint" id="sponsor" aria-labelledby="sp">
  <div class="wrap">
    <p class="kicker">Sponsorship</p>
    <h2 id="sp">Put your company behind free live music.</h2>
    <p class="lede">Sponsorship underwrites professional concerts and connects your business with neighbors across Southwest Houston at a welcoming public event.</p>
    <div class="grid g3">
      <div class="card"><h3>Underwrite a show</h3><p>Help cover artists, production and site operations for a free concert.</p></div>
      <div class="card"><h3>Be part of the community</h3><p>Show up where your customers and neighbors spend an evening together.</p></div>
      <div class="card"><h3>Grow with the series</h3><p>Start with the 2027 season and grow alongside Levitt Houston.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn-navy" href="?interest=sponsor#connect">Ask about sponsorship</a></div>
  </div>
</section>

<section id="connect" aria-labelledby="cn">
  <div class="wrap split">
    <div>
      <p class="kicker">Connect</p>
      <h2 id="cn">Tell us how you&rsquo;d like to help.</h2>
      <p class="lede">Volunteer, sponsor, partner or just learn more. Send a quick note and someone from Levitt Houston will follow up.</p>
      <p class="small">Prefer email? Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    <div class="form-card">{form("get-involved")}</div>
  </div>
</section>

<section class="tint tight" aria-labelledby="share">
  <div class="wrap">
    <h2 id="share">Bring someone with you.</h2>
    <p class="lede">The simplest way to help: come to a show, invite a friend and be first to know what&rsquo;s next.</p>
    <p><a class="textlink" href="{FB}">Follow Levitt Houston on Facebook</a></p>
  </div>
</section>
{signup("get-involved")}
'''
page("get-involved.html", "Get Involved | Levitt Pavilion Houston",
     "Sponsor a concert, volunteer, partner or donate. Help free live music grow at Willow Waterhole in Southwest Houston.", gi)

# ============================== DONATE ==============================
don = f'''
<section class="hero hero-split">
  <div class="wrap">
    <div>
      <p class="kicker">Donate</p>
      <h1>Keep free live music growing.</h1>
      <p class="lede">Every Levitt concert is free to attend. Your gift helps Levitt Houston bring people together through music and build a strong foundation for what comes next.</p>
      <div class="btn-row"><a class="btn btn-donate btn-big" href="{DONATE}">Donate now</a></div>
      <p class="small" style="color:rgba(255,255,255,0.8);margin-top:14px">Secure online giving through Square.</p>
    </div>
    <figure><img src="images/community-dancing.jpg" alt="Neighbors dancing together on the lawn at a free outdoor concert" fetchpriority="high"></figure>
  </div>
</section>

<section aria-labelledby="more">
  <div class="wrap">
    <div>
      <p class="kicker">Why it matters</p>
      <h2 id="more">A free concert gives more than music.</h2>
      <p class="lede">Your gift gives a family a night out together at no cost. It gives a young musician a real stage and a real audience. It gives neighbors a reason to meet on the same lawn.</p>
      <p>And every concert builds the audience and support that will bring a permanent Levitt Pavilion to Southwest Houston.</p>
    </div>
  </div>
</section>

<section class="tint" aria-labelledby="free">
  <div class="wrap">
    <p class="kicker">Your gift at work</p>
    <h2 id="free">Free for the audience. Made possible by the community.</h2>
    <p class="lede">Keeping admission free opens the lawn to everyone. Your support pays for the artists, production and people behind each show, and helps Levitt Houston build the partnerships and capacity to do more through music.</p>
    <div class="grid g3">
      <div class="card card-top"><h3>Great artists on a free stage</h3><p>Professional musicians performing for everyone on the lawn.</p></div>
      <div class="card card-top"><h3>A real show</h3><p>Sound, lighting and staging that make every concert a true night out.</p></div>
      <div class="card card-top"><h3>A safe, welcoming site</h3><p>Setup, safety and cleanup at Willow Waterhole for every show.</p></div>
      <div class="card card-top"><h3>More neighbors on the lawn</h3><p>Outreach that brings new families, schools and friends to every concert.</p></div>
      <div class="card card-top"><h3>The road to the pavilion</h3><p>Every concert grows the community behind a permanent home for free music.</p></div>
      <div class="card" style="background:var(--navy);color:#fff;border-color:var(--navy)"><h3>Give today</h3><p style="color:rgba(255,255,255,0.85)">One secure gift through Square, any amount.</p><div class="btn-row"><a class="btn btn-donate" href="{DONATE}">Donate now</a></div></div>
    </div>
  </div>
</section>

<section aria-labelledby="home-for-it">
  <div class="wrap">
    <p class="kicker">The permanent pavilion</p>
    <h2 id="home-for-it">Interested in supporting the permanent pavilion?</h2>
    <p class="lede">Major gifts toward the permanent Levitt Pavilion begin with a conversation. We&rsquo;d be glad to share current plans.</p>
    <div class="btn-row"><a class="btn btn-navy" href="contact.html?interest=pavilion#connect">Talk with us about the pavilion</a><a class="btn btn-ghost" href="pavilion.html">Pavilion plans</a></div>
  </div>
</section>

<section class="tint tight" aria-labelledby="part">
  <div class="wrap">
    <h2 id="part" style="font-size:1.5rem">More ways to be part of it.</h2>
    <p>Want to sponsor, volunteer or partner with us? <a class="textlink" href="get-involved.html">Explore ways to get involved</a></p>
  </div>
</section>

<section class="tight" aria-label="Organization information">
  <div class="wrap"><p class="small" style="max-width:none">Friends of Levitt Pavilion Houston, Inc. is a 501(c)(3) nonprofit. Gifts are tax deductible as allowed by law. 5300 N. Braeswood Blvd., Suite 4&#8209;202, Houston, TX 77096. Questions about a gift? <a href="contact.html">Contact us</a>.</p></div>
</section>
'''
page("donate.html", "Donate | Levitt Pavilion Houston",
     "Keep free live music growing in Southwest Houston. Give to Friends of Levitt Pavilion Houston, a 501(c)(3) nonprofit.", don)

# ============================== ABOUT ==============================
OFFICERS = [("Howard Sacks", "Chair"), ("Dave Hawes", "Vice Chair"), ("Deborah Anderson", "Secretary"), ("Valerie Runge", "Treasurer")]
MEMBERS = ["Becky Edmondson", "Carol Kehlenbrink", "Curtis Monroe", "Frank Staats", "Fred Meyer", "Jay Broadfoot", "Jeff Peters", "Kathleen Ownby", "Vernon Smith"]
roster = "".join(f"<li>{n}<span>{t}</span></li>" for n, t in OFFICERS) + "".join(f"<li>{n}</li>" for n in MEMBERS)

about = f'''
<section class="hero hero-graphic">
  <div class="wrap">
    <div>
      <p class="kicker">About Levitt Houston</p>
      <h1>Building community through music.</h1>
      <p class="lede">Levitt Pavilion Houston is the local nonprofit presenting free live music at Willow Waterhole and leading the effort to create a permanent Levitt Pavilion in Southwest Houston.</p>
    </div>
    <img class="mark" src="images/Logos/levitt-houston-mark-concept-white.png" alt="">
  </div>
</section>

<section aria-labelledby="story">
  <div class="wrap split">
    <figure><img src="images/mf-crowd-dancing-derrick.jpg" alt="Neighbors dancing on the lawn at MusicFest, with the Gasmer derrick in the distance" loading="lazy"><figcaption>MusicFest at Willow Waterhole. Photo: &copy; Steve N. Magoon.</figcaption></figure>
    <div>
    <p class="kicker">Our story</p>
    <h2 id="story">More than a decade of free music at Willow Waterhole.</h2>
    <p class="lede">Since 2012, MusicFest and related events have brought local artists, families and neighbors together for free live music at Willow Waterhole.</p>
    <p>That experience in producing concerts, building partnerships and bringing people together on the lawn is the foundation for today&rsquo;s Levitt Houston and the recurring concert series beginning in 2027.</p>
    <div class="btn-row"><a class="btn btn-ghost" href="musicfest.html">The MusicFest story</a><a class="btn btn-ghost" href="pavilion.html">The pavilion</a></div>
    </div>
  </div>
</section>

<section class="tint" aria-labelledby="who">
  <div class="wrap">
    <p class="kicker">Who we are</p>
    <h2 id="who">A Houston nonprofit building Levitt here.</h2>
    <p class="lede">Friends of Levitt Pavilion Houston is the local nonprofit responsible for bringing the Levitt model to Houston. We produce free music, build local support, lead planning for the permanent pavilion and work with public and community partners to move the effort forward.</p>
    <div class="grid g4">
      <div class="card card-green"><h3>Locally led</h3><p>A volunteer Houston board sets direction, raises support and stewards the organization.</p></div>
      <div class="card card-green"><h3>Proven on the lawn</h3><p>More than a decade of MusicFest gives us real experience producing free outdoor music at Willow Waterhole.</p></div>
      <div class="card card-green"><h3>Building the permanent home</h3><p>Levitt Houston is leading the planning and fundraising for a permanent pavilion beside Willow Waterhole Greenway.</p></div>
      <div class="card card-green"><h3>Part of the Levitt network</h3><p>Part of a national network built around free professional music, welcoming public spaces and community connection, supported by the Levitt Foundation.</p></div>
    </div>
    <div class="btn-row"><a class="btn btn-navy" href="levitt-network.html">Explore the Levitt network</a></div>
  </div>
</section>

<section id="partners" aria-labelledby="abp">
  <div class="wrap">
    <p class="kicker">Our partners</p>
    <h2 id="abp">Built through partnership.</h2>
    <p class="lede">Levitt Houston works with public, national and community partners to present free music today and create the permanent Levitt Pavilion for Southwest Houston.</p>
    <div class="grid g3">{PARTNER_CARDS}</div>
  </div>
</section>

<section class="tint" id="leadership" aria-labelledby="board">
  <div class="wrap">
    <p class="kicker">Leadership</p>
    <h2 id="board">Board of directors</h2>
    <p class="lede">A volunteer board of community and civic leaders guides Levitt Houston.</p>
    <ul class="roster">{roster}</ul>
  </div>
</section>

<section id="organization" aria-labelledby="org">
  <div class="wrap">
    <p class="kicker">Organization</p>
    <h2 id="org">Organization information</h2>
    <div class="grid g4">
      <div class="card"><h3>Legal name</h3><p>Friends of Levitt Pavilion Houston, Inc.</p></div>
      <div class="card"><h3>Status</h3><p>501(c)(3) nonprofit organization</p></div>
      <div class="card"><h3>Mailing address</h3><p>5300 N. Braeswood Blvd., Suite 4&#8209;202<br>Houston, TX 77096</p></div>
      <div class="card"><h3>Financials</h3><p>Our latest Form 990 is available on request. <a href="contact.html">Contact us</a>.</p></div>
    </div>
  </div>
</section>

<section class="dark tight" aria-labelledby="ct">
  <div class="wrap">
    <h2 id="ct">Questions, ideas or partnerships?</h2>
    <div class="btn-row" style="margin-top:0"><a class="btn btn-white" href="contact.html">Contact us</a></div>
  </div>
</section>
'''
page("about.html", "About | Levitt Pavilion Houston",
     "Levitt Pavilion Houston is a local nonprofit building community through free live music in Southwest Houston, part of the national Levitt network.", about)

# ============================== CONTACT ==============================
contact = f'''
<section class="hero hero-split">
  <div class="wrap">
    <div>
      <p class="kicker">Contact</p>
      <h1>Get in touch.</h1>
      <p class="lede">Questions, ideas, partnerships or just want to say hello? Send us a note and someone from Levitt Houston will get back to you.</p>
    </div>
    <figure><img src="images/ww-heron.jpg" alt="A heron wading at the edge of a lake at Willow Waterhole at golden hour" fetchpriority="high"><figcaption>Willow Waterhole Greenway.</figcaption></figure>
  </div>
</section>

<section id="connect" aria-labelledby="send">
  <div class="wrap split" style="align-items:start">
    <div class="form-card"><h2 id="send" style="font-size:1.6rem">Send a message</h2>{form("contact")}</div>
    <div>
      <div class="card" style="margin-bottom:20px"><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="card" style="margin-bottom:20px"><h3>Mailing address</h3><p>Friends of Levitt Pavilion Houston, Inc.<br>5300 N. Braeswood Blvd., Suite 4&#8209;202<br>Houston, TX 77096</p></div>
      <div class="card" style="margin-bottom:20px"><h3>Concerts</h3><p>Concert details, including times, parking and arrival information, will be posted on each <a href="concerts.html">concert page</a> as they are confirmed.</p></div>
      <div class="card"><h3>Follow along</h3><p><a href="{FB}">Facebook</a></p></div>
    </div>
  </div>
</section>
{signup("contact")}
'''
page("contact.html", "Contact | Levitt Pavilion Houston",
     "Contact Levitt Pavilion Houston about concerts, volunteering, sponsorship, partnerships or the permanent pavilion.", contact, image="images/ww-heron.jpg")

nf = '''
<section class="hero"><div class="wrap"><img src="images/Logos/levitt-houston-mark-concept-white.png" alt="" style="width:110px;margin-bottom:24px"><p class="kicker">Page not found</p><h1>That page took a different stage.</h1>
<p class="lede">The page you were looking for has moved or no longer exists.</p>
<div class="btn-row"><a class="btn btn-white" href="index.html">Home</a><a class="btn btn-ghost-light" href="concerts.html">2027 concerts</a></div></div></section>
'''
page("404.html", "Page not found | Levitt Pavilion Houston", "This page could not be found.", nf)
PAGES.remove("404.html")
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{'' if p == 'index.html' else p}</loc></url>\n" for p in PAGES) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
open(".nojekyll", "w").write("")
print("built")

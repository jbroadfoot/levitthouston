"""Builds every page with the shared header and footer.
Run: python3 build.py   (writes static HTML into this folder)
Edit copy in the PAGES section below, then rebuild."""
import os, json

DONATE = "https://square.link/u/yzNNS96a"
EMAIL = "info@levitthouston.org"
FB = "https://www.facebook.com/LevittHouston"
LOGO = "images/Logos/levitt-houston-logo.svg"
LOGO_WHITE = "images/Logos/levitt-houston-logo-white.svg"
PREVIEW = True  # adds noindex so the GitHub Pages preview stays out of search

NAV = [("Concerts", "concerts/"), ("The Pavilion", "pavilion/"), ("Get Involved", "get-involved/"), ("About", "about/")]

def mail(subject):
    return f"mailto:{EMAIL}?subject=" + subject.replace(" ", "%20")

def header(r, current):
    links = "".join(
        f'<a href="{r}{href}"{" aria-current=\"page\"" if current == href else ""}>{label}</a>' for label, href in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="nextbar"><div class="wrap"><span class="dot" aria-hidden="true"></span><p style="margin:0">Next concert: Saturday, March 20 at Willow Waterhole. Free. <a href="{r}concerts/march-20-2027/">Details</a></p></div></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r}"><img data-logo src="{r}{LOGO}" alt="Levitt Pavilion Houston home"></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"></span>Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {links}
      <a class="btn btn-donate" href="{r}donate/">Donate</a>
    </nav>
  </div>
</header>'''

def signup(source):
    return f'''<section class="signup band" aria-labelledby="signup-{source}">
  <div class="wrap">
    <div>
      <h2 id="signup-{source}">Be first to know who&rsquo;s playing.</h2>
      <p>Artist announcements, concert details and news from Levitt Houston. A few emails a season.</p>
    </div>
    <form class="signup-form" data-source="{source}" novalidate>
      <label for="email-{source}">Email address</label>
      <input id="email-{source}" type="email" name="email" autocomplete="email" required placeholder="you@example.com">
      <button class="btn" type="submit">Get concert updates</button>
      <p class="signup-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''

def footer(r):
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img data-logo src="{r}{LOGO_WHITE}" alt="Levitt Pavilion Houston">
        <p>Free live music at Willow Waterhole in Southwest Houston, and a permanent Levitt Pavilion on the way. Part of the national Levitt network.</p>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="{r}concerts/">Concerts</a></li>
          <li><a href="{r}concerts/musicfest/">MusicFest</a></li>
          <li><a href="{r}pavilion/">The Pavilion</a></li>
          <li><a href="{r}get-involved/">Get Involved</a></li>
          <li><a href="{r}about/">About</a></li>
          <li><a href="{r}donate/">Donate</a></li>
        </ul>
      </div>
      <div>
        <h2>Connect</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{FB}">Facebook</a></li>
          <li>5300 N. Braeswood Blvd., Suite 4&#8209;202<br>Houston, TX 77096</li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <span>&copy; 2026 Friends of Levitt Pavilion Houston, Inc. A 501(c)(3) nonprofit.</span>
      <a href="{r}about/#organization">Organization information</a>
    </div>
  </div>
</footer>'''

def page(path, title, desc, body, current="", schema=None):
    r = ""
    robots = '<meta name="robots" content="noindex">\n' if PREVIEW else ""
    sch = f'<script type="application/ld+json">{json.dumps(schema, indent=1)}</script>\n' if schema else ""
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css">
{sch}</head>
<body>
{header(r, current)}
<main id="main">
{body.replace("{r}", r)}
</main>
{footer(r)}
<script src="{r}assets/js/site.js"></script>
</body>
</html>
'''
    html = flatten(html)
    out = (path.split("/")[-1] + ".html") if path else "index.html"
    open(out, "w").write(html)
    return r

FLAT = [("concerts/march-20-2027/", "march-20-2027.html"), ("concerts/may-1-2027/", "may-1-2027.html"),
        ("concerts/musicfest/", "musicfest.html"), ("concerts/", "concerts.html"), ("pavilion/", "pavilion.html"),
        ("get-involved/", "get-involved.html"), ("donate/", "donate.html"), ("about/", "about.html"),
        ("assets/css/site.css", "site.css"), ("assets/js/site.js", "site.js")]
def flatten(html):
    for old, new in FLAT:
        html = html.replace(f'"{old}', f'"{new}')
    return html.replace('href=""', 'href="index.html"')

# ---------- shared pieces ----------
def card(slug, dow, day, mon, img=None):
    return f'''<a class="event" href="{{r}}concerts/{slug}/">
  <div class="stub" aria-hidden="true"><span class="dow">{dow}</span><span class="day">{day}</span><span class="mon">{mon}</span></div>
  <div class="event-body">
    <p class="visually-hidden">{dow}day, {mon.split()[0]} {day}, {mon.split()[1]}</p>
    <h3>Free Live Music at Willow Waterhole</h3>
    <p class="event-status">Artist announcement coming soon</p>
    <ul class="event-facts"><li>Free admission</li><li>All ages</li></ul>
    <span class="event-cta">View concert details</span>
  </div>
</a>'''

CARDS = card("march-20-2027", "Sat", "20", "March 2027") + "\n" + card("may-1-2027", "Sat", "1", "May 2027")

PARTNERS = [
    ("Levitt Foundation", "Provides the national Levitt model, experience and ongoing support for free outdoor music."),
    ("Southwest Houston Redevelopment Authority (TIRZ 20)", "Public property and site development partner for the future venue location."),
    ("City of Houston", "Public partner helping advance the future pavilion and broader community opportunity."),
    ("Brays Oaks Management District", "Neighborhood partner supporting the Brays Oaks area around Willow Waterhole."),
    ("Willow Waterhole Greenspace Conservancy", "Steward of Willow Waterhole Greenway and longtime host of MusicFest."),
]
PARTNER_STRIP = "".join(f"<li>{n.replace(' (TIRZ 20)', '')}</li>" for n, _ in PARTNERS)
PARTNER_ROLES = "".join(f"<li><h3>{n}</h3><p>{d}</p></li>" for n, d in PARTNERS)

# =====================================================================
# HOME
# =====================================================================
home = f'''
<section class="hero">
  <img src="{{r}}images/ww-crowd-sunset-dancing.jpg" alt="A crowd dancing on the lawn at Willow Waterhole as the sun sets" fetchpriority="high">
  <div class="wrap">
    <p class="kicker">2027 concert series</p>
    <h1>Free live music. Open to all.</h1>
    <p class="lede">Free concerts return to Willow Waterhole this spring. Join us Saturday, March 20 and Saturday, May 1.</p>
    <div class="actions">
      <a class="btn btn-light" href="{{r}}concerts/">See 2027 concerts</a>
      <a class="btn btn-ghost-light" href="#updates">Get concert updates</a>
    </div>
  </div>
</section>

<section class="band band-tint" aria-labelledby="next">
  <div class="wrap">
    <h2 id="next">Next on the lawn</h2>
    <p class="lede">Four free concerts in 2027. Here&rsquo;s what&rsquo;s first.</p>
    <div class="events">{CARDS}</div>
    <p class="after-events">More dates to come. <a class="textlink" href="#updates">Get updates</a></p>
  </div>
</section>

<section class="band" aria-labelledby="experience">
  <div class="wrap split">
    <figure><img src="{{r}}images/ww-picnic-blanket-cheering.jpg" alt="Friends on a picnic blanket cheering at a concert" loading="lazy"></figure>
    <div>
      <h2 id="experience">Bring a chair or blanket. Bring family and friends.</h2>
      <p class="lede">Free concerts give everyone a reason to come out, spend an evening outdoors and enjoy live music together at Willow Waterhole.</p>
      <ul class="facts"><li>Free<span>No cost to attend</span></li><li>All ages<span>Kids welcome</span></li><li>Outdoors<span>On the lawn</span></li></ul>
      <div class="actions"><a class="textlink" href="{{r}}concerts/#plan">What to expect</a></div>
    </div>
  </div>
</section>

<section class="band band-navy" aria-labelledby="proof">
  <div class="wrap split flip">
    <figure><img src="{{r}}images/mf-sunset-stage-perme.jpg" alt="A band on the MusicFest stage at sunset, seen from behind the drums" loading="lazy"><figcaption>MusicFest at Willow Waterhole. Photo: &copy; Eduardo Perme.</figcaption></figure>
    <div>
      <h2 id="proof">Free music at Willow Waterhole since 2012.</h2>
      <p>MusicFest has filled the lawn with student musicians, professional artists, families and neighbors for more than a decade. Along the way, we learned how to book talent, produce a professional stage, coordinate vendors, food and beverage, parking and permits, organize volunteers, and raise local sponsorship support.</p>
      <p class="pull">MusicFest proved the audience and built the experience. The concert series is the next step.</p>
      <a class="btn btn-light" href="{{r}}concerts/musicfest/">Explore MusicFest</a>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="home-next">
  <div class="wrap split">
    <figure><img src="{{r}}images/site-derrick-sunset.jpg" alt="The historic steel derrick on the former Shell Gasmer site at sunset" loading="lazy"><figcaption>The former Shell Gasmer site beside Willow Waterhole Greenway.</figcaption></figure>
    <div>
      <h2 id="home-next">The music is here. A permanent home is next.</h2>
      <p class="lede">Plans are moving forward for a permanent Levitt Pavilion beside Willow Waterhole Greenway, on the former Shell Gasmer site. It will give these concerts a home built for them and give Southwest Houston a gathering place for years to come.</p>
      <div class="actions"><a class="btn btn-primary" href="{{r}}pavilion/">Explore the pavilion</a></div>
    </div>
  </div>
</section>

<section class="band band-tint band-tight" aria-labelledby="partners">
  <div class="wrap">
    <h2 id="partners" style="font-size:1.35rem">Our partners</h2>
    <ul class="partners">{PARTNER_STRIP}</ul>
  </div>
</section>

<section class="band" aria-labelledby="help">
  <div class="wrap">
    <h2 id="help">Help keep free music growing.</h2>
    <div class="paths">
      <div class="path"><h3>Give</h3><p>Your gift helps bring free, professional concerts to Willow Waterhole.</p><a class="textlink" href="{{r}}donate/">Donate</a></div>
      <div class="path"><h3>Volunteer</h3><p>Lend a hand on concert day and meet your neighbors doing it.</p><a class="textlink" href="{{r}}get-involved/#volunteer">Volunteer</a></div>
      <div class="path"><h3>Sponsor</h3><p>Put your business behind free live music in Southwest Houston.</p><a class="textlink" href="{{r}}get-involved/#sponsor">Sponsor the series</a></div>
    </div>
    <p class="after-events" style="margin-top:2.5rem">The simplest way to help: come to a show and bring a friend.</p>
  </div>
</section>
<div id="updates"></div>
{signup("home")}
'''
page("", "Levitt Pavilion Houston | Free Live Music in Southwest Houston",
     "Free outdoor concerts at Willow Waterhole in Southwest Houston. Our 2027 series opens March 20, with plans underway for a permanent Levitt Pavilion.",
     home)

# =====================================================================
# CONCERTS
# =====================================================================
concerts = f'''
<section class="hero hero-short">
  <img src="{{r}}images/mf-dancing-lawn.jpg" alt="People dancing on the lawn in front of the stage" fetchpriority="high">
  <div class="wrap">
    <h1>Meet us on the lawn.</h1>
    <p class="lede">Free concerts at Willow Waterhole begin Saturday, March 20 and Saturday, May 1, 2027.</p>
    <div class="actions"><a class="btn btn-light" href="#upcoming">See the shows</a><a class="btn btn-ghost-light" href="#updates">Get concert updates</a></div>
  </div>
</section>

<section class="band band-tint" id="upcoming" aria-labelledby="up-h">
  <div class="wrap">
    <h2 id="up-h">Upcoming concerts</h2>
    <p class="lede">Four free concerts are planned for 2027. March 20 and May 1 are first up, with more dates to come.</p>
    <div class="events">{CARDS}</div>
  </div>
</section>

<section class="band" id="plan" aria-labelledby="plan-h">
  <div class="wrap">
    <h2 id="plan-h">What to expect</h2>
    <p class="lede">Free. Outdoors. All ages. Bring a chair or blanket and settle in on the lawn at Willow Waterhole Greenway.</p>
    <div class="details">
      <div><h3>Admission</h3><p>Every concert is free and open to all.</p></div>
      <div><h3>What to bring</h3><p>Lawn chairs, blankets, sunscreen and water.</p></div>
      <div><h3>Times and location</h3><p>Start times and exact location will be posted on each concert page as the date approaches.</p></div>
      <div><h3>Parking and access</h3><p>Parking, accessibility and arrival details are coming. Questions now? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
      <div><h3>Food and drink</h3><p>Details on food and beverage will be shared before each show.</p></div>
      <div><h3>Weather</h3><p>Weather updates will be posted here and sent to the email list.</p></div>
    </div>
  </div>
</section>

<section class="band band-navy" aria-labelledby="bridge">
  <div class="wrap split flip">
    <figure><img src="{{r}}images/mf-crowd-derrick.jpg" alt="MusicFest crowd under white tents with the derrick in the distance" loading="lazy"></figure>
    <div>
      <h2 id="bridge">A new series built on years of doing the work.</h2>
      <p class="lede">Levitt Houston is moving from a once a year festival to a recurring concert series, growing the audience, partners and sponsors show by show.</p>
      <a class="btn btn-light" href="{{r}}concerts/musicfest/">See the MusicFest story</a>
    </div>
  </div>
</section>
<div id="updates"></div>
{signup("concerts")}
'''
page("concerts", "2027 Concerts | Levitt Pavilion Houston",
     "Free concerts at Willow Waterhole in Southwest Houston. Saturday, March 20 and Saturday, May 1, 2027. All ages, free admission.",
     concerts, current="concerts/")

# =====================================================================
# EVENT PAGES
# =====================================================================
def event_page(slug, iso, dow_long, day, month, other_slug, other_label, img, alt):
    schema = {
        "@context": "https://schema.org", "@type": "MusicEvent",
        "name": "Free Live Music at Willow Waterhole",
        "startDate": iso, "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "isAccessibleForFree": True,
        "location": {"@type": "Place", "name": "Willow Waterhole Greenway",
                     "address": {"@type": "PostalAddress", "addressLocality": "Houston", "addressRegion": "TX", "addressCountry": "US"}},
        "organizer": {"@type": "Organization", "name": "Friends of Levitt Pavilion Houston", "url": "https://www.levitthouston.org/"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
        "description": "Free outdoor concert at Willow Waterhole in Southwest Houston. Artist announcement coming soon."
    }
    ymd = iso.replace("-", "")
    ics = f"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Levitt Pavilion Houston//EN\r\nBEGIN:VEVENT\r\nUID:{slug}@levitthouston.org\r\nDTSTAMP:20261001T000000Z\r\nDTSTART;VALUE=DATE:{ymd}\r\nSUMMARY:Levitt Houston free concert\r\nLOCATION:Willow Waterhole Greenway, Houston, TX\r\nDESCRIPTION:Free live music at Willow Waterhole. Details at levitthouston.org/concerts/{slug}/\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
    open(f"levitt-houston-{iso}.ics", "w", newline="").write(ics)
    body = f'''
<section class="event-hero">
  <div class="wrap">
    <div class="stub" aria-hidden="true"><span class="dow">{dow_long[:3]}</span><span class="day">{day}</span><span class="mon">{month} 2027</span></div>
    <div>
      <p class="kicker">{dow_long}, {month} {day}, 2027</p>
      <h1>Free Live Music at Willow Waterhole</h1>
      <p class="lede">Artist announcement coming soon.</p>
      <ul class="event-facts"><li>Free admission</li><li>All ages welcome</li><li>Willow Waterhole Greenway</li></ul>
      <div class="actions">
        <a class="btn btn-light" href="#updates">Get concert updates</a>
        <a class="btn btn-ghost-light" href="levitt-houston-{iso}.ics" download>Add to calendar</a>
      </div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="ev-plan">
  <div class="wrap split">
    <figure><img src="{{r}}images/{img}" alt="{alt}" loading="lazy"><figcaption>MusicFest at Willow Waterhole.</figcaption></figure>
    <div>
      <h2 id="ev-plan">Plan your evening</h2>
      <p class="lede">Bring a chair or blanket. Bring family and friends. We&rsquo;ll post the artist, times and arrival details here as the date gets closer.</p>
      <div class="details" style="grid-template-columns:1fr">
        <div><h3>Time</h3><p>Coming soon.</p></div>
        <div><h3>Location</h3><p>Willow Waterhole Greenway, Southwest Houston. Exact location and parking coming soon.</p></div>
        <div><h3>Accessibility</h3><p>Questions about access? Email <a href="mailto:{EMAIL}?subject=Accessibility">{EMAIL}</a>.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="band band-tint band-tight" aria-labelledby="also">
  <div class="wrap">
    <h2 id="also" style="font-size:1.6rem">Also coming up</h2>
    <p><a class="textlink" href="{{r}}concerts/{other_slug}/">{other_label}</a></p>
  </div>
</section>
<div id="updates"></div>
{signup(slug)}
'''
    page(f"concerts/{slug}", f"{dow_long}, {month} {day}, 2027 | Free Concert | Levitt Pavilion Houston",
         f"Free live music at Willow Waterhole on {dow_long}, {month} {day}, 2027. Free admission, all ages. Artist announcement coming soon.",
         body, current="concerts/", schema=schema)

event_page("march-20-2027", "2027-03-20", "Saturday", "20", "March", "may-1-2027", "Saturday, May 1, 2027", "mf-gazebo-sunset.jpg", "Concertgoers on the lawn near the gazebo at sunset")
event_page("may-1-2027", "2027-05-01", "Saturday", "1", "May", "march-20-2027", "Saturday, March 20, 2027", "mf-crowd-wide.jpg", "A wide view of the MusicFest crowd in lawn chairs facing the stage")

# =====================================================================
# MUSICFEST
# =====================================================================
POSTERS = [("poster-2012-nov", "November 2012"), ("poster-2013-apr", "April 2013"), ("poster-2013-oct", "October 2013"),
           ("poster-2014", "2014"), ("poster-2015", "2015"), ("poster-2016", "2016"), ("poster-2017", "2017"),
           ("poster-2017-artist-village", "2017 Artist Village"), ("poster-2018", "2018"), ("poster-2019", "2019"),
           ("poster-2020", "2020"), ("poster-2021", "2021"), ("poster-2022", "2022")]
poster_html = "".join(f'<figure><img src="{{r}}images/posters/{f}.jpg" alt="MusicFest poster, {c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for f, c in POSTERS)

musicfest = f'''
<section class="hero hero-short">
  <img src="{{r}}images/mf-sunset-stage-perme.jpg" alt="A band playing the MusicFest stage at sunset" fetchpriority="high">
  <div class="wrap">
    <h1>More than a decade of free music at Willow Waterhole.</h1>
    <p class="lede">Since 2012, MusicFest and related events have brought free live music to Willow Waterhole, bringing together neighbors, families, students, artists, volunteers, sponsors and community partners.</p>
    <div class="actions"><a class="btn btn-light" href="{{r}}concerts/">See what&rsquo;s next</a></div>
  </div>
  <span class="credit">Photo: &copy; Eduardo Perme</span>
</section>

<section class="band" aria-labelledby="mf-proof">
  <div class="wrap">
    <h2 id="mf-proof">We know what it takes to put on the show.</h2>
    <p class="lede">Over the years, the team behind Levitt Houston has built practical experience across every part of a free outdoor concert.</p>
    <ul class="capabilities">
      <li>Talent booking</li><li>Stage and production</li><li>Vendors, food and beverage</li>
      <li>Parking and site logistics</li><li>Permits</li><li>Volunteers</li>
      <li>Local sponsorship and fundraising</li><li>Student musicians</li><li>Community partnerships</li>
    </ul>
    <div class="actions"><a class="btn btn-primary" href="{{r}}donate/">Support the concert series</a></div>
  </div>
</section>

<section class="band band-tint" aria-labelledby="posters-h">
  <div class="wrap">
    <h2 id="posters-h">The posters</h2>
    <p class="lede">A look back at MusicFest through the posters that announced it.</p>
    <div class="posters" tabindex="0" aria-label="MusicFest posters, scroll sideways">{poster_html}</div>
  </div>
</section>

<section class="band" aria-labelledby="mf-moments">
  <div class="wrap split">
    <figure><img src="{{r}}images/mf-aerial-2018.jpg" alt="Aerial view of MusicFest 2018 at Willow Waterhole" loading="lazy"><figcaption>MusicFest 2018 from above. Photo: &copy; 2018 ev1pro.com + EAMD.</figcaption></figure>
    <figure><img src="{{r}}images/mf-dancing-crowd-2026.jpg" alt="A crowd dancing together at MusicFest 2026" loading="lazy"><figcaption>MusicFest, spring 2026. Photo: &copy; Steve N. Magoon.</figcaption></figure>
  </div>
</section>

<section class="band band-navy" aria-labelledby="mf-next">
  <div class="wrap">
    <h2 id="mf-next">From one big day to a season of free music.</h2>
    <p class="lede">MusicFest proved the audience and built the experience. The next step is a recurring Levitt concert series that grows the audience, sponsors, donors and rhythm of free music at Willow Waterhole, show by show.</p>
    <div class="actions"><a class="btn btn-light" href="{{r}}concerts/#upcoming">See upcoming shows</a></div>
  </div>
</section>
'''
page("concerts/musicfest", "MusicFest | Levitt Pavilion Houston",
     "MusicFest has brought free live music to Willow Waterhole since 2012. Now it grows into a recurring Levitt concert series.",
     musicfest, current="concerts/")

# =====================================================================
# THE PAVILION
# =====================================================================
pavilion = f'''
<section class="hero hero-short">
  <img src="{{r}}images/site-derrick-sunset.jpg" alt="The historic steel derrick on the former Shell Gasmer site at sunset" fetchpriority="high">
  <div class="wrap">
    <h1>A permanent home for free live music.</h1>
    <p class="lede">Plans are moving forward for a Levitt Pavilion at Willow Waterhole, a lasting outdoor home for the free concerts and community gatherings Levitt Houston is building now.</p>
    <div class="actions"><a class="btn btn-light" href="#progress">Follow the progress</a></div>
  </div>
</section>

<section class="band" aria-labelledby="why">
  <div class="wrap split">
    <figure><img src="{{r}}images/rendering-derrick-landscape.jpg" alt="Concept rendering of the restored derrick in a landscaped setting" loading="lazy"><figcaption>Concept rendering. Design is not final.</figcaption></figure>
    <div>
      <h2 id="why">A place built for the experience.</h2>
      <p class="lede">A permanent pavilion gives Levitt Houston the home to present free live music consistently, welcome larger audiences, support artists and production, and create a recognizable gathering place for Southwest Houston.</p>
      <a class="textlink" href="{{r}}concerts/">See the concerts</a>
    </div>
  </div>
</section>

<section class="band band-tint" aria-labelledby="place">
  <div class="wrap split flip">
    <figure><img src="{{r}}images/ww-bridge-riese.jpg" alt="A footbridge reflected in the water at Willow Waterhole Greenway" loading="lazy"><figcaption>Willow Waterhole Greenway. Photo: Charles Riese.</figcaption></figure>
    <div>
      <h2 id="place">Rooted at Willow Waterhole.</h2>
      <p class="lede">The future pavilion is planned on the former Shell Gasmer site beside Willow Waterhole Greenway, building on years of free music and community life already connected to this place.</p>
      <a class="textlink" href="https://willowwaterhole.org/">Learn about Willow Waterhole</a>
    </div>
  </div>
</section>

<section class="band" id="progress" aria-labelledby="prog-h">
  <div class="wrap">
    <h2 id="prog-h">Moving forward, step by step.</h2>
    <ol class="timeline">
      <li><span class="year">2012</span><h3>Levitt selects Houston</h3><p>The Levitt Foundation selects Willow Waterhole as the Houston location for a future Levitt venue. MusicFest begins the same year.</p></li>
      <li><span class="year">2016</span><h3>The city advances the pavilion</h3><p>Houston City Council approves plans to advance Levitt Pavilion Houston.</p></li>
      <li><span class="year">2019</span><h3>A new site beside the Greenway</h3><p>The City of Houston acquires the former Shell Gasmer property, and the future pavilion location later moves there.</p></li>
      <li><span class="year">2026</span><h3>The site moves forward</h3><p>Houston City Council approves the sale of the site to the Southwest Houston Redevelopment Authority (TIRZ 20).</p></li>
      <li class="next"><span class="year">2027</span><h3>The concert series begins</h3><p>Free Levitt concerts begin at Willow Waterhole while site planning, design and fundraising continue.</p></li>
    </ol>
  </div>
</section>

<section class="band band-tint" aria-labelledby="pav-partners">
  <div class="wrap">
    <h2 id="pav-partners">A community effort with strong partners.</h2>
    <p class="lede">Levitt Houston is advancing through local nonprofit leadership, public partnership, community support and the national Levitt network.</p>
    <ul class="partner-roles">{PARTNER_ROLES}</ul>
  </div>
</section>

<section class="band band-navy" aria-labelledby="lead">
  <div class="wrap">
    <h2 id="lead">Interested in leadership support?</h2>
    <p class="lede">Leadership gifts and partnerships connected to the permanent home begin with a conversation. We&rsquo;d be glad to share current plans and talk about how you can be part of what comes next.</p>
    <div class="actions"><a class="btn btn-light" href="{mail("Leadership support")}">Start a conversation</a></div>
  </div>
</section>
'''
page("pavilion", "The Pavilion | Levitt Pavilion Houston",
     "Plans are moving forward for a permanent Levitt Pavilion beside Willow Waterhole Greenway on the former Shell Gasmer site in Southwest Houston.",
     pavilion, current="pavilion/")

# =====================================================================
# GET INVOLVED
# =====================================================================
involved = f'''
<section class="hero hero-short">
  <img src="{{r}}images/mf-crowd-family.jpg" alt="Families and friends dancing in front of the MusicFest stage" fetchpriority="high">
  <div class="wrap">
    <h1>There&rsquo;s more than one way to make the music happen.</h1>
    <p class="lede">Come to a show. Sponsor. Volunteer. Introduce us. Join the list. Every one of them helps free live music grow in Southwest Houston.</p>
  </div>
</section>

<section class="band" id="sponsor" aria-labelledby="sp-h">
  <div class="wrap split">
    <figure><img src="{{r}}images/mf-brass-band.jpg" alt="A brass band performing on the MusicFest stage" loading="lazy"></figure>
    <div>
      <h2 id="sp-h">Put your company behind free live music.</h2>
      <p class="lede">Sponsorship helps underwrite professional concerts and connects your business with neighbors across Southwest Houston at a welcoming public event.</p>
      <div class="actions"><a class="btn btn-primary" href="{mail("Concert series sponsorship")}">Ask about sponsorship</a></div>
    </div>
  </div>
</section>

<section class="band band-tint" aria-labelledby="ways">
  <div class="wrap">
    <h2 id="ways" class="visually-hidden">More ways to help</h2>
    <div class="paths" style="margin-top:0">
      <div class="path" id="volunteer"><h3>Volunteer</h3><p>Volunteer roles will grow with the series. Tell us you&rsquo;re interested and we&rsquo;ll reach out as opportunities open.</p><a class="textlink" href="{mail("Volunteering")}">Volunteer</a></div>
      <div class="path" id="partner"><h3>Partner with us</h3><p>Community organization, school, arts group or neighborhood association? We&rsquo;d like to hear from you.</p><a class="textlink" href="{mail("Community partnership")}">Partner with us</a></div>
      <div class="path"><h3>Give</h3><p>A gift of any size helps keep every concert free.</p><a class="textlink" href="{{r}}donate/">Donate</a></div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="share">
  <div class="wrap">
    <h2 id="share">Bring someone with you.</h2>
    <p class="lede">The simplest way to help: come to a show, invite a friend and be first to know what&rsquo;s next.</p>
    <p><a class="textlink" href="{FB}">Follow Levitt Houston on Facebook</a></p>
  </div>
</section>
<div id="updates"></div>
{signup("get-involved")}
'''
page("get-involved", "Get Involved | Levitt Pavilion Houston",
     "Sponsor, volunteer, partner or give. Help free live music grow at Willow Waterhole in Southwest Houston.",
     involved, current="get-involved/")

# =====================================================================
# DONATE
# =====================================================================
donate = f'''
<section class="band band-navy">
  <div class="wrap split">
    <div>
      <h1>Keep free live music growing.</h1>
      <p class="lede">Every Levitt concert is free to attend. Producing a professional outdoor concert takes artists, sound and lighting, site operations, outreach, volunteers and community partners. Your gift helps Levitt Houston bring people together through music and build a strong foundation for what comes next.</p>
      <div class="actions"><a class="btn btn-donate" style="min-height:56px;font-size:1.1rem;padding:0.8rem 2rem" href="{DONATE}">Make a gift</a></div>
      <p style="margin-top:1rem;font-size:0.95rem;opacity:0.85">Secure giving through Square. Friends of Levitt Pavilion Houston, Inc. is a 501(c)(3) nonprofit. Gifts are tax deductible as allowed by law.</p>
    </div>
    <figure><img src="{{r}}images/mf-dancing-crowd-2026.jpg" alt="A crowd dancing together at MusicFest 2026" fetchpriority="high"><figcaption>MusicFest, spring 2026. Photo: &copy; Steve N. Magoon.</figcaption></figure>
  </div>
</section>

<section class="band" aria-labelledby="gift-does">
  <div class="wrap">
    <h2 id="gift-does">What your gift supports</h2>
    <ul class="facts">
      <li>Artists<span>Professional musicians on a free stage</span></li>
      <li>Production<span>Sound, lighting and staging</span></li>
      <li>Site operations<span>Setup, safety and cleanup</span></li>
      <li>Outreach<span>Bringing new neighbors to the lawn</span></li>
    </ul>
  </div>
</section>

<section class="band band-tint" aria-labelledby="lead-gift">
  <div class="wrap">
    <h2 id="lead-gift">Interested in the permanent pavilion?</h2>
    <p class="lede">Leadership gifts toward the permanent home begin with a conversation. We&rsquo;d be glad to share current plans and talk about how you can be part of what comes next.</p>
    <div class="actions"><a class="btn btn-primary" href="{mail("Leadership gift")}">Start a conversation</a></div>
  </div>
</section>

<section class="band band-tight" aria-labelledby="other">
  <div class="wrap">
    <h2 id="other" style="font-size:1.6rem">Other ways to help</h2>
    <p><a class="textlink" href="{{r}}get-involved/#sponsor">Sponsor the series</a> &nbsp;&nbsp; <a class="textlink" href="{{r}}get-involved/#volunteer">Volunteer</a> &nbsp;&nbsp; <a class="textlink" href="{{r}}concerts/">Come to a concert</a></p>
  </div>
</section>
'''
page("donate", "Donate | Levitt Pavilion Houston",
     "Keep free live music growing in Southwest Houston. Give to Friends of Levitt Pavilion Houston, a 501(c)(3) nonprofit.",
     donate)

# =====================================================================
# ABOUT
# =====================================================================
OFFICERS = [("Howard Sacks", "Chair"), ("Dave Hawes", "Vice Chair"), ("Deborah Anderson", "Secretary")]
MEMBERS = ["Becky Edmondson", "Carol Kehlenbrink", "Curtis Monroe", "Frank Staats", "Fred Meyer", "Jay Broadfoot", "Jeff Peters", "Kathleen Ownby", "Vernon Smith"]
ADVISORY = ["Ann Magoon", "Steve Magoon"]
roster = "".join(f"<li>{n}<span>{t}</span></li>" for n, t in OFFICERS) + "".join(f"<li>{n}</li>" for n in MEMBERS)
advisory = "".join(f"<li>{n}</li>" for n in ADVISORY)

about = f'''
<section class="hero hero-short">
  <img src="{{r}}images/mf-crowd-lawn.jpg" alt="Concertgoers relaxing in lawn chairs under the trees at MusicFest" fetchpriority="high">
  <div class="wrap">
    <h1>Building community through music.</h1>
    <p class="lede">Levitt Pavilion Houston is a local nonprofit bringing free, professional live music to Southwest Houston.</p>
  </div>
</section>

<section class="band" aria-labelledby="story">
  <div class="wrap">
    <h2 id="story">Our story</h2>
    <p class="lede">Our roots at Willow Waterhole go back more than a decade. MusicFest has brought student musicians, professional artists, families and neighbors together for free live music since 2012, and that community response is what brought a Levitt venue to Houston.</p>
    <p>Our next chapter pairs a recurring concert series, beginning in 2027, with plans for a permanent Levitt Pavilion beside Willow Waterhole Greenway.</p>
    <p><a class="textlink" href="{{r}}concerts/musicfest/">The MusicFest story</a> &nbsp;&nbsp; <a class="textlink" href="{{r}}pavilion/">The pavilion</a></p>
  </div>
</section>

<section class="band band-tint" id="network" aria-labelledby="net">
  <div class="wrap split">
    <figure><img src="{{r}}images/levitt-family-blanket.jpg" alt="A family on a blanket at a Levitt concert" loading="lazy"><figcaption>A free Levitt concert elsewhere in the national network.</figcaption></figure>
    <div>
      <h2 id="net">Part of the Levitt network.</h2>
      <p class="lede">Levitt Houston belongs to a national movement that uses free live music to bring public spaces to life and strengthen community connection.</p>
      <ul class="facts"><li>100+<span>communities in the network</span></li><li>1,000+<span>free concerts a year</span></li></ul>
      <div class="actions"><a class="textlink" href="https://levitt.org/">Explore the Levitt network</a></div>
    </div>
  </div>
</section>

<section class="band" id="leadership" aria-labelledby="board">
  <div class="wrap">
    <h2 id="board">Board of directors</h2>
    <p class="lede">A volunteer board of neighbors, musicians and civic leaders guides Levitt Houston.</p>
    <ul class="roster">{roster}</ul>
    <h3 style="margin-top:2.5rem">Advisory board</h3>
    <ul class="roster">{advisory}</ul>
  </div>
</section>

<section class="band band-tint" id="partners" aria-labelledby="ab-partners">
  <div class="wrap">
    <h2 id="ab-partners">Our partners</h2>
    <ul class="partner-roles">{PARTNER_ROLES}</ul>
  </div>
</section>

<section class="band" id="organization" aria-labelledby="org">
  <div class="wrap">
    <h2 id="org">Organization information</h2>
    <div class="info">
      <div><h3>Legal name</h3><p>Friends of Levitt Pavilion Houston, Inc.</p></div>
      <div><h3>Status</h3><p>501(c)(3) nonprofit organization</p></div>
      <div><h3>Mailing address</h3><p>5300 N. Braeswood Blvd., Suite 4&#8209;202<br>Houston, TX 77096</p></div>
      <div><h3>Financial information</h3><p>Our latest Form 990 is available on request. Email <a href="{mail("Form 990 request")}">{EMAIL}</a>.</p></div>
    </div>
  </div>
</section>

<section class="band band-navy" id="contact" aria-labelledby="contact-h">
  <div class="wrap">
    <h2 id="contact-h">Contact us</h2>
    <div class="info">
      <div><h3>General questions</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div><h3>Sponsorship</h3><p><a href="{mail("Concert series sponsorship")}">Ask about sponsorship</a></p></div>
      <div><h3>Leadership gifts</h3><p><a href="{mail("Leadership gift")}">Start a conversation</a></p></div>
      <div><h3>Media</h3><p><a href="{mail("Media inquiry")}">Media inquiries</a></p></div>
    </div>
  </div>
</section>
'''
page("about", "About | Levitt Pavilion Houston",
     "Levitt Pavilion Houston is a local nonprofit bringing free, professional live music to Southwest Houston, part of the national Levitt network.",
     about, current="about/")

# Squarespace partials: same header/footer with root links, for site wide code injection
open("squarespace-header.html", "w").write(header("/", ""))
open("squarespace-footer.html", "w").write(footer("/"))
open(".nojekyll", "w").write("")
print("built")

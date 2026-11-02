import json, os
from html import escape as E
from PIL import Image, ImageDraw, ImageFont
from data import *

ROOT = "."
FMT = {"pdf": "PDF", "docx": "Word", "xlsx": "Excel"}
_sz = {}


def w(path, s):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)


def imgsize(name):
    if name not in _sz: _sz[name] = Image.open(os.path.join(ROOT, "assets/images", name)).size
    return _sz[name]


def fsize(rel):
    b = os.path.getsize(os.path.join(ROOT, rel)); return "%d KB" % max(1, round(b / 1024))


def ld(o): return '<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False)


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": (BASE + "/" if p == "index.html" else f"{BASE}/{p}")} for i, (n, p) in enumerate(items)]}


# ---------------- layout ----------------
def head(title, desc, path, d, img=None, extra="", noindex=False):
    p = "../" if d else ""; canon = BASE + "/" if path == "index.html" else f"{BASE}/{path}"; img = img or f"{BASE}/assets/images/templivox-social-card.png"
    canon_tag = "" if noindex else f'<link rel="canonical" href="{canon}">'
    robots_tag = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{canon_tag}
{robots_tag}
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TemplivoX">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#1f3d2b">
<link rel="icon" href="{p}assets/images/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/css/style.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''


def header(d):
    p = "../" if d else ""
    cats = "".join(f'<li><a href="{p}{c[2]}">{c[1]}</a></li>' for c in CATS)
    return f'''<header class="site-header">
<div class="wrap bar">
<a class="logo" href="{p}index.html" aria-label="TemplivoX home"><span class="logo-word">Templivo</span><span class="logo-x" aria-hidden="true">X</span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle menu"><span></span><span></span><span></span></button>
<nav id="site-nav" class="nav" aria-label="Main">
<ul>
<li><a href="{p}index.html">Home</a></li>
<li><a href="{p}templates.html">All Templates</a></li>
<li class="dd"><button class="dd-btn" type="button" aria-expanded="false" aria-haspopup="true">Categories</button><ul class="dd-menu">{cats}</ul></li>
<li><a href="{p}about.html">About</a></li>
<li><a href="{p}contact.html">Contact</a></li>
</ul>
<form class="search" action="{p}templates.html" method="get" role="search">
<label class="sr" for="site-search">Search templates</label>
<input id="site-search" name="q" type="search" placeholder="Search templates" autocomplete="off">
<button type="submit" aria-label="Search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button>
</form>
</nav>
</div>
</header>
<main id="main">
'''


def footer(d):
    p = "../" if d else ""
    cats = "".join(f'<li><a href="{p}{c[2]}">{c[1]}</a></li>' for c in CATS)
    return f'''</main>
<footer class="site-footer">
<div class="wrap fgrid">
<div><a class="logo logo-light" href="{p}index.html" aria-label="TemplivoX home"><span class="logo-word">Templivo</span><span class="logo-x" aria-hidden="true">X</span></a>
<p>Free Templates. Made Simple.</p><p class="small">Printable PDF and editable Word and Excel templates for everyday life.</p></div>
<div><h2>Explore</h2><ul><li><a href="{p}index.html">Home</a></li><li><a href="{p}templates.html">All Templates</a></li><li><a href="{p}about.html">About</a></li><li><a href="{p}contact.html">Contact</a></li></ul></div>
<div><h2>Categories</h2><ul>{cats}</ul></div>
<div><h2>Legal</h2><ul><li><a href="{p}privacy-policy.html">Privacy Policy</a></li><li><a href="{p}terms.html">Terms of Use</a></li><li><a href="{p}disclaimer.html">Disclaimer</a></li></ul></div>
</div>
<div class="wrap copy">&copy; 2026 TemplivoX. All rights reserved.</div>
</footer>
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''


def crumbs(items, d):
    p = "../" if d else ""; out = []
    for i, (n, path) in enumerate(items):
        out.append(f'<li><a href="{p}{path}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{"".join(out)}</ol></div></nav>'


def card(t, d, eager=False):
    p = "../" if d else ""; url = f"{p}templates/{t['slug']}.html"; img = f"{t['slug']}-thumb.jpg"; iw, ih = imgsize(img)
    badges = "".join(f'<span class="badge">{FMT[f]}</span>' for f in t["fmts"])
    return f'''<article class="card" data-name="{E(t['title'].lower() + ' ' + CATMAP[t['cat']][1].lower())}" data-cat="{t['cat']}" data-formats="{' '.join(t['fmts'])}">
<a class="card-img" href="{url}" tabindex="-1"><img src="{p}assets/images/{img}" alt="Preview of the {E(t['title'])} printable template" width="{iw}" height="{ih}" {'' if eager else 'loading="lazy" '}decoding="async"></a>
<div class="card-body"><h3><a href="{url}">{E(t['title'])}</a></h3><p>{E(t['short'])}</p><div class="badges">{badges}</div><a class="btn btn-sm" href="{url}">View Template</a></div>
</article>'''


def grid(items, d, eager=0): return '<div class="grid">' + "".join(card(t, d, i < eager) for i, t in enumerate(items)) + "</div>"


def page(path, title, desc, body, crumb=None, extra_ld=None, d=0, img=None, noindex=False):
    graph = []
    if crumb: graph.append(crumbs_ld([("Home", "index.html")] + crumb))
    if extra_ld: graph += extra_ld
    extra = ld({"@context": "https://schema.org", "@graph": graph}) if graph else ""
    bc = crumbs([("Home", "index.html")] + crumb, d) if crumb else ""
    w(path, head(title, desc, path, d, img, extra, noindex) + header(d) + bc + body + footer(d))


# ---------------- pages ----------------
CAT_TIPS = {
    "study": ("Getting more from study planners", "Plan around your energy, not just your timetable. Put demanding subjects in the hours when you concentrate best, keep sessions to 25 to 50 minutes, and leave a day each week with no new material. Pair the weekly planner with the daily one: the weekly page shows balance, the daily page shows exactly what to do next."),
    "budget": ("Making a budget you can keep", "A budget works when it is easy to maintain. Start with last month's real spending, track for one full month before changing anything, and review once a week for ten minutes. If you prefer to calculate automatically, the Excel versions include formulas for totals and differences."),
    "daily": ("Planning without overloading", "Limit yourself to three priorities a day and let the rest wait on the to-do list. Use the weekly planner on Sunday to see the shape of the week, the monthly planner for deadlines, and the habit tracker to build routines one at a time."),
    "business": ("Paperwork that looks professional", "Clear documents get paid and approved faster. Use consistent numbering for invoices and quotations, state payment terms plainly, and keep a copy of everything you send. Tax and invoicing rules vary by country, so check your local requirements."),
    "calendars": ("Choosing the right calendar", "Use the yearly calendar for the big picture, the monthly calendar for deadlines, and the weekly calendar to schedule hours. The blank calendar is for anything unusual such as rotas, four-week cycles or content plans. All calendars start the week on Monday."),
    "personal": ("Small systems for a calmer home", "Routines are easier when they are visible. Plan meals before shopping, split cleaning into daily, weekly and monthly jobs, and log books and goals in one place so progress is easy to see and enjoy."),
}


def build_home():
    feat = [BY[s] for s in FEATURED]; late = [BY[s] for s in LATEST]
    hw = imgsize("weekly-study-planner-preview.jpg"); hb = imgsize("monthly-budget-planner-preview.jpg")
    cats = "".join(f'<a class="cat" href="{c[2]}"><h3>{c[1]}</h3><p>{c[3]}</p><span class="count">{sum(1 for t in TEMPLATES if t["cat"] == c[0])} templates</span></a>' for c in CATS)
    why = [("Free downloads", "Every template is free to download and use at home, at school or at work. No account or payment needed."),
           ("Easy-to-use templates", "Each page explains how to use the template, so you can start filling it in within a minute."),
           ("Printable PDF files", "Print-ready PDFs in A4 and US Letter sizes, designed to look clear in black and white too."),
           ("Editable formats", "Most templates also come as Word documents, and many as Excel spreadsheets with working formulas."),
           ("Simple and clean designs", "Plain layouts with generous writing space, so the template helps you instead of getting in the way.")]
    whyh = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in why)
    body = f'''<section class="hero"><div class="wrap hero-grid">
<div><h1>Free Templates to Organize Your Everyday Life</h1>
<p class="lead">Discover beautifully designed printable planners, trackers, calendars, and editable templates to make everyday tasks easier.</p>
<p class="cta"><a class="btn" href="templates.html">Explore Templates</a><a class="btn btn-ghost" href="#categories">Browse Categories</a></p></div>
<div class="hero-art" aria-hidden="false">
<img src="assets/images/weekly-study-planner-preview.jpg" alt="Weekly Study Planner template preview" width="{hw[0]}" height="{hw[1]}" fetchpriority="high">
<img src="assets/images/monthly-budget-planner-preview.jpg" alt="Monthly Budget Planner template preview" width="{hb[0]}" height="{hb[1]}">
</div></div></section>
<section class="sec" id="categories"><div class="wrap"><h2>Popular Categories</h2><p class="sub">Six collections covering study, money, time, work, dates and home life.</p><div class="cats">{cats}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>Featured Templates</h2><p class="sub">A good place to start if you are new here.</p>{grid(feat, 0)}</div></section>
<section class="sec"><div class="wrap"><h2>Why Choose TemplivoX?</h2><ul class="why">{whyh}</ul></div></section>
<!-- ADSENSE-SLOT: homepage-mid (inactive placeholder). See README, "Adding AdSense later". -->
<section class="sec alt"><div class="wrap"><h2>Latest Templates</h2><p class="sub">Recently added to the collection.</p>{grid(late, 0)}</div></section>
<section class="sec"><div class="wrap"><div class="news"><div><h2>Get new templates by email</h2>
<p>We plan to offer an occasional email when new templates are added. The newsletter is not live yet, because it needs a real email service behind it, so the form below is switched off for now.</p></div>
<form class="news-form" aria-describedby="news-note"><label for="news-email">Email address</label>
<div class="row"><input id="news-email" type="email" placeholder="you@example.com" disabled><button type="button" class="btn" disabled>Coming soon</button></div>
<p id="news-note" class="small">No emails are collected on this website.</p></form></div></div></section>
'''
    page("index.html", "TemplivoX | Free Printable Planners, Trackers & Templates",
         "Download free printable planners, budget trackers, calendars and business templates as PDF, Word and Excel files from TemplivoX.",
         body, extra_ld=[
             {"@type": "WebSite", "name": "TemplivoX", "url": BASE + "/", "description": "Free printable planners, trackers, calendars and editable templates in PDF, Word and Excel formats.", "inLanguage": "en"},
             {"@type": "Organization", "name": "TemplivoX", "url": BASE + "/", "email": EMAIL}])


def listing(path, h1, title, desc, intro, items, crumb, extra_html="", ld_name=None):
    il = {"@type": "CollectionPage", "name": h1, "description": desc, "url": f"{BASE}/{path}",
          "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/templates/{t['slug']}.html", "name": t["title"]} for i, t in enumerate(items)]}}
    return il


def build_listings():
    # all templates
    filt = '''<form id="filter-form" class="filters" role="search" aria-label="Filter templates">
<div><label for="f-q">Search by name</label><input id="f-q" type="search" placeholder="e.g. budget, planner" autocomplete="off"></div>
<div><label for="f-cat">Category</label><select id="f-cat"><option value="">All categories</option>%s</select></div>
<div><label for="f-fmt">File format</label><select id="f-fmt"><option value="">Any format</option><option value="pdf">PDF</option><option value="docx">Word (DOCX)</option><option value="xlsx">Excel (XLSX)</option></select></div>
</form>
<p id="result-count" class="count-line" aria-live="polite"></p>''' % "".join(f'<option value="{c[0]}">{c[1]}</option>' for c in CATS)
    body = f'''<section class="page-head"><div class="wrap"><h1>All Free Printable Templates</h1>
<p class="lead">Search and filter all {len(TEMPLATES)} templates by name, category or file format. Every template can be downloaded as a print-ready PDF, and most also as an editable file.</p></div></section>
<section class="sec"><div class="wrap">{filt}{grid(TEMPLATES, 0)}
<div id="no-results" class="empty" hidden><h2>No templates found</h2><p>Nothing matches your search. Try a shorter word, choose a different category, or set the format to Any. You can also <a href="contact.html">request a template</a>.</p></div></div></section>'''
    page("templates.html", "All Free Printable Templates (PDF, Word, Excel) | TemplivoX",
         "Browse every free printable planner, tracker, calendar and business template. Search by name and filter by category or file format.",
         body, crumb=[("All Templates", "templates.html")], extra_ld=[listing("templates.html", "All Templates", "", "", "", TEMPLATES, None)])
    for c in CATS:
        items = [t for t in TEMPLATES if t["cat"] == c[0]]; tip = CAT_TIPS[c[0]]
        others = "".join(f'<li><a href="{o[2]}">{o[1]}</a></li>' for o in CATS if o[0] != c[0])
        body = f'''<section class="page-head"><div class="wrap"><h1>Free {c[1]} (Printable PDF and Editable)</h1><p class="lead">{c[3]}</p></div></section>
<section class="sec"><div class="wrap">{grid(items, 0)}</div></section>
<section class="sec alt"><div class="wrap prose"><h2>{tip[0]}</h2><p>{tip[1]}</p>
<h2>Explore other categories</h2><ul class="inline">{others}<li><a href="templates.html?cat={c[0]}">Filter {c[1]} in the template finder</a></li></ul></div></section>'''
        page(c[2], f"Free Printable {c[1]} (PDF & Editable) | TemplivoX", c[3][:150] if len(c[3]) > 150 else c[3],
             body, crumb=[(c[1], c[2])], extra_ld=[listing(c[2], c[1], "", c[3], "", items, None)])


def build_template_pages():
    for t in TEMPLATES:
        s = t["slug"]; c = CATMAP[t["cat"]]; d = 1
        rel = [x for x in TEMPLATES if x["cat"] == t["cat"] and x["slug"] != s][:3]
        pw, ph = imgsize(f"{s}-preview.jpg")
        dl = [(f"downloads/pdf/{s}.pdf", "Download PDF (A4)", "btn")]
        dl.append((f"downloads/pdf/{s}-us-letter.pdf", "Download PDF (US Letter)", "btn btn-ghost"))
        if "docx" in t["fmts"]: dl.append((f"downloads/docx/{s}-editable.docx", "Download Editable Word (.docx)", "btn btn-ghost"))
        if "xlsx" in t["fmts"]: dl.append((f"downloads/xlsx/{s}-editable.xlsx", "Download Editable Excel (.xlsx)", "btn btn-ghost"))
        btns = "".join(f'<li><a class="{k}" href="../{h}" download>{lab}<small>{fsize(h)}</small></a></li>' for h, lab, k in dl)
        feats = "".join(f"<li>{E(f)}</li>" for f in t["feats"])
        faqs = [(t["fq"], t["fa"]), (f"Is the {t['title']} really free?", "Yes. You can download and print it for personal, educational or internal business use at no cost. See the Terms of Use for details."),
                ("Which paper sizes are available?", "The PDF comes in A4 and US Letter. Print at 100 percent or Actual size so nothing is scaled or cropped.")]
        faqh = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
        fm = ", ".join({"pdf": "PDF (print-ready)", "docx": "Word (.docx)", "xlsx": "Excel (.xlsx)"}[f] for f in t["fmts"])
        landscape = " The Word version uses a landscape page." if any(x in s for x in ("habit-tracker", "weekly-calendar", "reading-tracker", "debt-tracker")) else ""
        steps = ["Download the PDF to print, or the editable file to fill in on a computer.", t["how"],
                 "Print at 100 percent scale on A4 or US Letter paper, or save your edited file as a PDF."]
        steps = "".join(f"<li>{E(x)}</li>" for x in steps)
        rh = "".join([grid(rel, d)])
        fl = "PDF, Word & Excel" if "xlsx" in t["fmts"] else "PDF & Word"
        title = f"Free Printable {t['title']} ({fl})"
        if len(title) + 12 <= 66: title += " | TemplivoX"
        desc = (t["short"] + " " + t["more"])[:155].rsplit(" ", 1)[0] + "..." if len(t["short"] + t["more"]) > 158 else t["short"] + " " + t["more"]
        body = f'''<article>
<section class="page-head"><div class="wrap"><h1>{E(t['title'])}</h1><p class="lead">{E(t['short'])} {E(t['more'])}</p></div></section>
<section class="sec"><div class="wrap tpl">
<div class="tpl-prev"><a href="../downloads/pdf/{s}.pdf" aria-label="Open the {E(t['title'])} PDF"><img src="../assets/images/{s}-preview.jpg" alt="Large preview of the {E(t['title'])} printable template on A4 paper" width="{pw}" height="{ph}" fetchpriority="high"></a></div>
<div class="tpl-info">
<h2>Download {E(t['title'])}</h2>
<ul class="dl">{btns}</ul>
<p class="small">All files are real, ready-to-use downloads. No sign-up required.</p>
<!-- ADSENSE-SLOT: template-sidebar (inactive placeholder). See README, "Adding AdSense later". -->
<h2>Paper size and file formats</h2>
<dl class="facts"><dt>Paper size</dt><dd>A4 (210 x 297 mm) and US Letter (8.5 x 11 in)</dd><dt>Formats</dt><dd>{fm}</dd><dt>Category</dt><dd><a href="../{c[2]}">{c[1]}</a></dd></dl>
{("<p class=small>" + landscape.strip() + "</p>") if landscape else ""}
</div></div></section>
<section class="sec alt"><div class="wrap prose"><h2>Features and benefits</h2><ul>{feats}</ul>
<h2>How to use this template</h2><ol>{steps}</ol></div></section>
<!-- ADSENSE-SLOT: template-in-content (inactive placeholder). See README, "Adding AdSense later". -->
<section class="sec"><div class="wrap prose"><h2>Frequently asked questions</h2><div class="faq">{faqh}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>Related templates</h2>{rh}<p class="more"><a href="../{c[2]}">See all {c[1].lower()}</a></p></div></section>
</article>'''
        url = f"{BASE}/templates/{s}.html"
        page(f"templates/{s}.html", title, desc, body, d=1, img=f"{BASE}/assets/images/{s}-preview.jpg",
             crumb=[(c[1], c[2]), (t["title"], f"templates/{s}.html")],
             extra_ld=[{"@type": "WebPage", "name": t["title"], "description": desc, "url": url, "isPartOf": {"@type": "WebSite", "name": "TemplivoX", "url": BASE + "/"},
                        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{BASE}/assets/images/{s}-preview.jpg"}},
                       {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}])


def static(path, h1, title, desc, html_body, lead=""):
    body = f'<section class="page-head"><div class="wrap"><h1>{h1}</h1>{"<p class=lead>" + lead + "</p>" if lead else ""}</div></section><section class="sec"><div class="wrap prose">{html_body}</div></section>'
    page(path, title, desc, body, crumb=[(h1, path)])


def build_static():
    static("about.html", "About TemplivoX", "About TemplivoX | Free Templates. Made Simple.",
           "Learn who TemplivoX is for, how the free printable and editable templates are made, and how to get in touch.",
           f'''<h2>Our purpose</h2><p>TemplivoX is a library of free printable and editable templates for everyday organising. The goal is simple: give people clean, practical documents they can download in a minute and start using straight away, without sign-ups, pop-ups or clutter.</p>
<h2>How the templates are made</h2><p>Each template is built around one job, such as planning a study week, tracking a debt or writing an invoice. Layouts are kept plain so they print clearly on a home printer, and the PDF versions come in both A4 and US Letter. Editable versions are provided as Word documents and, where numbers are involved, as Excel spreadsheets with working formulas.</p>
<h2>What you will find here</h2><p>The library currently has {len(TEMPLATES)} templates in six categories: <a href="study-templates.html">study</a>, <a href="budget-templates.html">budget</a>, <a href="daily-planners.html">daily planning</a>, <a href="business-templates.html">business</a>, <a href="calendars.html">calendars</a> and <a href="personal-templates.html">personal life</a>. New ones are added over time, and you can <a href="contact.html">suggest a template</a> you would like to see.</p>
<h2>Our approach</h2><p>Templates are general-purpose tools, not professional advice. Please read the <a href="disclaimer.html">disclaimer</a> before relying on any financial, legal or business template.</p>''',
           "Free templates, designed to be useful the moment you download them.")
    static("contact.html", "Contact TemplivoX", "Contact TemplivoX | Questions, Feedback & Template Requests",
           "Contact TemplivoX with a question, a correction or a template request. The form opens your email app; there is no server.",
           f'''<p>We welcome questions, bug reports, corrections and ideas for new templates. You can email us directly at <a href="mailto:{EMAIL}">{EMAIL}</a>, or use the form below.</p>
<form id="contact-form" class="form" data-to="{EMAIL}"><div><label for="c-name">Your name</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
<div><label for="c-email">Your email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
<div><label for="c-sub">Subject</label><input id="c-sub" name="subject" type="text" required></div>
<div><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea></div>
<button class="btn" type="submit">Open in my email app</button>
<p class="small">This site has no server, so the form does not send messages itself. Pressing the button opens a ready-written email in your default email app for you to send.</p></form>
<noscript><p>JavaScript is off, so please email <a href="mailto:{EMAIL}">{EMAIL}</a> directly.</p></noscript>
<h2>Before you write</h2><p>Check the FAQ on the template page first, since many questions about paper sizes and editing are answered there. We cannot give legal, tax or financial advice.</p>''')
    static("privacy-policy.html", "Privacy Policy", "Privacy Policy | TemplivoX",
           "How TemplivoX handles information: no accounts, no forms stored, and what may change if advertising or analytics are added.",
           f'''<p>Last updated: 2 November 2026.</p>
<h2>What we collect</h2><p>TemplivoX does not require an account and does not store personal information in a database. The contact form does not send data to our servers: it opens your own email app, so anything you write is shared only when you choose to send that email. Searching and filtering templates happens in your browser.</p>
<h2>Hosting and logs</h2><p>The website is served by a third-party hosting provider, which may keep technical logs such as IP address, browser type and requested pages for security and reliability. We do not control those logs.</p>
<h2>Cookies, analytics and advertising</h2><p>The site does not currently set cookies of its own. If we later add analytics or advertising, for example Google AdSense, those services may use cookies or similar technologies to measure traffic or show ads. This policy will be updated before that happens and will explain the choices available to you.</p>
<h2>Downloads</h2><p>Template files are downloaded directly from this website. We do not track who downloads which file.</p>
<h2>Children</h2><p>The website is general-purpose and not directed at children under 13.</p>
<h2>Your rights and contact</h2><p>Depending on where you live, you may have rights over your personal data. Because we hold none, there is usually nothing to access or delete, but you can ask us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes</h2><p>We may update this policy and will change the date above when we do.</p>''')
    static("terms.html", "Terms of Use", "Terms of Use | TemplivoX",
           "Terms for using TemplivoX templates: personal and internal business use is free, resale and misrepresentation are not allowed.",
           '''<p>Last updated: 2 November 2026. By using this website you agree to these terms.</p>
<h2>Permitted use</h2><p>You may download, print and edit the templates for personal, educational and internal business use at no charge, including printing copies for your own team or classroom.</p>
<h2>Not permitted</h2><p>You may not sell, resell or redistribute the template files as your own product, claim them as your own work, or republish them in bulk on another website or file-sharing service. Linking to our pages is welcome.</p>
<h2>No warranty</h2><p>Templates and website content are provided as they are, without warranties of any kind. We do not guarantee that templates are error-free or suitable for your purpose, including any legal or tax requirement.</p>
<h2>Limitation of liability</h2><p>To the extent allowed by law, TemplivoX is not liable for losses arising from use of the website or templates.</p>
<h2>External links</h2><p>The website may link to other sites. We are not responsible for their content or practices.</p>
<h2>Changes</h2><p>We may change these terms from time to time. Continued use after a change means you accept the updated terms.</p>''')
    static("disclaimer.html", "Disclaimer", "Disclaimer | TemplivoX",
           "TemplivoX templates are general-purpose tools. Read this disclaimer before relying on financial, legal or business templates.",
           '''<p>Last updated: 2 November 2026.</p>
<h2>General information only</h2><p>The templates and text on TemplivoX are general tools for organising information. They are not legal, tax, accounting, financial or medical advice.</p>
<h2>Business and financial templates</h2><p>Invoices, quotations and receipts have different legal and tax requirements in different countries. Check what applies to you, such as tax identification numbers or mandatory wording, before using them in business. Spreadsheet formulas are simple helpers, so check the results yourself.</p>
<h2>Accuracy</h2><p>We take care to make the files work, but errors can happen and printing can vary between devices. Always review a document before using or sending it. The 2027 calendar uses the Gregorian calendar and does not mark public holidays.</p>
<h2>Third-party software</h2><p>Word and Excel are trademarks of Microsoft. The editable files also open in compatible applications, but formatting may vary slightly. TemplivoX is not affiliated with Microsoft.</p>''')


# ---------------- assets ----------------
CSS = """:root{--green:#1f3d2b;--green2:#2d5a3f;--beige:#f6f1e7;--beige2:#ece4d3;--ink:#1c231e;--muted:#5a625c;--line:#e2d9c6;--r:10px;--sh:0 1px 2px rgba(31,61,43,.06),0 8px 22px rgba(31,61,43,.07);--serif:Georgia,"Times New Roman",serif;--sans:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
*{box-sizing:border-box}[hidden]{display:none!important}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.65 var(--sans);color:var(--ink);background:#fff}
img{max-width:100%;height:auto;display:block}a{color:var(--green2)}a:hover{color:var(--green)}
:focus-visible{outline:3px solid #b8860b;outline-offset:2px}
.skip{position:absolute;left:-999px;top:0;background:var(--green);color:#fff;padding:.6rem 1rem;z-index:100}.skip:focus{left:0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--serif);color:var(--green);line-height:1.2;margin:0 0 .6em}
h1{font-size:clamp(2rem,5vw,3.1rem);letter-spacing:-.01em}h2{font-size:clamp(1.5rem,3vw,2rem)}h3{font-size:1.2rem}
.lead{font-size:1.15rem;color:var(--muted);max-width:62ch}.sub{color:var(--muted);margin-top:-.3em}.small{font-size:.88rem;color:var(--muted)}
.site-header{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.bar{display:flex;align-items:center;gap:20px;min-height:68px}
.logo{display:inline-flex;align-items:center;text-decoration:none;font:700 1.55rem var(--serif);color:var(--green);gap:3px}
.logo-x{background:var(--green);color:#fff;border-radius:6px;padding:0 7px;line-height:1.25;font-size:1.3rem}
.logo-light{color:#fff}.logo-light .logo-x{background:#fff;color:var(--green)}
.nav{display:flex;align-items:center;gap:18px;margin-left:auto}.nav ul{list-style:none;margin:0;padding:0;display:flex;gap:4px;align-items:center}
.nav a,.dd-btn{color:var(--ink);text-decoration:none;padding:.5rem .8rem;border-radius:8px;font:500 .98rem var(--sans);background:none;border:0;cursor:pointer;display:block}
.nav a:hover,.dd-btn:hover{background:var(--beige)}.dd-btn:after{content:"";display:inline-block;margin-left:.45em;border:4px solid transparent;border-top-color:currentColor;border-bottom:0}
.dd{position:relative}.nav .dd-menu{display:none;position:absolute;top:100%;left:0;min-width:220px;background:#fff;border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh);padding:6px;flex-direction:column;align-items:stretch}
.nav .dd.open .dd-menu{display:flex}.nav .dd-menu a{text-align:left}@media(hover:hover){.nav .dd:hover .dd-menu{display:flex}}
.search{display:flex;border:1px solid var(--line);border-radius:999px;background:var(--beige);overflow:hidden}
.search input{border:0;background:none;padding:.5rem .9rem;font:inherit;width:170px;min-width:0}.search input:focus-visible{outline:none}.search:focus-within{outline:3px solid #b8860b}
.search button{border:0;background:none;padding:0 .8rem;color:var(--green);cursor:pointer}
.nav-toggle{display:none;margin-left:auto;background:none;border:1px solid var(--line);border-radius:8px;padding:10px;cursor:pointer}
.nav-toggle span{display:block;width:20px;height:2px;background:var(--green);margin:4px 0}
.btn{display:inline-block;background:var(--green);color:#fff;text-decoration:none;padding:.75rem 1.4rem;border-radius:8px;font-weight:600;border:2px solid var(--green);cursor:pointer;font-size:1rem;font-family:var(--sans)}
.btn:hover{background:var(--green2);border-color:var(--green2);color:#fff}.btn:disabled{opacity:.55;cursor:not-allowed}
.btn-ghost{background:#fff;color:var(--green)}.btn-ghost:hover{background:var(--beige);color:var(--green)}
.btn-sm{padding:.5rem 1rem;font-size:.92rem}
.hero{background:var(--beige);border-bottom:1px solid var(--line)}.hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding:64px 20px}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:1.6rem}
.hero-art{display:flex;gap:16px;align-items:flex-start;justify-content:center}.hero-art img{width:48%;border:1px solid var(--line);border-radius:6px;box-shadow:var(--sh);background:#fff}.hero-art img+img{margin-top:36px}
.sec{padding:60px 0}.alt{background:var(--beige)}.page-head{background:var(--beige);border-bottom:1px solid var(--line);padding:44px 0 36px}.page-head h1{margin-bottom:.3em}
.crumbs{border-bottom:1px solid var(--line);font-size:.9rem;background:#fff}.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:.7rem 0}
.crumbs li+li:before{content:"/";margin-right:6px;color:var(--muted)}.crumbs a{text-decoration:none}
.cats{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.cat{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px;text-decoration:none;color:var(--ink);display:block;box-shadow:var(--sh);transition:border-color .15s}
.cat:hover{border-color:var(--green);color:var(--ink)}.cat h3{margin-bottom:.3em}.cat p{margin:0 0 .8rem;color:var(--muted);font-size:.96rem}.count{font-weight:600;color:var(--green2);font-size:.9rem}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;box-shadow:var(--sh)}
.card-img{display:block;background:var(--beige2);padding:18px 18px 0;border-bottom:1px solid var(--line);height:250px;overflow:hidden}
.card-img img{width:100%;border:1px solid var(--line);border-bottom:0;border-radius:4px 4px 0 0;background:#fff}
.card-body{padding:18px;display:flex;flex-direction:column;gap:10px;flex:1}.card-body h3{margin:0}.card-body h3 a{text-decoration:none;color:var(--green)}
.card-body p{margin:0;color:var(--muted);font-size:.95rem;flex:1}.card-body .btn{align-self:flex-start}
.badges{display:flex;gap:6px;flex-wrap:wrap}.badge{font-size:.78rem;font-weight:600;border:1px solid var(--line);background:var(--beige);border-radius:999px;padding:.1rem .6rem;color:var(--green)}
.why{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.why li{border-left:4px solid var(--green);padding:4px 0 4px 16px}.why p{margin:0;color:var(--muted)}
.news{background:var(--green);color:#fff;border-radius:14px;padding:40px;display:grid;grid-template-columns:1.2fr 1fr;gap:32px;align-items:center}
.news h2{color:#fff}.news p{margin:0;color:#e5ecdf}.news .small{color:#cdd9c8;margin-top:8px}
.news-form label{display:block;font-weight:600;margin-bottom:6px}.news-form .row{display:flex;gap:8px}
.news-form input{flex:1;min-width:0;padding:.7rem .9rem;border-radius:8px;border:1px solid #fff;font:inherit;background:#e9eee6}
.news-form .btn{background:#fff;color:var(--green);border-color:#fff}
.filters{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;background:var(--beige);border:1px solid var(--line);border-radius:var(--r);padding:18px;margin-bottom:12px}
label{font-weight:600;font-size:.92rem;display:block;margin-bottom:4px}
input[type=text],input[type=email],input[type=search],select,textarea{width:100%;padding:.65rem .8rem;border:1px solid #cfc5ae;border-radius:8px;font:inherit;background:#fff;color:var(--ink)}
.count-line{color:var(--muted);margin:8px 0 18px}.empty{text-align:center;padding:48px 20px;border:1px dashed #cfc5ae;border-radius:var(--r);background:var(--beige)}
.tpl{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}.tpl-prev img{border:1px solid var(--line);border-radius:6px;box-shadow:var(--sh);background:#fff;width:100%}
.dl{list-style:none;margin:0 0 12px;padding:0;display:grid;gap:10px}.dl .btn{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:left}.dl small{font-weight:500;opacity:.8}
.facts{display:grid;grid-template-columns:110px 1fr;gap:8px 12px;margin:0}.facts dt{font-weight:600}.facts dd{margin:0}
.prose{max-width:820px}.prose ul,.prose ol{padding-left:1.3rem}.prose li{margin:.35rem 0}.inline{list-style:none;padding:0!important;display:flex;flex-wrap:wrap;gap:8px 20px}
.faq details{border:1px solid var(--line);border-radius:var(--r);padding:14px 18px;margin-bottom:10px;background:#fff}.faq summary{cursor:pointer;font-weight:600;color:var(--green)}.faq p{margin:.6rem 0 0}
.more{margin-top:22px}.form{display:grid;gap:16px;max-width:560px;margin:24px 0}
.site-footer{background:var(--green);color:#dfe8da;padding-top:48px;margin-top:0}.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}
.site-footer h2{color:#fff;font-size:1rem;font-family:var(--sans);margin-bottom:.8em}.site-footer ul{list-style:none;padding:0;margin:0}.site-footer li{margin:.4rem 0}
.site-footer a{color:#dfe8da;text-decoration:none}.site-footer a:hover{text-decoration:underline;color:#fff}.site-footer .small{color:#b9c9b4}
.copy{border-top:1px solid rgba(255,255,255,.18);margin-top:36px;padding-top:18px;padding-bottom:22px;font-size:.88rem;color:#b9c9b4}
@media(max-width:960px){.grid,.cats,.why{grid-template-columns:repeat(2,1fr)}.fgrid{grid-template-columns:1fr 1fr}.tpl{gap:28px}}
@media(max-width:820px){.nav-toggle{display:block}.nav{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;align-items:stretch;padding:12px 20px 20px;margin:0;box-shadow:var(--sh)}
.nav.open{display:flex}.nav ul{flex-direction:column;align-items:stretch}.nav .dd-menu{display:flex;position:static;border:0;box-shadow:none;padding:0 0 0 14px;min-width:0}.dd-btn:after{display:none}.search input{width:100%}.search{width:100%}
.hero-grid,.tpl,.news,.filters{grid-template-columns:1fr}.hero-grid{padding:40px 20px}.hero-art{order:-1;max-width:420px;margin:0 auto}.tpl-prev{max-width:520px}}
@media(max-width:600px){.grid,.cats,.why{grid-template-columns:1fr}.fgrid{grid-template-columns:1fr}.sec{padding:44px 0}.news{padding:26px}.card-img{height:auto;max-height:300px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
@media print{.site-header,.site-footer,.crumbs,.skip{display:none}}
"""

JS = """(function () {
  'use strict';
  var d = document;
  var toggle = d.querySelector('.nav-toggle'), nav = d.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }
  var dd = d.querySelector('.dd');
  if (dd) {
    var btn = dd.querySelector('.dd-btn');
    var close = function () { dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', function (e) {
      var open = dd.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      e.stopPropagation();
    });
    d.addEventListener('click', function (e) { if (!dd.contains(e.target)) close(); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  var form = d.getElementById('filter-form');
  if (form) {
    var q = d.getElementById('f-q'), cat = d.getElementById('f-cat'), fmt = d.getElementById('f-fmt');
    var cards = Array.prototype.slice.call(d.querySelectorAll('.card[data-name]'));
    var count = d.getElementById('result-count'), empty = d.getElementById('no-results');
    var params = new URLSearchParams(window.location.search);
    q.value = params.get('q') || '';
    cat.value = params.get('cat') || '';
    fmt.value = params.get('format') || '';
    if (cat.value !== (params.get('cat') || '')) cat.value = '';
    var apply = function () {
      var term = q.value.trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var ok = (!term || c.getAttribute('data-name').indexOf(term) !== -1) &&
                 (!cat.value || c.getAttribute('data-cat') === cat.value) &&
                 (!fmt.value || c.getAttribute('data-formats').split(' ').indexOf(fmt.value) !== -1);
        c.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = 'Showing ' + shown + ' of ' + cards.length + ' templates';
      empty.hidden = shown !== 0;
    };
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    ['input', 'change'].forEach(function (ev) { form.addEventListener(ev, apply); });
    apply();
  }

  var cf = d.getElementById('contact-form');
  if (cf) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var g = function (n) { return cf.elements[n].value; };
      var body = 'Name: ' + g('name') + '\\nEmail: ' + g('email') + '\\n\\n' + g('message');
      window.location.href = 'mailto:' + cf.getAttribute('data-to') + '?subject=' + encodeURIComponent(g('subject')) + '&body=' + encodeURIComponent(body);
    });
  }
})();
"""

README = """# TemplivoX - Free Templates. Made Simple.

A static, multi-page template website (HTML5, CSS3, vanilla JavaScript). No framework, no backend, no database.
Works on GitHub Pages because every path is relative.

## What is inside

```
index.html, templates.html, 6 category pages, about, contact, privacy-policy, terms, disclaimer, 404.html
templates/        29 individual template pages (one per template)
assets/css/       style.css
assets/js/        main.js (menu, search, filters, contact form)
assets/images/    preview + thumbnail JPEGs (rendered from the real PDFs), favicon.svg, social card
downloads/pdf/    <name>.pdf (A4) and <name>-us-letter.pdf
downloads/docx/   <name>-editable.docx
downloads/xlsx/   <name>-editable.xlsx (formulas included)
sitemap.xml, robots.txt
tools/            the Python scripts that generated everything (optional)
```

## Run locally

Open `index.html` in a browser, or run a tiny local server (recommended, closest to GitHub Pages):

```
cd templivox
python3 -m http.server 8000
```

Then visit http://localhost:8000

## Publish on GitHub Pages

1. Create a repository named `husnainali847809-hub.github.io` (this exact name is required for the root GitHub Pages address you provided).
2. Upload everything inside this folder (drag and drop in the browser, or use `git add . && git commit && git push`).
3. Open Settings > Pages, choose "Deploy from a branch", branch `main`, folder `/ (root)`, and save.
4. After a minute your site is live at `https://husnainali847809-hub.github.io/`.

## Site configuration

This project is already configured for:

- Website: `https://husnainali847809-hub.github.io/`
- Contact: `husnainali847809@gmail.com`

Canonical URLs, Open Graph metadata, structured data, `sitemap.xml`, `robots.txt` and contact details are set to these values. If you change the repository name or domain later, update `BASE` and `EMAIL` in `tools/data.py` before rebuilding the site.

After publishing, add the site to Google Search Console and submit `https://husnainali847809-hub.github.io/sitemap.xml`.

## About the download files

All downloads are real files generated by `tools/build_site.py`: simple, original, print-ready layouts.
To use your own designed files instead, keep the same filenames and overwrite the file in `downloads/`.
To add a new template, add an entry in `tools/data.py` and re-run the build (see below), or copy an existing
page in `templates/`, rename it, and add its card to the listing pages.

Re-generating everything (requires Python 3 with reportlab, python-docx, openpyxl, Pillow and poppler's `pdftoppm`):

```
cd tools
python3 build_site.py ..
```

## Search and filters

`templates.html` reads each card's `data-name`, `data-cat` and `data-formats` attributes. Links such as
`templates.html?cat=budget`, `templates.html?q=invoice` and `templates.html?format=xlsx` also work.

## Newsletter and contact form

There is no backend. The newsletter form is intentionally disabled ("Coming soon"). Connect a real
email service later and replace that form. The contact form opens the visitor's email app (mailto).

## Adding AdSense later

No ad code is included. Inactive placeholder comments mark good spots: `ADSENSE-SLOT: homepage-mid`,
`template-sidebar` and `template-in-content`. Search for `ADSENSE-SLOT`. Only add Google's code after your site is approved.

## Honest notes

- Template text is original but short. Before applying to AdSense, expand each template page with more
  helpful content (examples, tips, use cases). Thin pages are a common reason for rejection.
- Privacy policy, terms and disclaimer are general starting points, not legal advice. Have them reviewed.
- Nothing here guarantees search rankings or ad approval.
- The yearly calendar is dated 2027. Regenerate it for other years by changing `year=` in `tools/data.py`.
"""


def social_card():
    im = Image.new("RGB", (1200, 630), "#f6f1e7"); dr = ImageDraw.Draw(im)
    try:
        big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 120)
        mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)
    except Exception:
        big = mid = ImageFont.load_default()
    dr.rectangle([0, 0, 1200, 24], fill="#1f3d2b")
    dr.text((90, 200), "Templivo", font=big, fill="#1f3d2b")
    x = 90 + dr.textlength("Templivo", font=big) + 16
    dr.rounded_rectangle([x, 205, x + 105, 345], radius=14, fill="#1f3d2b"); dr.text((x + 20, 200), "X", font=big, fill="white")
    dr.text((94, 390), "Free Templates. Made Simple.", font=mid, fill="#5a625c")
    im.save(os.path.join(ROOT, "assets/images/templivox-social-card.png"), optimize=True)


def build_site(root):
    global ROOT; ROOT = root
    w("assets/css/style.css", CSS); w("assets/js/main.js", JS); w("README.md", README)
    w("assets/images/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#1f3d2b"/><text x="32" y="46" font-family="Georgia,serif" font-size="40" font-weight="700" text-anchor="middle" fill="#fff">X</text></svg>')
    social_card(); build_home(); build_listings(); build_template_pages(); build_static()
    w("404.html", head("Page not found | TemplivoX", "The page you were looking for could not be found on TemplivoX.", "404.html", 0, noindex=True) + header(0) +
      '<section class="page-head"><div class="wrap"><h1>Page not found</h1><p class="lead">That page does not exist or has moved. Try the <a href="templates.html">template finder</a> or go back to the <a href="index.html">homepage</a>.</p></div></section>' + footer(0))
    pages = ["index.html", "templates.html"] + [c[2] for c in CATS] + ["about.html", "contact.html", "privacy-policy.html", "terms.html", "disclaimer.html"] + [f"templates/{t['slug']}.html" for t in TEMPLATES]
    urls = "".join(f"<url><loc>{BASE + '/' if p == 'index.html' else BASE + '/' + p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages)
    w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

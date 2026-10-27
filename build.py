"""Build the static pages from src/template.html + i18n/*.json + data/stays.json.

    python build.py

Writes index.html (English), fr/index.html, ar/index.html, sitemap.xml and robots.txt.
The generated files are committed, so GitHub Pages serves them as-is.
Change BASE when the site moves to its own domain.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

BASE = "https://shadymagorat-tech.github.io/shady-magora-365"
PHONE = "201026315970"
LANGS = ["en", "fr", "ar"]
OG_LOCALE = {"en": "en_US", "fr": "fr_FR", "ar": "ar_EG"}
FONTS = {
    "en": "https://fonts.googleapis.com/css2?family=Gloock&family=Manrope:wght@400;600;700;800&display=swap",
    "fr": "https://fonts.googleapis.com/css2?family=Gloock&family=Manrope:wght@400;600;700;800&display=swap",
    "ar": "https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Gloock&family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap",
}

ROOT = Path(__file__).parent


def url_for(code):
    return f"{BASE}/" if code == "en" else f"{BASE}/{code}/"


def wa(text):
    return f"https://wa.me/{PHONE}?text={quote(text)}"


def ribbon():
    """365 nights as thin ticks, grouped by month. Brass = booked, faint = open.
    A believable occupancy pattern: weekends, Eid, Christmas and summer fill first."""
    rng = random.Random(365)
    tick, gap, month_gap, h = 3, 1.6, 7, 34
    x, booked, open_ = 0.0, [], []
    start = date(2026, 1, 1)
    for i in range(365):
        d = start + timedelta(days=i)
        if i and d.day == 1:
            x += month_gap
        p = 0.42
        if d.weekday() in (3, 4):          # Thursday and Friday nights
            p += 0.35
        if d.month in (7, 8) or (d.month == 12 and d.day >= 20) or (d.month == 1 and d.day <= 4):
            p += 0.3
        if d.month == 3 and 18 <= d.day <= 23:   # around Eid al-Fitr 2026
            p += 0.4
        if d.month == 5 and 25 <= d.day <= 31:   # around Eid al-Adha 2026
            p += 0.4
        rect = f'<rect x="{x:.1f}" y="0" width="{tick}" height="{h}" rx="1"/>'
        (booked if rng.random() < min(p, 0.95) else open_).append(rect)
        x += tick + gap
    w = x - gap
    return (f'<svg viewBox="0 0 {w:.0f} {h}" preserveAspectRatio="none" role="img" '
            f'aria-label="A year of nights on the calendar" focusable="false">'
            f'<g class="open">{"".join(open_)}</g><g class="booked">{"".join(booked)}</g></svg>')


def jsonld(t):
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Shady Magora 365",
        "description": t["meta"]["description"],
        "url": url_for(t["lang"]),
        "image": f"{BASE}/assets/og.png",
        "telephone": "+20 102 631 5970",
        "email": "shadymagorat@gmail.com",
        "founder": {"@type": "Person", "name": "Shady Magora"},
        "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
        "areaServed": [{"@type": "City", "name": "Cairo"}, {"@type": "Place", "name": "Ain Sokhna"}],
        "knowsLanguage": ["ar", "en", "fr"],
    }
    return json.dumps(data, ensure_ascii=False)


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "src"), undefined=StrictUndefined, autoescape=True)
    tpl = env.get_template("template.html")
    stays = json.loads((ROOT / "data/stays.json").read_text(encoding="utf-8"))
    rib = ribbon()
    urls = {c: url_for(c) for c in LANGS}

    for code in LANGS:
        t = json.loads((ROOT / f"i18n/{code}.json").read_text(encoding="utf-8"))
        html = tpl.render(
            t=t, langs=LANGS, urls=urls, base=BASE,
            root="./" if code == "en" else "../",
            og_locale=OG_LOCALE[code], fonts_url=FONTS[code],
            jsonld=Markup(jsonld(t).replace("</", "<\\/")), ribbon=Markup(rib), stays=stays,
            wa={k: wa(v) for k, v in t["wa"].items()},
        )
        out = ROOT / ("index.html" if code == "en" else f"{code}/index.html")
        out.parent.mkdir(exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))

    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{urls[c]}"/>' for c in LANGS)
    entries = "".join(f"<url><loc>{urls[c]}</loc>{alts}</url>" for c in LANGS)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{entries}</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()

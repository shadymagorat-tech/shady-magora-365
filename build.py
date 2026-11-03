"""Build the static pages from src/*.html + i18n/*.json + data/stays.json.

    python build.py

Writes, for each language (English at the root, French in fr/, Arabic in ar/):
  index.html          the home page
  owners/index.html   the owner page (what I do, what I don't do, how to start)
plus sitemap.xml and robots.txt.
The generated files are committed, so GitHub Pages serves them as-is.
Change BASE when the site moves to its own domain.
"""
import json
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape

BASE = "https://shadymagorat-tech.github.io/shady-magora-365"
PHONE = "201026315970"
LANGS = ["en", "fr", "ar"]
OG_LOCALE = {"en": "en_US", "fr": "fr_FR", "ar": "ar_EG"}
FONTS = {
    "en": "https://fonts.googleapis.com/css2?family=Gloock&family=Manrope:wght@400;600;700;800&display=swap",
    "fr": "https://fonts.googleapis.com/css2?family=Gloock&family=Manrope:wght@400;600;700;800&display=swap",
    "ar": "https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Gloock&family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap",
}
# page id -> (template, path below the language folder)
PAGES = {"home": ("home.html", ""), "owners": ("owners.html", "owners/")}

ROOT = Path(__file__).parent
TBC = re.compile(r"\[TO CONFIRM[^\]]*\]")


def lang_dir(code):
    return "" if code == "en" else f"{code}/"


def url_for(code, page="home"):
    return f"{BASE}/{lang_dir(code)}{PAGES[page][1]}"


def out_path(code, page):
    return ROOT / lang_dir(code) / PAGES[page][1] / "index.html"


def rel_root(code, page):
    depth = (lang_dir(code) + PAGES[page][1]).count("/")
    return "../" * depth or "./"


def wa(text):
    return f"https://wa.me/{PHONE}?text={quote(text)}"


def tbc(text):
    """Escape text and highlight any [TO CONFIRM ...] placeholder so it can't be missed."""
    html = str(escape(text))
    return Markup(TBC.sub(lambda m: f'<mark class="tbc" dir="ltr" lang="en">{m.group(0)}</mark>', html))


def ribbon():
    """365 nights as thin ticks, grouped by month. Decorative only: every night looks
    the same, so the ribbon makes no claim about bookings or occupancy."""
    tick, gap, month_gap, h = 3, 1.6, 7, 34
    x, ticks = 0.0, []
    start = date(2026, 1, 1)
    for i in range(365):
        d = start + timedelta(days=i)
        if i and d.day == 1:
            x += month_gap
        ticks.append(f'<rect x="{x:.1f}" y="0" width="{tick}" height="{h}" rx="1"/>')
        x += tick + gap
    w = x - gap
    return (f'<svg viewBox="0 0 {w:.0f} {h}" preserveAspectRatio="none" aria-hidden="true" '
            f'focusable="false"><g class="nights">{"".join(ticks)}</g></svg>')


def jsonld(t, code, page):
    """Only facts the owner has given: name, phone, email, areas, languages."""
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Shady Magora 365",
        "description": t["meta"]["description"],
        "url": url_for(code, "home"),
        "image": f"{BASE}/assets/og.png",
        "telephone": "+201026315970",
        "email": "shadymagorat@gmail.com",
        "founder": {"@type": "Person", "name": "Shady Magora"},
        "areaServed": [
            {"@type": "City", "name": "Cairo"},
            {"@type": "Place", "name": "Ain Sokhna"},
        ],
        "knowsLanguage": ["ar", "en", "fr"],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+201026315970",
            "contactType": "customer service",
            "availableLanguage": ["Arabic", "English", "French"],
        },
    }
    return json.dumps(data, ensure_ascii=False)


def stay_photos(stays):
    """For each photo (WebP), offer an AVIF twin when one sits next to it."""
    for s in stays:
        s["photo_avif"] = None
        if s.get("photo"):
            avif = Path(s["photo"]).with_suffix(".avif").name
            if (ROOT / "assets/stays" / avif).exists():
                s["photo_avif"] = avif
    return stays


def main():
    env = Environment(loader=FileSystemLoader(ROOT / "src"), undefined=StrictUndefined, autoescape=True)
    env.filters["tbc"] = tbc
    stays = stay_photos(json.loads((ROOT / "data/stays.json").read_text(encoding="utf-8")))
    rib = Markup(ribbon())

    for code in LANGS:
        t = json.loads((ROOT / f"i18n/{code}.json").read_text(encoding="utf-8"))
        for page, (tpl_name, path) in PAGES.items():
            root = rel_root(code, page)
            meta = t["meta"] if page == "home" else t["owner_page"]["meta"]
            html = env.get_template(tpl_name).render(
                t=t, meta=meta, page=page, page_path=path, langs=LANGS, base=BASE, root=root,
                home=f"{root}{lang_dir(code)}",
                urls={c: url_for(c, page) for c in LANGS},
                links={c: f"{root}{lang_dir(c)}{path}" for c in LANGS},
                og_locale=OG_LOCALE[code], fonts_url=FONTS[code],
                jsonld=Markup(jsonld(t, code, page).replace("</", "<\\/")), ribbon=rib, stays=stays,
                wa={k: wa(v) for k, v in t["wa"].items()},
            )
            out = out_path(code, page)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print("wrote", out.relative_to(ROOT))

    entries = ""
    for page in PAGES:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{url_for(c, page)}"/>' for c in LANGS)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url_for("en", page)}"/>'
        entries += "".join(f"\n<url><loc>{url_for(c, page)}</loc>{alts}</url>" for c in LANGS)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{entries}\n</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()

# Shady Magora 365

Marketing site for Shady Magora's Airbnb management business in Cairo and Ain Sokhna. English, French and Arabic.

- Wording: `i18n/*.json`
- Listings shown on the site: `data/stays.json`
- Guest reviews (real only): `data/reviews.json`
- Layout: `src/base.html` (header, contact, footer), `src/home.html`, `src/owners.html`; styles in `assets/style.css`

`python build.py` regenerates the home and owner pages in each language (`index.html`, `owners/index.html`, `fr/...`, `ar/...`), `sitemap.xml` and `robots.txt` (needs `pip install jinja2`). Every push to `main` rebuilds and deploys to GitHub Pages.

The full brief and its hard rules are in `CLAUDE.md`. What's still missing is in `TODO.md`.

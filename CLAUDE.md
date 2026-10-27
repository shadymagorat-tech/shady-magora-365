# Shady Magora 365 — Website

## What this is
A fast, mobile-first marketing site for **Shady Magora 365**, the Airbnb management business of Shady Magora (Cairo). Two audiences:

1. **Property owners** in Cairo and Ain Sokhna who want their apartment or villa run on Airbnb.
2. **Guests** who want a day tour or a private airport pickup.

The site's only job is to turn visitors into WhatsApp conversations.

## Hard rules (do not break)
- **Never promise on-site operations.** No cleaning, no check-in/handover, no maintenance, no key handling. Shady manages the listing, not the building.
- **No invented content.** No fake reviews, testimonials, stats, guest counts, revenue numbers, or partner logos. Real reviews only, pasted by Shady, each with a link to its source.
- **No em dashes (—) in any visible copy.** Use commas, periods, or colons.
- **No fee or commission shown.** Pricing is discussed on WhatsApp.
- **Only Shady's own photos.** No stock photos of people. If a photo is missing, use a clean placeholder block and list it in `TODO.md`.
- **Do not name the airport driver.** The service is "private airport pickup in an electric car (Tesla)".
- Shady is a **tour leader**, not a licensed guide. Never write "guide".
- Surname spelling is **Magora** (never "Magoura") everywhere on the site.

## Languages
English (default), French, Arabic (full RTL layout, not just mirrored text). Language switcher in the header, choice remembered per visitor. All copy lives in `/i18n/en.json`, `fr.json`, `ar.json`; no hard-coded strings in HTML.

## Tone
Friendly, casual, a bit witty. Confident without hype. Short sentences. No corporate filler ("unlock", "seamless", "elevate", "delve", "in today's fast-paced world").

## Pages / sections
Single page with anchored sections, plus a separate page per language.

1. **Hero** — Name, one-line promise for owners, two buttons: "I'm an owner" and "I'm a guest". Airbnb Superhost badge (text only, no Airbnb logo).
2. **For owners — what I do**
   - Listing creation and full optimisation (title, description, photo order, amenities, in EN/FR/AR)
   - Pricing and calendar management
   - Guest communication, fast replies, day and night
   - Reviews, disputes, AirCover claims (draws on 4 years inside Airbnb)
   - Monthly payout settlement with the owner
3. **Why me** — Former Airbnb employee 2019–2023 (France Specialist and Trainer, Ambassador, AirCover Specialist). Current Airbnb Superhost. Speaks Arabic, English, French. Background in hotels and airlines.
4. **Areas** — Cairo (Zamalek, Sheikh Zayed and more) and Ain Sokhna (Palm Beach).
5. **Featured stays** — Cards for the 5 current listings, each linking to its Airbnb page. URLs and photos supplied by Shady; until then, placeholders listed in `TODO.md`.
6. **For guests**
   - Day tours with Shady as tour leader
   - Private airport pickup in a Tesla
   Each with its own WhatsApp button and a prefilled message.
7. **Reviews** — Empty component that renders real reviews from `/data/reviews.json` (fields: text, author first name, date, source URL). Hidden if the file is empty.
8. **FAQ** — Include: "Who handles cleaning and check-in?" → the owner's own team; Shady handles the listing, pricing, guests and payouts. Plus 4–5 more owner questions.
9. **Contact / footer** — WhatsApp +20 102 631 5970, email shadymagorat@gmail.com.

## WhatsApp buttons
Use `https://wa.me/201026315970?text=...` with a different URL-encoded prefilled message per button and per language (owner enquiry, tour enquiry, airport pickup enquiry).

## Tech
- Plain static HTML + CSS + small vanilla JS. No framework, no build step required.
- Mobile-first, fast: Lighthouse 90+ on Performance, Accessibility, SEO, Best Practices.
- Images in WebP, lazy-loaded, with width/height set.
- SEO: per-language `<title>`, meta description, `hreflang` tags, Open Graph + Twitter cards, `schema.org/LocalBusiness` JSON-LD.
- `sitemap.xml` and `robots.txt`.
- No cookies, no trackers in v1.
- Deploy with GitHub Pages via a GitHub Actions workflow. (GitHub Pages needs a public repo on the free plan; the site has no secrets, so public is fine.)

## Design direction
Warm, calm, premium but not stiff. Think Nile at golden hour and Sokhna sea: sand, deep teal, off-white. One display font + one body font from Google Fonts, plus an Arabic font that pairs well (e.g. IBM Plex Sans Arabic or Cairo). Generous spacing, big tap targets, sticky WhatsApp button on mobile.

## Definition of done
- All sections built in EN, FR, AR, with correct RTL for Arabic.
- Every WhatsApp button opens the right prefilled message.
- Deployed and live on GitHub Pages.
- Lighthouse 90+ on mobile.
- `TODO.md` lists every missing asset (photos, listing URLs, reviews, domain).
- No em dashes, no "guide", no "Magoura", no cleaning/check-in promises anywhere (grep to verify).

# TODO for Shady

## To go live (once)
- [ ] Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**. The next push publishes the site at https://shadymagorat-tech.github.io/shady-magora-365/

## Photos for the 5 stays
Right now each card shows a coloured block with the area name. To add a real photo:
1. Export your best photo of the listing as WebP, about 1200 × 900 px, under 200 KB.
2. Put it in `assets/stays/`, e.g. `assets/stays/zamalek-gallery.webp`.
3. In `data/stays.json`, set that listing's `"photo"` to the file name (`"zamalek-gallery.webp"`).

- [ ] zamalek-gallery
- [ ] zamalek-1br
- [ ] ganet-zayed-2br
- [ ] palm-beach-4br
- [ ] khorshid-villa

## Check the listing names and links
Names and Airbnb links in `data/stays.json` come from the pricing repo config.
- [ ] Khorshid villa: confirm the title "3BR Oasis Villa with Lagoon Pool Access" matches Airbnb.
- [ ] Open each "See it on Airbnb" link once and check it lands on the right listing.

## Reviews
Real reviews only. Add them to `data/reviews.json`, one per guest, each with a link to where it appears:
```json
[
  {"text": "The review text, exactly as the guest wrote it.", "author": "First name", "date": "Oct 2026", "source": "https://www.airbnb.com/rooms/1747283504789570481"}
]
```
The section stays hidden while the file is `[]`.

## Domain (optional)
- [ ] When you buy a domain, change `BASE` in `build.py`, run `python build.py`, and add the domain under Settings → Pages.

## Editing text
All wording lives in `i18n/en.json`, `i18n/fr.json`, `i18n/ar.json`. Edit there, never in the HTML; the deploy rebuilds the pages from these files.

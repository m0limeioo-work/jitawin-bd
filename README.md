# JitaWin BD — Affiliate Promotion Site

Bangladesh market **affiliate content site** for JitaWin (not the official platform).  
Stack: **HTML + CSS + Bootstrap 5** (CDN). No build step.

## Conversion links (fixed)

| Type | URL |
|------|-----|
| Home / general CTA | `https://www.jitaace.work/?pid=jitaaff` |
| Register CTA | `https://www.jitaace.work/signup?pid=jitaaff` |

## Source of truth

- Platform facts: `prompt/jitawin-info.md`
- Build brief: `prompt/jitawin-bulid prompt.md`
- UI design: `prompt/ui-design.md`

## Local preview

```bash
# from repo root
python3 -m http.server 8080
# open http://localhost:8080
```

Or open `index.html` directly in a browser.

## Structure

```
index.html                 # Homepage
about-jitawin/             # Brand, license, sister brands
guide/                     # Register, KYC, PWA
payment/                   # bKash/Nagad/Rocket/crypto + withdrawal FAQ
promotions/                # Welcome, cashback, wagering, VIP
games/                     # Slots, live, sports, fish, bingo
affiliate/                 # Commission + how to start
faq/  mirror-links/  responsible-gambling/  disclaimer/
assets/                    # css, images
scripts/build_pages.py     # Regenerates inner pages (optional)
prompt/                    # Specs & data (internal, not public)
```

## Tech

- Bootstrap 5.3 (CSS + JS bundle via jsDelivr CDN)
- Custom CSS only for brand colors, hero image, dark cards
- No custom site JS (Bootstrap handles navbar / accordion)
- Google Fonts: Inter + Noto Sans Bengali

## Content rules (summary)

- Body copy: Bengali (Bangladesh locale)
- Meta title/description/alt: English
- Currency: ৳
- App install: **PWA only** (not APK) — domain `w01.jitawin.com`
- Do not invent numbers outside `jitawin-info.md`

#!/usr/bin/env python3
"""
Inject page-appropriate JSON-LD schema into every HTML page.
Also sets <link rel="canonical"> and key Open Graph absolute URLs.

Honest positioning: this is a third-party affiliate content site,
NOT the official JitaWin operator (Altervance Ltd.).

Site base is read from site.config.json (default for this project),
overridable with env:
  SITE_BASE=https://example.com/path python3 scripts/inject_schema.py
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _load_site_base() -> str:
    env = os.environ.get("SITE_BASE", "").strip()
    if env:
        return env.rstrip("/")
    cfg_path = ROOT / "site.config.json"
    if cfg_path.exists():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            return str(data.get("siteBase", "")).rstrip("/")
        except Exception:
            pass
    return "https://m0limeioo-work.github.io/jitawin-bd"

SITE_BASE = _load_site_base()


def u(path: str) -> str:
    """Absolute site URL (includes GitHub Pages project path when SITE_BASE is set)."""
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and path.endswith("/index.html"):
        path = path[: -len("index.html")]
    if SITE_BASE:
        if path == "/":
            return SITE_BASE + "/"
        return SITE_BASE + path
    return path


def publisher_org() -> dict:
    return {
        "@type": "Organization",
        "name": "JitaWin BD Affiliate Guide",
        "description": (
            "Independent third-party affiliate content and review site about JitaWin "
            "for Bangladeshi players. Not the official operator or customer support."
        ),
        "url": u("/"),
        "logo": u("/assets/images/favicon.png"),
    }


# Subject brand (mentioned, not claimed as self)
BRAND_SUBJECT = {
    "@type": "Organization",
    "name": "JitaWin",
    "alternateName": "JW",
    "description": (
        "Online gaming brand operated by Altervance Ltd. "
        "(license ALSI-142311014, Anjouan, Union of Comoros)."
    ),
}


def script_tag(data: dict | list) -> str:
    body = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{body}\n  </script>\n'


def webpage(
    path: str,
    name: str,
    description: str,
    page_type: str = "WebPage",
    extras: dict | None = None,
) -> dict:
    data = {
        "@context": "https://schema.org",
        "@type": page_type,
        "@id": u(path) + "#webpage",
        "url": u(path),
        "name": name,
        "description": description,
        "inLanguage": "bn-BD",
        "isPartOf": {"@id": u("/") + "#website"},
        "about": BRAND_SUBJECT,
        "publisher": publisher_org(),
        "isAccessibleForFree": True,
    }
    if extras:
        data.update(extras)
    return data


def breadcrumb(items: list[tuple[str, str]]) -> dict:
    """items: (path, name) in order, path is site path."""
    elements = []
    for i, (path, name) in enumerate(items, start=1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": u(path),
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }


def article(path: str, name: str, description: str, crumbs: list[tuple[str, str]]) -> list:
    return [
        webpage(path, name, description, "Article", {"headline": name}),
        breadcrumb(crumbs),
    ]


def howto(
    path: str,
    name: str,
    description: str,
    steps: list[str],
    crumbs: list[tuple[str, str]],
) -> list:
    how = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "inLanguage": "en",
        "totalTime": "PT10M",
        "supply": [],
        "tool": [{"@type": "HowToTool", "name": "Smartphone or computer with browser"}],
        "step": [
            {
                "@type": "HowToStep",
                "position": i,
                "name": f"Step {i}",
                "text": text,
            }
            for i, text in enumerate(steps, start=1)
        ],
        "about": BRAND_SUBJECT,
    }
    return [
        webpage(path, name, description),
        how,
        breadcrumb(crumbs),
    ]


def faq_page(path: str, name: str, description: str, qas: list[tuple[str, str]], crumbs: list[tuple[str, str]] | None = None) -> list:
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": u(path) + "#faq",
        "url": u(path),
        "name": name,
        "description": description,
        "inLanguage": "bn-BD",
        "isPartOf": {"@id": u("/") + "#website"},
        "about": BRAND_SUBJECT,
        "publisher": publisher_org(),
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qas
        ],
    }
    out = [faq]
    if crumbs:
        out.append(breadcrumb(crumbs))
    return out


def collection(path: str, name: str, description: str, parts: list[tuple[str, str]], crumbs: list[tuple[str, str]]) -> list:
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "name": n,
                "url": u(p),
            }
            for i, (p, n) in enumerate(parts, start=1)
        ],
    }
    return [
        webpage(path, name, description, "CollectionPage"),
        item_list,
        breadcrumb(crumbs),
    ]


HOME_FAQ = [
    (
        "Is JitaWin safe and licensed?",
        "JitaWin is operated by Altervance Ltd. (company no. 000031825, Belize) under Anjouan, Union of Comoros gaming license ALSI-142311014. A license means the operator is registered with a regulator; always verify the current license status yourself and only deposit what you can afford to lose.",
    ),
    (
        "What is the minimum deposit on JitaWin with bKash or Nagad?",
        "Minimum deposit is generally ৳100. bKash limit is ৳100–25,000, Nagad ৳100–50,000, Rocket ৳100–30,000, with max +1% fee. USDT/USDC is also available.",
    ),
    (
        "Why was my JitaWin withdrawal rejected?",
        "Common reasons: incomplete KYC (name and mobile verification), bonus wagering not completed, or withdrawal account not matching deposit details. Complete verification before withdrawing and check active wagering requirements.",
    ),
    (
        "Is JitaWin App an APK download?",
        "No. JitaWin mobile is a PWA (Progressive Web App). Install from w01.jitawin.com via browser Add to Home Screen / Install app prompt — not a Play Store or APK install.",
    ),
    (
        "How does the JitaWin referral commission work?",
        "Three tiers on daily valid turnover: Direct 0.10%, Level 2 0.05%, Level 3 0.025%. Plus ৳88 per successful referral (VIP3+ referrer, with conditions) and monthly invite milestone bonuses.",
    ),
]


def schemas_for(rel: str) -> list[dict]:
    """Return list of JSON-LD objects for a page relative path."""
    # normalize
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        website = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": u("/") + "#website",
            "name": "JitaWin Bangladesh Affiliate Guide",
            "alternateName": "JitaWin BD Guide",
            "url": u("/"),
            "description": (
                "Independent affiliate content site about JitaWin for Bangladeshi players — "
                "deposit guides, bonuses, VIP, PWA install, and responsible gambling info."
            ),
            "inLanguage": ["bn-BD", "en"],
            "publisher": {"@id": u("/") + "#organization"},
            "about": BRAND_SUBJECT,
            "potentialAction": {
                "@type": "ReadAction",
                "target": u("/"),
            },
        }
        org = {
            "@context": "https://schema.org",
            "@id": u("/") + "#organization",
            **publisher_org(),
        }
        wp = webpage(
            "/",
            "JitaWin Bangladesh 2026 — Cricket Bet, bKash Deposit & Bonus Guide",
            "JitaWin Bangladesh review: bKash/Nagad deposit from ৳100, welcome bonus, VIP cashback, cricket sports betting and PWA app.",
        )
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": u("/") + "#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in HOME_FAQ
            ],
        }
        return [website, org, wp, faq]

    crumbs_home = [("/", "Home")]

    # About
    if rel == "about-jitawin/index.html":
        return collection(
            "/about-jitawin/",
            "What is JitaWin Bangladesh? Brand & Platform Guide",
            "Learn what JitaWin is for Bangladeshi players: operator, license, games, payments and sister brands.",
            [
                ("/about-jitawin/license-safety.html", "License & Safety"),
                ("/about-jitawin/sister-brands.html", "Sister Brands"),
                ("/guide/", "Beginner Guide"),
                ("/disclaimer/", "Disclaimer"),
            ],
            crumbs_home + [("/about-jitawin/", "About JitaWin")],
        ) + [
            webpage(
                "/about-jitawin/",
                "What is JitaWin Bangladesh?",
                "Independent overview of the JitaWin brand for Bangladesh players.",
                "AboutPage",
            )
        ]

    if rel == "about-jitawin/license-safety.html":
        return article(
            "/about-jitawin/license-safety.html",
            "JitaWin License & Safety — ALSI-142311014 Explained",
            "JitaWin operator Altervance Ltd., Anjouan license ALSI-142311014, and what a gaming license means for players.",
            crumbs_home
            + [
                ("/about-jitawin/", "About JitaWin"),
                ("/about-jitawin/license-safety.html", "License & Safety"),
            ],
        )

    if rel == "about-jitawin/sister-brands.html":
        return article(
            "/about-jitawin/sister-brands.html",
            "JitaWin Sister Brands — JITA PROGRAM & JitaOne Group",
            "Related brands around JitaWin: JITA SPORTS, Owin, JitaOne, HeyJita, JitaBet, JitaGo, Laki55.",
            crumbs_home
            + [
                ("/about-jitawin/", "About JitaWin"),
                ("/about-jitawin/sister-brands.html", "Sister Brands"),
            ],
        )

    # Guide hub
    if rel == "guide/index.html":
        return collection(
            "/guide/",
            "JitaWin Beginner Guide Bangladesh",
            "Step-by-step JitaWin beginner guide: register, KYC, deposit, withdraw and PWA install.",
            [
                ("/guide/register.html", "Register"),
                ("/guide/verification.html", "KYC Verification"),
                ("/guide/app-download.html", "App PWA Install"),
                ("/payment/", "Deposit & Withdraw"),
            ],
            crumbs_home + [("/guide/", "Guide")],
        )

    if rel == "guide/register.html":
        return howto(
            "/guide/register.html",
            "How to Register on JitaWin Bangladesh",
            "Create a JitaWin account with username, mobile OTP or Google continue, and accept Terms.",
            [
                "Open the affiliate signup link.",
                "Fill username, password, mobile number or continue with Google.",
                "Enter the mobile OTP verification code.",
                "Accept JitaWin Terms & Conditions and submit.",
                "Log in and complete name verification in profile.",
            ],
            crumbs_home + [("/guide/", "Guide"), ("/guide/register.html", "Register")],
        )

    if rel == "guide/verification.html":
        return howto(
            "/guide/verification.html",
            "How to Complete JitaWin KYC Verification",
            "Verify first name, last name and mobile for VIP2 and withdrawals on JitaWin.",
            [
                "Log in to your JitaWin account.",
                "Open profile or verification settings.",
                "Enter first name and last name matching payment account.",
                "Complete mobile verification.",
                "Retry withdrawal after verification is approved.",
            ],
            crumbs_home + [("/guide/", "Guide"), ("/guide/verification.html", "Verification")],
        )

    if rel == "guide/app-download.html":
        return howto(
            "/guide/app-download.html",
            "How to Install JitaWin App as PWA (Not APK)",
            "Install JitaWin mobile Progressive Web App from w01.jitawin.com using browser Install prompt.",
            [
                "Open the official entry or mirror site in Chrome or Safari.",
                "Go to the download/install page (reference domain w01.jitawin.com).",
                "Tap the Download App or Install button.",
                "Confirm the browser Install this app prompt.",
                "Open the home-screen icon like a native app; enable notifications if desired.",
            ],
            crumbs_home + [("/guide/", "Guide"), ("/guide/app-download.html", "App PWA")],
        )

    # Payment
    if rel == "payment/index.html":
        return collection(
            "/payment/",
            "JitaWin Deposit & Withdrawal Bangladesh",
            "bKash, Nagad, Rocket, USDT limits and fees plus withdrawal FAQ for JitaWin.",
            [
                ("/payment/bkash.html", "bKash"),
                ("/payment/nagad.html", "Nagad"),
                ("/payment/rocket.html", "Rocket"),
                ("/payment/crypto.html", "USDT/USDC"),
                ("/payment/withdrawal-faq.html", "Withdrawal FAQ"),
            ],
            crumbs_home + [("/payment/", "Payment")],
        ) + [
            {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": "How to Deposit on JitaWin",
                "description": "General deposit flow: open Deposit, choose method, submit amount, wait for wallet credit.",
                "step": [
                    {"@type": "HowToStep", "position": 1, "text": "Log in and open Deposit from the menu."},
                    {"@type": "HowToStep", "position": 2, "text": "Choose bKash, Nagad, Rocket or another supported method."},
                    {"@type": "HowToStep", "position": 3, "text": "Enter amount and required details; select a bonus if eligible; submit."},
                    {"@type": "HowToStep", "position": 4, "text": "Wait for the success message and check wallet balance."},
                ],
            }
        ]

    pay_methods = {
        "payment/bkash.html": (
            "bKash",
            "৳100–25,000",
            "Max +1%",
            "How to Deposit on JitaWin with bKash",
        ),
        "payment/nagad.html": (
            "Nagad",
            "৳100–50,000",
            "Max +1%",
            "How to Deposit on JitaWin with Nagad",
        ),
        "payment/rocket.html": (
            "Rocket",
            "৳100–30,000",
            "Max +1%",
            "How to Deposit on JitaWin with Rocket",
        ),
    }
    if rel in pay_methods:
        name, limit, fee, title = pay_methods[rel]
        path = "/" + rel
        return howto(
            path,
            title,
            f"Deposit and withdraw guide for {name} on JitaWin. Limit {limit}, fee {fee}.",
            [
                "Log in and open Deposit / Wallet.",
                f"Select {name} as payment method.",
                f"Enter an amount within {limit}.",
                "Select an active bonus if you want one.",
                f"Complete payment via {name} as shown on the platform.",
                "Keep the transaction ID or screenshot.",
            ],
            crumbs_home + [("/payment/", "Payment"), (path, name)],
        )

    if rel == "payment/crypto.html":
        return howto(
            "/payment/crypto.html",
            "How to Deposit USDT/USDC on JitaWin",
            "Deposit with USDT/USDC on BEP-20, TRC-20 or ERC-20. Limit ৳100–25,000 equivalent; use live platform rate.",
            [
                "Log in and open Deposit.",
                "Select USDT or USDC and the correct network (BEP-20, TRC-20 or ERC-20).",
                "Copy the deposit address carefully and send a small test first if unsure.",
                "Confirm the live conversion rate shown on the platform.",
                "Wait for network confirmation and wallet credit.",
            ],
            crumbs_home + [("/payment/", "Payment"), ("/payment/crypto.html", "Crypto")],
        )

    if rel == "payment/withdrawal-faq.html":
        return faq_page(
            "/payment/withdrawal-faq.html",
            "JitaWin Withdrawal Problems — Why Rejected",
            "Common JitaWin withdrawal rejects: KYC, wagering, account mismatch, and checklist to fix.",
            [
                (
                    "Why was my JitaWin withdrawal rejected?",
                    "Common reasons include incomplete KYC (name and mobile), unfinished bonus wagering, or deposit/withdraw account mismatch.",
                ),
                (
                    "What is the JitaWin single withdrawal limit?",
                    "Single withdrawal is commonly around ৳100–25,000 and may vary by activity or level.",
                ),
                (
                    "What should I check before withdrawing?",
                    "Complete name and mobile verification, clear bonus wagering, match payment account details, and have your login password ready.",
                ),
            ],
            crumbs_home + [("/payment/", "Payment"), ("/payment/withdrawal-faq.html", "Withdrawal FAQ")],
        )

    # Promotions
    if rel == "promotions/index.html":
        return collection(
            "/promotions/",
            "JitaWin Promotions Bangladesh — Bonus & VIP",
            "Welcome bonus, daily/weekly cashback, wagering rules and VIP overview.",
            [
                ("/promotions/welcome-bonus.html", "Welcome Bonus"),
                ("/promotions/cashback.html", "Cashback"),
                ("/promotions/wagering-explained.html", "Wagering Explained"),
                ("/promotions/vip.html", "VIP Levels"),
            ],
            crumbs_home + [("/promotions/", "Promotions")],
        )

    if rel == "promotions/welcome-bonus.html":
        return article(
            "/promotions/welcome-bonus.html",
            "JitaWin Welcome Bonus Bangladesh — First Deposit Offers",
            "New member first deposit bonuses for slots, fish, sports and crash with wagering requirements.",
            crumbs_home
            + [("/promotions/", "Promotions"), ("/promotions/welcome-bonus.html", "Welcome Bonus")],
        )

    if rel == "promotions/cashback.html":
        return article(
            "/promotions/cashback.html",
            "JitaWin Cashback & Rebate — Daily 10% Weekly 6%",
            "Daily slot cashback 2–10%, weekly 6% rebate, and 6% diamond top-up for VIP2+.",
            crumbs_home + [("/promotions/", "Promotions"), ("/promotions/cashback.html", "Cashback")],
        )

    if rel == "promotions/wagering-explained.html":
        return article(
            "/promotions/wagering-explained.html",
            "JitaWin Wagering / Turnover Explained with Examples",
            "What wagering means on JitaWin with worked examples for 20x and 30x bonus turnover.",
            crumbs_home
            + [("/promotions/", "Promotions"), ("/promotions/wagering-explained.html", "Wagering")],
        )

    if rel == "promotions/vip.html":
        return article(
            "/promotions/vip.html",
            "JitaWin VIP Levels 1–30 — Upgrade Weekly Monthly Bonus",
            "VIP club overview: 30 levels, VIP2 verification, monthly and weekly unlocks, key tier table.",
            crumbs_home + [("/promotions/", "Promotions"), ("/promotions/vip.html", "VIP")],
        )

    # Games
    if rel == "games/index.html":
        return collection(
            "/games/",
            "JitaWin Games Bangladesh — Slots Live Sports Fishing Bingo",
            "Game categories and providers: slots, live casino, cricket sports, fishing, bingo.",
            [
                ("/games/slots.html", "Slots"),
                ("/games/live-casino.html", "Live Casino"),
                ("/games/sports.html", "Sports"),
                ("/games/fishing.html", "Fishing"),
                ("/games/bingo.html", "Bingo"),
            ],
            crumbs_home + [("/games/", "Games")],
        )

    game_pages = {
        "games/slots.html": (
            "JitaWin Slots — Providers Guide",
            "Slot providers including JILI, PG, JDB, PP and more on JitaWin.",
            "Slots",
        ),
        "games/live-casino.html": (
            "JitaWin Live Casino Guide",
            "Live casino themes and providers such as EVO, SEXY and SA.",
            "Live Casino",
        ),
        "games/sports.html": (
            "JitaWin Cricket & Sports Betting Bangladesh",
            "Sportsbook providers and cricket-focused betting context for Bangladesh.",
            "Sports",
        ),
        "games/fishing.html": (
            "JitaWin Fishing Games Guide",
            "Fishing game providers and promo category notes.",
            "Fishing",
        ),
        "games/bingo.html": (
            "JitaWin Bingo Games Guide",
            "Bingo providers and related other game categories.",
            "Bingo",
        ),
    }
    if rel in game_pages:
        title, desc, short = game_pages[rel]
        path = "/" + rel
        return article(
            path,
            title,
            desc,
            crumbs_home + [("/games/", "Games"), (path, short)],
        )

    # Affiliate
    if rel == "affiliate/index.html":
        return collection(
            "/affiliate/",
            "JitaWin Affiliate & Referral Bangladesh",
            "Refer friends: ৳88 referral, daily commission tiers, milestones, how to start.",
            [
                ("/affiliate/commission.html", "Commission Structure"),
                ("/affiliate/how-to-start.html", "How to Start"),
            ],
            crumbs_home + [("/affiliate/", "Affiliate")],
        )

    if rel == "affiliate/commission.html":
        return article(
            "/affiliate/commission.html",
            "JitaWin Referral Commission Structure",
            "Daily commission 0.10%/0.05%/0.025%, ৳88 referral bonus rules, and monthly invite milestones.",
            crumbs_home
            + [("/affiliate/", "Affiliate"), ("/affiliate/commission.html", "Commission")],
        )

    if rel == "affiliate/how-to-start.html":
        return howto(
            "/affiliate/how-to-start.html",
            "How to Start JitaWin Referral Promotion",
            "Register, reach eligibility, get referral code/QR/link, share, and claim bonuses within 30 days.",
            [
                "Register via the affiliate signup link.",
                "Complete KYC and activity toward VIP3 if you want the ৳88 referral bonus.",
                "Copy your referral code, QR and link from the backend.",
                "Share with friends; avoid same device/IP duplicate referrals.",
                "Claim rewards in Notifications/Bonus within 30 days.",
            ],
            crumbs_home + [("/affiliate/", "Affiliate"), ("/affiliate/how-to-start.html", "How to Start")],
        )

    # FAQ
    if rel == "faq/index.html":
        return faq_page(
            "/faq/",
            "JitaWin FAQ Bangladesh — Deposit Withdraw App License",
            "Frequently asked questions about JitaWin safety, bKash limits, withdrawals, PWA app and referral.",
            HOME_FAQ
            + [
                (
                    "What if the JitaWin site does not open?",
                    "Try listed mirror domains and the tracked affiliate entry link. Availability can change; follow local laws.",
                ),
            ],
            crumbs_home + [("/faq/", "FAQ")],
        )

    # Mirror
    if rel == "mirror-links/index.html":
        return article(
            "/mirror-links/",
            "JitaWin Mirror Links & Working URL Bangladesh",
            "Alternate JitaWin domains and access notes when the main site is hard to open.",
            crumbs_home + [("/mirror-links/", "Mirror Links")],
        )

    # RG
    if rel == "responsible-gambling/index.html":
        return [
            webpage(
                "/responsible-gambling/",
                "Responsible Gambling — JitaWin Bangladesh Guide 18+",
                "Responsible gambling statement: 18+ only, play with disposable budget, stop if it becomes a problem.",
                "WebPage",
                {
                    "audience": {
                        "@type": "PeopleAudience",
                        "requiredMinAge": 18,
                    }
                },
            ),
            breadcrumb(crumbs_home + [("/responsible-gambling/", "Responsible Gambling")]),
        ]

    # Disclaimer
    if rel == "disclaimer/index.html":
        return [
            webpage(
                "/disclaimer/",
                "Disclaimer — Independent JitaWin Affiliate Content Site",
                "This website is a third-party affiliate content site about JitaWin, not the official operator or support.",
                "WebPage",
            ),
            breadcrumb(crumbs_home + [("/disclaimer/", "Disclaimer")]),
        ]

    # Fallback generic WebPage
    return [
        webpage(
            "/" + rel.replace("index.html", ""),
            rel,
            "JitaWin Bangladesh affiliate guide page.",
        )
    ]


def strip_existing_ldjson(html: str) -> str:
    return re.sub(
        r"\s*<script type=\"application/ld\+json\">.*?</script>\s*",
        "\n",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )


def page_canonical_url(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return u("/")
    if rel.endswith("/index.html"):
        return u("/" + rel[: -len("index.html")])
    return u("/" + rel)


def set_canonical_and_og(html: str, rel: str) -> str:
    """Ensure absolute canonical (+ homepage OG url/image) for GitHub Pages."""
    canon = page_canonical_url(rel)
    link = f'<link rel="canonical" href="{canon}" />'
    if re.search(r'rel=["\']canonical["\']', html, re.I):
        html = re.sub(
            r'<link\s+rel=["\']canonical["\'][^>]*>',
            link,
            html,
            count=1,
            flags=re.I,
        )
    else:
        # insert before stylesheet or before </head>
        if re.search(r'<meta name="theme-color"', html):
            html = re.sub(
                r'(<meta name="theme-color"[^>]*>\s*)',
                r"\1" + link + "\n  ",
                html,
                count=1,
            )
        else:
            html = html.replace("</head>", f"  {link}\n</head>", 1)

    if rel == "index.html":
        og_url = f'<meta property="og:url" content="{canon}" />'
        og_img = f'<meta property="og:image" content="{u("/assets/images/hero-cricket.webp")}" />'
        if re.search(r'property=["\']og:url["\']', html):
            html = re.sub(
                r'<meta\s+property=["\']og:url["\'][^>]*>',
                og_url,
                html,
                count=1,
            )
        else:
            html = re.sub(
                r'(<meta property="og:locale"[^>]*>\s*)',
                r"\1" + og_url + "\n  ",
                html,
                count=1,
            )
        if re.search(r'property=["\']og:image["\']', html):
            html = re.sub(
                r'<meta\s+property=["\']og:image["\'][^>]*>',
                og_img,
                html,
                count=1,
            )
        else:
            html = re.sub(
                r'(<meta property="og:url"[^>]*>\s*)',
                r"\1" + og_img + "\n  ",
                html,
                count=1,
            )
    return html


def inject(html: str, blocks: list[dict], rel: str) -> str:
    html = strip_existing_ldjson(html)
    html = set_canonical_and_og(html, rel)
    payload = "\n".join(script_tag(b) for b in blocks)
    if "</head>" not in html:
        raise ValueError("no </head>")
    return html.replace("</head>", payload + "</head>", 1)


def main() -> None:
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "prompt" in path.parts:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        blocks = schemas_for(rel)
        text = path.read_text(encoding="utf-8")
        new = inject(text, blocks, rel)
        path.write_text(new, encoding="utf-8")
        count += 1
        types = []
        for b in blocks:
            t = b.get("@type", "?")
            if isinstance(t, list):
                t = "+".join(t)
            types.append(str(t))
        print(f"OK {rel} -> {', '.join(types)}")
    print(f"\nDone: {count} pages. SITE_BASE={SITE_BASE or '(root-relative)'}")


if __name__ == "__main__":
    main()

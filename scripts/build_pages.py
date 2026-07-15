#!/usr/bin/env python3
"""Generate static inner pages for JitaWin BD affiliate site."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CTA_HOME = "https://www.jitaace.work/?pid=jitaaff"
CTA_SIGNUP = "../go/"  # register CTAs hop via /go/ then to jitaace signup
CTA_SIGNUP_FINAL = "https://www.jitaace.work/signup?pid=jitaaff"

NAV = [
    ("games/", "গেমস"),
    ("promotions/", "প্রমোশন"),
    ("payment/", "পেমেন্ট"),
    ("guide/", "গাইড"),
    ("affiliate/", "রেফারেল"),
    ("faq/", "FAQ"),
]


def asset_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def nav_html(prefix: str, active: str = "") -> str:
    items = []
    for href, label in NAV:
        cls = "nav-link active" if active and (active == href or active.startswith(href.rstrip("/"))) else "nav-link"
        items.append(f'<li class="nav-item"><a class="{cls}" href="{prefix}{href}">{label}</a></li>')
    return "\n          ".join(items)


def page(
    rel_path: str,
    title: str,
    description: str,
    h1: str,
    lead: str,
    body: str,
    breadcrumbs: list[tuple[str, str]],
    active_nav: str = "",
):
    depth = rel_path.count("/")
    # file at section/index.html -> depth 1; section/sub.html -> depth 1
    if rel_path.endswith("index.html"):
        depth = rel_path.count("/")  # about-jitawin/index.html -> 1
    else:
        depth = rel_path.count("/")  # payment/bkash.html -> 1
    p = asset_prefix(depth)

    crumbs = []
    for i, (href, label) in enumerate(breadcrumbs):
        if i == len(breadcrumbs) - 1:
            crumbs.append(f'<li class="breadcrumb-item active" aria-current="page">{label}</li>')
        else:
            crumbs.append(f'<li class="breadcrumb-item"><a href="{href}">{label}</a></li>')
    crumb_html = "\n            ".join(crumbs)

    html = f"""<!DOCTYPE html>
<html lang="bn" hreflang="bn-BD">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow" />
  <meta name="theme-color" content="#0f172a" />
  <link rel="icon" href="{p}assets/images/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="icon" href="{p}assets/images/favicon.png" type="image/png" sizes="any" />
  <link rel="apple-touch-icon" href="{p}assets/images/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Noto+Sans+Bengali:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet" />
  <link rel="stylesheet" href="{p}assets/css/style.css" />
</head>
<body class="bg-jw">
  <nav class="navbar navbar-expand-lg navbar-dark navbar-jw fixed-top">
    <div class="container">
      <a class="logo" href="{p}" aria-label="JitaWin BD Home">
        <span class="logo-mark">JW</span>
        <span class="logo-text">Jita<span>Win</span></span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="mainNav">
        <ul class="navbar-nav mx-lg-auto mb-2 mb-lg-0 gap-lg-1">
          {nav_html(p, active_nav)}
        </ul>
        <div class="d-flex flex-column flex-lg-row gap-2">
          <a class="btn btn-outline-gold btn-sm" href="{CTA_HOME}" rel="nofollow sponsored noopener" target="_blank">লগইন</a>
          <a class="btn btn-gold btn-sm" href="{CTA_SIGNUP}" rel="nofollow sponsored noopener" target="_blank">রেজিস্টার</a>
        </div>
      </div>
    </div>
  </nav>

  <header class="page-hero">
    <div class="container">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb breadcrumb-jw">
            {crumb_html}
        </ol>
      </nav>
      <h1>{h1}</h1>
      <p class="lead mb-0">{lead}</p>
    </div>
  </header>

  <main class="content-wrap">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-9 content-body">
{body}
          <div class="page-cta">
            <h2>JitaWin-এ এখনই শুরু করুন</h2>
            <p class="text-muted-jw small mb-3">bKash/Nagad · সর্বনিম্ন ৳১০০ · ১৮+ · Responsible play</p>
            <div class="d-grid d-sm-flex gap-2 justify-content-center">
              <a class="btn btn-gold" href="{CTA_SIGNUP}" rel="nofollow sponsored noopener" target="_blank">এখনই রেজিস্টার করুন</a>
              <a class="btn btn-jw-green" href="{CTA_HOME}" rel="nofollow sponsored noopener" target="_blank">সাইট ভিজিট করুন</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="row g-4 mb-4">
        <div class="col-md-5">
          <a class="logo mb-2 d-inline-flex" href="{p}">
            <span class="logo-mark">JW</span>
            <span class="logo-text">Jita<span>Win</span></span>
          </a>
          <p class="text-muted-jw small mt-2 mb-0">তৃতীয় পক্ষের এজেন্ট/কনটেন্ট সাইট — অফিসিয়াল অপারেটর নয়।</p>
        </div>
        <div class="col-6 col-md-3">
          <div class="footer-heading">লিংক</div>
          <ul class="list-unstyled small mb-0">
            <li class="mb-1"><a href="{p}guide/">গাইড</a></li>
            <li class="mb-1"><a href="{p}payment/">পেমেন্ট</a></li>
            <li class="mb-1"><a href="{p}promotions/">প্রমোশন</a></li>
            <li class="mb-1"><a href="{p}affiliate/">রেফারেল</a></li>
            <li><a href="{p}faq/">FAQ</a></li>
          </ul>
        </div>
        <div class="col-6 col-md-4">
          <div class="footer-heading">গুরুত্বপূর্ণ</div>
          <ul class="list-unstyled small mb-0">
            <li class="mb-1"><a href="{p}about-jitawin/">JitaWin কী?</a></li>
            <li class="mb-1"><a href="{p}mirror-links/">মিরর লিংক</a></li>
            <li class="mb-1"><a href="{p}responsible-gambling/">দায়িত্বশীল গেমিং</a></li>
            <li><a href="{p}disclaimer/">ডিসক্লেইমার</a></li>
          </ul>
        </div>
      </div>
      <hr class="border-secondary border-opacity-25" />
      <p class="small text-muted-jw mb-0">© 2026 JitaWin BD Affiliate Guide · ১৮+ · সব নিয়ম প্ল্যাটফর্মের সর্বশেষ T&amp;C অনুযায়ী।</p>
      <div class="disclaimer-box">এটি তৃতীয় পক্ষের প্রমোশন সাইট। অনলাইন বেটিং ঝুঁকিপূর্ণ।</div>
    </div>
  </footer>

  <div class="sticky-cta d-flex d-md-none gap-2">
    <a class="btn btn-outline-gold flex-fill" href="{CTA_HOME}" rel="nofollow sponsored noopener" target="_blank">ভিজিট</a>
    <a class="btn btn-gold flex-fill" href="{CTA_SIGNUP}" rel="nofollow sponsored noopener" target="_blank">রেজিস্টার</a>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
"""
    out = ROOT / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {rel_path}")


def cards(prefix: str, items: list[tuple[str, str, str, str]]) -> str:
    """items: href, icon, title, desc"""
    cols = []
    for href, icon, title, desc in items:
        cols.append(
            f"""          <div class="col-md-6">
            <a class="subpage-card" href="{href}">
              <div class="card card-jw p-3 h-100">
                <div class="d-flex gap-3 align-items-start">
                  <div class="icon-box icon-box-sm m-0"><i class="bi {icon}" aria-hidden="true"></i></div>
                  <div>
                    <h2 class="h6 mb-1 mt-0">{title}</h2>
                    <p class="card-text small mb-0">{desc}</p>
                  </div>
                </div>
              </div>
            </a>
          </div>"""
        )
    return '<div class="row g-3 mb-2">\n' + "\n".join(cols) + "\n          </div>"


def toc(items: list[tuple[str, str]]) -> str:
    lis = "\n".join(f'              <li class="mb-1"><a href="#{aid}">{label}</a></li>' for aid, label in items)
    return f"""          <nav class="toc-card" aria-label="Table of contents">
            <h2>এই পেজে যা আছে</h2>
            <ol>
{lis}
            </ol>
          </nav>"""


def exp(text: str) -> str:
    return f"""          <aside class="experience-box mt-4">
            <strong class="text-gold d-block mb-1"><i class="bi bi-pencil-square" aria-hidden="true"></i> আমার নোট</strong>
            {text}
          </aside>"""


# ---------------- PAGE CONTENT ----------------

def build_all():
    # ABOUT hub
    page(
        "about-jitawin/index.html",
        "What is JitaWin Bangladesh? Brand &amp; Platform Guide 2026",
        "Learn what JitaWin is for Bangladeshi players: operator Altervance Ltd., license ALSI-142311014, games, payments and sister brands.",
        "JitaWin কী? — বাংলাদেশ মার্কেটের জন্য সংক্ষিপ্ত পরিচিতি",
        "JitaWin একটি অনলাইন গেমিং প্ল্যাটফর্ম (স্লট, লাইভ, স্পোর্টস, ফিশিং)। এই সাইটটি অফিসিয়াল নয় — স্বাধীন এজেন্ট কনটেন্ট গাইড।",
        toc([("what", "JitaWin কী করে"), ("who", "কে চালায়"), ("links", "বিস্তারিত পেজ")])
        + """
          <h2 id="what">এক নজরে</h2>
          <p>JitaWin (JW) মূলত বাংলাদেশি খেলোয়াড়দের জন্য bKash/Nagad/Rocket ডিপোজিট, ক্রিকেট স্পোর্টস ও স্লট/লাইভ গেম এক জায়গায় দেয়। ইন্টারফেস ইংরেজি-প্রধান, কিছু বাংলা উপাদান (যেমন খবর) আছে।</p>
          <ul>
            <li>মূল ডোমেইন রেফারেন্স: jitawin.com</li>
            <li>মিরর: jitawin.casino, jitawin.cloud, jitawin.cc, jitawin.win, jitawin.vip</li>
            <li>মোবাইল: <strong class="text-white">PWA</strong> (APK নয়) — w01.jitawin.com</li>
          </ul>
          <h2 id="who">অপারেটর</h2>
          <p>অপারেটিং কোম্পানি: <strong class="text-white">Altervance Ltd.</strong> · রেজি. নং 000031825 · ঠিকানা: 9 Barrack Road, Belize City, Belize · লাইসেন্স: ALSI-142311014 (Anjouan, Union of Comoros)।</p>
          <h2 id="links">আরও পড়ুন</h2>
"""
        + cards("../", [
            ("license-safety.html", "bi-shield-check", "লাইসেন্স ও নিরাপত্তা", "কোম্পানি, লাইসেন্স নম্বর, লাইসেন্স মানে কী"),
            ("sister-brands.html", "bi-diagram-3", "সিস্টার ব্র্যান্ড", "JITA PROGRAM ও JitaOne Group"),
            ("../guide/", "bi-journal-text", "নতুনদের গাইড", "রেজিস্টার থেকে উইথড্র পর্যন্ত"),
            ("../disclaimer/", "bi-info-circle", "এই সাইটের ডিসক্লেইমার", "তৃতীয় পক্ষ প্রমোশন স্ট্যাটাস"),
        ])
        + exp("আমি এই গাইডে শুধু যাচাইযোগ্য প্ল্যাটফর্ম তথ্য রাখি — «গ্যারান্টিড জিতবেন» টাইপ দাবি এড়াই। প্রথমে লাইসেন্স পেজ ও ডিসক্লেইমার পড়ে নিন।"),
        [("../", "হোম"), ("#", "JitaWin কী?")],
        "about-jitawin",
    )

    page(
        "about-jitawin/license-safety.html",
        "JitaWin License &amp; Safety — ALSI-142311014 Explained",
        "JitaWin operator Altervance Ltd., Anjouan license ALSI-142311014, company registration and what a gaming license means for Bangladeshi players.",
        "লাইসেন্স ও নিরাপত্তা — ALSI-142311014",
        "«সেফ কি?» প্রশ্নের স্পষ্ট উত্তর: কে চালায়, কোন লাইসেন্স, আর লাইসেন্স কী গ্যারান্টি দেয় না।",
        toc([("company", "কোম্পানি তথ্য"), ("license", "লাইসেন্স"), ("mean", "লাইসেন্স মানে কী"), ("tips", "নিজের সুরক্ষা")])
        + """
          <h2 id="company">কোম্পানি</h2>
          <div class="table-wrap table-responsive mb-3">
            <table class="table table-jw table-striped mb-0">
              <tbody>
                <tr><td>ব্র্যান্ড</td><td>JitaWin (JW)</td></tr>
                <tr><td>অপারেটর</td><td>Altervance Ltd.</td></tr>
                <tr><td>রেজিস্ট্রেশন নং</td><td>000031825</td></tr>
                <tr><td>ঠিকানা</td><td>9 Barrack Road, Belize City, Belize</td></tr>
                <tr><td>ইমেইল (প্ল্যাটফর্ম)</td><td>admin@jitawin.com</td></tr>
              </tbody>
            </table>
          </div>
          <h2 id="license">গেমিং লাইসেন্স</h2>
          <ul>
            <li>ইস্যুয়ার: Union of Comoros — Anjouan স্বায়ত্তশাসিত কর্তৃপক্ষ</li>
            <li>লাইসেন্স নং: <strong class="text-gold">ALSI-142311014</strong></li>
          </ul>
          <h2 id="mean">লাইসেন্স মানে কী — আর কী নয়</h2>
          <p><strong class="text-white">মানে:</strong> অপারেটর একটি নির্দিষ্ট রেগুলেটরি ফ্রেমওয়ার্কের অধীনে রেজিস্টার্ড।</p>
          <p><strong class="text-white">মানে নয়:</strong> আপনি অবশ্যই জিতবেন, উইথড্র কখনো ডিলে হবে না, বা ঝুঁকি শূন্য — এসব গ্যারান্টি নয়।</p>
          <div class="callout callout-warn">
            <i class="bi bi-exclamation-triangle" aria-hidden="true"></i>
            এই প্রমোশন সাইট লাইসেন্স «ভেরিফাই সার্টিফিকেট» নয়। বর্তমান স্ট্যাটাস নিজে যাচাই করুন এবং শুধু হারাতে পারবেন এমন টাকা খেলুন।
          </div>
          <h2 id="tips">নিজের সুরক্ষা চেকলিস্ট</h2>
          <ol>
            <li>শুধু ট্রাস্টেড এন্ট্রি/অফিসিয়াল মিরর ব্যবহার করুন</li>
            <li>APK নয় — PWA ইনস্টল ফ্লো মেনে চলুন</li>
            <li>KYC ও ওয়েজারিং শেষ না করে বড় উইথড্র আশা করবেন না</li>
            <li>একই ডিভাইস/IP-এ মাল্টি অ্যাকাউন্ট এড়িয়ে চলুন</li>
          </ol>
"""
        + exp("Trustpilot/ফোরামে «উইথড্র আটকে» অভিযোগের বড় অংশ আসলে অসম্পূর্ণ ভেরিফিকেশন বা বোনাস ওয়েজারিং — লাইসেন্স থাকলেও নিয়ম মানা লাগে।"),
        [("../", "হোম"), ("index.html", "JitaWin কী?"), ("#", "লাইসেন্স")],
        "about-jitawin",
    )

    page(
        "about-jitawin/sister-brands.html",
        "JitaWin Sister Brands — JITA PROGRAM &amp; JitaOne Group",
        "Related brands around JitaWin: JITA SPORTS, Owin, JitaOne, HeyJita, JitaBet, JitaGo, Laki55 for Bangladesh market context.",
        "সিস্টার ব্র্যান্ড ও গ্রুপ পরিচিতি",
        "JitaWin-এর আশেপাশের ব্র্যান্ড ম্যাপ — কনফিউশন কমাতে সংক্ষিপ্ত তালিকা।",
        """
          <p>প্ল্যাটফর্ম ডেটা অনুযায়ী সম্পর্কিত ব্র্যান্ড দুই গ্রুপে দেখা যায়:</p>
          <h2>JITA PROGRAM</h2>
          <ul>
            <li>JITA SPORTS</li>
            <li>Owin</li>
          </ul>
          <h2>JITAONE GROUP (পার্টনার ব্র্যান্ড)</h2>
          <ul>
            <li>JitaOne</li>
            <li>HeyJita</li>
            <li>JitaBet</li>
            <li>JitaGo</li>
            <li>Laki55</li>
          </ul>
          <div class="callout callout-gold">
            ক্রস-ব্র্যান্ড প্রমোশন (যেমন Laki55 / JitaBet কোলাব) সময়সীমাবদ্ধ হতে পারে — সবসময় প্ল্যাটফর্মের চলমান অফার পেজ চেক করুন। এই সাইট প্রতিটি ব্র্যান্ডের অফিসিয়াল সাপোর্ট নয়।
          </div>
"""
        + exp("নতুনরা প্রায়ই JitaWin/JitaAce/JitaBet নাম মিশিয়ে ফেলে — রেজিস্টার লিংক ও বোনাস কোড কোন ব্র্যান্ডের, সেটা আগে নিশ্চিত করি।"),
        [("../", "হোম"), ("index.html", "JitaWin কী?"), ("#", "সিস্টার ব্র্যান্ড")],
        "about-jitawin",
    )

    # GUIDE
    page(
        "guide/index.html",
        "JitaWin Beginner Guide Bangladesh — Register to Withdraw",
        "Step-by-step JitaWin beginner guide for Bangladesh: register, KYC verification, deposit, play, withdraw and PWA install.",
        "নতুনদের সম্পূর্ণ গাইড",
        "রেজিস্টার → ভেরিফাই → ডিপোজিট → খেলা → উইথড্র — এক লাইনে শেখা।",
        """
          <p>নিচের ধাপগুলো অনুসরণ করলে বেশিরভাগ «উইথড্র হচ্ছে না» সমস্যা আগেভাগে এড়ানো যায়।</p>
"""
        + cards("", [
            ("register.html", "bi-person-plus", "রেজিস্টার টিউটোরিয়াল", "Username, OTP, Google login, Terms"),
            ("verification.html", "bi-person-vcard", "KYC / ভেরিফিকেশন", "নাম + মোবাইল — VIP2 ও উইথড্র"),
            ("app-download.html", "bi-phone", "App (PWA) ইনস্টল", "APK নয় — Add to Home Screen"),
            ("../payment/", "bi-wallet2", "ডিপোজিট ও উইথড্র", "bKash, Nagad, Rocket, USDT"),
            ("../promotions/wagering-explained.html", "bi-calculator", "ওয়েজারিং বোঝা", "টার্নওভার উদাহরণসহ"),
            ("../faq/", "bi-question-circle", "FAQ", "বারবার জিজ্ঞাসিত প্রশ্ন"),
        ])
        + """
          <h2>৪ ধাপ সারাংশ</h2>
          <ol>
            <li><strong class="text-white">রেজিস্টার</strong> — মোবাইল OTP বা Google</li>
            <li><strong class="text-white">ভেরিফাই</strong> — first/last name + mobile</li>
            <li><strong class="text-white">ডিপোজিট</strong> — ৳১০০+ , বোনাস সিলেক্ট</li>
            <li><strong class="text-white">খেলা ও উইথড্র</strong> — ওয়েজারিং শেষে রিকোয়েস্ট</li>
          </ol>
"""
        + exp("প্রথম দিনেই বড় বোনাস নিয়ে ৩০x ওয়েজারিং-এ আটকে যাওয়া কমন — ছোট ডিপোজিট দিয়ে ফ্লো শিখে নিন।"),
        [("../", "হোম"), ("#", "গাইড")],
        "guide",
    )

    page(
        "guide/register.html",
        "JitaWin Register Guide Bangladesh — Sign Up Steps",
        "How to register on JitaWin: username, password, mobile OTP, Google continue, Terms checkbox. Affiliate signup link for Bangladesh.",
        "JitaWin রেজিস্টার টিউটোরিয়াল",
        "নতুন অ্যাকাউন্ট খুলতে কী কী লাগে — ধাপে ধাপে।",
        toc([("need", "যা লাগবে"), ("steps", "ধাপ"), ("tips", "টিপস")])
        + f"""
          <h2 id="need">যা লাগবে</h2>
          <ul>
            <li>একটি ইউনিক Username</li>
            <li>Password + Confirm Password</li>
            <li>বাংলাদেশি Mobile Number + Verification Code (OTP)</li>
            <li>JitaWin Terms &amp; Conditions-এ সম্মতি (বাধ্যতামূলক)</li>
          </ul>
          <p>অল্টারনেটিভ: <strong class="text-white">Google</strong> দিয়ে এক ক্লিকে continue।</p>
          <h2 id="steps">ধাপসমূহ</h2>
          <ol>
            <li>এজেন্ট সাইনআপ লিংক খুলুন (নিচের বাটন)</li>
            <li>ফর্ম পূরণ করুন বা Google বেছে নিন</li>
            <li>মোবাইল OTP ভেরিফাই করুন</li>
            <li>Terms টিক দিন → অ্যাকাউন্ট তৈরি</li>
            <li>লগইন করে প্রোফাইলে নাম ভেরিফিকেশন শুরু করুন</li>
          </ol>
          <div class="callout callout-gold">
            লগইন স্ক্রিনে সাধারণত থাকে: Remember Me, Forgot Password, ভাষা সুইচ।
          </div>
          <h2 id="tips">টিপস</h2>
          <ul>
            <li>পাসওয়ার্ড সেভ করুন — শেয়ার করবেন না</li>
            <li>রেফারেল/প্রমো কোড থাকলে <strong class="text-white">রেজিস্টারের সময়ই</strong> ব্যবহার করুন (পরে বাইন্ড নাও হতে পারে)</li>
            <li>এক ডিভাইসে একাধিক অ্যাকাউন্ট রিস্কি</li>
          </ul>
          <p class="mt-3"><a class="btn btn-gold" href="{CTA_SIGNUP}" rel="nofollow sponsored noopener" target="_blank">রেজিস্টার পেজ খুলুন</a></p>
"""
        + exp("OTP না এলে নেটওয়ার্ক/নাম্বার ফরম্যাট চেক করি; Google login অনেক সময় দ্রুত হয়, তারপরও মোবাইল বাইন্ড করে নেওয়া ভালো।"),
        [("../", "হোম"), ("index.html", "গাইড"), ("#", "রেজিস্টার")],
        "guide",
    )

    page(
        "guide/verification.html",
        "JitaWin KYC Verification Guide — Name &amp; Mobile",
        "JitaWin identity verification: first name, last name, mobile verify for VIP2 and withdrawals. Why KYC blocks cashout.",
        "পরিচয় যাচাই (KYC) গাইড",
        "উইথড্র আটকানোর সবচেয়ে কমন কারণ — ভেরিফিকেশন অসম্পূর্ণ।",
        """
          <p>প্ল্যাটফর্ম নিয়ম অনুযায়ী উইথড্রের আগে <strong class="text-white">নাম (first/last) + মোবাইল ভেরিফিকেশন</strong> প্রয়োজন। VIP2-এর জন্যও একই ভেরিফিকেশন লাগে।</p>
          <h2>কী কী ভেরিফাই করবেন</h2>
          <ul>
            <li>প্রথম নাম / শেষ নাম — পেমেন্ট অ্যাকাউন্টের নামের সাথে মিল রাখুন</li>
            <li>মোবাইল নম্বর ভেরিফিকেশন</li>
          </ul>
          <div class="callout callout-warn">
            সিস্টেম মেম্বার লেভেল/শর্ত অনুযায়ী উইথড্র আটকে «ভেরিফাই করুন» বলতে পারে। বড় ডিপোজিটের আগেই KYC শেষ করুন।
          </div>
          <h2>VIP-এর সাথে সম্পর্ক</h2>
          <ul>
            <li><strong class="text-white">VIP1</strong> — রেজিস্ট্রেশনেই</li>
            <li><strong class="text-white">VIP2</strong> — নাম + মোবাইল ভেরিফাই করতে হয়</li>
            <li><strong class="text-white">VIP3+</strong> — ডিপোজিট/বেট থ্রেশহোল্ড</li>
          </ul>
          <h2>উইথড্র ফর্মে যা চাইতে পারে</h2>
          <ul>
            <li>লগইন পাসওয়ার্ড</li>
            <li>অ্যাকাউন্ট টাইপ</li>
            <li>অ্যাকাউন্ট হোল্ডারের নাম</li>
          </ul>
"""
        + exp("bKash নাম আর প্রোফাইল নাম না মিললে ম্যানুয়াল রিভিউ/রিজেক্ট দেখেছি — আগে মিলিয়ে নিন।"),
        [("../", "হোম"), ("index.html", "গাইড"), ("#", "ভেরিফিকেশন")],
        "guide",
    )

    page(
        "guide/app-download.html",
        "JitaWin App Download Bangladesh — PWA Install (Not APK)",
        "Install JitaWin mobile as PWA from w01.jitawin.com. Not Play Store APK. Chrome/Safari Add to Home Screen steps for Bangladesh.",
        "JitaWin APP ইনস্টল — PWA (APK নয়)",
        "মোবাইল ভার্সন Progressive Web App। অজানা APK ইনস্টল করবেন না।",
        toc([("truth", "সত্য কী"), ("steps", "ইনস্টল ধাপ"), ("btns", "ডাউনলোড পেজ বাটন")])
        + f"""
          <h2 id="truth">APK নয় — PWA</h2>
          <p>JitaWin মোবাইল = <strong class="text-white">Progressive Web App</strong>। App Store/Google Play নেটিভ অ্যাপ বা APK ডাইরেক্ট ইনস্টল নয়।</p>
          <p>ইনস্টল সোর্স ডোমেইন: <strong class="text-gold">w01.jitawin.com</strong></p>
          <div class="callout callout-warn">
            <i class="bi bi-exclamation-triangle" aria-hidden="true"></i>
            এই প্রমোশন সাইট থেকে কোনো APK ফাইল দেওয়া হয় না। নকল APK অ্যাকাউন্ট চুরির ঝুঁকি।
          </div>
          <h2 id="steps">ইনস্টল ধাপ</h2>
          <figure class="content-figure">
            <img src="../assets/images/guide-app-install.webp" alt="JitaWin mobile PWA install steps: open download page, tap Download App, confirm Install prompt on w01.jitawin.com" width="1200" height="800" loading="lazy" decoding="async" />
            <figcaption>ধাপ ১–৩: ডাউনলোড পেজ → প্রথম বাটন ট্যাপ → «Install» কনফার্ম (PWA · w01.jitawin.com)</figcaption>
          </figure>
          <ol>
            <li>Chrome বা Safari-এ অফিসিয়াল এন্ট্রি/মিরর দিয়ে লগইন-যোগ্য সাইট খুলুন</li>
            <li>ডাউনলোড/ইনস্টল পেজে যান (রেফারেন্স: <strong class="text-gold">w01.jitawin.com</strong>)</li>
            <li>«DOWNLOAD APP» / প্রথম বাটন ট্যাপ করুন</li>
            <li>ব্রাউজার «Install this app?» প্রম্পটে <strong class="text-white">Install</strong> চাপুন</li>
            <li>হোম স্ক্রিনে আইকন সেভ হয়ে গেলে App-এর মতো খুলবে · চাইলে নোটিফিকেশন অন করুন</li>
          </ol>
          <h2 id="btns">ডাউনলোড পেজের বাটন (রেফারেন্স)</h2>
          <ul>
            <li><strong class="text-white">ডাইনলোড</strong> — PWA ইনস্টল ট্রিগার</li>
            <li><strong class="text-white">নোটিফিকেশন সক্রিয় করুন</strong></li>
            <li><strong class="text-white">হোম পেজে ফিরে যান / Return to JitaWin</strong></li>
          </ul>
          <p class="text-muted-jw">পেজ কপি: «আপনার ডিভাইসে আজই JitaWin APP দিয়ে শুরু করুন»</p>
          <p class="mt-3"><a class="btn btn-jw-green" href="{CTA_HOME}" rel="nofollow sponsored noopener" target="_blank">প্ল্যাটফর্মে যান</a></p>
"""
        + exp("অনেকে ‘APK লিংক চাই’ বলে মেসেজ করে — আমি স্পষ্ট বলি PWA; ভুল APK দিলে ট্রাস্ট ও সিকিউরিটি দুটোই নষ্ট।"),
        [("../", "হোম"), ("index.html", "গাইড"), ("#", "App PWA")],
        "guide",
    )

    # PAYMENT hub + methods
    page(
        "payment/index.html",
        "JitaWin Deposit &amp; Withdrawal Bangladesh — bKash Nagad Rocket",
        "JitaWin payment methods for Bangladesh: bKash, Nagad, Rocket, USDT limits and fees, plus withdrawal FAQ.",
        "ডিপোজিট ও উইথড্র গাইড",
        "bKash, Nagad, Rocket, USDT — লিমিট, ফি, আর উইথড্র আটকানোর কারণ।",
        """
          <p>সর্বনিম্ন ডিপোজিট সাধারণত <strong class="text-gold">৳১০০</strong>। ডিপোজিটের সময় চলমান বোনাস বেছে নিতে পারেন।</p>
          <h2 id="deposit-steps">ডিপোজিট ধাপ (ছবিসহ)</h2>
          <figure class="content-figure">
            <img src="../assets/images/guide-deposit-steps.webp" alt="JitaWin deposit steps: open Deposit menu, choose bKash Nagad or Rocket, fill amount and submit, success confirmation" width="1200" height="900" loading="lazy" decoding="async" />
            <figcaption>ধাপ ১–৪: Deposit মেনু → মেথড বেছে নিন → তথ্য পূরণ/Submit → সফল রিকোয়েস্ট</figcaption>
          </figure>
          <ol>
            <li>লগইন করে মেনু থেকে <strong class="text-white">Deposit</strong> খুলুন</li>
            <li>পেমেন্ট মেথড বেছে নিন: bKash / Nagad / Rocket (বা অন্য সাপোর্টেড অপশন)</li>
            <li>অ্যামাউন্ট + প্রয়োজনীয় নম্বর/তথ্য পূরণ করুন · বোনাস থাকলে সিলেক্ট করুন → Submit</li>
            <li>সফল রিকোয়েস্ট দেখলে ওয়ালেট ব্যালেন্স কয়েক মিনিটের মধ্যে চেক করুন</li>
          </ol>
          <div class="callout callout-gold mb-4">ছবিটি সাধারণ ফ্লো দেখায়; প্রতিটি মেথডের লিমিট নিচের টেবিল ও আলাদা পেজে দেখুন। এই সাইট পেমেন্ট প্রসেস করে না।</div>
          <div class="table-wrap table-responsive mb-4">
            <table class="table table-jw table-striped mb-0">
              <thead><tr><th>মেথড</th><th>লিমিট</th><th>ফি</th></tr></thead>
              <tbody>
                <tr><td>bKash</td><td>৳100–25,000</td><td>Max +1%</td></tr>
                <tr><td>Nagad</td><td>৳100–50,000</td><td>Max +1%</td></tr>
                <tr><td>Rocket</td><td>৳100–30,000</td><td>Max +1%</td></tr>
                <tr><td>USDT/USDC</td><td>৳100–25,000</td><td>লাইভ রেট</td></tr>
                <tr><td>TPay / TFPay</td><td>স্কিম অনুযায়ী</td><td>+1%</td></tr>
              </tbody>
            </table>
          </div>
"""
        + cards("", [
            ("bkash.html", "bi-phone", "bKash", "৳100–25,000 · Max +1%"),
            ("nagad.html", "bi-phone", "Nagad", "৳100–50,000 · Max +1%"),
            ("rocket.html", "bi-phone", "Rocket", "৳100–30,000 · Max +1%"),
            ("crypto.html", "bi-currency-bitcoin", "USDT / USDC", "BEP-20 / TRC-20 / ERC-20"),
            ("withdrawal-faq.html", "bi-cash-stack", "উইথড্র FAQ", "কেন রিজেক্ট হয়"),
        ]),
        [("../", "হোম"), ("#", "পেমেন্ট")],
        "payment",
    )

    def pay_method(filename, title_en, name, limit, fee, extra=""):
        page(
            f"payment/{filename}",
            f"JitaWin {name} Deposit &amp; Withdraw Guide Bangladesh",
            f"How to deposit and withdraw on JitaWin with {name}. Limit {limit}, fee {fee}. Bangladesh mobile payment guide.",
            f"JitaWin {name} ডিপোজিট ও উইথড্র",
            f"লিমিট {limit} · ফি {fee} · বাংলাদেশি মোবাইল পেমেন্ট।",
            f"""
          <h2>সারাংশ</h2>
          <ul>
            <li>মেথড: <strong class="text-white">{name}</strong></li>
            <li>ডিপোজিট লিমিট: <strong class="text-gold">{limit}</strong></li>
            <li>ফি: {fee}</li>
            <li>সাধারণ মিনিমাম ডিপোজিট ফ্লোর: ৳১০০</li>
          </ul>
          <h2>ডিপোজিট ধাপ (সাধারণ)</h2>
          <figure class="content-figure">
            <img src="../assets/images/guide-deposit-steps.webp" alt="JitaWin deposit steps illustration for {name}: menu, payment method, form, success" width="1200" height="900" loading="lazy" decoding="async" />
            <figcaption>সাধারণ ডিপোজিট ফ্লো — বিস্তারিত <a href="index.html">পেমেন্ট ওভারভিউ</a></figcaption>
          </figure>
          <ol>
            <li>প্ল্যাটফর্মে লগইন → Deposit / Wallet</li>
            <li>{name} সিলেক্ট করুন</li>
            <li>অ্যামাউন্ট দিন (লিমিটের মধ্যে)</li>
            <li>চলমান বোনাস থাকলে সিলেক্ট করুন</li>
            <li>নির্দেশিত নম্বর/ইনভয়েস অনুযায়ী {name} দিয়ে পাঠান</li>
            <li>ট্রানজেকশন আইডি/স্ক্রিনশট রাখুন</li>
          </ol>
          <h2>উইথড্র নোট</h2>
          <ul>
            <li>উইথড্রের আগে নাম + মোবাইল KYC শেষ করুন</li>
            <li>বোনাস ওয়েজারিং বাকি থাকলে আটকে যেতে পারে</li>
            <li>সিঙ্গেল উইথড্র রেঞ্জ সাধারণত প্রায় ৳100–25,000 (অ্যাক্টিভিটি/লেভেলভেদে ভিন্ন হতে পারে)</li>
            <li>ডিপোজিট ও উইথড্র অ্যাকাউন্ট তথ্য মিলিয়ে নিন</li>
          </ul>
          {extra}
          <div class="callout callout-gold">এই সাইট পেমেন্ট প্রসেস করে না — সব ট্রানজেকশন প্ল্যাটফর্মের ভিতরে হয়।</div>
"""
            + exp(f"{name}-এ প্রথমবার ছোট অ্যামাউন্ট দিয়ে টেস্ট করি; বড় বোনাস সিলেক্টের আগে ওয়েজারিং হিসাব।"),
            [("../", "হোম"), ("index.html", "পেমেন্ট"), ("#", name)],
            "payment",
        )

    pay_method("bkash.html", "bKash", "bKash", "৳100–25,000", "Max +1%",
               "<p>bKash বাংলাদেশের সবচেয়ে কমন ডিপোজিট চ্যানেলগুলোর একটি। নম্বর/অ্যাকাউন্ট নাম ভুল হলে ডিপোজিট ডিলে হতে পারে।</p>")
    pay_method("nagad.html", "Nagad", "Nagad", "৳100–50,000", "Max +1%",
               "<p>Nagad-এর আপার লিমিট bKash-এর চেয়ে বেশি (৳50,000 পর্যন্ত) — বড় ডিপোজিটে সুবিধা হতে পারে।</p>")
    pay_method("rocket.html", "Rocket", "Rocket", "৳100–30,000", "Max +1%",
               "<p>Rocket (DBBL মোবাইল ব্যাংকিং) অনেক ইউজারের সেকেন্ডারি অপশন। লিমিট ৳100–30,000।</p>")

    page(
        "payment/crypto.html",
        "JitaWin USDT USDC Deposit Guide Bangladesh",
        "Deposit on JitaWin with USDT/USDC (BEP-20, TRC-20, ERC-20). Limits ৳100–25,000. Use live rate on platform.",
        "USDT / USDC ক্রিপ্টো ডিপোজিট",
        "BEP-20 / TRC-20 / ERC-20 সাপোর্ট · লিমিট ৳100–25,000 · রেট প্ল্যাটফর্মে লাইভ।",
        """
          <h2>মূল তথ্য</h2>
          <ul>
            <li>লিমিট: <strong class="text-gold">৳100–25,000</strong> (BDT ইকুইভ্যালেন্ট)</li>
            <li>নেটওয়ার্ক: BEP-20, TRC-20, ERC-20</li>
            <li>রেট: <strong class="text-white">প্ল্যাটফর্ম পেজে দেখানো লাইভ রেট</strong> অনুযায়ী (এখানে নির্দিষ্ট সংখ্যা ফিক্স করা হয়নি)</li>
          </ul>
          <h2>সতর্কতা</h2>
          <ul>
            <li>সঠিক নেটওয়ার্ক সিলেক্ট না করলে ফান্ড হারাতে পারেন</li>
            <li>ছোট টেস্ট ট্রান্সফার করে নিন</li>
            <li>কিছু বোনাস (যেমন ৬% ডায়মন্ড টপ-আপ) USDT-তে প্রযোজ্য নয়</li>
          </ul>
"""
        + exp("ক্রিপ্টোতে নেটওয়ার্ক মিসম্যাচই সবচেয়ে বড় রিস্ক — ঠিকানা কপি-পেস্ট ডাবল-চেক করি।"),
        [("../", "হোম"), ("index.html", "পেমেন্ট"), ("#", "Crypto")],
        "payment",
    )

    page(
        "payment/withdrawal-faq.html",
        "JitaWin Withdrawal Problem — Why Rejected &amp; How to Fix",
        "Common JitaWin withdrawal rejects: incomplete KYC, wagering not done, account mismatch. Limits and checklist for Bangladesh.",
        "উইথড্র সমস্যা ও রিজেক্টের কারণ",
        "কেন আটকে/রিজেক্ট হয় — চেকলিস্ট ও সমাধানের দিকনির্দেশ।",
        toc([("common", "কমন কারণ"), ("limit", "লিমিট"), ("check", "চেকলিস্ট"), ("delay", "ডিলে নোট")])
        + """
          <h2 id="common">সবচেয়ে কমন কারণ</h2>
          <ol>
            <li><strong class="text-white">KYC অসম্পূর্ণ</strong> — first/last name + মোবাইল ভেরিফাই হয়নি</li>
            <li><strong class="text-white">ওয়েজারিং বাকি</strong> — বোনাস টার্নওভার শেষ হয়নি</li>
            <li><strong class="text-white">অ্যাকাউন্ট মিসম্যাচ</strong> — ডিপোজিট/উইথড্র নাম বা নম্বর আলাদা</li>
            <li>ভুল পাসওয়ার্ড বা ফর্ম ফিল্ড</li>
          </ol>
          <h2 id="limit">উইথড্র লিমিট (রেফারেন্স)</h2>
          <p>সিঙ্গেল উইথড্র প্রায় <strong class="text-gold">৳100–25,000</strong> — অ্যাক্টিভিটি/লেভেলভেদে ভিন্ন হতে পারে।</p>
          <h2 id="check">উইথড্রের আগে চেকলিস্ট</h2>
          <ul>
            <li>প্রোফাইল নাম পূরণ ও মোবাইল verified</li>
            <li>Bonus/Wagering প্রোগ্রেস ০ বা ক্লিয়ার</li>
            <li>সঠিক পেমেন্ট মেথড ও হোল্ডার নাম</li>
            <li>লগইন পাসওয়ার্ড হাতে আছে</li>
          </ul>
          <h2 id="delay">ডিলে হলে</h2>
          <p>প্ল্যাটফর্মে ৳88 ডিলে কম্পেনসেশন অফার থাকতে পারে (শর্ত: ডিপোজিট ইতিহাস, দৈনিক লিমিট, ওয়েজারিং) — বিস্তারিত চলমান প্রমো পেজে। এই সাইট থেকে আবেদন প্রসেস হয় না।</p>
"""
        + exp("রিজেক্ট স্ক্রিনের মেসেজ স্ক্রিনশট রেখে ধাপে ধাপে KYC → wager → account match চেক করলে ৮০% কেস সলভ হয়।"),
        [("../", "হোম"), ("index.html", "পেমেন্ট"), ("#", "উইথড্র FAQ")],
        "payment",
    )

    # PROMOTIONS
    page(
        "promotions/index.html",
        "JitaWin Promotions Bangladesh — Bonus, Cashback, VIP",
        "JitaWin promo overview: welcome bonus, daily/weekly cashback, wagering rules and VIP. Bangladesh player guide.",
        "প্রমোশন ও বোনাস ওভারভিউ",
        "ওয়েলকাম, রিবেট, VIP — সবকটিতেই ওয়েজারিং আছে। নিয়ম পড়ে নিন।",
        """
          <div class="callout callout-warn mb-4">এক অ্যাকাউন্ট · অফার স্ট্যাক নয় · জালিয়াতি/মাল্টি অ্যাকাউন্টে লক ও ফান্ড বাজেয়াপ্ত হতে পারে।</div>
"""
        + cards("", [
            ("welcome-bonus.html", "bi-gift", "ওয়েলকাম / ফার্স্ট ডিপোজিট", "Slots/Fish/Sports/Crash"),
            ("cashback.html", "bi-arrow-repeat", "ডেইলি ও উইকলি রিবেট", "১০% স্লট · ৬% উইকলি"),
            ("wagering-explained.html", "bi-calculator", "ওয়েজারিং ব্যাখ্যা", "উদাহরণসহ টার্নওভার"),
            ("vip.html", "bi-award", "VIP ১–৩০", "আপগ্রেড, উইকলি, মান্থলি"),
        ]),
        [("../", "হোম"), ("#", "প্রমোশন")],
        "promotions",
    )

    page(
        "promotions/welcome-bonus.html",
        "JitaWin Welcome Bonus Bangladesh — First Deposit Offers",
        "JitaWin new member welcome bonus: slots ৳100 min 20x, fish, sports up to ৳5000, crash 50%. Full table.",
        "নতুন মেম্বার ফার্স্ট ডিপোজিট বোনাস",
        "একবারের ওয়েলকাম সিরিজ — ক্যাটাগরিভেদে লিমিট আলাদা।",
        """
          <div class="table-wrap table-responsive mb-3">
            <table class="table table-jw table-striped mb-0">
              <thead><tr><th>ক্যাটাগরি</th><th>মিন</th><th>বোনাস ক্যাপ</th><th>ম্যাক্স WD</th><th>ওয়েজার</th></tr></thead>
              <tbody>
                <tr><td>Slots</td><td>৳100</td><td>৳1,000</td><td>৳2,000</td><td>20x</td></tr>
                <tr><td>Fish</td><td>৳500</td><td>৳3,000</td><td>৳6,000</td><td>20x</td></tr>
                <tr><td>Sports</td><td>৳500</td><td>৳5,000</td><td>৳10,000</td><td>20x</td></tr>
                <tr><td>Crash 50%</td><td>Balance ৳500</td><td>৳1,000</td><td>No cap</td><td>15x</td></tr>
              </tbody>
            </table>
          </div>
          <div class="callout callout-gold">উদাহরণ (Slots 100% ধরে): ৳500 ডিপোজিট + ৳500 বোনাস = ৳1,000; 20x = ৳20,000 বেট ক্লিয়ার করতে হতে পারে (প্রমো রুল অনুযায়ী)।</div>
"""
        + exp("স্পোর্টস ওয়েলকাম ক্যাপ বেশি দেখে অনেকে নেয় — ওয়েজার 20x হিসাব না করলে উইথড্র দীর্ঘ হয়।"),
        [("../", "হোম"), ("index.html", "প্রমোশন"), ("#", "ওয়েলকাম")],
        "promotions",
    )

    page(
        "promotions/cashback.html",
        "JitaWin Cashback &amp; Rebate — Daily 10% Weekly 6%",
        "JitaWin daily slot cashback 2–10%, weekly 6% rebate, 6% diamond top-up VIP2+. Wagering notes for BD players.",
        "ডেইলি ও উইকলি রিবেট / ক্যাশব্যাক",
        "লস রিবেট ও ডিপোজিট টপ-আপ — শর্তসহ।",
        """
          <h2>১০% ডেইলি রিবেট (স্লট)</h2>
          <ul>
            <li>দিনের লসের উপর ২–১০% (টিয়ার)</li>
            <li>উইথড্র ক্যাপ ৳500,000</li>
            <li>ওয়েজার: <strong class="text-gold">1x</strong></li>
          </ul>
          <h2>৬% উইকলি রিবেট</h2>
          <p>প্রতি <strong class="text-white">বৃহস্পতিবার</strong> অতিরিক্ত রিবেট রিলিজ।</p>
          <h2>৬% ডায়মন্ড টপ-আপ (VIP2+)</h2>
          <ul>
            <li>প্রতিটি ডিপোজিটে — লিমিট/বার নেই</li>
            <li>প্রযোজ্য: JDB / JILI / PS / PG</li>
            <li><strong class="text-white">USDT প্রযোজ্য নয়</strong></li>
            <li>ওয়েজার 2x</li>
          </ul>
          <h2>উইকলি ১০০% সিরিজ (সারাংশ)</h2>
          <p>Crash / Sports / Slots / Fish — মিন ৳500, ক্যাপ ৳1,000, ওয়েজার 30x, সপ্তাহে একবার। স্লটস VIP3+ ও কিছু JILI এক্সক্লুশন আছে।</p>
"""
        + exp("ডেইলি 1x রিবেট তুলনামূলক «হালকা»; 30x উইকলি 100% নেওয়ার আগে হিসাব করি।"),
        [("../", "হোম"), ("index.html", "প্রমোশন"), ("#", "রিবেট")],
        "promotions",
    )

    page(
        "promotions/wagering-explained.html",
        "JitaWin Wagering / Turnover Explained with Examples",
        "What is wagering on JitaWin? Worked examples for 20x and 30x bonus turnover before withdrawal.",
        "ওয়েজারিং (টার্নওভার) কী?",
        "বোনাস নিলে কত বেট ক্লিয়ার করতে হয় — সংখ্যা দিয়ে বোঝা।",
        """
          <p><strong class="text-white">ওয়েজারিং/টার্নওভার</strong> মানে: বোনাস (বা বোনাস+ডিপোজিট — প্রমো রুল অনুযায়ী) উইথড্রযোগ্য করতে যে পরিমাণ বেট সম্পন্ন করতে হয়।</p>
          <h2>উদাহরণ ১ — 30x</h2>
          <p>ডিপোজিট ৳500 + 100% বোনাস = ৳1,000 ব্যবহারযোগ্য। ওয়েজার 30x হলে প্রায় <strong class="text-gold">৳30,000</strong> বেট সম্পন্ন করতে হতে পারে।</p>
          <h2>উদাহরণ ২ — 20x ওয়েলকাম স্লট</h2>
          <p>৳1,000 ডিপোজিট + ৳1,000 বোনাস (ক্যাপ অনুযায়ী) = ৳2,000 → 20x ≈ <strong class="text-gold">৳40,000</strong> বেট (রুল বেস অনুযায়ী যাচাই করুন)।</p>
          <h2>VIP রিওয়ার্ড</h2>
          <p>VIP বোনাসে সাধারণত <strong class="text-white">10–20x</strong> ওয়েজারিং থাকে (লেভেল/অফারভেদে)।</p>
          <div class="callout callout-warn">সব প্রমোর «বেস অ্যামাউন্ট» (শুধু বোনাস vs ডিপোজিট+বোনাস) প্ল্যাটফর্ম T&amp;C-তে দেখুন — এখানে শিক্ষামূলক উদাহরণ।</div>
"""
        + exp("আমি ইউজারকে প্রথমে ক্যালকুলেটর করে দেখাই: বোনাস × multiplier — না বুঝে ক্লিক করলেই পরে রাগ।"),
        [("../", "হোম"), ("index.html", "প্রমোশন"), ("#", "ওয়েজারিং")],
        "promotions",
    )

    page(
        "promotions/vip.html",
        "JitaWin VIP Levels 1–30 — Upgrade Bonus Weekly Monthly",
        "JitaWin VIP club: 30 levels, VIP2 verification, VIP5 monthly, VIP7 weekly. Key tier table for Bangladesh.",
        "VIP লেভেল ১–৩০",
        "Total Bet + Total Deposit · আপগ্রেড পরের দিন ০৩:০০ (GMT+6)।",
        """
          <ul>
            <li>VIP1: রেজিস্ট্রেশনেই</li>
            <li>VIP2: নাম + মোবাইল ভেরিফাই</li>
            <li>VIP5+: Monthly Bonus</li>
            <li>VIP7+: Weekly Bonus</li>
            <li>পয়েন্ট স্থায়ী (জিরো হয় না)</li>
            <li>রিওয়ার্ড ওয়েজার সাধারণত 10–20x</li>
          </ul>
          <div class="table-wrap table-responsive mb-3">
            <table class="table table-jw table-striped mb-0">
              <thead><tr><th>VIP</th><th>Total Bet</th><th>Total Deposit</th><th>Upgrade</th><th>Weekly</th><th>Monthly</th></tr></thead>
              <tbody>
                <tr><td>1</td><td>0</td><td>৳0</td><td>৳0</td><td>—</td><td>—</td></tr>
                <tr><td>3</td><td>1,000</td><td>৳300</td><td>৳8</td><td>—</td><td>—</td></tr>
                <tr><td>5</td><td>180,000</td><td>৳3,800</td><td>৳108</td><td>—</td><td>৳20</td></tr>
                <tr><td>7</td><td>1,380,000</td><td>৳28,000</td><td>৳288</td><td>৳5</td><td>৳50</td></tr>
                <tr><td>10</td><td>8,280,000</td><td>৳130,000</td><td>৳588</td><td>৳20</td><td>৳240</td></tr>
                <tr><td>15</td><td>26,800,000</td><td>৳1,380,000</td><td>৳1,588</td><td>৳45</td><td>৳540</td></tr>
                <tr><td>20</td><td>36,800,000</td><td>৳5,000,000</td><td>৳2,188</td><td>৳140</td><td>৳1,010</td></tr>
                <tr><td>30</td><td>300,800,000</td><td>৳10,000,000</td><td>৳3,688</td><td>৳250</td><td>৳2,000</td></tr>
              </tbody>
            </table>
          </div>
          <p class="small text-muted-jw">সম্পূর্ণ ৩০ লেভেল টেবিলের অংশবিশেষ। আপগ্রেড জাজমেন্ট: পরদিন ০৩:০০ GMT+6 · বোনাস ১২:০০ GMT+6।</p>
"""
        + exp("VIP3 রেফারেল ৳88-এর শর্ত — তাই নতুন প্রমোটারকে আগে ভেরিফাই+অ্যাক্টিভিটি বুঝিয়ে দিই।"),
        [("../", "হোম"), ("index.html", "প্রমোশন"), ("#", "VIP")],
        "promotions",
    )

    # GAMES
    page(
        "games/index.html",
        "JitaWin Games Bangladesh — Slots Live Sports Fishing Bingo",
        "JitaWin game categories and providers: slots, live casino, cricket sports, fishing, bingo for Bangladesh players.",
        "গেম ক্যাটাগরি ও প্রোভাইডার",
        "স্লট থেকে ক্রিকেট স্পোর্টস — কোন সেকশনে কী পাবেন।",
        cards("", [
            ("slots.html", "bi-grid-3x3-gap", "Slot", "JILI, PG, JDB, PP…"),
            ("live-casino.html", "bi-suit-spade", "Live Casino", "EVO, SEXY, SA…"),
            ("sports.html", "bi-trophy", "Sport / ক্রিকেট", "9W, SABA, CMD…"),
            ("fishing.html", "bi-water", "Fisher", "JILI, JDB, FC…"),
            ("bingo.html", "bi-circle", "Bingo", "R88, JDB, JILI…"),
        ])
        + """
          <h2>জনপ্রিয় / লোকালাইজড টাইটেল (উদাহরণ)</h2>
          <p>Lucky Ace, Fortune Gems 2, SuperAce, Piggy Win, Wild Bandito ইত্যাদি — JILI/JDB/PG/PS কোলাব।</p>
""",
        [("../", "হোম"), ("#", "গেমস")],
        "games",
    )

    games = [
        ("slots.html", "Slots", "JitaWin Slots — JILI PG JDB Providers", "bi-grid-3x3-gap",
         "JILI, JDB, FC, VP, PG, FS, SG, PP, PS, BNG, RT, HB, KA, JOKER, EVOPLAY, RELAX, PLAY8, HS",
         "স্লট সেকশনে ডজনখানেক প্রোভাইডার। ওয়েলকাম/রিবেট অনেক সময় স্লট-কেন্দ্রিক — JILI এক্সক্লুশন কিছু প্রমোতে আছে কিনা চেক করুন।"),
        ("live-casino.html", "Live Casino", "JitaWin Live Casino — Baccarat Dragon Tiger", "bi-suit-spade",
         "EVO, SEXY, HRLIVE, MJ, SA, PT, BETGAMES, EZ, PP, SABA, BG, TVBET",
         "থিম: Baccarat, AndarBahar, DragonTiger, Roulette, SicBo, Poker ইত্যাদি।"),
        ("sports.html", "Sport / Cricket", "JitaWin Cricket &amp; Sports Betting Bangladesh", "bi-trophy",
         "9W, SABA, CMD, DIGITAIN, AP",
         "বাংলাদেশে ক্রিকেট/IPL ডিমান্ড বেশি। স্পোর্টস ওয়েলকাম বোনাস আলাদা টেবিলে — ওয়েজারিং পড়ুন।"),
        ("fishing.html", "Fisher Game", "JitaWin Fishing Games Guide", "bi-water",
         "SG, JOKER, FC, R88, FS, JDB, KA, YB, JILI, PT, PS",
         "ফিশিংয়ের আলাদা ওয়েলকাম/উইকলি বোনাস ক্যাটাগরি থাকতে পারে।"),
        ("bingo.html", "Bingo", "JitaWin Bingo Games", "bi-circle",
         "R88, JDB, KM, YB, JILI",
         "বিঙ্গো ছাড়াও Other Game-এ Crash / Table / Arcade / E-Sport থাকতে পারে।"),
    ]
    for fn, name, title_en, icon, providers, blurb in games:
        page(
            f"games/{fn}",
            f"{title_en}",
            f"JitaWin {name} providers and tips for Bangladesh players. List: {providers[:80]}…",
            f"{name}",
            blurb,
            f"""
          <div class="icon-box mb-3"><i class="bi {icon}" aria-hidden="true"></i></div>
          <h2>প্রোভাইডার তালিকা</h2>
          <p class="text-muted-jw">{providers}</p>
          <p>{blurb}</p>
          <p><a class="btn btn-jw-green" href="{CTA_HOME}" rel="nofollow sponsored noopener" target="_blank">প্ল্যাটফর্মে গেম দেখুন</a></p>
"""
            + exp("গেম «সহজ জয়» গ্যারান্টি দিই না — শুধু ক্যাটাগরি ও প্রোমো ফিট বুঝিয়ে দিই।"),
            [("../", "হোম"), ("index.html", "গেমস"), ("#", name)],
            "games",
        )

    # AFFILIATE
    page(
        "affiliate/index.html",
        "JitaWin Affiliate &amp; Referral — Earn Commission Bangladesh",
        "JitaWin refer friends program: ৳88 referral, daily commission 0.10%/0.05%/0.025%, milestones. How to start.",
        "রেফারেল ও এজেন্ট কমিশন",
        "তিন লেয়ার কমিশন + ৳88 রেফারেল + মাইলস্টোন।",
        cards("", [
            ("commission.html", "bi-percent", "কমিশন স্ট্রাকচার", "0.10% / 0.05% / 0.025% + ৳88"),
            ("how-to-start.html", "bi-rocket-takeoff", "কীভাবে শুরু করবেন", "লিংক, QR, VIP3 শর্ত"),
        ])
        + """
          <h2>এক নজরে</h2>
          <ul>
            <li>Daily commission: Tier1 0.10% · Tier2 0.05% · Tier3 0.025%</li>
            <li>প্রতি সফল রেফার: ৳88 (VIP3+ রেফারার, শর্তসহ, 10x)</li>
            <li>মাইলস্টোন মাসিক রিসেট</li>
          </ul>
""",
        [("../", "হোম"), ("#", "রেফারেল")],
        "affiliate",
    )

    page(
        "affiliate/commission.html",
        "JitaWin Referral Commission Calculator Structure",
        "JitaWin affiliate rates: direct 0.10%, level2 0.05%, level3 0.025%, ৳88 bonus, invite milestones with examples.",
        "কমিশন স্ট্রাকচার ও উদাহরণ",
        "ডেইলি টার্নওভার কমিশন + রেফারেল বোনাস + মাইলস্টোন।",
        toc([("daily", "ডেইলি কমিশন"), ("ref", "৳88 রেফারেল"), ("mile", "মাইলস্টোন"), ("ex", "উদাহরণ")])
        + """
          <h2 id="daily">ডেইলি কমিশন</h2>
          <ul>
            <li>ডাউনলাইনের দৈনিক ভ্যালিড টার্নওভারে রিয়েল-টাইম</li>
            <li>আনলিমিটেড · আলাদা ওয়েজারিং নেই</li>
            <li>ডাউনলাইন দিনে <strong class="text-gold">৳3,000+</strong> ভ্যালিড টার্নওভার হলেই কাউন্ট</li>
            <li>Tier1 Direct <strong class="text-gold">0.10%</strong> · Tier2 <strong class="text-gold">0.05%</strong> · Tier3 <strong class="text-gold">0.025%</strong></li>
          </ul>
          <h2 id="ref">রেফারেল বোনাস ৳88</h2>
          <ul>
            <li>রেফারার: VIP3+</li>
            <li>৭ দিনের মধ্যে: রেফার লিংক/কোডে রেজিস্টার → ডিপোজিট ৳500 → ৳3,000 স্লট ভ্যালিড টার্নওভার → মোবাইল+Email ভেরিফাই</li>
            <li>বোনাস ওয়েজার 10x</li>
          </ul>
          <h2 id="mile">মাইলস্টোন (মাসিক)</h2>
          <div class="table-wrap table-responsive mb-3">
            <table class="table table-jw table-striped mb-0">
              <thead><tr><th>সফল আমন্ত্রণ</th><th>বোনাস</th><th>ওয়েজার</th></tr></thead>
              <tbody>
                <tr><td>5</td><td>৳50</td><td>5x</td></tr>
                <tr><td>20</td><td>৳220</td><td>5x</td></tr>
                <tr><td>50</td><td>৳600</td><td>5x</td></tr>
                <tr><td>100</td><td>৳1,300</td><td>5x</td></tr>
                <tr><td>301+</td><td>৳3,500</td><td>5x</td></tr>
              </tbody>
            </table>
          </div>
          <p class="small text-muted-jw">মাসে শুধু সর্বোচ্চ মাইলস্টোন টিয়ার পেমেন্ট · মাসিক রিসেট।</p>
          <h2 id="ex">দ্রুত উদাহরণ</h2>
          <p>ডাইরেক্ট ডাউনলাইনের একদিনের ভ্যালিড টার্নওভার ৳100,000 → 0.10% = <strong class="text-gold">৳100</strong> ডেইলি কমিশন (শর্ত পূরণ সাপেক্ষে)।</p>
"""
        + exp("কমিশন «গ্যারান্টি আয়» নয় — ডাউনলাইনের রিয়েল প্লে দরকার; স্প্যাম ট্রাফিক ব্যান রিস্ক।"),
        [("../", "হোম"), ("index.html", "রেফারেল"), ("#", "কমিশন")],
        "affiliate",
    )

    page(
        "affiliate/how-to-start.html",
        "How to Start JitaWin Affiliate Referral Promotion",
        "Start JitaWin referral: register, reach VIP3, get referral code QR link, claim bonuses in 30 days.",
        "রেফারেল প্রমোশন কীভাবে শুরু করবেন",
        "লিংক/QR পেতে অ্যাকাউন্ট + শর্ত — সংক্ষিপ্ত রোডম্যাপ।",
        f"""
          <ol>
            <li><a href="{CTA_SIGNUP}" rel="nofollow sponsored noopener" target="_blank">রেজিস্টার</a> করুন</li>
            <li>KYC শেষ করে অ্যাক্টিভ থাকুন — ৳88 বোনাসের জন্য VIP3+ লক্ষ্য</li>
            <li>ব্যাকএন্ডে Referral: কোড, QR, লিংক কপি করুন</li>
            <li>বন্ধু/কনটেন্টে শেয়ার — একই ডিভাইস/IP ডুপ্লিকেট এড়িয়ে</li>
            <li>Notifications/Bonus থেকে <strong class="text-white">৩০ দিনের মধ্যে</strong> ক্লেইম</li>
          </ol>
          <div class="callout callout-gold">Invite Friends Leaderboard ও Bonus Records ট্যাব ব্যাকএন্ডে থাকে। সন্দেহজনক অ্যাকাউন্ট ডিসকোয়ালিফাই হতে পারে।</div>
"""
        + exp("আমি প্রমোটারকে প্রথমে নিজের ছোট ডিপোজিট+KYC শেষ করতে বলি — নাহলে রেফার বোনাস এলিজিবিলিটি বোঝে না।"),
        [("../", "হোম"), ("index.html", "রেফারেল"), ("#", "শুরু")],
        "affiliate",
    )

    # MIRROR
    page(
        "mirror-links/index.html",
        "JitaWin Mirror Links &amp; Working URL Bangladesh 2026",
        "JitaWin alternate domains: jitawin.casino, .cloud, .cc, .win, .vip. Access tips if main site blocked. Not official ISP advice.",
        "লেটেস্ট মিরর / অল্টারনেট URL",
        "মেইন সাইট না খুললে ব্যাকআপ ডোমেইন রেফারেন্স — নিয়মিত আপডেট করতে হতে পারে।",
        f"""
          <p>প্ল্যাটফর্ম ডেটায় উল্লিখিত মিরর/ব্যাকআপ ডোমেইন:</p>
          <ul>
            <li>jitawin.com (প্রাইমারি রেফারেন্স)</li>
            <li>jitawin.casino</li>
            <li>jitawin.cloud</li>
            <li>jitawin.cc</li>
            <li>jitawin.win</li>
            <li>jitawin.vip</li>
          </ul>
          <p>এন্ট্রি/রেজিস্টারের জন্য এই প্রমো সাইটের ট্র্যাকড লিংক ব্যবহার করুন:</p>
          <p>
            <a class="btn btn-gold me-2" href="{CTA_HOME}" rel="nofollow sponsored noopener" target="_blank">ভিজিট লিংক</a>
            <a class="btn btn-jw-green" href="{CTA_SIGNUP}" rel="nofollow sponsored noopener" target="_blank">সাইনআপ লিংক</a>
          </p>
          <div class="callout callout-warn">
            ISP ব্লক/DNS সমস্যা স্থানীয় নেটওয়ার্কভেদে হয়। Cloudflare 1.1.1.1-এর মতো পাবলিক DNS কিছু ইউজার ব্যবহার করে — এটি সাধারণ নেটওয়ার্ক টিপস, আইন লঙ্ঘনের পরামর্শ নয়। স্থানীয় আইন মেনে চলুন।
          </div>
          <p class="small text-muted-jw">এই পেজের ডোমেইন তালিকা প্ল্যাটফর্ম তথ্যসূত্র অনুযায়ী; লাইভ অ্যাভেইলেবিলিটি পরিবর্তন হতে পারে।</p>
"""
        + exp("মিরর লিংক শেয়ারের সময় ফিশিং ডোমেইন এড়াতে অফিসিয়াল স্পেলিং ডাবল-চেক করি।"),
        [("../", "হোম"), ("#", "মিরর লিংক")],
        "",
    )

    # FAQ
    page(
        "faq/index.html",
        "JitaWin FAQ Bangladesh — Deposit Withdraw App License",
        "Frequently asked questions about JitaWin for Bangladesh: safety, bKash limits, withdrawal rejects, PWA app, referral commission.",
        "সচরাচর জিজ্ঞাসিত প্রশ্ন (FAQ)",
        "নিরাপত্তা, পেমেন্ট, উইথড্র, App, রেফারেল — এক পেজে।",
        """
          <div class="accordion accordion-jw" id="faqPage">
            <div class="accordion-item">
              <h2 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">JitaWin কি সেফ? লাইসেন্স কী?</button></h2>
              <div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqPage"><div class="accordion-body">Altervance Ltd. · লাইসেন্স ALSI-142311014 (Anjouan, Comoros)। বিস্তারিত: <a href="../about-jitawin/license-safety.html">লাইসেন্স পেজ</a>।</div></div>
            </div>
            <div class="accordion-item">
              <h2 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">মিনিমাম ডিপোজিট কত?</button></h2>
              <div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqPage"><div class="accordion-body">সাধারণত ৳১০০। bKash ৳100–25k, Nagad ৳100–50k, Rocket ৳100–30k, ফি Max +1%।</div></div>
            </div>
            <div class="accordion-item">
              <h2 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">উইথড্র কেন আটকে?</button></h2>
              <div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqPage"><div class="accordion-body">KYC, ওয়েজারিং, অ্যাকাউন্ট মিসম্যাচ। <a href="../payment/withdrawal-faq.html">উইথড্র FAQ</a> দেখুন।</div></div>
            </div>
            <div class="accordion-item">
              <h2 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">App কি APK?</button></h2>
              <div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqPage"><div class="accordion-body">না — PWA। w01.jitawin.com থেকে Install/Add to Home Screen। <a href="../guide/app-download.html">App গাইড</a>।</div></div>
            </div>
            <div class="accordion-item">
              <h2 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">রেফারেল কমিশন?</button></h2>
              <div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqPage"><div class="accordion-body">0.10% / 0.05% / 0.025% + ৳88 শর্তসহ। <a href="../affiliate/commission.html">কমিশন পেজ</a>।</div></div>
            </div>
            <div class="accordion-item">
              <h2 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">সাইট না খুললে?</button></h2>
              <div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqPage"><div class="accordion-body">মিরর ডোমেইন তালিকা: <a href="../mirror-links/">মিরর লিংক</a>। এন্ট্রিতে ট্র্যাকড লিংক ব্যবহার করুন।</div></div>
            </div>
          </div>
"""
        + exp("FAQ-তে শুধু যাচাইকৃত নিয়ম রাখি; কাস্টমার সাপোর্ট সময়সূচি এখনো নিশ্চিত নয় — অনুমান করে লিখি না।"),
        [("../", "হোম"), ("#", "FAQ")],
        "faq",
    )

    # RESPONSIBLE
    page(
        "responsible-gambling/index.html",
        "Responsible Gambling — JitaWin Bangladesh Guide 18+",
        "Responsible gambling statement for JitaWin affiliate guide: 18+ only, limits, help mindset for Bangladeshi players.",
        "দায়িত্বশীল গেমিং (Responsible Gambling)",
        "১৮+ · বিনোদন বাজেট · সমস্যা হলে থামুন।",
        """
          <h2>মূল নীতি</h2>
          <ul>
            <li>শুধু <strong class="text-white">১৮ বছর+</strong></li>
            <li>হারাতে পারবেন এমন টাকাই খেলুন</li>
            <li>লোন/প্রয়োজনীয় খরচের টাকা দিয়ে খেলবেন না</li>
            <li>সময় ও লস লিমিট নিজে সেট করুন</li>
            <li>জিততে «পুনরুদ্ধার» করতে গিয়ে বারবার ডিপোজিট করবেন না</li>
          </ul>
          <h2>সতর্ক সংকেত</h2>
          <ul>
            <li>পরিবার/কাজ লুকিয়ে খেলা</li>
            <li>ঋণ করে ডিপোজিট</li>
            <li>থামাতে না পারা</li>
          </ul>
          <div class="callout callout-warn">সমস্যা মনে হলে অ্যাকাউন্ট বন্ধ/ব্রেক নিন এবং স্থানীয় সহায়তা খুঁজুন। এই সাইট থেরাপি বা ক্রাইসিস হটলাইন নয়।</div>
          <p>প্ল্যাটফর্ম টুলস (লিমিট/সেলফ-এক্সক্লুশন) থাকলে অ্যাকাউন্ট সেটিংসে খুঁজুন — অপশন অপারেটর UI অনুযায়ী ভিন্ন হতে পারে।</p>
"""
        + exp("কনটেন্টে আমি রোমাঞ্চ দেখাই, কিন্তু সবসময় ১৮+ ও বাজেট রিমাইন্ডার রাখি — দীর্ঘমেয়াদি ট্রাস্টের জন্য জরুরি।"),
        [("../", "হোম"), ("#", "Responsible")],
        "",
    )

    # DISCLAIMER
    page(
        "disclaimer/index.html",
        "Disclaimer — Independent JitaWin Affiliate Content Site",
        "This website is a third-party affiliate content site about JitaWin, not the official operator or customer support.",
        "ডিসক্লেইমার ও সাইট পরিচিতি",
        "আমরা কে · কী করি না · ঝুঁকি সতর্কতা।",
        f"""
          <h2>এই সাইট কী</h2>
          <p>এটি <strong class="text-white">তৃতীয় পক্ষের এজেন্ট/অ্যাফিলিয়েট কনটেন্ট ও রিভিউ গাইড</strong>। উদ্দেশ্য: বাংলাদেশি পাঠককে JitaWin সম্পর্কে তথ্য দিয়ে রেজিস্টার লিংকে পাঠানো।</p>
          <h2>এই সাইট কী নয়</h2>
          <ul>
            <li>JitaWin অফিসিয়াল ওয়েবসাইট নয়</li>
            <li>ডিপোজিট/উইথড্র/ওয়ালেট অপারেট করে না</li>
            <li>অফিসিয়াল কাস্টমার সাপোর্ট নয়</li>
            <li>জয়/আয়ের গ্যারান্টি দেয় না</li>
          </ul>
          <h2>অ্যাফিলিয়েট লিংক</h2>
          <p>CTA বাটন ট্র্যাকড এন্ট্রি ব্যবহার করে:</p>
          <ul>
            <li><code>{CTA_HOME}</code></li>
            <li><code>go/</code> → <code>{CTA_SIGNUP_FINAL}</code></li>
          </ul>
          <h2>তথ্যের সঠিকতা</h2>
          <p>বোনাস, লিমিট, VIP সংখ্যা পরিবর্তন হতে পারে। চূড়ান্ত নিয়ম প্ল্যাটফর্মের লাইভ T&amp;C।</p>
          <h2>আইন ও বয়স</h2>
          <p>১৮+। আপনার স্থানীয় আইন মেনে ব্যবহার করুন। অনলাইন বেটিং ঝুঁকিপূর্ণ।</p>
"""
        + exp("প্রথম পরিচয়েই বলি: আমি অফিসিয়াল সাপোর্ট নই — এতে পরে কম অভিযোগ ও বেশি ট্রাস্ট হয়।"),
        [("../", "হোম"), ("#", "ডিসক্লেইমার")],
        "",
    )

    print("done")


if __name__ == "__main__":
    build_all()

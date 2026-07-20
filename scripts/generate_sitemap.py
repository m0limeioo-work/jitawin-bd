#!/usr/bin/env python3
"""Generate sitemap.xml from HTML pages using site.config.json siteBase."""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def site_base() -> str:
    cfg = ROOT / "site.config.json"
    if cfg.exists():
        return str(json.loads(cfg.read_text(encoding="utf-8")).get("siteBase", "")).rstrip("/")
    return "https://jitaacewin.com"

def meta(rel: str):
    if rel == "index.html":
        return "1.0", "weekly"
    if rel.endswith("/index.html") and rel.count("/") == 1:
        return "0.9", "weekly"
    if rel.startswith(("guide/", "payment/", "promotions/", "faq/", "mirror-links/")):
        return "0.8", "weekly"
    if rel.startswith(("about-jitawin/", "affiliate/", "games/")):
        return "0.7", "monthly"
    if rel in ("disclaimer/index.html", "responsible-gambling/index.html"):
        return "0.5", "yearly"
    return "0.6", "monthly"

def page_url(base: str, rel: str) -> str:
    if rel == "index.html":
        return base + "/"
    if rel.endswith("/index.html"):
        return base + "/" + rel[: -len("index.html")]
    return base + "/" + rel

def main() -> None:
    base = site_base()
    today = date.today().isoformat()
    urls = []
    for p in sorted(ROOT.rglob("*.html")):
        if "prompt" in p.parts:
            continue
        # Skip affiliate hop / noindex utility pages
        if "go" in p.parts and p.name == "index.html" and p.parent.name == "go":
            continue
        urls.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    urls.sort(key=lambda r: (0 if r == "index.html" else 1, r))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel in urls:
        pri, freq = meta(rel)
        lines += [
            "  <url>",
            f"    <loc>{page_url(base, rel)}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>\n")
    out = ROOT / "sitemap.xml"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({len(urls)} URLs) base={base}")

if __name__ == "__main__":
    main()

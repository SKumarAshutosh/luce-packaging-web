#!/usr/bin/env python3
"""
Lucè Packaging — static site builder.

    python build.py            build the site into docs/
    python build.py --serve    build, then serve it at http://localhost:8000
    python build.py --watch    rebuild automatically whenever a file changes
    python build.py --dns      just print the DNS records for your domain

Everything the site says comes from config.py and content.py. This script
renders the Jinja2 templates over that data and writes plain HTML — so the
output is a normal static site that GitHub Pages can host for free.
"""

from __future__ import annotations

import argparse
import http.server
import json
import shutil
import socketserver
import sys
import time
from datetime import date
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
    from markupsafe import Markup
except ImportError:
    sys.exit(
        "Jinja2 is missing. Install it with:\n\n    python -m pip install -r requirements.txt\n"
    )

import config
import content

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / config.OUTPUT_DIR

# GitHub Pages' apex-domain IPs. Stable, but if a domain ever fails to verify,
# check https://docs.github.com/pages for the current set.
GH_PAGES_IPS = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]
GH_PAGES_IPV6 = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def whatsapp_is_valid() -> bool:
    """A usable wa.me number is 10-15 digits and nothing else."""
    wa = config.WHATSAPP or ""
    return wa.isdigit() and 10 <= len(wa) <= 15


def whatsapp_link() -> str:
    """Chat link, or a fallback to the quote form if no number is set yet."""
    return f"https://wa.me/{config.WHATSAPP}" if whatsapp_is_valid() else "#quote"


def json_script(data, indent=None) -> Markup:
    """
    Serialise `data` for embedding inside a <script> tag.

    Returned as Markup because autoescape is on — without this the quotes come
    out as &#34; which is a JavaScript syntax error, and invalid JSON-LD.

    `</` is escaped to `<\\/` (valid inside a JSON string) so a value can never
    close the surrounding script tag early.
    """
    text = json.dumps(data, ensure_ascii=False, indent=indent)
    return Markup(text.replace("</", "<\\/"))


def build_json_ld() -> Markup:
    """LocalBusiness structured data, so Google can read the business details."""
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": config.COMPANY_NAME,
        "url": f"{config.base_url()}/",
        "description": config.SITE_DESCRIPTION,
        "image": f"{config.base_url()}/{config.OG_IMAGE}",
        "telephone": config.PHONE_DIAL,
        "email": config.EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": config.ADDRESS["street"],
            "addressLocality": config.ADDRESS["city"],
            "addressRegion": config.ADDRESS["state"],
            "postalCode": config.ADDRESS["pincode"],
            "addressCountry": config.ADDRESS["country"],
        },
        "openingHours": config.OPENING_HOURS_SCHEMA,
    }
    return json_script(data, indent=2)


def build_js_config() -> Markup:
    """
    The subset of config the browser script needs, as a JSON literal.

    Only what the WhatsApp/email composer actually uses — everything else is
    already rendered into the HTML, so it never has to be duplicated here.
    """
    return json_script(
        {
            "whatsapp": config.WHATSAPP,
            "email": config.EMAIL,
            "company": config.COMPANY_NAME,
            "waValid": whatsapp_is_valid(),
        }
    )


def active_social() -> list[tuple[str, str]]:
    """Only the social links that have actually been filled in."""
    names = {"instagram": "insta", "linkedin": "linkedin", "facebook": "facebook"}
    return [
        (names[key], url)
        for key, url in config.SOCIAL.items()
        if url and key in names
    ]


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,          # escape by default; opt out with |safe
        undefined=StrictUndefined,  # a typo in a template is an error, not a blank
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    return env


def shared_context() -> dict:
    """Values every page needs."""
    return {
        "cfg": config,
        "base_url": config.base_url(),
        "year": date.today().year,
        "nav": content.NAV,
        "footer_tagline": content.FOOTER_TAGLINE,
        "footer_columns": content.FOOTER_COLUMNS,
        "social": active_social(),
        "wa_link": whatsapp_link(),
        "wa_valid": whatsapp_is_valid(),
        "js_config": build_js_config(),
        "home_href": "#top",
    }


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def copy_static() -> int:
    """Mirror static/ into the output folder. Returns the file count."""
    dest = OUT / "static"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(STATIC, dest)
    return sum(1 for p in dest.rglob("*") if p.is_file())


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" keeps the output identical on Windows and Linux, so git
    # doesn't report churn just because the build ran on a different machine.
    path.write_text(text, encoding="utf-8", newline="\n")


def build() -> None:
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    env = make_env()
    ctx = shared_context()

    # ---- index.html ----
    index_ctx = {
        **ctx,
        "page_path": "",
        "json_ld": build_json_ld(),
        "hero": content.HERO,
        "stats": content.STATS,
        "marquee": content.MARQUEE,
        "products_intro": content.PRODUCTS_INTRO,
        "products": content.PRODUCTS,
        "specs_intro": content.SPECS_INTRO,
        "spec_columns": content.SPEC_COLUMNS,
        "spec_rows": content.SPEC_ROWS,
        "spec_notes": content.SPEC_NOTES,
        "capability_intro": content.CAPABILITY_INTRO,
        "features": content.FEATURES,
        "process_intro": content.PROCESS_INTRO,
        "steps": content.STEPS,
        "about": content.ABOUT,
        "faq_intro": content.FAQ_INTRO,
        "faqs": content.FAQS,
        "quote_intro": content.QUOTE_INTRO,
        "product_options": content.PRODUCT_OPTIONS,
        "ply_options": content.PLY_OPTIONS,
    }
    write(OUT / "index.html", env.get_template("index.html").render(**index_ctx))

    # ---- 404.html ----
    write(
        OUT / "404.html",
        env.get_template("404.html").render(**{**ctx, "page_path": "404.html",
                                               "home_href": "index.html"}),
    )

    # ---- static assets ----
    asset_count = copy_static()

    # ---- robots.txt ----
    write(
        OUT / "robots.txt",
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {config.base_url()}/sitemap.xml\n",
    )

    # ---- sitemap.xml ----
    write(
        OUT / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url>\n"
        f"    <loc>{config.base_url()}/</loc>\n"
        f"    <lastmod>{date.today().isoformat()}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>1.0</priority>\n"
        "  </url>\n"
        "</urlset>\n",
    )

    # ---- .nojekyll — stops GitHub Pages running the output through Jekyll ----
    write(OUT / ".nojekyll", "")

    # ---- CNAME — only when a custom domain is configured ----
    cname = OUT / "CNAME"
    if config.DOMAIN:
        write(cname, f"{config.DOMAIN}\n")
    elif cname.exists():
        # Domain was removed from config; don't leave a stale file behind.
        cname.unlink()

    elapsed = (time.perf_counter() - started) * 1000
    print(f"  Built {config.OUTPUT_DIR}/ in {elapsed:.0f} ms")
    print(f"    index.html, 404.html, robots.txt, sitemap.xml, .nojekyll")
    print(f"    {asset_count} static files")
    print(f"    base URL: {config.base_url()}")
    if config.DOMAIN:
        print(f"    CNAME: {config.DOMAIN}")
    else:
        print("    CNAME: not written (config.DOMAIN is None)")
    if not whatsapp_is_valid():
        print("\n  ! config.WHATSAPP is not a valid number yet, so the chat")
        print("    buttons fall back to the quote form instead of opening a")
        print("    broken wa.me link. Set it in config.py.")


# ---------------------------------------------------------------------------
# serve / watch
# ---------------------------------------------------------------------------

def serve(port: int = 8000) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(OUT), **kw)

        def end_headers(self):
            # Never cache during development, so a rebuild always shows up.
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def log_message(self, fmt, *args):
            pass  # keep the console readable

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\n  Serving {config.OUTPUT_DIR}/ at http://localhost:{port}")
        print("  Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Stopped.")


def watched_files() -> list[Path]:
    paths = [ROOT / "config.py", ROOT / "content.py", ROOT / "build.py"]
    paths += sorted(TEMPLATES.rglob("*.html"))
    paths += [p for p in STATIC.rglob("*") if p.is_file()]
    return paths


def watch() -> None:
    """Poll for changes and rebuild. No extra dependency needed."""
    def snapshot() -> dict[Path, float]:
        return {p: p.stat().st_mtime for p in watched_files() if p.exists()}

    print("  Watching for changes. Press Ctrl+C to stop.\n")
    last = snapshot()
    try:
        while True:
            time.sleep(0.6)
            now = snapshot()
            if now != last:
                changed = [
                    p.relative_to(ROOT)
                    for p in set(now) | set(last)
                    if now.get(p) != last.get(p)
                ]
                print(f"  Changed: {', '.join(str(c) for c in changed[:4])}")
                try:
                    build()
                except Exception as err:  # keep watching after a template typo
                    print(f"  Build failed: {err}")
                print()
                last = now
    except KeyboardInterrupt:
        print("\n  Stopped watching.")


# ---------------------------------------------------------------------------
# DNS helper
# ---------------------------------------------------------------------------

def print_dns() -> None:
    if not config.DOMAIN:
        print("\n  config.DOMAIN is None - set your domain in config.py first.\n")
        return

    domain = config.DOMAIN
    apex = domain[4:] if domain.startswith("www.") else domain
    gh = f"{config.GITHUB_USER}.github.io"

    print(f"\n  === DNS records for {domain} ===\n")
    print("  Type    Name    Value")
    print("  ----    ----    -----")
    for ip in GH_PAGES_IPS:
        print(f"  A       @       {ip}")
    print(f"  CNAME   www     {gh}")
    print("\n  Optional (IPv6):")
    for ip in GH_PAGES_IPV6:
        print(f"  AAAA    @       {ip}")
    print(f"\n  Delete any existing A / CNAME records on '@' first - parking-page")
    print("  records left in place will stop the domain resolving.\n")
    print("  Then:")
    print("    1. git add -A && git commit -m \"Point site at "
          f"{apex}\" && git push")
    print(f"    2. GitHub repo -> Settings -> Pages -> Custom domain -> {domain}")
    print("    3. Once the DNS check passes, tick 'Enforce HTTPS'\n")


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        # ASCII only: this is printed by --help, and the Windows console
        # codepage mangles accented characters.
        description="Build the Luce Packaging site.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--serve", action="store_true",
                        help="build, then serve the output locally")
    parser.add_argument("--watch", action="store_true",
                        help="rebuild whenever a source file changes")
    parser.add_argument("--port", type=int, default=8000,
                        help="port for --serve (default 8000)")
    parser.add_argument("--dns", action="store_true",
                        help="print the DNS records for your domain and exit")
    args = parser.parse_args()

    if args.dns:
        print_dns()
        return

    print()
    build()

    if args.watch:
        print()
        watch()
    elif args.serve:
        serve(args.port)
    else:
        print(f"\n  Preview it with:  python build.py --serve\n")


if __name__ == "__main__":
    main()

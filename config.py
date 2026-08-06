"""
Lucè Packaging — site configuration.

▶ THIS IS THE ONLY FILE YOU NEED TO EDIT to put your real details live.

Everything else (the pages, the WhatsApp button, the CNAME file, robots.txt,
sitemap.xml, the Google structured data) is generated from the values below,
so you change each detail exactly once and then run:

    python build.py
"""

# ---------------------------------------------------------------------------
# CONTACT DETAILS
# ---------------------------------------------------------------------------

# WhatsApp number in FULL INTERNATIONAL FORM — country code + number,
# digits only. No "+", no spaces, no dashes.
# India example: 91 followed by the 10-digit number.
WHATSAPP = "919999999999"

# How the phone number should be *displayed* on the page.
PHONE_DISPLAY = "+91 99999 99999"

# What the call button should actually dial.
PHONE_DIAL = "+919999999999"

EMAIL = "hello@luce-packaging.com"

# ---------------------------------------------------------------------------
# BUSINESS DETAILS
# ---------------------------------------------------------------------------

COMPANY_NAME = "Lucè Packaging"
COMPANY_SHORT = "Lucè"

ADDRESS = {
    "street": "Plot No. 00, Industrial Area",
    "city": "Your City",
    "state": "Your State",
    "pincode": "000000",
    "country": "IN",
}

# One-line address used in the top bar and footer.
ADDRESS_LINE = "Plot No. 00, Industrial Area, Your City"

OPENING_HOURS_TEXT = "Mon – Sat, 9:30 am – 6:30 pm"
OPENING_HOURS_SCHEMA = "Mo-Sa 09:30-18:30"

# Your GSTIN. Set to None to hide the line entirely.
GSTIN = "00AAAAA0000A1Z0"

# Line under the quote in the About section.
FOUNDER_LINE = "Founder, Lucè Packaging"

# ---------------------------------------------------------------------------
# DOMAIN / HOSTING
# ---------------------------------------------------------------------------

# Your custom domain, WITHOUT https:// and WITHOUT a trailing slash.
#   e.g. "lucepackaging.com"
#
# Leave as None until you have one — the site still builds and works, it just
# won't emit a CNAME file and the sitemap will use GITHUB_PAGES_URL instead.
DOMAIN = 'lucepackagingsolutions.com'

# Your GitHub username and repo name. Used for the DNS instructions build.py
# prints, and — while DOMAIN is None — to build GITHUB_PAGES_URL below, which
# every canonical / sitemap / Open Graph URL is derived from. Get these wrong
# and those URLs point at a page that doesn't exist.
GITHUB_USER = "SKumarAshutosh"
GITHUB_REPO = "luce-packaging-web"

# Fallback address used when DOMAIN is None.
GITHUB_PAGES_URL = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}"


def base_url() -> str:
    """The site's canonical root URL, no trailing slash."""
    if DOMAIN:
        return f"https://{DOMAIN}"
    return GITHUB_PAGES_URL


def asset_prefix() -> str:
    """
    Path prefix for static files.

    On a custom domain the site sits at the root, so plain relative paths are
    correct. On github.io/<repo>/ they are also correct, because every page is
    generated at the top level of the output folder. Kept as a function so
    there is one obvious place to change if you ever nest pages in folders.
    """
    return ""


# ---------------------------------------------------------------------------
# SOCIAL LINKS — set any to None to hide that icon
# ---------------------------------------------------------------------------

SOCIAL = {
    "instagram": None,
    "linkedin": None,
    "facebook": None,
}

# ---------------------------------------------------------------------------
# SEO
# ---------------------------------------------------------------------------

SITE_TITLE = "Lucè — Corrugated Boxes & Premium Packaging Manufacturer"

SITE_DESCRIPTION = (
    "Lucè manufactures corrugated boxes, printed premium cartons, sheets, "
    "partitions and custom die-cut packaging. 3-ply to 7-ply, made to your "
    "exact size and strength."
)

SITE_KEYWORDS = (
    "corrugated box manufacturer, 5 ply boxes, printed cartons, "
    "die cut mailer, packaging sheets, partitions, export packaging"
)

OG_TITLE = "Lucè — Corrugated Boxes & Premium Packaging"
OG_DESCRIPTION = (
    "Corrugated boxes, printed premium cartons and custom die-cut packaging. "
    "Built to your size, strength and brand."
)

# Social scrapers cannot render SVG, so this points at a PNG you export from
# static/img/og-image.svg (1200×630). See the README.
OG_IMAGE = "static/img/og-image.png"

# ---------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------

# GitHub Pages can serve straight from a /docs folder on your main branch,
# which means no CI and no second branch to manage.
OUTPUT_DIR = "docs"

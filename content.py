"""
Lucè Packaging — page content.

All the words and numbers on the site live here as plain Python data. Add a
product by appending a dict to PRODUCTS; add an FAQ by appending to FAQS. No
HTML editing needed — run `python build.py` and the pages regenerate.

`amp=True` on a heading tells the template to render its "&" in the body font.
Fraunces turns the ampersand into a decorative swash at display sizes, which
reads as a symbol rather than an "&", so headings opt out of it.
"""

# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------

NAV = [
    ("Products", "#products"),
    ("Specifications", "#specs"),
    ("Capabilities", "#capability"),
    ("Process", "#process"),
    ("About", "#about"),
]

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------

HERO = {
    "eyebrow": "Corrugated & Premium Packaging",
    "heading": "Packaging that protects your product —",
    "heading_em": "and your brand.",
    "lede": (
        "Lucè manufactures corrugated boxes from 3-ply to 7-ply, high-finish "
        "printed cartons, sheets, partitions and custom die-cut packs. Every "
        "box is made to your exact dimensions, load rating and artwork."
    ),
    "ticks": [
        "Custom sizes, no fixed moulds",
        "Bulk & MOQ-friendly",
        "Recyclable kraft stock",
    ],
}

# ⚠️ PLACEHOLDER NUMBERS — replace with your real figures before going live.
# `count` is what the number animates up to; `suffix` is appended after it.
STATS = [
    {"label": "Years in packaging", "count": 12, "suffix": "+"},
    {"label": "Boxes produced yearly", "count": 20, "suffix": "L+"},
    {"label": "Ply options", "count": 7, "prefix": "3–", "suffix": ""},
    {"label": "Quote turnaround", "count": 24, "suffix": "h"},
]

MARQUEE = [
    "E-commerce fulfilment",
    "Food & beverage",
    "Pharma & healthcare",
    "Textile & apparel",
    "Electronics",
    "Auto components",
    "Agri & horticulture",
    "Export cargo",
]

# ---------------------------------------------------------------------------
# PRODUCTS
# ---------------------------------------------------------------------------

PRODUCTS_INTRO = {
    "eyebrow": "Our Range",
    "heading": "Four product families, one standard of finish",
    "sub": (
        "Whether you ship 200 units a month or 2 lakh, we tool the job to your "
        "spec — dimensions, ply, print and bursting strength."
    ),
}

PRODUCTS = [
    {
        "tag": "Core line",
        "title": "Corrugated Boxes: 3, 5 & 7 Ply",
        "image": "prod-corrugated.svg",
        "alt": "Stacked plain corrugated shipping cartons in kraft brown",
        "body": (
            "Regular slotted cartons (RSC) and full-overlap boxes for shipping, "
            "storage and transit. The workhorse of any supply chain."
        ),
        "points": [
            "3-ply for light retail & inner packs",
            "5-ply for e-commerce & general freight",
            "7-ply for heavy, dense or export loads",
        ],
    },
    {
        "tag": "Premium",
        "title": "Printed & Laminated Boxes",
        "image": "prod-printed.svg",
        "alt": "Multi-colour printed premium gift and mailer boxes",
        "body": (
            "Offset-laminated and flexo-printed cartons where the box <em>is</em> "
            "the packaging. Retail shelf, D2C unboxing, gifting."
        ),
        "points": [
            "Up to 4-colour offset lamination",
            "Matt / gloss BOPP, spot UV, foiling",
            "Rigid gift boxes & e-commerce mailers",
        ],
    },
    {
        "tag": "Protection",
        "title": "Sheets, Partitions & Trays",
        "image": "prod-sheets.svg",
        "alt": "Corrugated sheets, partition dividers and layer pads",
        "body": (
            "Inner protection that stops damage before it starts — the cheapest "
            "insurance in your BOM."
        ),
        "points": [
            "Corrugated rolls, sheets & layer pads",
            "Slotted partitions & cell dividers",
            "Fruit, bottle & component trays",
        ],
    },
    {
        "tag": "Bespoke",
        "title": "Custom Die-Cut & Specialty",
        "image": "prod-diecut.svg",
        "alt": "Custom die-cut mailer box shown flat and assembled",
        "body": (
            "Odd shapes, tight tolerances, awkward loads. Send a drawing or a "
            "sample — we'll build the die."
        ),
        "points": [
            "Die-cut mailers & tuck-top boxes",
            "Telescopic & heavy-duty export cases",
            "ISPM-compliant & edge-protected packs",
        ],
    },
]

# ---------------------------------------------------------------------------
# SPECIFICATIONS
# ---------------------------------------------------------------------------

SPECS_INTRO = {
    "eyebrow": "Specifications",
    "heading": "Pick the ply, we'll match the strength",
    "sub": (
        "Indicative ranges below. Final GSM and bursting strength are set "
        "against your actual load, stacking height and transit route."
    ),
}

SPEC_COLUMNS = [
    "Construction",
    "Best suited for",
    "Bursting strength",
    "Board GSM",
    "Safe load",
]

# Check these against what your plant actually produces.
SPEC_ROWS = [
    {
        "ply": "3 Ply",
        "ply_class": "ply-chip--3",
        "cells": [
            "Inner cartons, light retail, courier packs",
            "8 – 12 kg/cm²",
            "120 – 180",
            "up to 10 kg",
        ],
    },
    {
        "ply": "5 Ply",
        "ply_class": "ply-chip--5",
        "cells": [
            "E-commerce, FMCG, general freight",
            "14 – 20 kg/cm²",
            "180 – 250",
            "10 – 25 kg",
        ],
    },
    {
        "ply": "7 Ply",
        "ply_class": "ply-chip--7",
        "cells": [
            "Industrial, dense goods, export cargo",
            "20 – 32 kg/cm²",
            "250 – 400",
            "25 – 50 kg",
        ],
    },
]

SPEC_NOTES = [
    {
        "title": "Flute profiles",
        "body": (
            "A, B, C and E-flute available. E-flute for fine print and slim "
            "retail packs, C-flute for cushioning, B for stacking rigidity."
        ),
    },
    {
        "title": "Paper grades",
        "body": (
            "Kraft, semi-kraft, golden yellow, natural shade and virgin "
            "white-top liners. Water-resistant coating on request."
        ),
    },
    {
        "title": "Testing",
        "body": (
            "Bursting strength, GSM, cobb value and box compression checked per "
            "batch. Test certificates issued with dispatch."
        ),
    },
]

# ---------------------------------------------------------------------------
# CAPABILITIES
# ---------------------------------------------------------------------------

CAPABILITY_INTRO = {
    "eyebrow": "Why Lucè",
    "heading": "Small enough to care, equipped enough to deliver",
}

# `icon` maps to a named SVG in templates/macros.html
FEATURES = [
    {
        "icon": "box",
        "title": "Made to your millimetre",
        "body": (
            "No catalogue-only sizing. Give us L×B×H and we cut the board to it, "
            "so you stop paying to ship air."
        ),
    },
    {
        "icon": "clock",
        "title": "Quotes in 24 hours",
        "body": (
            "Send specs or a photo of your current box. You get a costed quote "
            "with ply recommendation the next working day."
        ),
    },
    {
        "icon": "shield",
        "title": "Batch-tested quality",
        "body": (
            "Every lot is checked for GSM and bursting strength before it leaves "
            "the floor. Rejections are our problem, not yours."
        ),
    },
    {
        "icon": "factory",
        "title": "In-house, end to end",
        "body": (
            "Corrugation, printing, die-cutting, stitching and pasting under one "
            "roof — fewer handoffs, tighter timelines."
        ),
    },
    {
        "icon": "leaf",
        "title": "100% recyclable stock",
        "body": (
            "Kraft board, starch-based adhesive, water-based inks. Fully "
            "recyclable and compliant with plastic-free mandates."
        ),
    },
    {
        "icon": "chart",
        "title": "Scales with your volume",
        "body": (
            "Trial runs to standing monthly schedules. Buffer stock held on "
            "request so a spike in orders never stalls dispatch."
        ),
    },
]

# ---------------------------------------------------------------------------
# PROCESS
# ---------------------------------------------------------------------------

PROCESS_INTRO = {
    "eyebrow": "How it works",
    "heading": "From enquiry to loaded truck in five steps",
}

STEPS = [
    {
        "title": "Share your requirement",
        "body": (
            "Dimensions, monthly quantity, what goes inside and how it travels. "
            "A photo of your current box works too."
        ),
    },
    {
        "title": "Spec & quote",
        "body": (
            "We recommend ply, flute and GSM for your load, then send a "
            "transparent per-piece price with slabs."
        ),
    },
    {
        "title": "Sample approval",
        "body": (
            "A physical sample — and a print proof if artwork is involved — "
            "signed off by you before bulk starts."
        ),
    },
    {
        "title": "Production & QC",
        "body": (
            "Scheduled run with in-line checks on creasing, pasting and "
            "strength. Test report attached to the batch."
        ),
    },
    {
        "title": "Dispatch",
        "body": (
            "Bundled, strapped and loaded to your dock or transporter, with "
            "repeat schedules set up on request."
        ),
    },
]

# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------

ABOUT = {
    "eyebrow": "About Lucè",
    "heading": "A packaging partner, not just a box supplier",
    "paragraphs": [
        "Lucè was built on a simple observation: most businesses overpay for "
        "packaging that still doesn't fit. Boxes too big, board too thin, "
        "artwork printed off-register — and no one on the other end of the phone.",
        "We do it differently. You talk to the people who run the machines. We "
        "right-size the box to your product, pick board that survives your "
        "actual transit route, and hold the quality line batch after batch.",
        "The name means <em>light</em> — and that's the intent behind the mark: "
        "clear pricing, clear specs, clear commitments.",
    ],
    "points": [
        ("Right-sized", "cut freight and warehousing cost per unit"),
        ("Consistent", "same spec on order one and order fifty"),
        ("Responsive", "one point of contact, start to finish"),
    ],
    "quote": (
        "Get the box right and everything downstream gets cheaper — freight, "
        "storage, damages, returns. That's the whole job."
    ),
    "minis": [
        ("Recyclable", "Kraft & water-based inks"),
        ("Custom", "Any L × B × H"),
        ("Tested", "Per-batch certificates"),
        ("Local", "Direct factory pricing"),
    ],
}

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------

FAQ_INTRO = {
    "eyebrow": "Questions",
    "heading": "Straight answers before you enquire",
}

FAQS = [
    {
        "q": "What is your minimum order quantity?",
        "a": (
            "It depends on the size and whether printing is involved. Plain "
            "corrugated boxes start low, printed cartons need a larger run to "
            "justify plate and die costs. Tell us your monthly volume and we'll "
            "tell you honestly whether it's viable — or suggest a cheaper route."
        ),
    },
    {
        "q": "Can you match a box I'm already buying?",
        "a": (
            "Yes. Send a photo with a measuring tape across the length, or "
            "courier a sample. We'll reverse-engineer the size, ply and board "
            "grade and quote against it like-for-like."
        ),
    },
    {
        "q": "How long does an order take?",
        "a": (
            "Plain repeat orders typically dispatch within a few working days of "
            "confirmation. First-time printed jobs take longer because of "
            "die-making and proofing. You get a committed date with the quote, "
            "not a vague estimate."
        ),
    },
    {
        "q": "Do you supply printed boxes in small quantities?",
        "a": (
            "For low volumes we usually suggest a plain box with a single-colour "
            "flexo print or a printed label — you get branding without paying "
            "for offset lamination setup. We'll walk you through the cost "
            "difference."
        ),
    },
    {
        "q": "Which ply should I choose?",
        "a": (
            "Rough guide: under 10 kg and travelling short distances, 3-ply. "
            "E-commerce or general freight, 5-ply. Heavy, dense or export, "
            "7-ply. Stacking height matters as much as weight — share both and "
            "we'll spec it properly."
        ),
    },
    {
        "q": "Do you deliver outside your city?",
        "a": (
            "Yes, through transporters for bulk consignments. Freight is quoted "
            "separately and transparently so you can compare against your own "
            "logistics."
        ),
    },
]

# ---------------------------------------------------------------------------
# QUOTE FORM
# ---------------------------------------------------------------------------

QUOTE_INTRO = {
    "eyebrow": "Get a quote",
    "heading": "Tell us about your box",
    "lede": (
        "Fill this in and it opens a ready-to-send WhatsApp message — or email, "
        "if you prefer. No forms lost in a spam folder."
    ),
}

PRODUCT_OPTIONS = [
    "Corrugated boxes (3 / 5 / 7 ply)",
    "Printed & laminated premium boxes",
    "Sheets, partitions & trays",
    "Custom die-cut / specialty",
    "Not sure — need advice",
]

PLY_OPTIONS = ["Recommend for me", "3 Ply", "5 Ply", "7 Ply"]

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------

FOOTER_TAGLINE = (
    "Corrugated boxes, premium printed cartons, sheets and custom die-cut "
    "packaging — made to your exact spec."
)

FOOTER_COLUMNS = [
    (
        "Products",
        [
            ("Corrugated boxes", "#products"),
            ("Printed & laminated", "#products"),
            ("Sheets & partitions", "#products"),
            ("Custom die-cut", "#products"),
        ],
    ),
    (
        "Company",
        [
            ("About us", "#about"),
            ("Capabilities", "#capability"),
            ("How we work", "#process"),
            ("FAQs", "#faq"),
        ],
    ),
]

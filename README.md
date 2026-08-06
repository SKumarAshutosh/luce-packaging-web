# Lucè — Corrugated Box & Premium Packaging Website

A fast, single-page marketing site for a corrugated box manufacturer. Plain
HTML, CSS and JavaScript — **no build step, no dependencies, no server code**,
so it drops straight onto GitHub Pages.

---

## 1. Put your real details in (do this first)

Everything customer-facing lives in **one config block**. Open
[`assets/js/main.js`](assets/js/main.js) and edit the top of the file:

```js
const CONFIG = {
  whatsapp:     '919999999999',            // country code + number, digits only
  phoneDisplay: '+91 99999 99999',         // how it looks on the page
  phoneDial:    '+919999999999',           // what the call button dials
  email:        'hello@luce-packaging.com',
  address:      'Plot No. 00, Industrial Area, Your City',
  companyName:  'Lucè Packaging'
};
```

The top bar, quote section, footer and the floating WhatsApp button all read
from here — so you change each detail exactly once.

> **WhatsApp number format matters.** Use full international form with no `+`,
> no spaces and no dashes. For India that's `91` + your 10 digits, e.g.
> `919876543210`. If the number isn't valid the floating button falls back to
> scrolling to the quote form instead of opening a broken chat.

### Then search the project for `EDIT`

Remaining placeholders are marked with an `EDIT` comment. Every one of them:

| Where | What to change |
| --- | --- |
| `index.html` — `<meta>` block | description, keywords, `canonical` URL |
| `index.html` — JSON-LD script | full postal address, city, state, PIN, hours |
| `index.html` — `.stats` block | **the four headline numbers are placeholders** |
| `index.html` — `.panel-card__by` | your name / designation under the quote |
| `index.html` — `.foot-social` | real Instagram / LinkedIn / WhatsApp links |
| `index.html` — `.foot-bottom__gst` | your GSTIN, or delete the line |
| `robots.txt` and `sitemap.xml` | your real domain |

⚠️ **The four stat numbers (12+ years, 20L+ boxes, 3–7 ply, 24h quotes) are
illustrative.** Replace them with your actual figures before publishing —
don't ship claims you can't stand behind.

The spec table figures (bursting strength, GSM, safe load) are standard
industry ranges. Check them against what your plant actually produces.

---

## 2. Preview it locally

Just double-click `index.html` — it works from the file system.

For a closer-to-production preview (needed if you later add fetch calls):

```powershell
# any one of these, from the project folder
npx serve .
python -m http.server 8080
```

Then open <http://localhost:8080>.

---

## 3. Push to GitHub

From the project folder:

```powershell
git init
git add -A
git commit -m "Add Lucè packaging website"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Set your commit identity first if git complains:

```powershell
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

---

## 4. Turn on GitHub Pages

1. Open your repo on github.com → **Settings** → **Pages**
2. Under *Build and deployment* → **Source**, choose **Deploy from a branch**
3. Branch: **main**, folder: **/ (root)** → **Save**
4. Wait ~1 minute. Your site is live at
   `https://<your-username>.github.io/<your-repo>/`

The `.nojekyll` file is already included so GitHub serves the `assets/` folder
untouched.

### Custom domain (optional)

If you own `luce-packaging.com` or similar:

1. Settings → Pages → **Custom domain**, enter it, Save
2. At your domain registrar add these DNS records:
   - Four `A` records for the apex domain → `185.199.108.153`,
     `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - One `CNAME` for `www` → `<your-username>.github.io`
3. Come back and tick **Enforce HTTPS** once the certificate is issued

---

## 5. Project structure

```
corrugated-box/
├── index.html                  the whole site
├── 404.html                    friendly not-found page
├── robots.txt / sitemap.xml    search engine basics
├── .nojekyll                   tells GitHub Pages to serve assets/ as-is
├── README.md
└── assets/
    ├── css/style.css           all styling; design tokens at the top
    ├── js/main.js              CONFIG block + interactions
    └── img/
        ├── logo.svg            standalone Lucè lockup
        ├── favicon.svg         browser tab icon
        ├── og-image.svg        social share preview
        └── prod-*.svg          four product illustrations
```

---

## 6. How the quote form works

There is no backend and nothing is stored. On submit the form:

1. checks that name and phone are filled in
2. assembles a readable enquiry from whatever fields you completed
3. opens **WhatsApp** with that message pre-typed (or your **email** app if you
   click the second button)

You then just hit send. Nothing to host, nothing to maintain, nothing lost in
a spam folder.

**Want enquiries emailed automatically instead?** Create a free
[Formspree](https://formspree.io) form, then in `index.html` give the
`<form id="quoteForm">` an `action="https://formspree.io/f/YOUR_ID"` plus
`method="POST"`, and delete the `form.addEventListener('submit', …)` handler in
`main.js` so the browser submits normally.

---

## 7. Making design changes

All colours, fonts and spacing are CSS custom properties at the top of
[`assets/css/style.css`](assets/css/style.css):

```css
:root {
  --sun:  #D9902A;   /* the orange from your logo   */
  --blue: #1479C4;   /* the blue "è" accent          */
  --ink:  #17130F;   /* body text                    */
  --kraft-100: #F2EADC;  /* kraft paper backgrounds  */
}
```

Change one value there and it updates consistently everywhere — buttons,
badges, icon tiles, table chips, the 3D hero box, the lot.

**Editing content** is plain HTML in `index.html`. Each section is wrapped in a
banner comment (`<!-- ==== PRODUCTS -->`) so it's easy to find.

---

## 8. A note on the social preview image

`assets/img/og-image.svg` is a vector, and **WhatsApp, Facebook and LinkedIn
don't render SVG link previews**. For a preview thumbnail to show when you share
the link, export it as a PNG (1200 × 630) and point the meta tag at it:

```html
<meta property="og:image" content="assets/img/og-image.png">
```

Any browser can do the export: open the SVG, screenshot at full size — or use
`npx sharp-cli -i assets/img/og-image.svg -o assets/img/og-image.png`.

---

## 9. What's built in

- Responsive from 320 px up to wide desktop
- Sticky header, mobile drawer nav, scroll-linked active section
- Pure-CSS 3D corrugated box in the hero (no images, no library)
- Scroll reveals and counting stats — both fully disabled under
  `prefers-reduced-motion`
- Keyboard accessible: skip link, visible focus rings, labelled form fields,
  `aria-live` status messages
- Renders sensibly if JavaScript is blocked (nothing stays hidden)
- Print stylesheet, so a customer can print the spec sheet cleanly
- `LocalBusiness` structured data for Google

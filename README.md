# Levain Kit

**Interactive, responsive, multilingual website templates for artisan bakeries and patisseries.**
Three design systems · four languages (English · Français · Español · العربية) · zero dependencies · one build command.

Built for the thing bakeries actually ask for: a menu that is easy to change, a pre-order basket that
works on a phone in the queue, an "open now" badge that tells the truth, and a site that speaks the
neighbourhood's languages instead of apologising about it.

---

## 60-second tour

```bash
git clone https://github.com/abdoo606/BLAblalba.git && cd BLAblalba
npm run dev          # → http://localhost:5173  (no install step, there are no dependencies)
```

Then:

- `/` — the kit hub: live template switcher with a real iframe demo, viewport emulator,
  language lab, and the client pricing calculator
- `/templates/artisan/` — **Bois & Levain** · rustic, wood-fired, dark & warm
- `/templates/patisserie/` — **Rose & Glacé** · ivory, blush, editorial pâtisserie
- `/templates/moderno/` — **Horno Vivo** · terracotta, bold type, Mediterranean corner shop

Other scripts:

| Command | What it does |
|---|---|
| `npm run build` | regenerates `dist/` from `src/` (~0.5 s) |
| `npm run dev` | build + serve + rebuild on any change in `src/` |
| `npm start` | serve `dist/` only |
| `npm run validate` | locale key parity, broken refs, alt/aria smoke test |
| `npm run package` | `dist/` + docs + data → `release/levain-kit.zip` for the client |

`dist/` is committed on purpose: a client (or a designer who doesn't touch a terminal) can open the
folder, double-click `index.html` and everything works — the dictionaries are inlined, the fonts come
from the system, and there is no `fetch` that dies under `file://`.

## What is inside every page

| Capability | How |
|---|---|
| 4-language site with one switch | `data-i18n` hooks + generated dictionaries, choice persisted in `localStorage`, `<html lang>` and `dir` rewritten live |
| Real RTL (Arabic) | logical CSS properties only — `margin-inline`, `inset-inline-start`, `text-align: start`. One attribute flips the layout, marquee direction, carousel swipe and drawer side |
| Pre-order basket | add / remove / quantity, remembered per template, hands the order to WhatsApp or email. Nothing is charged, nothing to maintain |
| Filterable menu | category chips + diet tags + instant search **across all four languages** at once (search "cake" while the page is in French and it still finds *gâteau*) |
| Live oven countdown | "next bake in 42:07" from `site.json → batches`, ticks every second, flips to *just out of the oven*, pauses when the tab is hidden |
| Open-now truth | computed from `site.json → hours` against the visitor's clock, shown in the hero float and the hours card |
| Accessibility | skip link, visible focus, `aria-live` basket, labelled icon buttons, 44 px targets, `prefers-reduced-motion`, keyboard carousel and lightbox |
| Performance | ~30 KB of app JS, system fonts, preloaded hero, `loading="lazy"` below the fold, no third-party calls |
| SEO | per-page title/description/OG, `hreflang` for all four languages, canonical, `sitemap.xml`, `robots.txt`, `schema.org/Bakery` JSON-LD with real opening hours |
| Print | `@media print` gives the counter a clean menu sheet |

## Content model (this is the part clients edit)

```
src/data/site.json          products, prices, categories, hours, batches,
                            stats, testimonials ids, gallery, templates, packages
src/data/locales/en.json    every string, one flat namespace per concern
src/data/locales/fr.json    ┐
src/data/locales/es.json    ├ same keys, enforced by the build
src/data/locales/ar.json    ┘
src/styles/core.css         tokens + components + the three theme blocks
src/styles/hub.css          hub-only blocks (showcase, calculator, docs)
src/js/app.js               runtime engine
src/js/hub.js               hub extras (showcase, calculator, clipboard)
src/build.mjs               the whole generator
```

Rules the generator enforces:

- a locale file that gains or loses a key **fails the build** (parity check at the end of `build.mjs`)
- the same rule runs in `npm run validate`, together with a broken-reference check on `dist/`
- prices are **numbers** in `site.json`, never strings: currency, decimal separator and direction come
  from `Intl` at render time, so `€2.40` is `2,40 €` in French and `٢٫٤٠ €` in Arabic without anyone
  re-typing it

## Add a language (fifth: German, Dutch, Turkish…)

1. `cp src/data/locales/en.json src/data/locales/de.json`
2. add `{ "code": "de", "locale": "de-DE", "name": "German", "native": "Deutsch", "dir": "ltr" }` to `site.json → languages`
3. translate, `npm run build` — the picker, hreflang block, sitemap and JSON-LD pick it up automatically
4. anything you missed shows the English string rather than a key, and `npm run validate` names the key

## Theming

Each template is one `data-theme` block that overrides custom properties — colours, radii, the type
scale, the display face. To clone a theme for a new client:

```css
[data-theme="myclient"] {
  --bg: #0f1418; --surface: #171d22; --text: #eef4f6; --muted: #9fb0ba;
  --line: #232c33; --accent: #f0a04b; --accent-ink: #10161a; --accent-soft: #2a2114;
  --radius: .6rem; --radius-lg: 1rem;
}
```

…then add `{ "id": "myclient", "theme": "myclient", … }` to `site.json → templates`.

## Images

`src/assets/img/` holds the demo art. Photographed items are `.jpg`; the made-to-order celebration
pieces are drawn as `.svg` — an intentional device ("illustrated = baked to order") and a placeholder
for the client's own photos or the paid photo pass. Real client sites should replace all of it:
`magick in.jpg -resize 1200x900^ -gravity center -extent 1200x900 -quality 78 out.jpg`.

## Deploy

Any static host. Build command `npm run build`, publish directory `dist`.
Netlify / Cloudflare Pages / Vercel / GitHub Pages / the client's own Apache box — see
`docs/HANDOVER.md` for the client-facing version of those instructions.

## Repo map

```
dist/            built site, committed so it can be opened without a build
src/             data, locales, styles, runtime, generator
docs/            PRICING.md · PROSPECTS.md · HANDOVER.md
sales/           the pipeline: prospects-2026.csv/.json · drive-clients-pricing.csv (Drive) ·
                 OUTREACH.md (pitch in 3 languages) · OUTREACH-LOG.csv (per-lead audit trail) ·
                 COMPLIANCE.md (prospecting law) · TAX-SCOPE.md (which countries cost nothing) ·
                 REPLY-PLAYBOOK.md (replies, scoping, domain procedure) · QUOTE-TEMPLATE.md ·
                 INVOICE-TEMPLATE.md · TERMS.md · PRIVACY-NOTICE.md · DRIVE-SALES-PACK.md
tools/           dev watcher, static server, validator, packager
```

## Sales

- `docs/PRICING.md` — four packages, nine add-ons, quoting rules, margin check
- `docs/PROSPECTS.md` / `sales/prospects-2026.csv` — 141 shops in the UK, FR, ES and US with a 2026 growth signal; 42 verified by opening their own site, 16 contacted (43,124  € quoted). Client contact data lives in `sales/`, never in the published docs.
  **These are commercially sensitive and this repo is public**: the built `dist/` deliberately excludes
  `PROSPECTS.md` (see the `PRIVATE` filter in `src/build.mjs`) so GitHub Pages can never serve the client list,
  but the files themselves are readable in this repository. Keep the working copy in Drive / a private repo.
  with the price proposed for each (≈ 82,000 € one-off, ≈ 96,000 € first year)
- `sales/OUTREACH.md` — first email, WhatsApp DM, follow-up and objection answers in EN/FR/ES
- `sales/COMPLIANCE.md` — what is legal in a B2B cold email (FR/UK/US), records to keep, what we refuse to do
- `sales/TAX-SCOPE.md` — why no client country can make you register or pay VAT, and the one rule that keeps it true
- `sales/QUOTE-TEMPLATE.md` · `sales/INVOICE-TEMPLATE.md` · `sales/TERMS.md` · `sales/PRIVACY-NOTICE.md` — the four documents every job needs

## License

Private. The kit is the studio's product; sell sites built with it, not the kit itself (unless the
redistribution licence is paid).

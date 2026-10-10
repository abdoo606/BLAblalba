# Handover — what the client gets and how to keep it alive

Attach this to every delivery, in the client's own language. Sections 1–2 are safe to paste into an email as-is.

---

## 1. What you are receiving

```
your-site/
├── index.html                  the site. one file, opens in any browser
├── assets/                     styles, scripts, images, dictionaries, favicon, manifest
└── docs/                       this file, the price list, the content sheet
```

No database. No plugin. No subscription you can forget about. If the host disappears you can move the
folder to another host in an afternoon and it still works.

## 2. Change the four things that change

All of it happens in **one file**: `src/data/site.json` (or, if you got only the built site, ask us and we
send the source — it is yours).

| You want to… | Edit | Example |
|---|---|---|
| change a price | `products → price` | `"price": 2.6` |
| mark something sold out / add a new bake | `products →` add or remove a block | copy a block, change `id`, `name`, `image` |
| change opening hours | `hours` | `"open": "07:00", "close": "19:00"`, `null` = closed |
| change bake times (the countdown) | `batches → time` | `"time": "07:15"` |
| change a sentence | `src/data/locales/fr.json` | search for the phrase, edit between the quotes |
| add a language | `site.json → languages` + copy a locale file | see the README |

Then rebuild (`npm run build`) and upload the `dist/` folder. If you would rather not touch a terminal,
send the changes by WhatsApp and it is a five-minute job for us.

**Rules that keep it from breaking**

- Prices are numbers, not text: write `2.6`, never `2,60 €` — the site adds the currency symbol and the
  right format for each language.
- Keep the English and French quotes and commas exactly as they are. A missing comma is the whole error.
- Keep one key per line in the locale files; the build compares every language against the English one and
  tells you which keys are missing or extra.
- Photos: 1200×900 JPG, quality 78, under 300 KB. No TIFF from the camera, no iPhone HEIC.

## 3. Deploy (pick one)

**Netlify / Cloudflare Pages — what we recommend**
1. Push this repo to GitHub.
2. New site → import the repo. Build command `npm run build`. Publish directory `dist`.
3. Add your domain in DNS settings (Netlify gives you HTTPS automatically).

**Vercel**: framework preset *Other*, build `npm run build`, output `dist`, then a redirect `/ → /index.html`
in `vercel.json` so deep links stay clean.

**GitHub Pages**: `npm run build`, then push `dist/` to a `gh-pages` branch (or run the Action), set Pages to
that branch, tick "HTTPS".

**The client's own server**: FTP/SFTP the contents of `dist/` into the web root. That's it — no PHP, no Node
runtime, nothing to keep patched.

## 4. After launch — the 10 things that actually matter

- [ ] Google Business profile claimed, hours pasted in, 8+ photos, the website link set
- [ ] Search Console added, sitemap.xml submitted
- [ ] Test order placed from a phone, on 4G, in each language — the WhatsApp/email arrives?
- [ ] Phone number, address and "closed Monday" checked against reality (three times a year they drift)
- [ ] Prices checked against the chalkboard after the next increase
- [ ] Seasonal items archived, not deleted (history keeps the page relevant)
- [ ] Photos: at least three of people's hands or faces — pure product shots don't stop a scroll
- [ ] Reviews: two lines in the FAQ about how to complain, answered within a day, publicly
- [ ] Backup: this repo pushed = your site backed up
- [ ] Care plan decision written down, not remembered

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Text shows as `product.croissant.name` | locale key missing or typo'd | `npm run validate` names the key |
| Arabic page is still left-to-right | dictionary entry without `dir: rtl` in `languages` | set `"dir": "rtl"` |
| Basket empty after reload | browser in private mode | normal — localStorage is not shared |
| Countdown wrong for visitors abroad | it reads the *visitor's* clock by design | fix the store's own timezone only if the client insists; document it |
| Images look stretched | wrong aspect ratio | re-export at 1200×900 and let CSS crop |
| Site loads styles but no interactivity | `app.js` path changed by hand | relative paths assume `assets/` — don't move files |
| "It worked yesterday" | the host ran out of free-tier bandwidth | check the host dashboard; a bakery site is ~2 GB/month |

## 6. What we do *not* promise

Payments, gift cards, delivery routing, stock counters in the kitchen, social posting, photography beyond
the agreed pass, and any claim about ranking on Google. If those are needed, they are separate quotes with
their own numbers — say so before they get excited.

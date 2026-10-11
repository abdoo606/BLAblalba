# Wild Hearth Bakery — design board & pitch

Comrie, Perthshire, GB · A — hot · template **artisan** · croissant · 2410 €
Verified 2026-10-11: **YES**

## 1. Why them, now
NEW ENTRY in Britain's 50 Best Bakeries 2026; one baker (John Castley), mill-to-oven range from sourdough bomboloni to German schrotbrot
Source on file: thegoodfoodguide.co.uk — Britain's 50 Best Bakeries 2026 (2026-06-08).

## 2. What their web presence actually is
Wood-fired, one baker, wholesale across the central belt + a new Drummond Street shop (8-2pm Wed-Sat) - but the product images in the shop are the theme's own placeholder-*.png files, the catalogue asks trade buyers to register before they can see prices, and the two addresses/hours are scattered across Home and Contact. Scottish Bread Championships 2023 medals.
Found live: https://www.wildhearthbakery.com (WordPress/WooCommerce)
Contact: orders@wildhearthbakery.com (on their own site, delivery enquiries) · 15a Cultybraggan Camp, Comrie PH6 2AB + new shop on Drummond Street PH6 2DS · 03330 151304

## 3. The design I'd ship
- **Template:** artisan · **palette:** Cocoa nib, ember, cream — `#2a1f1a ink / #a8562a accent / #f7ece1 paper / #6b4b36 muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer → **wholesale order page** → **gallery: 9 shots, client-shot, I direct remotely**
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf £5.80 · bread · Baguette De Tradition £1.60 · bread · Seeded Rye Brick £6.40 · bread · Butter Croissant £2.40 · viennoiserie · Pain Au Chocolat £2.70 · viennoiserie · Morning Bun £3.20 · viennoiserie
- **Hero line:** “Wild Hearth Bakery — the loaf people queue for” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi Wild Hearth Bakery team — I looked at https://www.wildhearthbakery.com (WordPress/WooCommerce) this morning. Wood-fired, one baker, wholesale across the central belt + a new Drummond Street shop (8-2pm Wed-Sat) - but the product images in the shop are the theme's own placeholder-*.png files, the catalogue asks trade buyers to register before they can see prices, and the two addresses/hours are scattered across Home and Contact. Scottish Bread Championships 2023 medals.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 2075 £, delivered in 7 days. The files and repository are yours; optional ongoing services are separate. Includes wholesale + photo.
> No VAT on my invoice: you account for local VAT yourself (reverse charge), and it nets off if you are VAT-registered.
> If this isn't the right conversation, say so once and I won't write again.
>
> Abdulrhman Thali · freelance web developer · Karm El-Zeitoun, Homs, Syria
> You're getting this only if the address was verified on your own website. Reply “remove me” and I remove you from my active list and never contact you again.

*(If the first sentence in that quote is not true today, do not send the quote. Fix it, then send.)*

## 5. Before you press send — this lead's checklist
- [ ] Opened their site / Instagram / Google listing **today**
- [ ] Confirmed the sentence in §4 is a fact, not an assumption (write what you saw)
- [ ] Contact address is one *they* published (never guessed, never bought)
- [ ] Package + price match `sales/drive-clients-pricing.csv` — nothing renegotiated in a cold email
- [ ] Signature has the real name and a real postal address
- [ ] Permanent suppression check passed for the address, domain and business: `python3 tools/suppression.py check --email ADDRESS --site OWN_SITE --business NAME`
- [ ] Opt-out line present; any refusal triggers removal, not a follow-up
- [ ] 1:1 send from a normal mailbox (no Mailchimp/Brevo broadcast, max 5–10/day)
- [ ] Log updated in `sales/OUTREACH-LOG.csv` (status + date + source of address)

## 6. If they reply yes
1. 12 scoping questions on one 10-min call (`sales/REPLY-PLAYBOOK.md` §4)
2. Quote from §3 + the 40 % deposit invoice (payment route agreed **first** — see the note at the bottom of `sales/PROGRESS-CHECKLIST.md`)
3. Domain **in their name**, on their email, their 2FA (RDAP check first: `curl https://rdap.org/domain/<name>`)
4. Content deadline 7 days · build in this kit on branch `client/41-wild-hearth-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

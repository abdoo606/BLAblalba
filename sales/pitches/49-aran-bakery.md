# ARAN Bakery — design board & pitch

Dunkeld, Perthshire, GB · A — hot · template **artisan** · croissant · 1910 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Good Food Guide Britain's 50 Best Bakeries 2026; 200-year-old building in Dunkeld, 98% from 224 Google reviews
Source on file: aran-bakery.com/contact-1 + Daily Record GFG 2026 Scotland list (2026-03-24).

## 2. What their web presence actually is
Their own contact page: hello@ for 'menu, pre-orders and celebration cakes', manager@ for everything else, and two near-identical warnings that 'we will close when we sell out'. Opening hours Mon-Sat 9.30-3.30 / Sun 10-3.30 with no live sold-out state - so every pre-order is an email exchange and every sale after noon is luck.
Found live: https://www.aran-bakery.com
Contact: hello@aran-bakery.com (pre-orders + cakes) · manager@aran-bakery.com · 2 Atholl Street, Dunkeld PH8 0AR · 01350 727 029

## 3. The design I'd ship
- **Template:** artisan · **palette:** Flour, crust, burnt sugar — `#2f1c12 ink / #b4530a accent / #f6ece0 paper / #7d5a3c muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer → **pre-order basket → WhatsApp**
- **Languages:** en, 1 more: FR · PL · RO · ES — pick the one your street actually speaks
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf £5.80 · bread · Baguette De Tradition £1.60 · bread · Seeded Rye Brick £6.40 · bread · Butter Croissant £2.40 · viennoiserie · Pain Au Chocolat £2.70 · viennoiserie · Morning Bun £3.20 · viennoiserie
- **Hero line:** “ARAN Bakery — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi ARAN Bakery team — I looked at https://www.aran-bakery.com this morning. Their own contact page: hello@ for 'menu, pre-orders and celebration cakes', manager@ for everything else, and two near-identical warnings that 'we will close when we sell out'. Opening hours Mon-Sat 9.30-3.30 / Sun 10-3.30 with no live sold-out state - so every pre-order is an email exchange and every sale after noon is luck.
> That's exactly the part I build: hero, marquee, specialties, menu — 1645 £ delivered in 7 days, and the files and repository are yours, no subscription, no Shopify fees. Includes preorder.
> No VAT on my invoice: you account for local VAT yourself (reverse charge), and it nets off if you are VAT-registered.
> If this isn't the right conversation, say so once and I won't write again.
>
> Abdulrhman Thali · freelance web developer · Karm El-Zeitoun, Homs, Syria
> You're getting this because your contact details are published by you / in public listings. Reply “remove me” and I delete you from my list permanently.

*(If the first sentence in that quote is not true today, do not send the quote. Fix it, then send.)*

## 5. Before you press send — this lead's checklist
- [ ] Opened their site / Instagram / Google listing **today**
- [ ] Confirmed the sentence in §4 is a fact, not an assumption (write what you saw)
- [ ] Contact address is one *they* published (never guessed, never bought)
- [ ] Package + price match `sales/drive-clients-pricing.csv` — nothing renegotiated in a cold email
- [ ] Signature has the real name and a real postal address
- [ ] Opt-out line present, and the reply goes straight into the suppression list
- [ ] 1:1 send from a normal mailbox (no Mailchimp/Brevo broadcast, max 5–10/day)
- [ ] Log updated in `sales/OUTREACH-LOG.csv` (status + date + source of address)

## 6. If they reply yes
1. 12 scoping questions on one 10-min call (`sales/REPLY-PLAYBOOK.md` §4)
2. Quote from §3 + the 40 % deposit invoice (payment route agreed **first** — see the note at the bottom of `sales/PROGRESS-CHECKLIST.md`)
3. Domain **in their name**, on their email, their 2FA (RDAP check first: `curl https://rdap.org/domain/<name>`)
4. Content deadline 7 days · build in this kit on branch `client/49-aran-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

# The Bakery House — design board & pitch

Bryn Mawr / Paoli, PA, US · A — hot · template **moderno** · croissant · 2082 €
Verified 2026-10-11: **YES**

## 1. Why them, now
37 years old and just OPENED A SECOND STOREFRONT (Paoli Village Shoppes, announced 25 Sep 2026); Philadelphia Magazine “Best Pie” 2024; custom cakes, croissants, chicken salad
Source on file: patch.com — award-winning bakery opens new shop in Paoli (2026-09-25).

## 2. What their web presence actually is
A real commerce site: shop, custom-cake quote form, review wall. Gaps I could see: one hero for two stores with no Paoli hours page yet, a Bars product image still hot-linked to a dead 3dcart CDN (shop-thebakeryhouse-net.3dcartstores.com), 240 Bread Share subscribers and 4 wholesale cafes running off-paper, and 2,500 Thanksgiving pies a year with no seasonal order cutoff page.
Found live: https://www.thebakeryhouse.net (own shop + quote form)
Contact: thebakeryhouse604@gmail.com (their Facebook page; also published by SAVVY Mainline and vista.today as the business contact) · 604 W Lancaster Ave Bryn Mawr PA + new Paoli Village Shoppes store (opened 28 Sep 2026) · 610-525-4139 · owner Sandy Stauffer

## 3. The design I'd ship
- **Template:** moderno · **palette:** Concrete, ember, steel — `#101314 ink / #e2622a accent / #f4f5f4 paper / #40535c muted`
- **Sections, in order:** hero → specialties → menu → batch → story → services → gallery → hours → testimonials → order → faq → footer → **wholesale order page**
- **Languages:** en, 1 more: ES · FR · ZH · KO
- **Menu to enter (their real items, from their own posts):** Butter Croissant $2.40 · viennoiserie · Morning Bun $3.20 · viennoiserie · Vanilla & Fruit Tart $4.50 · pastry · King Cake (Galette) $24.00 · celebration · Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread
- **Hero line:** “The Bakery House — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/moderno/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi The Bakery House team — I looked at https://www.thebakeryhouse.net (own shop + quote form) this morning. A real commerce site: shop, custom-cake quote form, review wall. Gaps I could see: one hero for two stores with no Paoli hours page yet, a Bars product image still hot-linked to a dead 3dcart CDN (shop-thebakeryhouse-net.3dcartstores.com), 240 Bread Share subscribers and 4 wholesale cafes running off-paper, and 2,500 Thanksgiving pies a year with no seasonal order cutoff page.
> That's exactly the part I build: hero, specialties, menu, batch — 2270 $ delivered in 7 days, and the files and repository are yours, no subscription, no Shopify fees. Includes extra-location + wholesale.
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
4. Content deadline 7 days · build in this kit on branch `client/43-the-bakery-house` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

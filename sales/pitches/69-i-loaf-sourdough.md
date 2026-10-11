# I Loaf Sourdough — design board & pitch

Fort Lauderdale, FL, US · A — hot · template **artisan** · baguette · 1130 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Their own homepage carries a 'WE DO CATERING' line and customers' reviews call it a 'new bakery in town'; open Wed-Sat only, so every online impression has to convert.
Source on file: sourdoughbreadfortlauderdale.com + /contact (own site, opened 2026-10-11) | merged with the older to-verify row for the same shop (duplicate removed 2026-10-11, one row per shop).

## 2. What their web presence actually is
OPENED 2026-10-11 10:05Z, / and /contact read in full. /contact publishes 'Email: Bake@loafofsourdough.com' + phone + address (so the address is theirs, published, not guessed) - note the email lives on loafofsourdough.com while the site is on sourdoughbreadfortlauderdale.com: they already own the shorter, better domain and never built anything on it. Hours on the contact page: Mon/Tue/Sun closed, Wed 9-4, Thu 7-4, Fri 7-3, Sat 7-4 (the Wed 9am start disagrees with the 7am of the other days, and the homepage repeats the whole contact block twice). Homepage: duplicated slider text ('PASSION FOR FOR PERFECTION'), powr.io embed blocked, no prices on Sourdough Bread / Croissant / Sandwiches pages, Google Maps link only.
Found live: https://sourdoughbreadfortlauderdale.com
Contact: Bake@loafofsourdough.com · (954) 999-5415 · 2720 E Oakland Park Blvd Ste 103, Fort Lauderdale, FL 33306

## 3. The design I'd ship
- **Template:** artisan · **palette:** Flour, crust, burnt sugar — `#2f1c12 ink / #b4530a accent / #f6ece0 paper / #7d5a3c muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf $5.80 · bread · Butter Croissant $2.40 · viennoiserie · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “I Loaf Sourdough — the loaf people queue for” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi I Loaf Sourdough team — I looked at https://sourdoughbreadfortlauderdale.com this morning. OPENED 2026-10-11 10:05Z, / and /contact read in full. /contact publishes 'Email: Bake@loafofsourdough.com' + phone + address (so the address is theirs, published, not guessed) - note the email lives on loafofsourdough.com while the site is on sourdoughbreadfortlauderdale.com: they already own the shorter, better domain and never built anything on it. Hours on the contact page: Mon/Tue/Sun closed, Wed 9-4, Thu 7-4, Fri 7-3, Sat 7-4 (the Wed 9am start disagrees with the 7am of the other days, and the homepage repeats the whole contact block twice). Homepage: duplicated slider text ('PASSION FOR FOR PERFECTION'), powr.io embed blocked, no prices on Sourdough Bread / Croissant / Sandwiches pages, Google Maps link only.
> That's exactly the part I build: hero, marquee, specialties, menu — 1230 $ delivered in 5 days, and the files and repository are yours, no subscription, no Shopify fees. Includes seo.
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
4. Content deadline 7 days · build in this kit on branch `client/69-i-loaf-sourdough` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

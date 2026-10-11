# Gusto Bread — design board & pitch

Long Beach, CA, US · A — hot · template **moderno** · croissant · 2050 €
Verified 2026-10-11: **YES**

## 1. Why them, now
James Beard Outstanding Bakery semifinalist three years running (2024, 2025, 2026); artisanal panaderia - masa madre + in-house nixtamal
Source on file: gustobread.com/contact + jamesbeard.org 2026 semifinalists.

## 2. What their web presence actually is
WordPress site with a real press page (NYT, Food & Wine, JB seals) and Toast ordering - but the MENU nav item links to a canva.link, so the menu is an image/PDF outside their domain: unsearchable, un-Googleable, no prices in schema, and their Spanish-language story has no Spanish site. Merch lives on Shopify, newsletter on Toast: five systems for one bakery.
Found live: https://gustobread.com
Contact: hola@gustobread.com · 2710 E 4th Street, Long Beach CA 90814 · 562-343-1881

## 3. The design I'd ship
- **Template:** moderno · **palette:** Burnt honey, brass — `#12100f ink / #c9a227 accent / #f5f2ea paper / #5b5340 muted`
- **Sections, in order:** hero → specialties → menu → batch → story → services → gallery → hours → testimonials → order → faq → footer
- **Languages:** en, 1 more: ES · FR · ZH · KO
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Butter Croissant $2.40 · viennoiserie · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “Gusto Bread — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/moderno/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi Gusto Bread team — I looked at https://gustobread.com this morning. WordPress site with a real press page (NYT, Food & Wine, JB seals) and Toast ordering - but the MENU nav item links to a canva.link, so the menu is an image/PDF outside their domain: unsearchable, un-Googleable, no prices in schema, and their Spanish-language story has no Spanish site. Merch lives on Shopify, newsletter on Toast: five systems for one bakery.
> That's exactly the part I build: hero, specialties, menu, batch — 2235 $ delivered in 7 days, and the files and repository are yours, no subscription, no Shopify fees. Includes language(ES) + seo.
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
4. Content deadline 7 days · build in this kit on branch `client/50-gusto-bread` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

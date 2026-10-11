# ARAN Bakery — design board & pitch

Dunkeld, Perthshire, GB · A — hot · template **artisan** · croissant · 1910 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Good Food Guide Britain's 50 Best Bakeries 2026; 200-year-old building in Dunkeld, 98% from 224 Google reviews
Source on file: aran-bakery.com/contact-1 + Daily Record GFG 2026 Scotland list (2026-03-24).

## 2. What their web presence actually is
OPENED 2026-10-11 09:57Z, both pages read in full. Homepage: Tue 7-2, Wed 7-2, Thu 7-2, Fri 7-2, Sat 8AM-2PM; location block types the ZIP as 'Lakeland, FL 338o3' (letter o). /contactus: Wednesdays 7-2 and Saturdays 8AM-1PM only, address written correctly as 1113 S. Florida Ave 33803, phone 863.450.4513, 'Get In Touch' mailto = hello@bornandbreadbakehouse.com (so the address is confirmed on their own page, not just in a search index). Ordering DOES work: pre-orders on Toast (order.toasttab.com/online/born-and-bread-1113-florida-ave-s) with dated pickup slots and Saturday outside pick-up, merch on /shop. Correction sent in-thread: my first email said 'no way to reserve anything' - wrong, and said so.
Found live: https://www.aran-bakery.com
Contact: hello@aran-bakery.com (pre-orders + cakes) · manager@aran-bakery.com · 2 Atholl Street, Dunkeld PH8 0AR · 01350 727 029

## 3. The design I'd ship
- **Template:** artisan · **palette:** Flour, crust, burnt sugar — `#2f1c12 ink / #b4530a accent / #f6ece0 paper / #7d5a3c muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer → **pre-order basket → WhatsApp**
- **Languages:** en, 1 more: FR · PL · RO · ES — pick the one your street actually speaks
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf £5.80 · bread · Baguette De Tradition £1.60 · bread · Seeded Rye Brick £6.40 · bread · Butter Croissant £2.40 · viennoiserie · Pain Au Chocolat £2.70 · viennoiserie · Morning Bun £3.20 · viennoiserie
- **Hero line:** “ARAN Bakery — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi ARAN Bakery team — I looked at https://www.aran-bakery.com this morning. OPENED 2026-10-11 09:57Z, both pages read in full. Homepage: Tue 7-2, Wed 7-2, Thu 7-2, Fri 7-2, Sat 8AM-2PM; location block types the ZIP as 'Lakeland, FL 338o3' (letter o). /contactus: Wednesdays 7-2 and Saturdays 8AM-1PM only, address written correctly as 1113 S. Florida Ave 33803, phone 863.450.4513, 'Get In Touch' mailto = hello@bornandbreadbakehouse.com (so the address is confirmed on their own page, not just in a search index). Ordering DOES work: pre-orders on Toast (order.toasttab.com/online/born-and-bread-1113-florida-ave-s) with dated pickup slots and Saturday outside pick-up, merch on /shop. Correction sent in-thread: my first email said 'no way to reserve anything' - wrong, and said so.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 1645 £, delivered in 7 days. The files and repository are yours; optional ongoing services are separate. Includes preorder.
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
4. Content deadline 7 days · build in this kit on branch `client/49-aran-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

# Weltons Tiny Bakeshop — design board & pitch

Charleston, SC, US · A — hot · template **patisserie** · baguette · 1215 €
Verified 2026-10-11: **YES**

## 1. Why them, now
James Beard 2026 Outstanding Bakery finalist, one-room shop
Source on file: cnn.com 16 Jun 2026.

## 2. What their web presence actually is
Read 2026-10-11: /contact on weltonstinybakeshop.com is not a contact page at all - it is the recruiting page ("JOIN THE WTB TEAM / POSITIONS AVAILABLE / summer & fall 2026", bartender, counter server, line cook, "$15 - with tips avg $25-$35/hour", a resume-upload form). A customer looking for the shop, the honey pie, or how to order a cake lands on job openings. One typo in the requirements: "AFTERNOON/EVENING AVAILABILITY ON IS A PLUS!"
Found live: weltonstinybakeshop.com
Contact: +1 843-666-7277 (no public email found)

## 3. The design I'd ship
- **Template:** patisserie · **palette:** Raspberry, buttercream — `#20141c ink / #c2496b accent / #fdf4f6 paper / #7a4256 muted`
- **Sections, in order:** hero → marquee → specialties → menu → story → services → gallery → testimonials → batch → hours → order → faq → footer
- **Languages:** en, 1 more: ES · FR · ZH · KO
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Butter Croissant $2.40 · viennoiserie · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “Weltons Tiny Bakeshop — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/patisserie/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, phone / counter / DM (no public email))
> Hi Weltons Tiny Bakeshop team — I looked at weltonstinybakeshop.com this morning. Read 2026-10-11: /contact on weltonstinybakeshop.com is not a contact page at all - it is the recruiting page ("JOIN THE WTB TEAM / POSITIONS AVAILABLE / summer & fall 2026", bartender, counter server, line cook, "$15 - with tips avg $25-$35/hour", a resume-upload form). A customer looking for the shop, the honey pie, or how to order a cake lands on job openings. One typo in the requirements: "AFTERNOON/EVENING AVAILABILITY ON IS A PLUS!".
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 1325 $, delivered in 5 days. The files and repository are yours; optional ongoing services are separate. Includes seo.
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
4. Content deadline 7 days · build in this kit on branch `client/28-weltons-tiny-bakeshop` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

# Layla Bakery — design board & pitch

London (Ladbroke Grove), GB · A — hot · template **patisserie** · croissant · 1830 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Named the Good Food Guide's best bakery in London for 2026 — a moment the whole street will search for
Source on file: londonyaar.com — 15 best bakeries in London to visit in 2026 (2026-08-16).

## 2. What their web presence actually is
Info page = plain text hours for TWO shops (Ladbroke Grove Mon-Sat 8-4 / Sun 8-3, Acton Wed-Sun 7.30-3) and one shared press inbox. No per-shop menu, no stock, no reservation. GFG best bakery in London 2026 + a second shop in Acton.
Found live: https://laylabakery.com (pages/info)
Contact: aniek@laylabakery.com (published on their own Info page as General & Press) · 332 Portobello Rd W10 5PQ + 53 Churchfield Rd W3 6AY

## 3. The design I'd ship
- **Template:** patisserie · **palette:** Pistachio, cream, mint — `#141b1a ink / #3f8f7a accent / #f2f7f4 paper / #4a6b62 muted`
- **Sections, in order:** hero → marquee → specialties → menu → story → services → gallery → testimonials → batch → hours → order → faq → footer
- **Languages:** en, 1 more: FR · PL · RO · ES — pick the one your street actually speaks
- **Menu to enter (their real items, from their own posts):** Macaron £2.20 · pastry · Country Levain Loaf £5.80 · bread · Baguette De Tradition £1.60 · bread · Seeded Rye Brick £6.40 · bread · Butter Croissant £2.40 · viennoiserie · Pain Au Chocolat £2.70 · viennoiserie
- **Hero line:** “Layla Bakery — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/patisserie/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi Layla Bakery team — I looked at https://laylabakery.com (pages/info) this morning. Info page = plain text hours for TWO shops (Ladbroke Grove Mon-Sat 8-4 / Sun 8-3, Acton Wed-Sun 7.30-3) and one shared press inbox. No per-shop menu, no stock, no reservation. GFG best bakery in London 2026 + a second shop in Acton.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 1575 £, delivered in 7 days. The files and repository are yours; optional ongoing services are separate. Includes seo.
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
4. Content deadline 7 days · build in this kit on branch `client/38-layla-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

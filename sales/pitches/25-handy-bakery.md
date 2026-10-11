# Handy Bakery — design board & pitch

Barcelona (Gràcia) — Carrer de Rabassa 5, ES · A — hot · template **patisserie** · croissant · 2830 €
Verified 2026-10-11: **YES**

## 1. Why them, now
New 2025 opening (bakery + patisserie + specialty coffee) - greenfield, needs everything
Source on file: inandoutbarcelona.net 14 Nov 2025.

## 2. What their web presence actually is
Read 2026-10-11: handybakery.es returns its hosting provider's page - "Account Suspended. This Account has been suspended. Contact your hosting provider" (the mailto on that page is webmaster@handybakery.es, the host's generic address - not a contact we may use). No live site at all.
Found live: handybakery.es — one sentence: “Contáctanos por Instagram”
Contact: Instagram @handybakery_ · Carrer de Rabassa 5, Gràcia (NOT Plaça de la Vila)

## 3. The design I'd ship
- **Template:** patisserie · **palette:** Plum, meringue, lilac — `#1c1a24 ink / #b4708c accent / #f8f2f4 paper / #6d5a7a muted`
- **Sections, in order:** hero → marquee → specialties → menu → story → services → gallery → testimonials → batch → hours → order → faq → footer → **pre-order basket → WhatsApp** → **gallery: 9 shots, client-shot, I direct remotely**
- **Languages:** es, 2 more: EN · FR · DE (plus Catalan/Valencian where it is the street language)
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf €5.80 · bread · Baguette De Tradition €1.60 · bread · Seeded Rye Brick €6.40 · bread · Butter Croissant €2.40 · viennoiserie · Pain Au Chocolat €2.70 · viennoiserie · Morning Bun €3.20 · viennoiserie
- **Hero line:** “Handy Bakery — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/patisserie/index.html?lang=es` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, phone / counter / DM (no public email))
> Hi Handy Bakery team — I looked at handybakery.es — one sentence: “Contáctanos por Instagram” this morning. Read 2026-10-11: handybakery.es returns its hosting provider's page - "Account Suspended. This Account has been suspended. Contact your hosting provider" (the mailto on that page is webmaster@handybakery.es, the host's generic address - not a contact we may use). No live site at all.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 2830 €, delivered in 7 days. The files and repository are yours; optional ongoing services are separate. Includes photo + seo + preorder.
> Billed without VAT under the reverse charge (art. 196 Directive 2006/112) — send me your VAT number. If you are not VAT-liable (franchise en base / módulos), you self-account 21 % you cannot recover, so budget about 3425 €.
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
4. Content deadline 7 days · build in this kit on branch `client/25-handy-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

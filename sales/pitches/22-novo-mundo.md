# Novo Mundo — design board & pitch

Madrid (La Latina), ES · B — upgrade · template **artisan** · croissant · 2042 €
Verified 2026-10-11: **NO — do the 4-minute check before anything is sent**

## 1. Why them, now
'La panadería del Rastro', best bread in Madrid 2023, café + counter
Source on file: timeout.es 03 Aug 2026.

## 2. What their web presence actually is
public notes say: “No e-commerce” — open their site before you use this sentence
Claimed earlier (press/aggregator): No e-commerce

## 3. The design I'd ship
- **Template:** artisan · **palette:** Cocoa nib, ember, cream — `#2a1f1a ink / #a8562a accent / #f7ece1 paper / #6b4b36 muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer → **gallery: 9 shots, client-shot, I direct remotely**
- **Languages:** es, 1 more: EN · FR · DE (plus Catalan/Valencian where it is the street language)
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf €5.80 · bread · Baguette De Tradition €1.60 · bread · Seeded Rye Brick €6.40 · bread · Butter Croissant €2.40 · viennoiserie · Pain Au Chocolat €2.70 · viennoiserie · Morning Bun €3.20 · viennoiserie
- **Hero line:** “Novo Mundo — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/artisan/index.html?lang=es` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, to be found during verification)
> Hi Novo Mundo team — I looked at ? this morning. public notes say: “No e-commerce” — open their site before you use this sentence.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 2040 €, delivered in 7 days. The files and repository are yours; optional ongoing services are separate. Includes seo + photo.
> Billed without VAT under the reverse charge (art. 196 Directive 2006/112) — send me your VAT number. If you are not VAT-liable (franchise en base / módulos), you self-account 21 % you cannot recover, so budget about 2470 €.
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
4. Content deadline 7 days · build in this kit on branch `client/22-novo-mundo` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

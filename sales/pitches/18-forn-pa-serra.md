# Forn Pa Serra — design board & pitch

Barcelona, ES · A — hot · template **moderno** · baguette · 1148 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Third generation since 1929; source states plainly: 'no tienen ni web, ni redes sociales. Old school.'
Source on file: inandoutbarcelona.net 14 Nov 2025.

## 2. What their web presence actually is
Confirmed: no website, no social media. Third-party pages publish incorrect hours, and a scraper site ranks for their name.
Found live: NONE — only Yelp/Tripadvisor/aggregators + a junk auto-generated page 'pa-serra.weeblyte.com' with WRONG opening hours
Contact: +34 934 242 541 · Carrer de l'Olivera 31, 08004 BCN

## 3. The design I'd ship
- **Template:** moderno · **palette:** Glaze, blueberry, ice — `#0f1113 ink / #2f80c4 accent / #f1f5f8 paper / #3a5a72 muted`
- **Sections, in order:** hero → specialties → menu → batch → story → services → gallery → hours → testimonials → order → faq → footer
- **Languages:** es, 1 more: EN · FR · DE (plus Catalan/Valencian where it is the street language), ca/valencià — same layout, RTL-safe code is already in the kit (Spanish + Catalan is what sells in this city; Arabic RTL is already in the codebase if you want a halal/wedging crowd served)
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf €5.80 · bread · Baguette De Tradition €1.60 · bread · Seeded Rye Brick €6.40 · bread · Butter Croissant €2.40 · viennoiserie · Pain Au Chocolat €2.70 · viennoiserie · Morning Bun €3.20 · viennoiserie
- **Hero line:** “Forn Pa Serra — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/moderno/index.html?lang=es` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, phone / counter / DM (no public email))
> Hi Pa Serra team — I looked at NONE — only Yelp/Tripadvisor/aggregators + a junk auto-generated page 'pa-serra.weeblyte.com' with WRONG opening hours this morning. Confirmed: no website, no social media. Third-party pages publish incorrect hours, and a scraper site ranks for their name.
> That's exactly the part I build: hero, specialties, menu, batch — 1150 € delivered in 5 days, and the files and repository are yours, no subscription, no Shopify fees. Includes seo.
> Billed without VAT under the reverse charge (art. 196 Directive 2006/112) — send me your VAT number. If you are not VAT-liable (franchise en base / módulos), you self-account 21 % you cannot recover, so budget about 1390 €.
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
4. Content deadline 7 days · build in this kit on branch `client/18-forn-pa-serra` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

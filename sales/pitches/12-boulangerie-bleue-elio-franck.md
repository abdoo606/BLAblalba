# Boulangerie Bleue (Elio & Franck) — design board & pitch

Rueil-Malmaison, FR · B — upgrade · template **artisan** · croissant · 1830 €
Verified 2026-10-11: **NO — do the 4-minute check before anything is sent**

## 1. Why them, now
2025 Best Artisan Baker trophy, Hauts-de-Seine (employer category) + apprentice medals
Source on file: sortiraparis.com 06 Nov 2025.

## 2. What their web presence actually is
public notes say: “Local site; no English for expat clients” — open their site before you use this sentence
Claimed earlier (press/aggregator): Local site; no English for expat clients

## 3. The design I'd ship
- **Template:** artisan · **palette:** Cocoa nib, ember, cream — `#2a1f1a ink / #a8562a accent / #f7ece1 paper / #6b4b36 muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer
- **Languages:** fr, 1 more: EN · ES · DE · IT
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf €5.80 · bread · Baguette De Tradition €1.60 · bread · Seeded Rye Brick €6.40 · bread · Butter Croissant €2.40 · viennoiserie · Pain Au Chocolat €2.70 · viennoiserie · Morning Bun €3.20 · viennoiserie
- **Hero line:** “Boulangerie Bleue (Elio & Franck) — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/artisan/index.html?lang=fr` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, to be found during verification)
> Hi Bleue (Elio & Franck) team — I looked at ? this morning. public notes say: “Local site; no English for expat clients” — open their site before you use this sentence.
> That's exactly the part I build: hero, marquee, specialties, menu — 1830 € delivered in 7 days, and the files and repository are yours, no subscription, no Shopify fees. Includes seo.
> Billed without VAT under the reverse charge (art. 196 Directive 2006/112) — send me your VAT number. If you are not VAT-liable (franchise en base / módulos), you self-account 21 % you cannot recover, so budget about 2215 €.
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
4. Content deadline 7 days · build in this kit on branch `client/12-boulangerie-bleue-elio-franck` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

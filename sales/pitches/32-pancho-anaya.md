# Pancho Anaya — design board & pitch

Tulsa, OK, US · B — big fish, wrong front door · template **moderno** · patisserie · 3600 €
Verified 2026-10-11: **NO — do the 4-minute check before anything is sent**

## 1. Why them, now
Panadería founded 1912 in Michoacán, four generations, three retail locations + a manufacturing plant co-packing nationally since 2020.
Source on file: foodandwine.com best bakeries.

## 2. What their web presence actually is
public notes say: “Squarespace store called "Pancho Anaya Products" - it sells packaged goods (Café de Olla) with cart + sign-in. The four retail bakeries have no page of their own: /locations is a text list of addresses and hours, no map embed, no online ordering.” — open their site before you use this sentence
Claimed earlier (press/aggregator): Squarespace store called "Pancho Anaya Products" - it sells packaged goods (Café de Olla) with cart + sign-in. The four retail bakeries have no page of their own: /locations is a text list of addresses and hours, no map embed, no online ordering.

## 3. The design I'd ship
- **Template:** moderno · **palette:** Glaze, blueberry, ice — `#0f1113 ink / #2f80c4 accent / #f1f5f8 paper / #3a5a72 muted`
- **Sections, in order:** hero → specialties → menu → batch → story → services → gallery → hours → testimonials → order → faq → footer → **gallery: 9 shots, client-shot, I direct remotely**
- **Languages:** en, 2 more: ES · FR · ZH · KO
- **Menu to enter (their real items, from their own posts):** Morning Bun $3.20 · viennoiserie · Vanilla & Fruit Tart $4.50 · pastry · King Cake (Galette) $24.00 · celebration · Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread
- **Hero line:** “Pancho Anaya — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/moderno/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, to be found during verification)
> Hi Pancho Anaya team — I looked at ? this morning. public notes say: “Squarespace store called "Pancho Anaya Products" - it sells packaged goods (Café de Olla) with cart + sign-in. The four retail bakeries have no page of their own: /locations is a text list of addresses and hours, no map embed, no online ordering.” — open their site before you use this sentence.
> That's exactly the part I build: hero, specialties, menu, batch — a one-time project fee of 3925 $, delivered in 14 days. The files and repository are yours; optional ongoing services are separate. Includes seo + photo.
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
4. Content deadline 7 days · build in this kit on branch `client/32-pancho-anaya` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

# Café Dear Leon — design board & pitch

Canton + Remington, Baltimore, MD, US · A — hot · template **patisserie** · croissant · 2010 €
Verified 2026-10-11: **YES**

## 1. Why them, now
James Beard 2026 Outstanding Bakery semifinalist; second location (La Maison, Remington) opened for 2026; the viral crab-dip bagel queue is covered in BmoreArt (Jan 2026).
Source on file: cafedearleon.com (own site) + BmoreArt 2026-01-13 + jamesbeard.org 2026 semifinalists | merged with the older to-verify row for the same shop (duplicate removed 2026-10-11, one row per shop).

## 2. What their web presence actually is
Read 2026-10-11: /contact on cafedearleon.com returns the WordPress "Page not found - Whoops, that page is gone" (Bricks builder: "Skip to main content / Skip to footer"). The site's own contact page is gone; no menu, hours, or email readable on it.
Found live: https://cafedearleon.com
Contact: (667) 335-9160 · 2929 O'Donnell St (Canton) + 2600 N Howard St (Remington) · NO email published; /contact/ returns a 404

## 3. The design I'd ship
- **Template:** patisserie · **palette:** Plum, meringue, lilac — `#1c1a24 ink / #b4708c accent / #f8f2f4 paper / #6d5a7a muted`
- **Sections, in order:** hero → marquee → specialties → menu → story → services → gallery → testimonials → batch → hours → order → faq → footer
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Butter Croissant $2.40 · viennoiserie · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “Café Dear Leon — what the whole street talks about” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/patisserie/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, phone / counter / DM (no public email))
> Hi Café Dear Leon team — I looked at https://cafedearleon.com this morning. Read 2026-10-11: /contact on cafedearleon.com returns the WordPress "Page not found - Whoops, that page is gone" (Bricks builder: "Skip to main content / Skip to footer"). The site's own contact page is gone; no menu, hours, or email readable on it.
> That's exactly the part I build: hero, marquee, specialties, menu — 2190 $ delivered in 7 days, and the files and repository are yours, no subscription, no Shopify fees. Includes extra location, seo.
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
4. Content deadline 7 days · build in this kit on branch `client/70-cafe-dear-leon` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

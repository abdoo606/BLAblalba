# The Local General Store — design board & pitch

Honolulu, HI, US · C - from a 2026 list · template **artisan** · Croissant · 1450 €
Verified 2026-10-11: **NO — do the 4-minute check before anything is sent**

## 1. Why them, now
Best bakery in Hawaii (Food Republic, 18/08/2026); bakery/butchery hybrid born of Hawaii's Sovereign food movement, sourcing only from the islands - Char Siu pork croissants, liliko'i baklava danishes, chocolate banana muffins.
Source on file: foodrepublic.com/2234748 (18 Aug 2026).

## 2. What their web presence actually is
public notes say: “to find” — open their site before you use this sentence
Claimed earlier (press/aggregator): to find

## 3. The design I'd ship
- **Template:** artisan · **palette:** Flour, crust, burnt sugar — `#2f1c12 ink / #b4530a accent / #f6ece0 paper / #7d5a3c muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Butter Croissant $2.40 · viennoiserie · Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “The Local General Store — what the whole street talks about” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, to be found during verification)
> Hi The Local General Store team — I looked at thelocalgeneralstorehi.com this morning. public notes say: “to find” — open their site before you use this sentence.
> That's exactly the part I build: hero, marquee, specialties, menu — 1580 $ delivered in 7 days, and the files and repository are yours, no subscription, no Shopify fees.
> VAT treatment to be confirmed — I invoice from outside the EU.
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
4. Content deadline 7 days · build in this kit on branch `client/163-the-local-general-store` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

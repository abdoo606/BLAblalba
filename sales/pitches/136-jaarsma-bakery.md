# Jaarsma Bakery — design board & pitch

Pella, IA, US · A - hot · template **artisan** · baguette · 1450 €
Verified 2026-10-11: **NO — do the 4-minute check before anything is sent**

## 1. Why them, now
Food Republic's best bakery in Iowa 2026; Dutch heritage, bakery plus cafe
Source on file: Food Republic, 'best bakery in every US state', 2026-08-18.

## 2. What their web presence actually is
public notes say: “Tourism-driven town, national press, nothing to book” — open their site before you use this sentence
Claimed earlier (press/aggregator): Tourism-driven town, national press, nothing to book

## 3. The design I'd ship
- **Template:** artisan · **palette:** Rye, linen, walnut — `#22201c ink / #8a6d3b accent / #f3efe6 paper / #5d5340 muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer → **gallery: 9 shots, client-shot, I direct remotely**
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Morning Bun $3.20 · viennoiserie · Vanilla & Fruit Tart $4.50 · pastry · Burnt Basque Cheesecake $28.00 · celebration · Saint Honoré $32.00 · celebration · King Cake (Galette) $24.00 · celebration · Country Levain Loaf $5.80 · bread
- **Hero line:** “Jaarsma Bakery — what the whole street talks about” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, to be found during verification)
> Hi Jaarsma Bakery team — I looked at your online presence this morning. public notes say: “Tourism-driven town, national press, nothing to book” — open their site before you use this sentence.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 1580 $, delivered in 5 days. The files and repository are yours; optional ongoing services are separate. Includes seo, photo.
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
4. Content deadline 7 days · build in this kit on branch `client/136-jaarsma-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

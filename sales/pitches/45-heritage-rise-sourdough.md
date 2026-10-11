# Heritage Rise Sourdough — design board & pitch

Elk Grove, CA, US · B — upgrade · template **artisan** · baguette · 1070 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Family microbakery (2023) on a 1790s starter; farmers market every Sunday, porch pickups, classes - and they say themselves that products sell out weekly
Source on file: heritagerisesourdough.com (opened 2026-10-11) (2026-10-11).

## 2. What their web presence actually is
GoDaddy site with a shop tab but pickup is 'By Appointment' for all seven days; Featured Products block renders empty; cottage-food licence PR 160389-A in the footer
Found live: heritagerisesourdough.com
Contact: Owner@heritagerisesourdough.com (on their own Contact block) · 9806 Lucca Way, Elk Grove CA 95757 · (279) 282-5409

## 3. The design I'd ship
- **Template:** artisan · **palette:** Cocoa nib, ember, cream — `#2a1f1a ink / #a8562a accent / #f7ece1 paper / #6b4b36 muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer → **gallery: 9 shots, client-shot, I direct remotely**
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Butter Croissant $2.40 · viennoiserie · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “Heritage Rise Sourdough — the loaf people queue for” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why we check it on day 1.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi Heritage Rise Sourdough team — I looked at heritagerisesourdough.com this morning. GoDaddy site with a shop tab but pickup is 'By Appointment' for all seven days; Featured Products block renders empty; cottage-food licence PR 160389-A in the footer.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 1165 $, delivered in 5 days. The files and repository are yours; optional ongoing services are separate. Includes photo.
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
4. Content deadline 7 days · build in this kit on branch `client/45-heritage-rise-sourdough` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

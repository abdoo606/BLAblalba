# Daily Bread Sourdough Bakery — design board & pitch

Madison, OH, US · A — hot · template **artisan** · baguette · 1130 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Opened a storefront on 22 Nov 2025 at 50 W Main St (Madison Village) after roadside and farm-store selling; owner is explicitly planning more ovens for wholesale
Source on file: news-herald.com 30 Jan 2026 + dbsourdough.com (opened 2026-10-11) (2026-01-30).

## 2. What their web presence actually is
One-page Squarespace site: hero photos and a PRE ORDER button that sends customers to Hotplate (a third-party marketplace). No hours, no address block, no wholesale or catering page.
Found live: dbsourdough.com
Contact: swarthomestead@gmail.com (published by the News-Herald as the business contact, 30 Jan 2026) · dbsourdough.com · 50 W Main St, Madison, OH · call/text 719-331-2089 · owner Katie Beth Swart

## 3. The design I'd ship
- **Template:** artisan · **palette:** Rye, linen, walnut — `#22201c ink / #8a6d3b accent / #f3efe6 paper / #5d5340 muted`
- **Sections, in order:** hero → marquee → specialties → menu → batch → story → services → gallery → testimonials → hours → order → faq → footer
- **Languages:** en
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf $5.80 · bread · Baguette De Tradition $1.60 · bread · Seeded Rye Brick $6.40 · bread · Butter Croissant $2.40 · viennoiserie · Pain Au Chocolat $2.70 · viennoiserie · Morning Bun $3.20 · viennoiserie
- **Hero line:** “Daily Bread Sourdough Bakery — the loaf people queue for” — one language, so it stays human.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/artisan/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi Daily Bread Sourdough Bakery team — I looked at dbsourdough.com this morning. One-page Squarespace site: hero photos and a PRE ORDER button that sends customers to Hotplate (a third-party marketplace). No hours, no address block, no wholesale or catering page.
> That's exactly the part I build: hero, marquee, specialties, menu — a one-time project fee of 1230 $, delivered in 5 days. The files and repository are yours; optional ongoing services are separate. Includes seo.
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
4. Content deadline 7 days · build in this kit on branch `client/46-daily-bread-sourdough-bakery` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

# Chatsworth Bakehouse — design board & pitch

London (Crystal Palace), GB · A — hot · template **moderno** · croissant · 2090 €
Verified 2026-10-11: **YES**

## 1. Why them, now
Destination bakery people cross London for; Good Food Guide 2026 list; sandwiches and pastries sell out daily
Source on file: londonyaar.com — 15 best bakeries in London to visit in 2026 (2026-08-16).

## 2. What their web presence actually is
MERGED: this lead was in the original award-based list (row 2) and I re-added it today as "new" (row 39) - duplicate removed 2026-10-11, one email sent in total. Homepage: two addresses both pointing at the SAME Google Maps query for 120A, split opening blocks (116 walk-in Wed-Fri 12.30-4, Sat 11-4; 120a pre-order collection Weds-Fri 12.30-4 + Sat slices from 1pm), a sandwich pre-order on a separate order. subdomain, and a Kickstarter link as the about page. Bread/pastry pre-order, stock visibility and per-address hours are the gaps.
Found live: https://www.chatsworthbakehouse.com (Squarespace)
Contact: hello@chatsworthbakehouse.com (on their homepage) · 116 + 120A Anerley Rd SE19 2AN

## 3. The design I'd ship
- **Template:** moderno · **palette:** Concrete, ember, steel — `#101314 ink / #e2622a accent / #f4f5f4 paper / #40535c muted`
- **Sections, in order:** hero → specialties → menu → batch → story → services → gallery → hours → testimonials → order → faq → footer → **pre-order basket → WhatsApp** → **per-location hours & stock**
- **Languages:** en, 1 more: FR · PL · RO · ES — pick the one your street actually speaks
- **Menu to enter (their real items, from their own posts):** Country Levain Loaf £5.80 · bread · Baguette De Tradition £1.60 · bread · Seeded Rye Brick £6.40 · bread · Butter Croissant £2.40 · viennoiserie · Pain Au Chocolat £2.70 · viennoiserie · Morning Bun £3.20 · viennoiserie
- **Hero line:** “Chatsworth Bakehouse — what the whole street talks about” — written once, mirrored in the second language, never machine-translated.
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why this is clause 1 of this project.
- **Live preview:** `dist/templates/moderno/index.html?lang=en` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, email)
> Hi Chatsworth Bakehouse team — I looked at https://www.chatsworthbakehouse.com (Squarespace) this morning. MERGED: this lead was in the original award-based list (row 2) and I re-added it today as "new" (row 39) - duplicate removed 2026-10-11, one email sent in total. Homepage: two addresses both pointing at the SAME Google Maps query for 120A, split opening blocks (116 walk-in Wed-Fri 12.30-4, Sat 11-4; 120a pre-order collection Weds-Fri 12.30-4 + Sat slices from 1pm), a sandwich pre-order on a separate order. subdomain, and a Kickstarter link as the about page. Bread/pastry pre-order, stock visibility and per-address hours are the gaps.
> That's exactly the part I build: hero, specialties, menu, batch — a one-time project fee of 1795 £, delivered in 7 days. The files and repository are yours; optional ongoing services are separate. Includes preorder + multi-location.
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
4. Content deadline 7 days · build in this kit on branch `client/2-chatsworth-bakehouse` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week

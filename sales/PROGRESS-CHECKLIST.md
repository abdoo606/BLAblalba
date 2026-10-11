# PROGRESS-CHECKLIST — the whole pipeline, one page, self-updating

Run `node tools/progress.mjs` (or `npm run progress`) any time. It reads `sales/OUTREACH-LOG.csv` and
`sales/pitches/INDEX.md`, prints the funnel, and tells you the next action per lead — including the sentence
to say. Nothing here is manual bookkeeping except the one column that changes when something happens:
`status` in `sales/OUTREACH-LOG.csv`.

## 0. The gate that comes before every other line (read this first)

> **Where we are (2026-10-11, after verification batch 2):** 134 leads · **31 looked at by us (site opened)** · 18 with a real email - all of them sent ·
> **18 SENT** (34,504 € quoted) · 0 human replies · 1 auto-reply (ARAN) · 0 bounces · 3 verified leads reachable only by phone/DM (Pa Serra, Handy,
> Weltons) · 59 rows still unverified. One duplicate caught and merged (Chatsworth Bakehouse was on the original
> list *and* re-added as new) — `tools/make-sheet.py` now refuses to build a sheet with duplicate shop names.
> `npm run progress` regenerates this picture; `npm run sheet` rebuilds the Drive CSV from the prospects file.

Three things must exist **before the first email leaves**, and none of them is technical:

1. **A payment route that actually lands.** *Settled on 2026-10-11:* the client pays by **bank transfer in EUR
   by default**, or by **USDT at the euro amount written on the invoice — only when that client has agreed to
   it**, asked at quote stage and never in a cold email. Full rule-sheet in `sales/PAYMENTS-USDT.md` (fix the
   rate on the invoice date, write the tx hash on the receipt, TRC-20/BEP-20 before ERC-20, declare it as
   ordinary income, screen your own address, and if their accountant says no you take the transfer without
   argument). Stripe / PayPal / Wise do not serve Syrian residents and a wire to a Syrian bank can die at the
   correspondent bank — which is precisely why the crypto option is offered *as an alternative*, not as the
   only door. What has **not** changed: no fake EU entity, no borrowed IBAN, no hiding Homs on the paperwork.
   If the first real payment cannot be received, the honest move is to pause outreach and fix the rails.
   **One-time task before the next quote goes out:** 30-60 minutes with a sanctions-aware accountant, and one
   test transfer of ~20 € between your own wallets so you know the fee and the arrival time in advance.
2. **A mailbox with your real name.** `abdulrhmant948@gmail.com` currently has no display name → set it to
   `Abdulrhman Thali` in Gmail → Accounts → "When sending a message" (5 minutes, non-optional).
3. **One honest sentence about who you are** in the signature: freelance web developer, Homs, Syria. Small
   bakeries don't care where you live; their *accountant* might, and finding out at invoice time is how a yes
   becomes a no.

## 1. Per-lead states (the vocabulary, so the log means the same thing every time)

| status | meaning | who moves it |
|---|---|---|
| `to-verify` | on the list, never looked at | start here |
| `DISPUTED` | could not confirm the business exists / the note doesn't match reality | stop; find the real shop or drop the row |
| `verified-ready` | exists, channel confirmed, pitch written | `sales/pitches/<lead>.md` is ready |
| `draft-in-gmail` | message prepared, waiting for you | you review |
| `sent` | delivered | you (or me, when you say so explicitly) |
| `replied-interested` | they wrote back | me: classify + draft the answer |
| `call-booked` → `scoped` | 12 questions answered | you on the call, me writing the notes |
| `quoted` | one-page quote sent, valid 21 days | me |
| `won` | deposit invoice paid | you |
| `lost` / `parked(2026-11)` / `do-not-contact` | closed | me, with one line why |

## 2. The loop, in order

- [ ] **Existence check** — Google `"«name»" «city»` + open their site/Instagram. Write the date in `verified`.
- [ ] **Channel** — only an address they published. If none: phone script from the pitch file, call 13:30–15:30 local.
- [ ] **Sentence** — the pitch file's §4. If any word in it isn't true today, fix it, don't send it.
- [ ] **Send** — 5–10/day, one by one, mailbox with your display name. Log `sent` + date immediately.
- [ ] **Reply ≤ 4h** — answer with the 3 tiers and the middle one recommended; ask for their VAT number only in
      the *second* exchange (wave-2 leads).
- [ ] **Scope** — 12 questions (`sales/REPLY-PLAYBOOK.md` §4). No quote without them.
- [ ] **Quote + deposit** — `sales/QUOTE-TEMPLATE.md` → `sales/INVOICE-TEMPLATE.md` variant per wave.
- [ ] **Domain** — `curl https://rdap.org/domain/<name>`, then client registers it **in their name**; we hand over
      the DNS records, SPF/DKIM/DMARC, and a written note of who owns the account.
- [ ] **Design** — the pitch file's §3 becomes the build; branch `client/<lead>`, theme + palette already chosen.
- [ ] **Live + care** — handover doc, Google listing hours corrected, care plan signed the same week.
- [ ] **Housekeeping** — suppression list, delete silence > 3 years, invoices numbered without gaps, 7-year archive.

## 3. What to say, by stage (the crib)

| They are… | You say (one breath, then stop) |
|---|---|
| at the phone | “I'm not selling anything today — I looked at your page and your Google listing show different hours. If someone fixed that for you in a day, would that be worth a conversation?” |
| replying “how much?” | the three tiers, one line each, middle recommended, “I confirm the exact price after 10 minutes of questions — tomorrow 14:00 or 16:00?” |
| replying “not interested” | “Understood — I'll take you off my list. Good bakes.” *(and mean it)* |
| “my nephew can do it” | “Great — here's the repository; if you want the menu entered properly it's 180 € and you keep every file.” |
| “send portfolio” | the demo link + “it's my first product line, so I priced it like it needs to prove itself — test the basket on your phone.” |
| “we already have a site” | agree, then narrow to one page: menu + pre-orders in their second language, and name the smaller price. |
| “where are you based?” | “Homs, Syria — I work remotely and I invoice without VAT; if your accountant needs an EU entity, tell me and I'll save you both the time.” |
| “can you take payment by card?” | “The card account has to be yours (Stripe is fine on your side); my invoice is a bank transfer.” Never pretend you can take cards. |

## 4. What I will not do, so you can plan around it

Mass-send from your Gmail without a per-lead read; invent or scrape emails; quote a price that isn't in
`sales/drive-clients-pricing.csv`; register a domain in your name; sign anything; take a call; sit between
turns watching your inbox (ping me with “check replies” and I do it in the same minute).

## The 103 to-verify queue — how it is being worked (started 2026-10-11)
Verification is the bottleneck, not writing. One unit of work = one shop: open their own site, paste what the
page says into `audit_note`, record the published email in `contact_verified`, set `verification` to
`VERIFIED 2026-10-11`, then `node tools/make-pitches.mjs` + `python3 tools/make-sheet.py`. If an address was
published on their own page, it is sent the same morning; if not, the row becomes a phone/DM row and stays unsent.
Order of work: (1) Britain's Best Loaf 2026 medallists and GFG 50 Best 2026 entries in Great Britain,
(2) the 2026 US state picks, (3) older to-verify rows. Batch 1 is done: Imma The Bakery (verified → emailed)
and Sea Wolf Bakers (verified → no pitch, their stack is ahead of ours). Nothing is sent from a press list
without the site being opened first, and the numbers in `README.md`, `sales/OUTREACH.md` and the register PDF
are regenerated from the CSVs - `python3 tools/make-register.py` - never typed.

# PROGRESS-CHECKLIST — the whole pipeline, one page, self-updating

Run `node tools/progress.mjs` (or `npm run progress`) any time. It reads `sales/OUTREACH-LOG.csv` and
`sales/pitches/INDEX.md`, prints the funnel, and tells you the next action per lead — including the sentence
to say. Nothing here is manual bookkeeping except the one column that changes when something happens:
`status` in `sales/OUTREACH-LOG.csv`.

## 0. The gate that comes before every other line (read this first)

Three things must exist **before the first email leaves**, and none of them is technical:

1. **A payment route that actually works from where you live.** You are in Homs. Stripe / PayPal / Wise /
   Revolut do not serve Syrian residents, and a wire from a US/UK/EU bakery to a Syrian bank is very likely to
   be rejected by the correspondent bank even though nothing about your service is prohibited. Until a client
   can pay you, outreach is practice. Realistic options, in order of how clean they are:
   - a registered company or sole proprietorship in a country where you can lawfully bank and invoice (this is
     the standard route for Syrian freelancers; do it with an accountant who has done it before, not DIY);
   - a payment platform that covers your situation (some work via a foreign entity + local payout rules);
   - an EU/UK-based partner who invoices on a real contract with you underneath.
   What I will not do: put a Dutch address or a Dutch company on the paperwork to make the invoice look
   easier — that's the kind of shortcut that turns a €2,000 website into a frozen account and a fraud question.
   And I won't tell you how to route around sanctions; that's a one-hour paid conversation with a sanctions-aware
   accountant (search "Syria freelancer payments OFAC" and you'll see why they'll want details).
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

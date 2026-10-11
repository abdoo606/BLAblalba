# Tax scope — where this business is allowed to bill you, and what "no extra tax" really means

> ## ⚠️ Status override, 2026-10-11
> You told me you live in **Homs (Syria), Karm El-Zeitoun** — not in the Netherlands. If that is your tax
> residence, then **everything below under “What you DO owe (all of it in the Netherlands)” does not apply to
> you**: no Dutch BTW, no KOR, and no ICP listing, because those are obligations of an entrepreneur
> *established in the Netherlands*. What applies instead is the simpler shape:
>
> | Buyer | Your duty as a Syria-based independent |
> |---|---|
> | EU business (FR, ES) | **None in their country.** Place of supply = the customer's country, so *they* self-account VAT (art. 44 + art. 196 Directive 2006/112). You never register, never file, never charge VAT. If they are not VAT-liable (franchise en base / módulos) they still owe it and cannot reclaim — say so in the quote. |
> | UK business (GB) | Same mechanics: the UK customer reverse-charges; HMRC's manual VATPOSS14700 confirms an overseas supplier with no UK establishment has **no liability to register in the UK**. |
> | US business | No VAT exists. Services performed wholly outside the US are foreign-source for the customer's side; they may ask for a **W-8BEN** (never sign a W-9). |
> | Your own income tax | Whatever Syria requires of you. That's the one return in this whole pipeline — and the only place your numbers actually go. |
>
> **Two things this does not solve, and I won't paper over:**
> 1. **Getting paid.** Stripe/PayPal/Wise/Revolut don't serve Syrian residents, and correspondent banks
>    routinely reject transfers to Syrian banks even for lawful services (web design for a bakery is not a
>    sanctioned supply under EU Reg. 36/2012 or the US Syrian Sanctions Regulations — the friction is bank
>    over-compliance and the absence of rails, not a prohibition on your work). Some EU/US buyers' own
>    compliance policy will still refuse to contract with a Syria-based vendor. Fix: talk to an accountant who
>    has actually set up payment + entity structures for Syria-based freelancers **before** promising a client
>    "I'll invoice you next week". I won't invent a Dutch entity or a Dutch address to make it look easier, and
>    I won't help route around sanctions — those two shortcuts cost more than every €1,450 site in this list.
> 2. **Never claim to be somewhere you aren't.** Your signature must say Homs, Syria (or an entity you really
>    own). Misstating the sender's identity is exactly the thing that makes B2B cold email illegal in France
>    (L.34-5 requires clear identification) and unprofessional everywhere else.
>
> *If you do in fact hold Dutch residency and a KVK registration and the Homs address is family*, tell me and I
> will flip this file back to the NL version below (which is written out in full for exactly that case).

Subject: **Abdulrhman Thali, freelance web developer, Naaldwijk, The Netherlands** (sole proprietor / eenmanszaak).
Checked 2026-10-10 against HMRC's own manual, CRA guidance, Belastingdienst/impots.gouv.fr and Dutch invoicing
guides. This is a working rule-sheet, not a tax opinion: one 45-minute call with a boekhouder (~€120) confirms
it against your actual KOR/btw status. **The whole point below: as long as you work from the Netherlands, no
country in our 36-lead list can make you register for tax, file a return, or pay VAT there.** Three real
duties exist — and two of them are paperwork, not money.

## The one rule that keeps all of this true

> **Do the work from the Netherlands. Do not perform the service on the client's premises.**

Income from services is sourced where the *work is done*. A non-resident performing services entirely outside
the US owes no US federal tax and no US withholding (IRS general rule; foreign-source under IRC §861) — but
the moment part of the service is performed inside that country, *that part* becomes local-source and can be
taxed there. Same logic in the UK, Canada and France.

So the things that would create foreign tax are exactly the things that feel "nice": flying to Charleston for
a photo shoot, two weeks on site in Newcastle, renting a desk at the client's bakery, hiring a local
subcontractor who bills you. **Decline them politely and sell the photo pass as a client-shot kit** (we already
have a €320 "photo pass" — reframe it as "you photograph, I direct: shot list + lighting notes over a 20-minute
call, then I retouch"). No on-site work = no permanent establishment = no foreign filing.

## What you DO owe (all of it in the Netherlands)

| Duty | What it is |
|---|---|
| **Inkomstenbelasting** | Box 1 income tax on profit, in NL, on all of it — whoever the client was. No way around it and nothing foreign about it. Self-employed deductions (zelfstandigenaftrek €1,200 in 2026, urencriterium 1,225 h) are on the table if you qualify. |
| **BTW position** | If your turnover stays ≤ €20,000/yr you can apply for the **KOR** (kleineondernemersregeling): no BTW charged, no BTW returns, no reclaim of input BTW, note on every invoice *"Vrijgesteld van btw op grond van de kleineondernemersregeling"*. Since 2025 you can leave the KOR at any time. Since 2025 there is also an **EU-KOR** up to €100,000 EU-wide. Decide with the boekhouder *before* the first invoice, because it changes the invoice text. |
| **ICP listing** (only for EU sales) | B2B services to a business in another EU country must be reported on the *opgaaf intracommunautaire prestaties* (ICP). It's a nil-tax listing of amounts and the customer's VAT number — not a payment. UK/US/CA sales are **not** in the ICP. |

## Per-country verdict for the 43 leads (6 verified, 3 emailed 2026-10-11)

| Wave | Countries | Verdict for you | What the invoice says |
|---|---|---|---|
| **1 — send freely** | **US** (12) + **GB** (16) = **28 leads, 64,746 €** | No VAT in scope, no registration, no filing abroad. US: services performed abroad are foreign-source → no withholding (send a W-8BEN if their AP asks; never sign a W-9). UK: HMRC's own manual says the overseas supplier has **no liability to register in the UK** and the customer accounts for VAT under the reverse charge, whether or not they are VAT-registered. Canada: a non-resident **not carrying on business in Canada** does not register for GST/HST, and services performed wholly outside Canada are generally outside GST/HST. | *"Place of supply: [customer's country]. No VAT charged — reverse charge / outside the scope of Dutch BTW."* Bill in EUR, or in £/$ at the rate in the quote. |
| **2 — fine, needs their VAT number** | **FR** (7) + **ES** (8) = **15 leads, 30,689 €** | EU B2B → **btw verlegd / reverse charge**: the client accounts for local VAT in their own return; in most cases they reclaim it, so it costs them nothing. You charge no Dutch BTW, but you must list it in the ICP and put **their VAT number** on the invoice (verify in VIES). | *"BTW verlegd — VAT reverse charge, art. 196 Directive 2006/112/EG. Klant-Id: [their VAT number]."* |
| **3 — hold, ask first** | *not present in this list* (would be French **DOM**: Réunion, Guadeloupe, Martinique — and CH/NO if we widen it) | The DOM are inside the EU customs union but **outside the EU VAT territory** (art. 6 Directive 2006/112), with their own TVA (8.5 % / 2.1 %) under art. 294 CGI, and DOM businesses have **no intracommunity VAT number**, so the clean EU mechanics don't line up. | Don't invoice until the boekhouder answers. Contacting them is harmless — just no quote yet. Same care for Canada (a non-resident **not carrying on business in Canada** need not register for GST/HST, and services performed wholly outside Canada are generally outside it) and for Switzerland/Norway (own VAT regimes, thresholds there). |

### The trap in wave 2 that will actually cost a client money

A lot of these bakeries are *not* VAT-liable: French `micro-entrepreneur` under *franchise en base*, Spanish
autónomo in *módulos*, Greek small regime. Reverse charge still applies (they are businesses), but **they
cannot reclaim the VAT** — so a €1,450 site really costs them €1,450 + €290 out of pocket, and they will feel
tricked if they learn that at invoice time. Handle it in the quote, in one line:

> *If you are not VAT-registered (franchise en base / módulos), you will self-account 20 % TVA on this invoice
> and cannot recover it — so budget 1,740 € rather than 1,450 €. Tell me and I'll note it on the quote.*

That single disclosure is worth more than a discount: nobody else selling to village bakeries mentions it.

## Order of work, rewritten around tax (this is what I applied to the Drive sheet)

1. **Wave 1 first — US + UK: 28 of 43 leads, 64,746 € of the pipeline (95,435 € total), zero foreign administration.** No VAT
   in scope for you, no ICP, no return to file anywhere but the Netherlands. **And the two verified email
   addresses we have (August Bakery, Northern Rye) are both UK** — so the only two cold emails that can go out
   today are also the two cleanest ones tax-wise. Weltons (US, James Beard finalist, phone only) belongs to this
   wave too: it's a call at 13:30, not an email.
2. **Wave 2 next — FR (7) + ES (8): 30,689 €, legal and duty-free, but needs two things.** Their VAT number
   before invoicing (ask in the *second* reply, not the first — asking for a fiscal number in a cold email reads
   like a scam), and your ICP listing in the Netherlands. *"Pour la facture, envoyez-moi votre numéro de TVA
   (ou dites-moi si vous êtes en franchise en base)."*
3. **Wave 3 — nobody in today's list is here.** Keep the rule for when the list grows (DOM, CH, NO, and CA
   if we ever chase Montréal).

## Five habits that keep the file boring

1. **Number invoices sequentially with no gaps**, forever (Dutch requirement, and the one auditors check first).
2. Never put your `omzetbelastingnummer` (it contains your BSN) on an invoice — only the **btw-id**
   `NL123456789B01` plus your KVK number.
3. Keep the client's country, their address and their VAT ID on every cross-border invoice; without them the
   reverse charge can be reversed *onto you* with Dutch BTW added retroactively.
4. Invoice in EUR where possible. £ and $ are fine, but fix the rate in the quote and on the invoice, or a
   "€1,450 site" becomes a negotiation.
5. Say **no to marketplace/PayPal-goods invoicing** ("just bill it as a product so it's easier"): that is how a
   service export becomes a taxable goods sale with customs, octroi de mer, and a VAT number you don't have.
   One service invoice, one line item, always.

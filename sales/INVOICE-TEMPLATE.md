# Invoice template (EN/NL/FR/ES header) — one file, three VAT variants

Keep the layout identical for every client; only the VAT block changes. Sequential numbers, no gaps, ever.

```
FACTUUR / INVOICE / FACTURE / FACTURA                Nº  2026-001
Abdulrhman Thali — freelance web developer
Naaldwijk, The Netherlands
KvK : [8 digits]        BTW-id : NL[000000000]B01
IBAN : NL[.. ....] .... ....   BIC : .......
Invoice date : 2026-10-..      Date of supply : 2026-10-..
Bill to : [BAKERY LEGAL NAME], [street], [city], [country]
Client VAT ID : [FR12345678901 / ESB1234567A / GB999 9999 99 / n.a.]

Description                                                     Amount
Website build — [Package], [n] languages, pre-order basket       X.XXX,00
Add-on: local SEO listing pass                                     380,00
Add-on: photo direction pass (remote)                              320,00
Care plan, 12 months prepaid                                       540,00
                                                          _______________
                                                          Total          X.XXX,00
                                                          BTW omgezet   0,00
                                                          Due            X.XXX,00

Payment : within 14 days. 40% deposit received on [date] : [amount].
Settled in : bank transfer in EUR  /  USDT on [date], tx [hash], 1:1 against the EUR amount above
              (whichever the client agreed to on the quote - see sales/PAYMENTS-USDT.md)
```

## Pick exactly one VAT block

**A — customer in the EU, VAT-registered (FR / ES / GR)**
```
BTW verlegd — VAT reverse charge.
Klant is belastingplichtig in [land]; art. 196 Directive 2006/112/EG.
Geen Nederlandse BTW berekend. / No Dutch VAT charged.
```
→ Then: list this invoice on the Dutch **ICP (opgaaf intracommunautaire prestaties)**. No tax to pay, one nil
listing. If their VAT number is missing or invalid in VIES, do **not** send the invoice — you'd owe 21 % Dutch
BTW on it yourself.

**B — customer in the US / UK / Canada (wave 1)**
```
Place of supply : [United States / United Kingdom / Canada] — outside the EU.
No VAT charged. UK customer: UK VAT is accounted for by the customer under the
reverse charge (VATA 1994 Sch. 5 / Notice 828). US customer: no US sales tax applies to
professional services performed wholly outside the United States; foreign-status form
W-8BEN available on request (do not sign a W-9). Canadian customer: non-resident not
carrying on business in Canada, no GST/HST registered — none charged.
```

**C — you are in the KOR (≤ €20,000 turnover)**
```
Vrijgesteld van btw op grond van de kleineondernemersregeling (KOR).
No VAT line, no 0 % line, no gross/net split — just the amount.
```
Never write "0 % BTW" under KOR: it reads as a zero-rated supply, not an exemption, and it invites a question.
If you are in the KOR, the amounts you bill to EU clients still need a chat with the boekhouder about the ICP
and the EU-KOR (€100,000 EU-wide ceiling).

**Réunion / any French DOM** — hold until the boekhouder confirms (art. 294 CGI, local TVA 8.5 %, no
intracommunity VAT number). Do not use variant A for them.

## Housekeeping that prevents 90 % of invoice arguments

1. One line item per agreed thing. No "various adjustments".
2. The quote number appears on the invoice; the invoice number appears in the email subject.
3. Attach the 1-page T&Cs (`sales/TERMS.md`) to the deposit invoice, not at delivery — whoever signs first
   reads them.
4. Late payment: statutory B2B terms — interest at the legal rate plus **€40 fixed recovery cost** (Directive
   2011/7/EU). Say it once, in the T&Cs, not in an angry email.
5. If they pay by card via a link, the processor's fee is theirs or stated, never silently absorbed at 2.9 % —
   it's the difference between a €1,450 job and a €1,408 job you already told them about.
6. Save every invoice as `2026-001-bakeryname.pdf`; keep 7 years (Dutch retention rule).

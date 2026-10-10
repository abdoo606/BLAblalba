# Compliance — what is legal, what is not, and the line I will not cross

Checked 2026-10-10 against public guidance (CNIL/RGPD doctrine, L.34-5 CPCE, CAN-SPAM, UK PECR/ICO).
This is a working checklist, not legal advice: for a real contract and for VAT status in your country,
ask an accountant once — it costs less than one lawsuit.

## 1. Cold outreach by email — allowed, with conditions

| Where | Rule for B2B email to a business | Mandatory in every message |
|---|---|---|
| **France** (and most EU) | Lawful **without prior consent** (opt-out) under legitimate interest, art. 6.1.f RGPD + art. L.34-5 CPCE, *provided* the offer relates to their professional activity | Real identity of the sender · a free, immediate way to object (“reply *stop*”) · data collected lawfully |
| **Generic addresses** `contact@`/`info@` | Not personal data in French doctrine → most comfortable channel for a small shop | same as above |
| **UK** | Permitted to **corporate bodies** under PECR (the consent rule bites for sole traders/individuals, not limited companies) | identity + unsubscribe; respect objections |
| **US / Canada** | CAN-SPAM: no consent needed for B2B, but **a valid physical postal address is required**, no deceptive subject/headers, opt-out honoured within 10 business days. Canada (CASL) is stricter — opt-in | full postal address in the footer · working opt-out · truthful subject |
| **Sole traders / micro-entrepreneurs** | Grey zone: many are legally “individuals”, so treat them closer to the B2C rule — phone, a DM, or a visit beats a cold email | prefer non-email first touch |

Extra French note: the anti-harassment call law that entered into force **11 August 2026** targets
*consumers*; B2B calls to a professional line remain under legitimate interest. And keep in mind:
**you may not** buy a prospect list, harvest personal addresses of the owner's private mailbox, or send
from a fake identity — CNIL fines go up to €20M or 4 % of global turnover.

## 2. Records you must keep (nobody does this, everybody should)

- A log: who was contacted, when, from which public source, what was said. → `sales/OUTREACH-LOG.csv`
- A **suppression list kept forever** (the point is not to re-contact someone who said no — re-contacting
  an objector is the fastest way to a complaint).
- Prospect data deleted after **3 years** of silence (CNIL doctrine).
- GDPR art. 14: because we collected their address *indirectly*, the first message must say who we are,
  where the address came from, and how to object — one sentence does it:
  > *Je vous écris parce que [boutique] apparaît dans [source]. Vos coordonnées professionnelles sont
  > publiques. Vous pouvez vous opposer à tout moment à ces messages en répondant « stop ».*
- A short privacy notice page on our own site (hosting the demo is already enough to need one).

## 3. Sending mechanics (where accounts actually die)

- 1:1 personalised messages from a normal mailbox: **max 5–10/day**, unique body, no attachments in the
  first message, no link shorteners, SPF + DKIM + DMARC configured on the sending domain.
- Do **not** push this list through Mailchimp/Brevo/HubSpot marketing: their ToS require opt-in and they
  suspend accounts for purchased/scraped B2B lists — the platform rule is stricter than the law.
- A domain used for outreach should be a **secondary domain** you are willing to burn, not your main one.
- WhatsApp/Instagram DM: fine for a first touch, but no broadcast lists, no automated blasts — Meta bans
  the number, and a bakery owner seeing a bot message is a lost referral.

## 4. The pitch itself — truth rules

- ✅ “Votre site est en une seule langue”, “il n’y a pas de précommande”, “vos horaires sur Google ne
  correspondent pas à votre page” — all checkable, all said politely, all verified before we write it.
- ❌ “Votre site est nul”, “vos clients vous quittent à cause de ça”, “votre concurrent X nous a engagé”,
  “il ne me reste que 2 créneaux” (fake scarcity), “nous sommes partenaires de [prix James Beard/M6]”.
- ❌ Never use their **brand name in the subject line** as if we were affiliated: “à propos de la
  Page du Marché” is fine, “[Brand] × OurStudio” is not.
- ❌ No press photos, no images from their Instagram in our proposals or our own marketing without asking.
  Our demo uses our own generated imagery — keep it that way until they sign.
- Mentioning that they won an award, in a private proposal, as a fact with a source: fine. Building an ad
  around it: not fine.

## 5. Money and contract

- Written quote valid 21 days, with **what is excluded** listed (that is where disputes come from).
- Deposit 40 % before work, balance at go-live, late-payment terms stated.
- VAT: if you are under the *franchise en base* threshold, invoice “TVA non applicable, art. 293 B du CGI”
  (FR) — say it on every quote, and register for VAT when you pass the threshold. UK/US clients: no EU VAT
  on services to a VAT-numbered business — get their number.
- **Domain and hosting belong to the client**, in their name, on their email, with their own 2FA. If we
  pay for it first, we disclose that, bill it at cost (+ €25 admin), and transfer the registrar account
  within 7 days. Never register it in our name to keep them “sticky” — that is both bad practice and, in
  several countries, an abusive clause.
- When we handle their customers' data (pre-order basket → their WhatsApp/email), we are a processor:
  no retention on our side, no analytics cookies without consent banner, and a one-paragraph DPA clause
  in the contract.
- Professional indemnity insurance (RC Pro / E&O) before the third paying client.

## 6. What I (the agent) will not do — and why

| Request | My answer |
|---|---|
| “Send 36 cold emails now” | I will prepare and *queue* drafts, show you each one, and send only after you approve each batch — from your account, in your name, with your legal identity. I need real name + studio + postal address first, otherwise the message is illegal in the US and sloppy everywhere. |
| “Negotiate for me, promise a date” | I draft, you decide. A contract and a delivery date are commitments in your name. |
| “Answer the phone / sit a meeting” | I can't. I can prep a call sheet and write the follow-up within a minute of your notes. |
| “Buy the domains” | I can't pay and I can't be the registrant. I can check availability (RDAP/DNS), prepare the exact registrar basket, DNS zone, SPF/DKIM/DMARC records and the transfer email. |
| “Say their site is terrible” | Never in writing. Verified facts only. |

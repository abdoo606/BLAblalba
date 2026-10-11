# Compliance review — conditional, not a guarantee · 2026-10-11

**Status: sending paused.** This is a working review of official published guidance, not a legal opinion, approval of previous sends, or a promise that a message is lawful in every jurisdiction. Rules can depend on the actual sender, recipient, routing, entity, consent, data processing and transaction. No substitute nationality, city, company, phone or address is allowed.

## What changed

- Marketing signatures no longer contain provider locality. Real identity and a working reply/opt-out route remain. Where lawful disclosure is required in billing, contracts, tax, privacy or payment/KYC, provide truthful information or decline the transaction; do not conceal it.
- US recipients are permanently removed from this campaign by the user's instruction. Canada is permanently blocked from future imports. These are **user exclusions**, not invented recipient opt-outs.
- Remaining markets are research/draft-only until recipient entity/consent, contact purpose, privacy information and sender-side obligations are documented. A business-looking email address is not proof of corporate status.
- Old sent copies were moved to Gmail trash at the user's request. This does not edit, recall or erase recipients' copies, or establish retroactive compliance. New copy is draft-only and must not be replayed as a fresh first contact.

## Official rules relevant to the decisions

| Market | Published guidance | Campaign action |
|---|---|---|
| US | CAN-SPAM covers commercial messages including B2B, requires truthful headers/subjects, advertisement identification, a valid physical postal address and opt-out. The address rule is not a requirement to state nationality. [1](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) | Permanently excluded; do not remove a mandatory footer or invent a local mailbox. |
| Canada | CASL generally requires consent, identifying information and unsubscribe; its mailing-address guidance permits real alternatives such as a PO box. Public publication is not a broad licence to send, and requirements must be assessed case by case. [1](https://crtc.gc.ca/eng/com500/faq500.htm) | Permanently excluded from this no-address campaign, including future imports. |
| UK | Corporate-subscriber email differs from sole traders/ordinary partnerships. Unknown subscriber status should be treated as individual; public contact details alone do not supply the consent required for individuals. Identity and a valid opt-out contact remain required. Named contact data may engage UK GDPR. ICO also flags that guidance is under review after legislative changes. [2](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/) | Hold until corporate status or appropriate consent and privacy/source review are documented. No blanket UK/B2B exemption. |
| France | CNIL distinguishes professional relevance/information/objection from prior consent for consumer marketing; sender identity and a simple objection route remain necessary. [2](https://www.cnil.fr/en/node/14686) | Hold pending a documented lawful route, information, relevance and privacy review. Do not extrapolate to all Europe. |
| Spain | Article 21 generally prohibits unrequested/unauthorised electronic promotions, with a limited previous-contract/similar-product exception. [3](https://www.aepd.es/documento/2018-0173.pdf) | Hold without documented prior authorisation or an applicable reviewed exception. A public email is not enough. |

Excluding a recipient country **does not prove** that sender-side or other applicable laws disappear. The actual sender-side jurisdictions are not verified in this project. Do not use a phone, DM, intermediary or a second address to bypass a blocked marketing route.

## Billing, tax and payments are separate checks

- EU guidance lists supplier and customer full name/address on a full VAT invoice. The applicable invoice type and obligations require transaction-specific review. [1](https://taxation-customs.ec.europa.eu/taxation/vat/vat-businesses/invoicing_en)
- UK place-of-supply/reverse-charge rules depend on where the parties belong and what is supplied. They do not establish that everybody owes no tax. [1](https://www.gov.uk/guidance/vat-place-of-supply-of-services-notice-741a)
- OFAC's updated guidance reports changes to comprehensive country sanctions while preserving targeted restrictions. This is not an approval of a particular person, bank, transfer, payment provider or contract. [2](https://ofac.treasury.gov/faqs/topic/1571)
- No blanket “no VAT anywhere”, “legal for sure”, unsupported payment-availability assertion, or automatic tax-form selection remains authorised. Sender identity, applicable jurisdictions, tax treatment and a supported lawful payment route must be reviewed before sending a priced proposal or taking a deposit.

## Storage and public history

Repository visibility and Drive sharing must be reviewed before publishing new compiled contact data. A public repository can expose both present records and older Git revisions. Making it private reduces exposure but does not erase earlier public copies, recipients' messages, caches or trash. Technical visibility/ACL checks do not by themselves prove compliance with privacy law. No privacy-storage approval is recorded yet.

## Enforced workflow

`python3 tools/suppression.py` blocks opt-outs, user exclusions and excluded recipient countries. `python3 tools/outreach_policy.py check-send ID` fails closed if any required evidence or approval is missing. An earlier recipient needs separate follow-up approval. The gate is an operational safeguard, not a legal certificate.

If a prospective client makes provider-locality disclosure a condition and the user declines it: exclude that client with reason `user-exclusion`; do not invent an answer or work around the requirement. An opt-out is acted on immediately, without re-pitch or a second confirmation.

# Reply playbook — what happens after the first message

## 1. Statuses (used in `OUTREACH-LOG.csv`, mirrored in the Drive sheet)

`to-verify → sent → opened? → replied-interested → call-booked → scoped → quoted → negotiated →
won / lost / parked(month) → do-not-contact`

Every row gets: date of each step, who replied, exact price quoted, and the source of the contact address.
Nothing goes to `quoted` before the scoping questions below are answered — that is how a €1,450 job turns
into 40 unpaid hours.

## 2. Answer within four hours, then let it breathe

A bakery owner answers between 14:00 and 16:00 (after the lunch rush, before the afternoon bake) and on
Sunday evening. Send Tuesday–Thursday morning, follow up once at day 5, once at day 14, then stop. Two
follow-ups is the professional ceiling; a third makes you the guy from the horror stories.

## 3. The six replies you will actually get

| They write | You send (short — under 90 words) |
|---|---|
| **“Combien?”** | The three tiers with one line each, middle marked *recommandé*, plus: “je confirme le prix exact après 3 questions — 10 minutes au téléphone demain 14h ou 16h ?” Never a long email in exchange for one word. |
| **“Pas intéressé”** | “Compris — je vous retire de ma liste, bonne fournée 🥖.” Then *actually* put them in the suppression list. No “puis-je vous demander pourquoi ?”. |
| **“Faites-vous du Shopify / Instagram / des pubs?”** | “Non, et c'est volontaire : je fais le site et je vous laisse les outils que vous utilisez déjà. Si les pubs sont un vrai besoin, je vous recommande [partner] — sans commission pour moi.” Honesty is the referral engine. |
| **“Mon neveu peut le faire”** | Send the repo link + the 5-minute install note + “s'il préfère que j'entre le contenu, c'est 180 € — et vous gardez tous les fichiers”. You lose the project, you win the goodwill (and 30 % of those nephews quit in week 3). |
| **“Envoyez un portfolio”** | The live demo + the price list + one honest line: “peu de références publiques pour l'instant — voilà ce que le site fait, testez le panier et le compteur vous-même.” Never invent clients. |
| **“On a déjà un site, il marche”** | Agree, then narrow: “parfait — alors l'offre utile est la page menu+précommande dans votre langue, 380 €… non, 1 450 € avec deux langues et WhatsApp. Si ça ne vous intéresse pas, je ne reviens pas.” (Correcting yourself live and lowering is fine; inventing a lower price later is not.) |

## 4. Scoping questions — all twelve, on one call, ten minutes

1. Who opens, who closes, and what actually changes in summer/December? *(hours table)*
2. What sells out, and at what time? *(countdown + “notify me”)*
3. How do pre-orders arrive today — phone, paper, Instagram DM, nothing? *(basket design)*
4. Do you take deposits for cakes? What stops the no-show? *(payment add-on)*
5. What do tourists / the English-speaking neighbours ask you every week? *(language 2)*
6. Who updates the prices, and when do they change? *(content model)*
7. Do you have allergies/gluten-free handling worth saying properly? *(menu tags)*
8. Wedding/event enquiries: how many a month, and where do they get lost? *(form fields)*
9. Wholesale: who are the 5 biggest accounts and how do they order today? *(B2B page)*
10. Do you have Google Business, and are the hours/photos right on it? *(SEO pack)*
11. Who owns your domain and your Instagram password, and when did you last log in? *(access, and the abuse flag if it's an ex-agency)*
12. If I delivered this in 7 days, what would still make you say “not worth it”? *(the real objection)*

## 5. Quote → order flow

1. One-page proposal (their words, five bullets, three prices, what's excluded, 21-day validity).
2. Deposit invoice 40 %, IBAN, SIRET/registration number, T&Cs page number.
3. Kickoff: brand assets + content deadline (7 days) + “photos of the day” slot.
4. Build in the kit → staging link → they test on their own phone, in their language.
5. Two revision rounds written into the price (a third is €90).
6. Go-live: DNS, HTTPS, Google Business link, sitemap submitted, printed counter sheet.
7. Handover doc + training call + care-plan signature in the same week (not a month later).

## 6. Domains — the exact procedure (this is the part clients get burned by)

**The domain is always registered in the client's name, on their email, with their 2FA. We never hold it.**

1. Ask: do they already own it? (`.fr` may sit with an ex-web-designer — WHOIS/RDAP shows the registrar and
   the registrant email. If it's an agency's mailbox, that's a transfer, not a purchase — tell them now.)
2. Check availability (no account needed): `curl https://rdap.org/domain/example.fr` → 404 = free, 200 = taken.
   For `.fr`, AFNIC also has `https://www.afnic.fr/outil/whois`. `.es` → `https://www.dominios.es`.
3. Prefer the client's own registrar (OVH/Infomaniak/Cloudflare/Porkbun). Ours is irrelevant to them.
4. Buy → set auto-renew ON → set registrant email = client's → transfer the login to them in writing →
   we keep only a **technical contact** + a delegated “DNS management” access where possible.
5. DNS: `A`/`CNAME` to the host, `www` CNAME, MX for their mail, SPF `v=spf1 include:<host> ~all`,
   DKIM from the host, DMARC `p=none; rua=mailto:dmarc@client` for the first 30 days.
6. Order-flow email must be on the same domain (name@bakery) or the WhatsApp handoff — never a Gmail
   address, or their orders land in spam and they blame the site.
7. Document everything in the handover file: registrar, expiry date, who owns the account, support link.
   Send a calendar reminder 45 days before expiry — a lost domain is how agencies get sued.

**If they refuse to hold it themselves:** say no. Offer instead to bill at cost + €25 admin, once a year,
with the account transferred immediately. A €25 admin fee is worth less than your reputation.

## 7. How we work with the agent (me) on this pipeline

- **I can:** verify each lead (site, hours, language gap), write the personalised message, prepare the
  Gmail draft, log every status, read replies when you ping me, draft the answer in their language, quote
  from the price list, check domain availability, produce the proposal and the invoice text, update the
  Drive sheet.
- **Only you can:** press *send* on the first batch, agree a price outside the list, sign, take the call,
  give the bank details, and be the human named in the message.
- The loop: you say “check replies” → I list new messages, classify them, put a one-paragraph summary + a
  ready draft for each → you approve/edit → it goes out from your mailbox. Nothing leaves without you.

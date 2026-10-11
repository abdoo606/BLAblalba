# Data quality / deletion notes · 2026-10-11

## Full removal, not a suppressed sales dossier

One requested opt-out was removed from all active prospect/contact source lists, the active sent-contact export and generated boards. No new pitch or second confirmation was sent. The Gmail conversation was moved to trash and removed from the client label.

Only pseudonymous SHA-256 fingerprints remain in `sales/SUPPRESSION-LIST.json`, for the sole purpose of preventing re-import and any future contact. No name, email address, site, reply quotation or offered price is retained in that suppression record. Hashes are not encryption and not guaranteed anonymity. Git history and Gmail/Drive trash are not erased by this operation. Superseded Drive copies must be trashed after successful replacement.

Commands and deletion regressions: `tools/suppression.py`, `tests/test_suppression.py`. Every outreach generator now refuses blocked source records, and the board generator deletes its own orphaned numeric-prefix files before packaging.

## Corrected price lookup: a shared mailbox is not a unique lead key

Rows 66 (Niedlov's Bakery & Cafe, actual sent quote EUR 2,900) and 73 (Niedlov's Breadworks, no-pitch licence placeholder EUR 149) have the same published mailbox. The old resume and Arabic-register dictionaries let the later discovery row overwrite the contacted row. This understated those reports by EUR 2,751; it did not change the offer that was actually sent.

`tools/outreach_data.py` now prioritises the action log's contacted row over the uncontacted duplicate and refuses two equally active matches. The two discovery rows have **not** been silently merged; review them before any future research or campaign. The English register and log already used the contacted row's price. `tests/test_outreach_data.py` tests both row orders and ambiguous matches.

Standing-offer totals exclude bounced messages as well as removed leads. These totals are hypothetical offers, **not** earned money, signed contracts, payment commitments or verified customer budgets. Historical send counts in current exports exclude the fully removed contact, while the separate suppression counter records that one deletion took place.

## Reply classification

White Horse's receipt acknowledgement dated 2026-10-11T14:33:13Z was booked as automatic. It is not human interest, budget approval or an opt-in. No answer was sent; its existing 2026-10-20 chase date is unchanged. The current active log has five automatic acknowledgements.

## Sales interpretation

An award, a weak site, or a salary comparison does not establish the owner's wealth or available budget. Do not infer that an expression such as "a month's wages" means a recurring fee, especially if the original offer explicitly says there is no monthly charge. Keep the project fee one-time, optional services separate, and prioritise evidence of a relevant commercial need on the shop's own pages.

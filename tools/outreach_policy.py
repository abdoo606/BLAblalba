#!/usr/bin/env python3
"""Single source of sender identity, smaller scopes and fail-closed sending gates.

python3 tools/outreach_policy.py audit
python3 tools/outreach_policy.py check-send LEAD_ID [--follow-up]

This is a prevention checklist, not a legal opinion or a sender. No network send occurs.
"""
import argparse
import csv
import json
import re
from pathlib import Path
from suppression import ROOT, EMAIL, check_sources, is_blocked, load_registry

CONFIG = "sales/OUTREACH-POLICY.json"


def load_policy(root=ROOT):
    policy = json.loads((Path(root) / CONFIG).read_text(encoding="utf-8"))
    if policy.get("version") != 1 or not isinstance(policy.get("send_paused"), bool):
        raise ValueError("Missing or invalid send policy; do not send.")
    sender = policy.get("sender", {})
    if not sender.get("display_name") or not EMAIL.fullmatch(sender.get("reply_to", "")):
        raise ValueError("A real sender name and working reply address are required.")
    if sender.get("marketing_signature_includes_location") is not False:
        raise ValueError("Marketing signatures must not publish provider locality.")
    for key in ("licence", "baguette", "croissant", "patisserie"):
        pack = policy.get("packages", {}).get(key, {})
        if not isinstance(pack.get("price_eur"), int) or pack["price_eur"] <= 0 or not pack.get("scope"):
            raise ValueError("Invalid fixed-scope package.")
    return policy


def package_for(row, policy):
    return policy["packages"][row["package"]]


def money(eur, policy, currency="USD"):
    return round(eur * policy["rates"][currency])


def send_blocks(row, policy, registry, follow_up=False):
    blocks = []
    if is_blocked(row, registry):
        blocks.append("permanent suppression or excluded market")
    if policy["send_paused"]:
        blocks.append("campaign sending is paused")
    if policy.get('storage', {}).get('privacy_storage_reviewed') is not True:
        blocks.append('repository/Drive disclosure and privacy-storage review is pending')
    sender = policy["sender"]
    if sender.get("legal_identity_verified") is not True:
        blocks.append("sender legal identity and applicable jurisdictions are unverified")
    if sender.get("legal_review_status") != "reviewed" or not sender.get("legal_review_reference"):
        blocks.append("sender-side and cross-border legal review is pending")
    if sender.get("tax_review_status") != "reviewed" or not sender.get("tax_review_reference"):
        blocks.append("pricing tax treatment is unverified")
    if sender.get("payment_route_verified") is not True:
        blocks.append("a lawful supported payment route is unverified")
    address = EMAIL.search(row.get("contact_verified") or "")
    if not address or row.get("contact_source_verified") != "yes" or not row.get("contact_source_url"):
        blocks.append("address publication on the business's own page is not fully documented")
    if row.get("contact_purpose") not in {"general-business", "owner-business", "vendor-proposals"}:
        blocks.append("contact purpose is restricted or unverified")
    country = row.get("country", "")
    market = policy.get("markets", {}).get(country, {})
    if market.get("status") == "excluded-permanent" or not market:
        blocks.append("recipient market is excluded or unreviewed")
    basis = row.get("legal_basis", "")
    if country == "GB" and basis == "corporate-subscriber":
        if row.get("recipient_entity_type") != "corporate" or not row.get("legal_evidence_url"):
            blocks.append("UK corporate-subscriber status lacks evidence")
    elif basis == "explicit-consent":
        if not row.get("consent_evidence"):
            blocks.append("prior consent lacks evidence")
    elif country == "FR" and basis == "professional-relevance-reviewed":
        if not row.get("legal_evidence_url"):
            blocks.append("professional relevance and objection/information review lacks evidence")
    else:
        blocks.append("a permissible jurisdiction-specific marketing basis is not documented")
    if row.get("legal_status") != "reviewed" or not row.get("legal_reviewed_on"):
        blocks.append("recipient legal review is not complete")
    if row.get("privacy_information_ready") != "yes":
        blocks.append("required privacy information is not ready")
    if row.get("already_contacted_at"):
        if not follow_up or row.get("follow_up_approved") != "yes":
            blocks.append("previous recipient: no automatic replay or unapproved follow-up")
    if row.get("offer_state") != "approved-for-send":
        blocks.append("proposal is a draft, not approved for sending")
    if row.get("package") == "licence":
        blocks.append("DIY files are not an unsolicited commissioned-work pitch")
    return list(dict.fromkeys(blocks))


def validate_email(subject, body):
    forbidden = r"\b(?:Homs|Syria|Syrian|Karm[ -]El[ -]Zeitoun|tax[- ]free|no VAT|100% legal|based in|UK[- ]based|US[- ]based)\b|حمص|سوريا"
    if re.search(forbidden, body, re.I):
        raise ValueError("Location, substitute-location or unsupported legal/tax claim in email.")
    if len(subject.split()) > 10 or len(subject) > 85 or subject.startswith("Re:"):
        raise ValueError("Use an honest, short subject; no invented reply prefix.")
    words = len(body.split())
    if not 70 <= words <= 210:
        raise ValueError(f"Email should be concise: found {words} words.")
    for required in ("one-time", "outline", "remove me", "Abdulrhman Thali"):
        if required not in body:
            raise ValueError(f"Missing fixed-price, CTA, opt-out or identity element: {required}")
    if re.search(r"guarantee(?:d)? (?:sales|rankings|revenue)|your site is (?:broken|ugly|terrible)", body, re.I):
        raise ValueError("No invented commercial guarantees or insulting audit language.")
    return words


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("audit")
    send = sub.add_parser("check-send")
    send.add_argument("id")
    send.add_argument("--follow-up", action="store_true")
    args = parser.parse_args()
    try:
        check_sources()
        policy, registry = load_policy(), load_registry()
        with (ROOT / "sales/prospects-2026.csv").open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        if args.command == "check-send":
            row = next((r for r in rows if r["id"] == args.id), None)
            if row is None:
                raise ValueError("Lead not in the active list; do not send.")
            blocks = send_blocks(row, policy, registry, args.follow_up)
            if blocks:
                raise ValueError("SEND BLOCKED:\n- " + "\n- ".join(blocks))
            print("Checklist gates passed. This is not a legal guarantee or an automatic send.")
        else:
            ready = sum(not send_blocks(r, policy, registry) for r in rows)
            print(f"Policy audit: {len(rows)} active leads · {ready} send-ready · paused={policy['send_paused']}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()

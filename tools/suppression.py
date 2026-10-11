#!/usr/bin/env python3
"""Fingerprint-only opt-outs and user-directed permanent market exclusions.

python3 tools/suppression.py
python3 tools/suppression.py check --email ADDRESS --country GB
python3 tools/suppression.py remove ID --date YYYY-MM-DD [--site OWN_SITE]
python3 tools/suppression.py exclude-countries US CA --date YYYY-MM-DD

Hashes are pseudonymous identifiers, not encryption or guaranteed anonymity.
Shared mail/web providers are never treated as a business's own domain.
"""
import argparse
import csv
import hashlib
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = "sales/SUPPRESSION-LIST.json"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOMAIN = re.compile(r"(?:[a-z0-9-]+\.)+[a-z]{2,}", re.I)
KINDS = ("email", "domain", "business", "lead_id")
REASONS = {"opt-out", "user-exclusion"}
SHARED_HOSTS = {
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.co.uk", "ymail.com",
    "hotmail.com", "hotmail.co.uk", "outlook.com", "live.com", "live.co.uk",
    "aol.com", "icloud.com", "me.com", "mail.com", "proton.me", "protonmail.com",
    "facebook.com", "instagram.com", "squarespace.com", "wix.com", "shopify.com",
    "shop.app", "sumupstore.com", "linktr.ee", "google.com", "goo.gl", "wordpress.com",
}


def normalize(kind, value):
    value = unicodedata.normalize("NFKC", str(value)).strip().casefold()
    if kind == "email":
        match = EMAIL.search(value)
        return match.group(0) if match else ""
    if kind == "domain":
        match = DOMAIN.search(value)
        return match.group(0).removeprefix("www.") if match else ""
    if kind == "business":
        return " ".join(re.sub(r"[^\w\s]", " ", value).split())
    return value


def fingerprint(kind, value):
    value = normalize(kind, value)
    return hashlib.sha256(f"levain-suppression:v1:{kind}:{value}".encode()).hexdigest() if value else ""


def load_registry(root=ROOT):
    data = json.loads((Path(root) / REGISTRY).read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("entries"), list):
        raise ValueError("Invalid suppression registry; do not send.")
    markets = data.get("blocked_countries", {})
    if not isinstance(markets, dict):
        raise ValueError("Invalid country exclusions; do not send.")
    for country, rule in markets.items():
        if not re.fullmatch(r"[A-Z]{2}", country) or not isinstance(rule, dict) or rule.get("reason") != "user-exclusion":
            raise ValueError("Invalid permanent market exclusion; do not send.")
        date.fromisoformat(rule["blocked_on"])
    for entry in data["entries"]:
        if not isinstance(entry, dict) or entry.get("reason") not in REASONS or not isinstance(entry.get("removed_on"), str):
            raise ValueError("Invalid suppression entry; do not send.")
        date.fromisoformat(entry["removed_on"])
        identifiers = entry.get("fingerprints")
        if not isinstance(identifiers, dict) or not any(identifiers.values()):
            raise ValueError("Empty suppression entry; do not send.")
        for kind, values in identifiers.items():
            if kind not in KINDS or not isinstance(values, list) or any(
                not isinstance(v, str) or not re.fullmatch(r"[a-f0-9]{64}", v) for v in values
            ):
                raise ValueError("Invalid suppression fingerprint; do not send.")
    return data


def is_blocked(candidate, registry):
    if (candidate.get("country") or "").strip().upper() in registry.get("blocked_countries", {}):
        return True
    tokens = {kind: set() for kind in KINDS}
    for field in ("email", "contact_verified", "contact_used", "to"):
        for address in EMAIL.findall(candidate.get(field) or ""):
            tokens["email"].add(fingerprint("email", address))
            domain = normalize("domain", address.rsplit("@", 1)[1])
            if domain and domain not in SHARED_HOSTS:
                tokens["domain"].add(fingerprint("domain", domain))
    for field in ("site", "site_found"):
        domain = normalize("domain", candidate.get(field) or "")
        if domain and domain not in SHARED_HOSTS:
            tokens["domain"].add(fingerprint("domain", domain))
    for kind, field in (("business", "business"), ("lead_id", "id")):
        token = fingerprint(kind, candidate.get(field) or "")
        if token:
            tokens[kind].add(token)
    return any(tokens[kind].intersection(entry.get("fingerprints", {}).get(kind, []))
               for entry in registry["entries"] for kind in KINDS)


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames, list(reader)


def write_csv(path, fields, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def check_sources(root=ROOT):
    root, registry = Path(root), load_registry(root)
    for name in ("prospects-2026.csv", "OUTREACH-LOG.csv", "SENT-RECORD.csv", "prospects-2026.json"):
        path = root / "sales" / name
        rows = (json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json" else read_csv(path)[1])
        for position, row in enumerate(rows, 1):
            if is_blocked(row, registry):
                raise ValueError(f"Suppressed contact in sales/{name}, record {position}; do not generate or send.")
    return len(registry["entries"])


def entry_for(lead, log, removed_on, reason="opt-out", site=""):
    addresses = set(EMAIL.findall(lead.get("contact_verified") or ""))
    for row in log:
        if row["id"] == lead["id"]:
            addresses.update(EMAIL.findall(row.get("contact_used") or ""))
    domains = {normalize("domain", address.rsplit("@", 1)[1]) for address in addresses}
    domains.update(normalize("domain", value) for value in (lead.get("site_found") or "", site))
    domains -= SHARED_HOSTS | {""}
    return {"removed_on": removed_on, "reason": reason, "fingerprints": {
        "email": sorted({fingerprint("email", value) for value in addresses}),
        "domain": sorted({fingerprint("domain", value) for value in domains}),
        "business": [fingerprint("business", lead["business"])],
        "lead_id": [fingerprint("lead_id", lead["id"])],
    }}


def prune_sources(registry, root=ROOT):
    root, counts = Path(root), {}
    for name in ("prospects-2026.csv", "OUTREACH-LOG.csv", "SENT-RECORD.csv"):
        path = root / "sales" / name
        fields, rows = read_csv(path)
        kept = [r for r in rows if not is_blocked(r, registry)]
        write_csv(path, fields, kept)
        counts[name] = len(rows) - len(kept)
    path = root / "sales/prospects-2026.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    kept = [r for r in rows if not is_blocked(r, registry)]
    if len(kept) != len(rows):
        path.write_text(json.dumps(kept, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    counts[path.name] = len(rows) - len(kept)
    active_ids = {r["id"] for r in read_csv(root / "sales/prospects-2026.csv")[1]}
    for directory, suffix in ((root / "sales/pitches", "md"), (root / "sales/pitches/html", "html"),
                              (root / "sales/email-drafts", "txt")):
        for path in directory.glob(f"*.{suffix}"):
            match = re.match(r"^(\d+)-", path.name)
            if match and match.group(1) not in active_ids:
                path.unlink()
    check_sources(root)
    return counts


def save_registry(registry, root):
    (Path(root) / REGISTRY).write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def remove_lead(lead_id, removed_on, site="", root=ROOT, reason="opt-out"):
    date.fromisoformat(removed_on)
    if reason not in REASONS:
        raise ValueError("Invalid removal reason; no changes made.")
    root, registry = Path(root), load_registry(root)
    _, rows = read_csv(root / "sales/prospects-2026.csv")
    matches = [r for r in rows if r["id"] == lead_id]
    if len(matches) != 1:
        raise ValueError("Removal needs exactly one existing lead ID; no changes made.")
    _, log = read_csv(root / "sales/OUTREACH-LOG.csv")
    registry["entries"].append(entry_for(matches[0], log, removed_on, reason, site))
    # Persist prevention first. An interrupted purge stays blocked rather than contactable.
    save_registry(registry, root)
    return prune_sources(registry, root)


def exclude_countries(countries, removed_on, root=ROOT):
    date.fromisoformat(removed_on)
    countries = {country.strip().upper() for country in countries}
    if not countries or any(not re.fullmatch(r"[A-Z]{2}", c) for c in countries):
        raise ValueError("Use explicit two-letter recipient-country codes.")
    root, registry = Path(root), load_registry(root)
    _, rows = read_csv(root / "sales/prospects-2026.csv")
    _, log = read_csv(root / "sales/OUTREACH-LOG.csv")
    matches = [row for row in rows if row["country"].strip().upper() in countries]
    registry.setdefault("blocked_countries", {}).update({country: {
        "blocked_on": removed_on, "reason": "user-exclusion",
        "basis": "User excludes location/valid-postal-address disclosure in commercial email; no workaround permitted."
    } for country in sorted(countries)})
    registry["entries"].extend(entry_for(row, log, removed_on, "user-exclusion") for row in matches)
    save_registry(registry, root)
    return prune_sources(registry, root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check")
    for option in ("email", "site", "business", "id", "country"):
        check.add_argument(f"--{option}", default="")
    remove = sub.add_parser("remove")
    remove.add_argument("id")
    remove.add_argument("--date", required=True)
    remove.add_argument("--site", default="")
    remove.add_argument("--reason", choices=sorted(REASONS), default="opt-out")
    markets = sub.add_parser("exclude-countries")
    markets.add_argument("countries", nargs="+")
    markets.add_argument("--date", required=True)
    args = parser.parse_args()
    try:
        if args.command in ("remove", "exclude-countries"):
            counts = (remove_lead(args.id, args.date, args.site, reason=args.reason) if args.command == "remove"
                      else exclude_countries(args.countries, args.date))
            print("Removed active records: " + ", ".join(f"{name}={n}" for name, n in counts.items()))
            print("Permanent prevention stored. Rebuild deliverables and replace Drive copies.")
        else:
            count = check_sources()
            if args.command == "check" and is_blocked(vars(args), load_registry()):
                raise ValueError("DO NOT CONTACT: permanent suppression or market exclusion.")
            print(f"Suppression gate passed: {count} permanently excluded record(s); active sources clean.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()

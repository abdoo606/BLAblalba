#!/usr/bin/env python3
"""Permanent opt-out gate; keep fingerprints, not deleted contact dossiers.

python3 tools/suppression.py                         # check all active source lists
python3 tools/suppression.py check --email ADDRESS   # required before any send
python3 tools/suppression.py remove ID --date YYYY-MM-DD [--site OWN_SITE]

Fingerprints are pseudonymous SHA-256 identifiers, not encryption or anonymous data.
They are retained only to prevent re-import and contact after an opt-out.
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
    path = Path(root) / REGISTRY
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("entries"), list):
        raise ValueError("Invalid suppression registry; do not send.")
    for entry in data["entries"]:
        if not isinstance(entry, dict) or entry.get("reason") != "opt-out" or not isinstance(entry.get("removed_on"), str):
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
    tokens = {kind: set() for kind in KINDS}
    for field in ("email", "contact_verified", "contact_used", "to"):
        for address in EMAIL.findall(candidate.get(field) or ""):
            tokens["email"].add(fingerprint("email", address))
            tokens["domain"].add(fingerprint("domain", address.rsplit("@", 1)[1]))
    for field in ("site", "site_found"):
        token = fingerprint("domain", candidate.get(field) or "")
        if token:
            tokens["domain"].add(token)
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
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def check_sources(root=ROOT):
    root = Path(root)
    registry = load_registry(root)
    for name in ("prospects-2026.csv", "OUTREACH-LOG.csv", "SENT-RECORD.csv", "prospects-2026.json"):
        path = root / "sales" / name
        rows = (json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json"
                else read_csv(path)[1])
        for position, row in enumerate(rows, 1):
            if is_blocked(row, registry):
                raise ValueError(f"Suppressed contact in sales/{name}, record {position}; do not generate or send.")
    return len(registry["entries"])


def remove_lead(lead_id, removed_on, site="", root=ROOT):
    root = Path(root)
    date.fromisoformat(removed_on)
    registry = load_registry(root)
    fields, rows = read_csv(root / "sales/prospects-2026.csv")
    matches = [r for r in rows if r["id"] == lead_id]
    if len(matches) != 1:
        raise ValueError("Removal needs exactly one existing lead ID; no changes made.")
    lead = matches[0]
    _, log = read_csv(root / "sales/OUTREACH-LOG.csv")
    addresses = set(EMAIL.findall(lead.get("contact_verified") or ""))
    for row in log:
        if row["id"] == lead_id:
            addresses.update(EMAIL.findall(row.get("contact_used") or ""))
    domains = {normalize("domain", address.rsplit("@", 1)[1]) for address in addresses}
    for value in (lead.get("site_found") or "", site):
        domain = normalize("domain", value)
        if domain:
            domains.add(domain)
    entry = {"removed_on": removed_on, "reason": "opt-out", "fingerprints": {
        "email": sorted({fingerprint("email", value) for value in addresses}),
        "domain": sorted({fingerprint("domain", value) for value in domains}),
        "business": [fingerprint("business", lead["business"])],
        "lead_id": [fingerprint("lead_id", lead_id)],
    }}
    # Write the safety record first. An interrupted purge stays blocked rather than contactable.
    registry["entries"].append(entry)
    (root / REGISTRY).write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
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
    for directory, suffix in ((root / "sales/pitches", "md"), (root / "sales/pitches/html", "html")):
        for path in directory.glob(f"{lead_id}-*.{suffix}"):
            path.unlink()
    check_sources(root)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check")
    for option in ("email", "site", "business", "id"):
        check.add_argument(f"--{option}", default="")
    remove = sub.add_parser("remove")
    remove.add_argument("id")
    remove.add_argument("--date", required=True)
    remove.add_argument("--site", default="")
    args = parser.parse_args()
    try:
        if args.command == "remove":
            counts = remove_lead(args.id, args.date, args.site)
            print("Removed active records: " + ", ".join(f"{name}={n}" for name, n in counts.items()))
            print("Fingerprint-only block stored. Rebuild all deliverables and replace Drive copies now.")
        else:
            count = check_sources()
            if args.command == "check" and is_blocked(vars(args), load_registry()):
                raise ValueError("DO NOT CONTACT: candidate matches permanent suppression.")
            print(f"Suppression gate passed: {count} permanent opt-out(s); no blocked active records.")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()

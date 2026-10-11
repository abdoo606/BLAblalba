"""Resolve sent-mail contacts to the action log, not the last duplicate CSV row."""
import re

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def contact_index(prospects, log):
    index, priorities = {}, {}
    for row in prospects:
        match = EMAIL.search(row.get("contact_verified") or "")
        if not match:
            continue
        address = match.group(0).lower()
        status = log.get(row["id"], {}).get("status", "").strip()
        priority = 2 if status.startswith("sent") else 1 if status == "bounced" else 0
        if address in index and priority > 0 and priorities[address] == priority:
            raise ValueError("Ambiguous sent-mail contact: multiple active lead IDs use one mailbox. Resolve before rebuilding.")
        if address not in index or priority > priorities[address]:
            index[address], priorities[address] = row, priority
    return index

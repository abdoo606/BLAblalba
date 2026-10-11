#!/usr/bin/env python3
"""Build sales/drive-clients-pricing.csv from sales/prospects-2026.csv.

The Drive sheet is a *view*, never edited by hand: prices live in the prospects CSV, so this script is the
only thing that should write drive-clients-pricing.csv. Run with `npm run sheet` (or python3 tools/make-sheet.py).
Sort order: VERIFIED first, then tax wave, then price - the order you actually work down the list.
"""
import csv
import re
import sys
import unicodedata

SRC = "sales/prospects-2026.csv"
OUT = "sales/drive-clients-pricing.csv"
WAVE = {"US": 1, "GB": 1, "CA": 1, "FR": 2, "ES": 2, "GR": 2, "RE": 3}
PKG = {"baguette": "Baguette - 1 langue", "croissant": "Croissant - 2 langues + panier",
       "patisserie": "Patisserie - 4 langues + theme sur mesure", "licence": "Licence kit"}


def slug(name):
    s = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    rows = list(csv.DictReader(open(SRC, newline="")))
    names = [r["business"].strip().lower() for r in rows]
    dups = {n for n in names if names.count(n) > 1}
    if dups and "--force" not in sys.argv:
        sys.exit("REFUSED: duplicate business names in the source: %s\nDe-duplicate first (one row per shop) or pass --force."
                 % ", ".join(sorted(dups)))

    out = []
    for r in rows:
        v = r.get("verification_2026_10_10", "")
        st = "VERIFIED" if v.startswith("VERIFIED") else ("PARTIAL" if v.startswith("PARTIAL") else "to verify")
        w = WAVE.get(r["country"], 2)
        eur, usd = int(r["quote_eur"] or 0), int(r["quote_usd"] or 0)
        out.append(dict(
            id=r["id"], b=r["business"], city=r["city"], c=r["country"], w=w, st=st,
            contact=(r.get("contact_verified") or "to be found") if st != "to verify" else "to be found",
            web=((r["site_found"] + " | ") if r.get("site_found") else "") + (r.get("audit_note") or r.get("web_presence_note") or ""),
            pkg=PKG.get(r["package"], r["package"]) + (" + " + r["addons"] if r.get("addons") else ""),
            eur=eur, usd=usd, care=int(r.get("care_eur_per_month") or 45),
            vat="wave 1: no VAT anywhere" if w == 1 else "wave 2: reverse charge + their VAT number",
            prio=r.get("priority", ""), pitch="%s-%s.md" % (r["id"], slug(r["business"]))))
    order = {"VERIFIED": 0, "PARTIAL": 1, "to verify": 2}
    out.sort(key=lambda x: (order[x["st"]], x["w"], -x["eur"]))

    log = list(csv.DictReader(open("sales/OUTREACH-LOG.csv", newline="")))
    sent = [r for r in log if r["status"].startswith("sent")]
    auto = [r for r in log if "auto-reply" in r["status"]]
    human = [r for r in log if (("replied" in r["status"] and "auto-reply" not in r["status"]) or r["status"].startswith(("quoted", "negotiated", "won")))]
    decline = [r for r in log if "do not contact" in r["status"]]

    with open(OUT, "w", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["#", "Client / العميل", "City", "Country", "Tax wave", "Status", "Contact / channel",
                    "Their web presence (VERIFIED = we opened their own site)", "Package", "Price EUR", "Price USD",
                    "Care €/mo", "VAT note", "Priority", "Design board"])
        for r in out:
            w.writerow([r["id"], r["b"], r["city"], r["c"], r["w"], r["st"], r["contact"], r["web"], r["pkg"],
                        r["eur"], r["usd"], r["care"], r["vat"], r["prio"], r["pitch"]])
        n_v = sum(1 for r in out if r["st"] == "VERIFIED")
        n_p = sum(1 for r in out if r["st"] == "PARTIAL")
        w.writerow(["TOTAL",
                    "%d prospects · %d VERIFIED · %d PARTIAL · %d to verify" % (len(out), n_v, n_p, len(out) - n_v - n_p),
                    "wave 1: %d leads" % sum(1 for r in out if r["w"] == 1), "", "", "", "", "",
                    sum(r["eur"] for r in out), format(sum(r["usd"] for r in out), ","),
                    "%d €/mo if all take care" % (45 * len(out)),
                    "SENT: %d leads · %s € quoted" % (len(sent), format(sum(int(r["quoted_eur"] or 0) for r in sent), ",")),
                    "", "sales/pitches/"])
    print("%d rows · %d verified · total %d EUR · %d sent · %d human replies · %d auto-replies (not replies)" % (
        len(out), sum(1 for r in out if r["st"] == "VERIFIED"), sum(r["eur"] for r in out),
        len(sent), len(human), len(auto)))


if __name__ == "__main__":
    main()

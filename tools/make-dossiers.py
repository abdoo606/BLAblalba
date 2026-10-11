#!/usr/bin/env python3
"""Per-shop dossier - the file Abdulrhman reads when he opens Drive from another session.

One block per shop: what we found on their own page, our direction, where it stands,
what happens next, and the price. Everything is read from the CSVs - nothing is typed
here, so a dossier cannot stay friendly while the register moves on.

  python3 tools/make-dossiers.py        -> sales/SHOP-DOSSIERS.md
"""
import csv, os, re, subprocess, datetime
from suppression import check_sources

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATES = {"USD": 1.09, "GBP": 0.86, "SYP": 1.09 * 14500}
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def main():
    check_sources()
    rows = list(csv.DictReader(open(os.path.join(ROOT, "sales/prospects-2026.csv"), newline="", encoding="utf-8")))
    log = {r["id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "sales/OUTREACH-LOG.csv"), newline="", encoding="utf-8"))}
    sent_by_email = {}
    for r in csv.DictReader(open(os.path.join(ROOT, "sales/SENT-RECORD.csv"), newline="", encoding="utf-8")):
        sent_by_email[r["to"].strip().lower()] = r

    today = datetime.date.today().isoformat()
    out = []
    A = out.append
    A(f"# ملف لكل محل — Shop dossiers · {today}")
    A("")
    A("كل محل له بلوك: شو لقينا بصفحته هو (مو من مقال)، اتجاهنا، وين إحنا، الخطوة الجاية، والسعر.")
    A("الملف مولّد من `sales/prospects-2026.csv` + `OUTREACH-LOG.csv` + `SENT-RECORD.csv` بـ `tools/make-dossiers.py`.")
    A("لا تحرّروه بالدرايف — عدّل الـCSV وأعيدوا التوليد.")
    A("")

    def worked(r):
        st = (log.get(r["id"], {}).get("status") or "")
        # a shop counts as "worked" only when the LOG says we did something with it.
        # A placeholder audit_note (added with the row, before anyone opened the site) is NOT work.
        return st != "to-verify"
    done = [r for r in rows if worked(r)]
    wait = [r for r in rows if not worked(r)]

    def money(q):
        return f"{q:,} €  ·  ≈ {round(q*RATES['USD']):,} $  ·  ≈ {round(q*RATES['GBP']):,} £"

    A(f"## القسم الأول — محلات تحركنا فيها ({len(done)})")
    for r in sorted(done, key=lambda r: -(int(r.get("quote_eur") or 0))):
        lg = log.get(r["id"], {})
        st = lg.get("status") or "to-verify"
        m = EM.search(r.get("contact_verified") or "")
        rec = sent_by_email.get((m.group(0).lower() if m else ""), None)
        q = int(r.get("quote_eur") or 0)
        A("")
        A(f"### {r['business']} — {r['city']}, {r['country']}  ·  {st}")
        A(f"**وين إحنا:** {r.get('verification') or 'لم يفتح موقعه بعد'}")
        if r.get("site_found"):
            A(f"**الموقع:** {r['site_found']}")
        if r.get("contact_verified") and r["contact_verified"] != "not checked yet":
            A(f"**اللي نشروه عندهن:** {r['contact_verified']}")
        if r.get("audit_note"):
            A(f"**شو لقينا بصفحتهم (حرفاً):** {r['audit_note']}")
        if r.get("growth_signal_why_now"):
            A(f"**ليش هلأ:** {r['growth_signal_why_now']}")
        if r.get("pitch_angle"):
            A(f"**اتجاهنا:** {r['pitch_angle']}")
        if q:
            A(f"**السعر:** {money(q)} · رعاية {r.get('care_eur_per_month') or 0} €/شهر · السنة الأولى {int(r.get('first_year_value_eur') or 0):,} €")
        if rec:
            A(f"**المبعوث:** {rec['to']} · {rec['sent_utc']} · “{rec['subject']}”")
        if lg.get("next_action"):
            A(f"**الخطوة الجاية:** {lg['next_action']}" + (f" — {lg['next_action_date']}" if lg.get("next_action_date") else ""))
        A(f"**مصدر الاسم:** {r.get('source') or '—'}")
        if (lg.get("suppression_list") or "").lower() == "yes":
            A("**على قائمة الحذف:** لا يُراسَل مجدداً أبداً.")

    A("")
    A(f"## القسم الثاني — {len(wait)} محلاً بالقائمة، ما فتحنا موقعهن بعد (ما صالح للتواصل)")
    A("كل سطر هنا اسمه من مصدر 2026 موثّق، بس ما قرينا صفحة ولا واحد منهن: لا إيميل، لا عرض، لا وعد. الطابور يمشي محل-بمحل.")
    A("")
    A("سطر لكل محل: الاسم · المدينة · السعر · الإشارة. ما في إيميل ولا عرض مفصّل - لأنو ما قرينا صفحة ولا واحد منهن.")
    for r in sorted(wait, key=lambda r: (r["country"], r["business"])):
        q = int(r.get("quote_eur") or 0)
        A(f"- **{r['business']}** — {r['city']}, {r['country']} · {money(q) if q else '—'} · {(r.get('growth_signal_why_now') or '')[:90]}")

    p = os.path.join(ROOT, "sales", "SHOP-DOSSIERS.md")
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote {p} ({os.path.getsize(p):,} bytes, {len(rows)} shops)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The one document a brand-new session reads first: where we stand, what to click, in what order.

Everything is computed from the CSVs + sales/DRIVE-HANDOVER.txt, so the numbers on Drive
can never drift from the repository. Run it inside the same rebuild chain as the registers:

  python3 tools/make-resume.py        ->  sales/DRIVE-RESUME.md

Then push that text into Drive doc `00` (update_file_content) and it is readable cold.
"""
import csv, os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATES = {"USD": 1.09, "GBP": 0.86, "SYP": 1.09 * 14500}
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
LADDER = [
    ("Baguette - موقع تعريف بسيط", 750),
    ("Croissant - موقع + قائمة + طلب مسبق", 1450),
    ("Patisserie - متجر كامل ولغات", 2900),
    ("رخصة القالب للمحل", 149),
    ("لغة إضافية", 220),
    ("تحسين الظهور بجوجل", 380),
    ("تصوير المنتجات", 320),
    ("فرع/موقع إضافي", 180),
    ("صفحة طلبات الجملة", 640),
    ("العناية الشهرية (للمرة)", 45),
    ("الاستضافة بالسنة (للمرة)", 90),
]
# The live Drive ids, 00..08. Refresh this map whenever a file is re-uploaded, then re-run.
DRIVE = [
    ("00", "ابدأ من هنا (هذا الملف)", "1ut9Ruyy2o7uYitZq-Cn8klfT5ZpZLYsqY5KiLPCqfZk", "doc"),
    ("01", "Register EN — سجل الإرسال", "15HLKSl4-d6db9t64x2VPwLc_Hbo8gvBW", "file"),
    ("02", "السجل بالعربي", "17ox4Ib0UvIUnQ_7k-sV-noyvBi6rcEB0", "file"),
    ("03", "Pitch Boards (141) · zip", "1BxNVZJEWZ2UmjQR0cFAtkOjjzYWD8T6j", "file"),
    ("04", "Clients & Pricing · جدول 141×26", "1rHlCeF-in6d_OmDziplUVm8O-K0hMj_dquUgRB5DQ9I", "sheet"),
    ("05", "Sales pack — التسعير والقوالب", "1s5locBBaIyQmL-xylxESO_eTZ7bUva-14l8X3CY6txU", "doc"),
    ("06", "Compliance — لماذا بلا ضريبة على الزبون", "1-cHQByvBH2V2uAlamMXRVKG5ERbw1ajXM6pfLbOtSJ0", "doc"),
    ("07", "TODO لكل رسالة", "1goQ3qcHVfcrv9lrQlkngCaGMMNCHXJRZmFkYrexNlBM", "doc"),
    ("08", "Shop dossiers — ملف لكل محل", "14_65Xl2k7nfIHnRy5jPmUdLTjfgZovsVP2YtymI9OuA", "doc"),
]


def money(eur):
    return f"{eur:,} € = {round(eur * RATES['USD']):,} $"


def read(name):
    with open(os.path.join(ROOT, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    pros = read("sales/prospects-2026.csv")
    log = {r["id"]: r for r in read("sales/OUTREACH-LOG.csv")}
    sent = [r for r in read("sales/SENT-RECORD.csv") if r["kind"] == "cold pitch"]

    by_email = {}
    for r in pros:
        m = EM.search(r.get("contact_verified") or "")
        if m:
            by_email[m.group(0).lower()] = r
    emailed = [by_email[s["to"].strip().lower()] for s in sent if s["to"].strip().lower() in by_email]
    total_eur = sum(int(r["quote_eur"] or 0) for r in emailed)
    all_eur = sum(int(r["quote_eur"] or 0) for r in pros)

    st = {}
    for r in log.values():
        st[r["status"].strip()] = st.get(r["status"].strip(), 0) + 1
    pby = {r["id"]: r for r in pros}
    # queue order: US/GB first (no VAT paperwork), then the rest; inside that, by row id
    prio = {"US": 0, "GB": 1, "FR": 2, "ES": 3}
    queue = sorted((i for i, r in log.items() if r["status"].strip() == "to-verify"),
                   key=lambda i: (prio.get(pby.get(i, {}).get("country", ""), 9), int(i)))
    opened = len(pros) - len(queue)
    bounce = st.get("bounced", 0)
    auto = st.get("sent (auto-reply)", 0)
    live = st.get("sent", 0) + auto
    emails = st.get("sent", 0) + auto + bounce
    deposit = round(total_eur * RATES["USD"] * 0.4)

    head = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%h · %s"],
                          capture_output=True, text=True).stdout.strip() or "(git unavailable)"
    branch = subprocess.run(["git", "-C", ROOT, "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip() or "?"
    handover = open(os.path.join(ROOT, "sales/DRIVE-HANDOVER.txt"), encoding="utf-8").read().strip()
    pre_path = os.path.join(ROOT, "sales/RESUME-PREAMBLE.md")
    preamble = open(pre_path, encoding="utf-8").read().strip() if os.path.exists(pre_path) else ""

    o = []
    A = o.append
    A("ابدأ من هنا — وين وصلنا بالضبط، وشو الخطوة الجاية")
    A(f"آخر توليد: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · الفرع {branch} · آخر commit: {head}")
    A("الملف مولّد بـ `python3 tools/make-resume.py` من ملفات الـCSV. لا تعدّله بالإيد لا هنا ولا بالمستودع — عدّل المصدر وأعد التوليد.")
    A("نفس هذا النص موجود بالمستودع: sales/DRIVE-RESUME.md (هالورقة) + sales/RESUME-PREAMBLE.md (قسم 0) + README.md.")
    A("")
    if preamble:
        A(preamble)
        A("")
    A("1) وين نحنا (السلطة الوحيدة للأرقام: sales/OUTREACH-LOG.csv، أو node tools/progress.mjs)")
    A(f"   {len(pros)} محلاً بالقائمة · فتحنا موقعهن بأنفسنا: {opened} · بعتنالهم إيميل: {emails} ({live} حيّة + {bounce} مرتد)")
    A(f"   مجموع المعروض للمُرسل: {money(total_eur)} · الدفعة الأولى 40% = {deposit:,} $")
    A(f"   بالطابور (ما فتحنا موقعهن بعد): {len(queue)} · جاهزون للتحقق بهاتف/DM بس: {st.get('verified-ready', 0)} · "
      f"لا نبعثلن (سبب مسجل): {st.get('no-pitch', 0)} · أسماء متنازع عليها: {st.get('DISPUTED', 0)} · "
      f"parked: {st.get('parked - no own site found', 0)} · موقعو مطفي: {st.get('not contacted - their site is offline', 0)}")
    A("   الردود البشرية: 0 · الردود الآلية (ما بتحسب رد): " + str(auto) + " — ARAN و Landrace، تذكير صباح الثلاثاء 13/10، وتاني 20/10، وبعدها بنتركهن.")
    A("")
    A("2) لو معك 60 بس: اعمل هيك")
    A("   أ. افتح 08 · Shop dossiers — القسم الأول فيه بلوک لكل محل تحركنا فيه، وآخر الملف جدول الطابور كله.")
    A("   ب. خد أول سطر بالطابور (قائمتو تحت) — ابحث عن موقعو المحل، افتح صفحة التواصل عنده، اقرأها كاملة.")
    A("   ج. الإيميل بس للعنوان المنشور بصفحتهن. غير هيك: ما في إرسال، ولسا ما في عرض.")
    A("   د. أي شي بتغيّرو بيصير بملفات الـCSV بالمستودع وبعدها chain التوليد - ما بيصير بالدرايف.")
    A("")
    A(f"3) الطابور — أول {min(12, len(queue))} محلاً (من {len(queue)}) · بالترتيب، وكلهن بلا تحقق")
    for i in queue[:12]:
        r = pby[str(i)]
        A(f"   id {i} · {r['business']} — {r['city']}, {r['country']} · {money(int(r['quote_eur'] or 0))} · "
          f"مصدر الاسم: {(r['source'] or '')[:60]}")
    A("")
    A("4) الحلقة اللي بتتكرر مع كل رسالة — الأوامر بالحرف")
    A("   python3 tools/make-sheet.py")
    A("   python3 tools/make-register.py")
    A("   python3 tools/make-register-ar.py")
    A("   python3 tools/make-dossiers.py")
    A("   python3 tools/make-resume.py")
    A("   node tools/make-pitches.mjs && node src/build.mjs && node tools/validate.mjs")
    A("   ثم أعد ضغط release/levain-pitches.zip، وانسخ الـPDFs للجذر:")
    A("   cp -f sales/OUTREACH-REGISTER.pdf /home/user/levain-outreach-register.pdf")
    A("   cp -f sales/OUTREACH-REGISTER-AR.pdf /home/user/levain-outreach-register-ar.pdf")
    A("   وبعدها git add -A && git commit && git push origin " + branch)
    A("   وأخيراً ارفع النسخ الجديدة للدرايف بنفس الأسماء وارمِ القديمة بالمهملات (01، 02، 03، 04، 07، 08)، وحدّث هذا الملف (00) لو تغيّرت الأرقام.")
    A("")
    A("5) جدول التسعير (كل عقد بيبدأ من هون)")
    for name, eur in LADDER:
        A(f"   {name}: {money(eur)}")
    A("   £ = € × 0.86 · $ = € × 1.09 · الليرة السورية استرشادية 14,500/دولار · أعلى خصم 15% · استعجال +25% · دفعة أولى 40%")
    A(f"   لو وافقوا كلن نظرياً (قياس فقط): {money(all_eur)} — ما بنعرض هالرقم على أي زبون.")
    A("")
    A("6) موقوفون عن الإرسال — لا تنسى السبب، ما بنرجعلهن بالغلط")
    for i, r in sorted(((int(k), v) for k, v in log.items()
                         if v["status"].strip() in ("DISPUTED", "no-pitch", "parked - no own site found",
                                                    "not contacted - their site is offline"))):
        why = (r["notes"] or r["suppression_list"] or "").strip().replace("\n", " ").strip(" |")
        why = " ".join(w for w in why.split() if w != "|")
        A(f"   id {i} · {r['business']} — {r['status'].strip()}" + (f": {why[:190]}" if why else ""))
    A("")
    A("7) الشي اللي ما صار بعد (حتى ما ينحسب تمام)")
    A(f"   أ. طابور التحقق ({len(queue)} محلاً) لسا ما فتحنا موقعهن واحد واحد — هاي الشغلة الشغالة.")
    A("   ب. وعد «قائمة 100 محل جديدة» لسا ما انسلم: آخر دفعة زادت 3 محلات بس. المصادر الجاهزة: Food Republic أجزاء 2-5 و Britain's Best Loaf 2026 أجزاء 1-3.")
    A("   ج. محلات فرنسا واسبانيا بالقائمة ما بعتنالهن ولا صف — مستنين الإشارة منك لأنو فيهما TVA/autónomo (ورقة 06).")
    A("   د. أي محل يردّ علينا انسان: بنسأل عبد الرحمن قبل ما نبعتلو أي شي — القاعدة مكتوبة بـ 07.")
    A("")
    A("8) خريطة الدرايف — نسخة حية وحدة لكل ملف (لا تكاوير)")
    for num, label, fid, kind in DRIVE:
        if num == "00":
            A("   00 · ابدأ من هنا — هذا الملف نفسه، وأحدث نسخة إلو بمجلد Levain Kit (لا تبحث عن رابط قديم)")
            continue
        url = (f"https://docs.google.com/document/d/{fid}/edit" if kind == "doc"
               else f"https://docs.google.com/spreadsheets/d/{fid}/edit" if kind == "sheet"
               else f"https://drive.google.com/file/d/{fid}/view")
        A(f"   {num} · {label}\n        {url}")
    A("   المستودع: github.com/abdoo606/BLAblalba — الفرع " + branch)
    A("   الملفات المصدّرة: sales/prospects-2026.csv (القائمة) · sales/OUTREACH-LOG.csv (الحالة، السلطة للأرقام) · "
      "sales/SENT-RECORD.csv (مين انبعثلو) · sales/SHOP-DOSSIERS.md (08) · sales/EVERY-MESSAGE-CHECKLIST.md (07)")
    A("")
    A("9) باقي ورقة التسليم — القواعد والتفصيل")
    A("")
    A(handover)

    out = os.path.join(ROOT, "sales/DRIVE-RESUME.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")
    print(f"wrote {out} ({os.path.getsize(out):,} bytes)")
    print(f"numbers: {len(pros)} leads · {opened} opened · {emails} emails · {money(total_eur)} · {len(queue)} in queue")


if __name__ == "__main__":
    main()

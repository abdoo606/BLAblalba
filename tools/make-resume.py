#!/usr/bin/env python3
"""The one document a brand-new session reads first: where we stand, what to click, in what order.

Everything is computed from the CSVs + sales/DRIVE-HANDOVER.txt, so the numbers on Drive
can never drift from the repository. Run it inside the same rebuild chain as the registers:

  python3 tools/make-resume.py        ->  sales/DRIVE-RESUME.md

Then push that text into Drive doc `00` (update_file_content) and it is readable cold.
"""
import csv, os, re, subprocess, datetime
from suppression import check_sources
from outreach_data import contact_index

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATES = {"USD": 1.09, "GBP": 0.86, "SYP": 1.09 * 14500}
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
LADDER = [
    ("Baguette - موقع تعريف بسيط", 750),
    ("Croissant - موقع + قائمة + طلب مسبق", 1450),
    ("Patisserie - متجر كامل ولغات", 2900),
    ("رخصة القالب للمحل", "149 $"),
    ("لغة إضافية", 220),
    ("تحسين الظهور بجوجل", 380),
    ("تصوير المنتجات", 320),
    ("فرع/موقع إضافي", 180),
    ("صفحة طلبات الجملة", 640),
    ("العناية الشهرية (اختيارية، كل شهر)", 45),
    ("الاستضافة (اختيارية، كل سنة)", 90),
]
# Stable Drive section names, not expiring file IDs. Read the folder listing before replacing copies.
DRIVE = [
    ("00", "ابدأ من هنا (هذا الملف)"),
    ("01", "Register EN — سجل الإرسال"),
    ("02", "السجل بالعربي"),
    ("03", "Pitch Boards ({lead_count}) · zip"),
    ("04", "Clients & Pricing · جدول {lead_count} محلاً"),
    ("05", "Sales pack — التسعير والقوالب"),
    ("06", "Compliance — ورقة الالتزام"),
    ("07", "TODO لكل رسالة"),
    ("08", "Shop dossiers — ملف لكل محل"),
]


def money(eur):
    return f"{eur:,} € = {round(eur * RATES['USD']):,} $"


def read(name):
    with open(os.path.join(ROOT, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    suppressed_count = check_sources()
    pros = read("sales/prospects-2026.csv")
    log = {r["id"]: r for r in read("sales/OUTREACH-LOG.csv")}
    sent = [r for r in read("sales/SENT-RECORD.csv") if r["kind"] == "cold pitch"]

    by_email = contact_index(pros, log)
    emailed = [by_email[s["to"].strip().lower()] for s in sent if s["to"].strip().lower() in by_email]
    supp_ids = {i for i, r in log.items() if (r.get("suppression_list") or "").strip().lower() == "yes"}
    emailed = [r for r in emailed if r["id"] not in supp_ids and log.get(r["id"], {}).get("status", "").strip() != "bounced"]
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
    sentish = [r for r in log.values() if r["status"].strip().startswith("sent")]
    declined = [r for r in sentish if "do not contact" in r["status"]]
    live = len(sentish) - len(declined)
    emails = len(sentish) + bounce
    deposit = round(total_eur * RATES["USD"] * 0.4)

    head = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%h"],
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
    A(f"   العروض القائمة (ليست إيراداً؛ بلا المرتدات أو المحذوفين): {money(total_eur)} · دفعة 40% لو وافق الجميع = {deposit:,} $")
    A(f"   طلبات حذف منفّذة: {suppressed_count} · بصمات منع فقط؛ لا أسماء أو عناوين للمحذوفين في القوائم الحالية. لم يُمحَ تاريخ Git أو مهملات البريد/الدرايف.")
    A(f"   بالطابور (ما فتحنا موقعهن بعد): {len(queue)} · جاهزون للتحقق بهاتف/DM بس: {st.get('verified-ready', 0)} · "
      f"لا نبعثلن (سبب مسجل): {st.get('no-pitch', 0)} · أسماء متنازع عليها: {st.get('DISPUTED', 0)} · "
      f"parked: {st.get('parked - no own site found', 0)} · موقعو مطفي: {st.get('not contacted - their site is offline', 0)}")
    human = sum(1 for r in log.values() if "replied" in r["status"] and "auto-reply" not in r["status"])
    A(f"   الردود البشرية بالقائمة الحالية: {human} · الردود الآلية (ما بتحسب اهتمام): {auto}. المواعيد من OUTREACH-LOG، وليس من رد آلي.")
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
    A("   python3 tools/suppression.py   # بوابة المنع قبل الاستيراد والتوليد والإرسال")
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
        A(f"   {name}: {money(eur) if isinstance(eur, int) else eur}")
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
    A("8) ملفات الدرايف — نسخة حية وحدة لكل رقم (00 ← 08)")
    A("   لا تلصق روابط داخل الملفات: الـid بيتغيّر مع كل رفع جديد، والرقم والاسم ما بيتغيّروا. كل الملفات بنفس المجلد مرتّبة:")
    for num, label in DRIVE:
        A(f"   {num} · {label.format(lead_count=len(pros))}")
    A("   المجلد: https://drive.google.com/drive/folders/0ACdYKa5qpuxEUk9PVA")
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
    print(f"suppressed: {suppressed_count} fingerprint-only opt-out(s); not in active exports")
    print(f"numbers: {len(pros)} leads · {opened} opened · {emails} emails · {money(total_eur)} · {len(queue)} in queue")


if __name__ == "__main__":
    main()

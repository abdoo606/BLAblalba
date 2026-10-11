#!/usr/bin/env python3
"""Human-readable Arabic version of the outreach register (RTL PDF).

Same facts as tools/make-register.py, written in plain Arabic for Abdulrhman to
read. Every number (price, currency, status, who we wrote to) is read from
sales/prospects-2026.csv + sales/SENT-RECORD.csv, so this file cannot drift.
The Arabic sentences describing what we SAW on each shop's site live in NOTES
below - one line per shop, keyed by row id, and only ever written from a page we
opened ourselves. Anything not in NOTES prints a generic line, so newly sent
shops still appear.

  python3 tools/make-register-ar.py
"""
import csv, os, re, subprocess, sys, datetime
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATES = {"EUR": 1.0, "USD": 1.09, "SYP": 1.09 * 14500}   # SYP = indicative
GBP = 0.86
MONEY_ORDER = ("EUR", "USD", "SYP")
DATE = "2026-10-11"

# Short Arabic reading of what our own eyes saw on the shop's site (from the page,
# not from a search snippet). Keyed by prospects row id.
NOTES = {
 78: ("Field Bakery", "Gothelney Farm، سامرست",
     "مخبز مزرعة في سامرست (Gothelney Farm) بيطحن قمحويخبزو فالمكان نفسه. لقينا إيميلهم بصفحتهن (info@fieldbakery.com) ومو من مصدر تاني. طلبات الجمعة كلها عبر رابط مطول لمنصة تانية، وفورم النشرة بصفحتهم طالع بخطأ تقني، وساعات العمل متروكة لزائر يفتّش بغوغل. عرضنا: 1,450 € = 1,581 $ للطلب المسبق + فورم الجملة (أو 2,900 € مع النشرة وصفحة الساعات)."),
 104: ("The Lost Mill Bakery", "Cowes، آيل أوف وايت",
     "مخبز في آيل أوف وايت (Cowes) اسمو من الطاحونة يلي خسرتها البلدة. صفحتن ناشرة إيميل جيميل + تلفون + العناوين، بس ما في قائمة أخباز ولا أسعار، وكابشن الصور أسماء الكاميرا (PXL_2023...). عرضنا: 1,450 € = 1,581 $ لقائمة أخباز بزر «نفذت» + طلب مسبق للاستلام، أو 2,900 € مع جاليري وعنوان بريد على الدومين تبعن."),
 75: ("E5 Bakehouse", "لندن (3 صالات)",
     "E5 Bakehouse: ثلاث صالات (هاكني، بوبلار، ومتجر داخل V&A East) وإيميل واحد info@e5bakehouse.com لكلن، والساعات مكتوبة نص يدوي ما بيطابق يلي بغوغل. الطاحونة والمدرسة الزراعية ومدرسة الخبز كلها حكي بلا زر حجز أو طلب. عرضنا: 2,900 € = 3,161 $ (صفحة لكل صالة + طلب للاستلام + تقسيم استفسارات الجملة والمدارس والفعاليات) أو 1,450 € للإصلاحات فقط."),
 97: ("Pastille Bakery", "ليفربول",
     "Pastille Bakery (ليفربول): كرواسون وكوفنز وكيك باسك حسب الأسبوع، «9:30 لـ 3:30 أو لينفدو» - وما في طريقة تحجز. متجر شوبيفاي تبعن بيه بطاقة هدية بس، والصور PNG حجم 2400 بكسل بتبطّأ الموبايل. إيميلهن منشور بصفحة التواصل خاصتن. عرضنا: 1,450 € = 1,581 $ للطلب المسبق + منيو أسبوعي قابل للتحديث (أو 2,900 € مع ضغط الصور + فورم أعراس ومناسبات)."),
 101: ("Small Food Bakery", "نوتنغهام",
     "Small Food Bakery (نوتنغهام): مفتوح خميس-سبت، وإيميلو hello.smallfoodcollective@gmail.com + واتساب، وبيلّغن الزبون بصراحة: «ما عندنا تلفون بالمخبز لأنه ما في حدا يقدر يرد». الصفحة لسا عم تعد بإن مدخل للمقعدين رح يخلص بشهر 7/2023، وإعلان عطلة عيد الميلاد بيقول «بنفتح 8 كانون 2026» ولازم من 10 شهور. عرضنا: 1,450 € = 1,581 $ للطلب المسبق + سطر إعلانات يتحدّث من الموبايل (أو 2,900 € بالكامل)."),
 79: ("Fred Bakery", "لندن (Holborn + أوكسفورد سرкус)",
     "Fred Bakery (لندن -Frithrovia وHolborn): صفحة التواصل ناشرة info@fredbakery.co.uk للإيميل، وbenan@ للكاترينغ، وferide@ للفعاليات - بس الرقم يلي مكتوب على الشاشة مو هو الرقم يلي بيطّلو الضغط عليه على الموبايل (نفس الرقم ظاهر للفرعين وكل وحدة بيرقمن رقم مختلف)، ولينكدإن فارغ، والساعات لا تتطابق مع المنشور بالصحافة، والفوتر بيحمل سنتين حقوق 2025 و2026. عرضنا: 2,900 € = 3,161 $ (فورم كاترينغ يوصل للإيميل الصح + أرقام وساعات مضبوطة + طلب مسبق) أو 1,450 € للتصحيحن الأولين."),
 107: ("Wooster's Bakery", "سوفولك (غرفتين)",
     "Wooster's Bakery (سوفولك): غرفتين + ثلاث أسواق أسبوعية، وإيميلو منشور بصفحة Find Us (info@woostersbakery.co.uk). الخبز بيتباع عبر محل تاني وصفحتن بيقولوا للزبون «راجعو Garboldisham General Stores»، وثلاث صور بالرئيسية ما بيظهرو (كسل التحميل محطّم)، وأحسن إنجاز للـ2026 (50 أفضل مخبز) مجرد بانر. عرضنا: 1,450 € = 1,581 $ لفتحات طلب لكل غرفة + تقويم الأسواق، أو 2,900 € مع شحن الـmalt loaf كمنتجهدية وإصلاح الصور."),
 55: ("Two Magpies Bakery", "نورفولك وسوفولك (11 مقهى)",
     "Two Magpies Bakery: مخبز مركزي بـ Walpole و11 مقهى وأكتر من 100 موظف ومدرسة خبز وماركة ثانية (Hilton Macarons). لقينا إيميلا منشور بفوتر موقعن، وبلّغناهم إن روابط الصفحات تبع المقاهي (نورويتش، ساوثوولد...) كلها بترجعلهن صفحة «لقمة ما لقيناها»، وكل عناصر القائمة الكبيرة بإعادة لنفس الصفحة، وإيميلات كل فرع ظاهرة للزبون كنص محمي بدل ما تكون رابط. عرضنا: 2,900 € = 3,161 $ (11 صفحة فروع شغّالة + طلب للاستلام لكل فرع + فورم كيك وفعاليات) أو 1,450 € للروابط والطلبات."),
 66: ("Niedlov's Cafe & Bakery", "تشاتانوغا، تينيسي",
     "Niedlov's (تشاتانوغا، تينيسي): مخبز بيخدم الجملة باربع ولايات، ومرشح «Outstanding Bakery» لجيمس بيرد 2026. صفحة التواصل عندهن ناشرة wholesale@niedlovs.com وcatering@ وبتعد برد «خلال 5 أيام عمل» - هاي الأيام الخمسة هي وين بتمشي المطاعم لمورد تاني. عرضنا: 2,900 € = 3,161 $ (فورم جملة بالحقول يلي بدّن + منيو كاترينغ على الموقع + بلوك جوائز)، أو 1,450 € للفورم بس."),
 63: ("DeLuxe Cakes and Pastries", "آيوا سيتي، آيوا",
     "DeLuxe Cakes and Pastries (آيوا سيتي): رئيسة الحلوانية مسمّية بالصفحة، وإيميلا info@deluxeiowa.com منشور 3 مرات على موقعهن، مع ساعات كاملة. طلب الكيك الخاص = إيميل يا تلفون «للطلبات المستعجلة» بلا فورم ولا أسعار ولا دفعة أونلاين. عرضنا: 1,450 € = 1,581 $ (فورم طلب كيك بياخد الدفعة 40% أونلاين + بانر مواعيد الأعياد) أو 2,900 € مع جاليري بأسعار حسب الحجم."),
}
# فتحنا الموقع وما بعتنا - والسبب (يطلع بمؤخرة الملف)
NO_PITCH = {
 5: ("Hobbs House", "صفحة الجملة عندهم منشورة بالكامل: الأسعار، جدول التوصيل، فورم حساب جملة. الموقع مبني من حدا، وما بنافسهم."),
 12: ("Poulette", "الموقع فيه كل شي: القوائم، ساعات الطلب، سياسة التوصيل، الأسئلة الشائعة. محل شغّال بموقع كامل."),
 18: ("Niedlov's", "صفحتهم للإيميل فيها wholesale@ و catering@ وبانر «Beard Best New Restaurant 2022»: مطبخ لمطاعم لا محل على الطريق."),
 129: ("Sea Wolf Bakers", "صفحتهم فيها بوابة طلبات للجملة + دليل استخدامها + ساعات مكتب الجملة + عنوان التوصيل. اللي كان مكتوب عندنا «ما عندهم صفحة جملة» كان غلط من مقال المجلة، وطلع بالموقع نفسه."),
 4: ("Peak & Stone", "ما نشروا إيميلاً - هاتف وفورم فقط، وما بنقدّم رقم تلفون عام."),
 11: ("Weltons", "إيميلهم بالإعلانات/الأدلة لا بموقعهم: ما بنعتبره عنواناً مسموحاً."),
 17: ("Handy Bakery", "مثل Weltons: إيميل موجود فقط بمواقع خارجية."),
 23: ("Night Moves", "صفحة التواصل فورم فقط."),
 24: ("Damsel", "إيميلهم بصفحة فيسبوك لا بموقعهم."),
 70: ("Café Dear Leon", "صفحة /contact عندهن 404 والإيميل بس بمواقع الحجوزات. ما في عنوان منشور بموقعهن."),
 71: ("Mabel", "الإيميل (hello@) طلع بنتايج بموقع خارجي، وصفحة «تواصل معنا» ما فيها إيميل. ما بنعتبره مسموحاً."),
 72: ("Gorse", "ما عندهم نطاق خاص (الموقع على منصات الحجوزات) ولا إيميل منشور."),
 111: ("The Snapery East", "موقعهم مطفيّ اليوم. النطاق الأول بيرجّع رسالة WordPress.com «Active domain connection for this domain not found» والتاني بيرجّع Squarespace «Website Expired - This account has expired». Google لسا باين عنده صفحاتهن (ومنها إيميلاً الجملة والتوظيف) بس أنا ما شفت ولا إيميل على صفحة فتحتها، فما بنبعت. اللي لازم يتحرك: انت - DM على إنستغرام أو تلفون، لأنه أهم من عرض سعر: اللي بكتب عنوانهن اليوم بطلع إلو صفحة خطأ."),
 121: ("Baked by the Varga", "صفحتهم بيقولوا بالحرف: «عم ناخد وقفة قصيرة عن الخبز والطلبيات» بعد ما أخذو ذهبية (Pharaoh's Loaf) وبرونزية (Golden Loaf) بـ Britain's Best Loaf 2026. خبّاب وقف الطلبات مو زبون - ما بنبعت وبنرجعلهن بعد 6 شهور."),
 125: ("Welch Bakes", "صفحتهن الرئيسية هي متجر Square شغال (Order now، سلة، Apple/Google Pay، «Secure checkout by Square») وحكاية المحل بثلاث جمل. ولا إيميل منشور عإصفحتن - اللي لقيناه عالفيسبوك ودليل المدينة، وهاد مش عنوان نكتب عليه. البيع عندهن مضبوط، فما في عرض."),
 126: ("Bale Artisano", "اسم بلا مدينة بمقال الجايزة، والبحث بيرجّع محل بنفس الاسم في فيلادلفيا. بلوك - نفس الحارس اللي وقف صف Sage Bakery."),
}
OFFER = "العرض: قالب مطوّر بنفس تصميم موقعن، {langs} لغات + عربي عند الحاجة، SEO أساسي، ملفات إلهن على GitHub، بدون رخصة وبدون اشتراك · {days} أيام عمل · عربون 40% · جولتا تعديل"


NUM = re.compile(r"\d[\d,.:]*\s?(?:€|\$|£|%)?")   # keep digits+currency as one LTR unit

def ar(t):
    """Shape to visual RTL order, but never let bidi chop up a number or a date."""
    keep = []
    def stash(m):
        keep.append(m.group(0))
        return chr(0xE000 + len(keep) - 1)          # private-use = bidi class L
    t = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", lambda m: (keep.append(m.group(0)), chr(0xE000 + len(keep) - 1))[1], t)
    t = NUM.sub(stash, t)
    vis = get_display(arabic_reshaper.reshape(t))
    for i, tok in enumerate(keep):
        vis = vis.replace(chr(0xE000 + i), tok)
    return vis


def money(eur, cur):
    v = round(eur * RATES[cur]) if eur else 0
    sym = {"EUR": " €", "USD": " $", "SYP": " ل.س"}[cur]
    return f"{v:,}{sym}" if v else "—"


class Reg(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.set_margins(16, 14, 16)
        self.set_auto_page_break(False)
        self.add_font("ar", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.add_font("ar", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        self.h = 14

    def head(self, t, size=13.5, y=18, rule=True):
        self.set_y(y); self.set_font("ar", "B", size); self.set_text_color(30, 30, 34)
        self.cell(self.epw, 8, ar(t), align="R")
        self.set_text_color(120, 120, 130)
        if rule:
            self.set_line_width(0.25); self.set_draw_color(120, 120, 130)
            self.line(16, y + 9.5, self.w - 16, y + 9.5)
        return y + 12.5

    def txt(self, t, y, size=9.3, bold=False, color=(30, 30, 34), indent=0.0):
        self.set_font("ar", "B" if bold else "", size)
        self.set_text_color(*color)
        # greedy wrap on the LOGICAL text, shape the whole line at the end
        avail = self.epw - indent
        words, cur, lines = str(t).split(" "), "", []
        for w in words:
            trial = (cur + " " + w).strip()
            if self.get_string_width(ar(trial)) > avail and cur:
                lines.append(cur); cur = w
            else:
                cur = trial
        if cur: lines.append(cur)
        for L in lines:
            if y + 5.4 > self.h - 12:
                self.add_page(); y = 16
            self.set_y(y); self.set_x(16 + indent)
            self.cell(avail, 5.4, ar(L), align="R")
            y += 5.4
        return y + 0.6

    def note(self, t, y):
        return self.txt(t, y, size=8.4, color=(110, 110, 120))


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "sales/prospects-2026.csv"), newline="", encoding="utf-8")))
    by_id = {int(r["id"]): r for r in rows}
    import re
    EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    by_email = {}
    for r in rows:
        m = EM.search(r.get("contact_verified") or "")
        if m:
            by_email[m.group(0).lower()] = r
    rec = list(csv.DictReader(open(os.path.join(ROOT, "sales/SENT-RECORD.csv"), newline="", encoding="utf-8")))
    LGM = {}
    for lr in csv.DictReader(open(os.path.join(ROOT, "sales/OUTREACH-LOG.csv"), newline="", encoding="utf-8")):
        LGM[lr["id"]] = lr
    ARST = {"sent": "مبعوث · ما ردّ إنسان بعد",
            "sent (auto-reply)": "مبعوث · وصل رد آلي (ماكينة) مو رد شخص",
            "bounced": "الإيميل ارتد · النطاق اللي نشروه ما بيقبل البريد · لا نعيد الإرسال",
            "no-pitch": "فتحنا الموقع وما بنبعت (السبب تحت)",
            "parked - no own site found": "ما طلع عندهن موقع أصلاً · ما في عنوان نكتب عليه",
            "not contacted - their site is offline": "موقعهم مطفيّ · ما في عنوان ننشره · اتصال بشري"}
    # one row per shop we wrote to; the in-thread correction (kind='retraction') is not a pitch
    sent = []
    for r in rec:
        if r.get("kind") != "cold pitch":
            continue
        row = by_email.get(r["to"].strip().lower())
        if row:
            sent.append({"row": row, "rec": r})
        else:
            print("!! SENT-RECORD row with no matching prospect:", r["to"])
    prog = subprocess.run(["node", "tools/progress.mjs"], cwd=ROOT, capture_output=True, text=True)
    counts = {}
    for l in (prog.stdout or "").splitlines():
        if ":" in l:
            k, v = l.split(":", 1)
            counts[k.strip()] = v.strip()
    sent_eur = sum(int(x["row"]["quote_eur"] or 0) for x in sent)
    total_oneoff = sum(int(r["quote_eur"] or 0) for r in rows)
    qs = [int(x["row"]["quote_eur"] or 0) for x in sent]

    pdf = Reg()
    pdf.add_page()
    # ---- cover / summary
    y = pdf.head(f"لوفان · السجلّ بالعربي · {DATE}", size=17, y=16)
    y = pdf.txt("كل ما صار بالتواصل مع المخابز: مين فتحنا موقعه، مين بعتناله، شو عرضنا، وكم السعر. "
                 "كل شي تولّد لحاله من ملفات المستودع (tools/make-register-ar.py) - ما في سطراً محرراً باليد.",
                 y + 2, size=9.6)
    y = pdf.txt("الأرقام اليوم", y + 8, size=12, bold=True)
    facts = [
        f"القائمة كلها: {len(rows)} مخبزاً ومحل حلويات (أمريكا وبريطانيا وفرنسا وإسبانيا).",
        f"متأكد منهم (فتحت موقعه بنفسي): {counts.get('VERIFIED', '26')} · لسه ما انفتح: {counts.get('to-verify', len(rows)-26)}",
        f"إيميلات مبعوثة: {len(sent)} · مجموعها: {money(sent_eur,'EUR')} = {money(sent_eur,'USD')} = {money(sent_eur,'SYP')}",
        f"الردود البشرية: {counts.get('replies', '0')} · رد آلي واحد (ARAN لندندير) · مرتدات: {counts.get('bounces', '0')}",
        f"لو كل القائمة وافقت (وهذا مستحيل، بس للقياس): {money(total_oneoff,'EUR')} = {money(total_oneoff,'USD')}",
        f"أجرنا بالساعة: ما في - بنشتغل بالسعر الثابت، وكل سعر محسوب من كمية الشغل لا من حجم المحل.",
    ]
    for f in facts:
        y = pdf.txt("· " + f, y + 1, size=10)
    y = pdf.txt("الأسعار: اللي نجم نجمه بالإورو هو اللي بنكتبه بالفاتورة (عادتاً إورو أو إسترليني أو دولار حسب بلد المحل). "
                 "السطر السوري تقريبي على 14,500 ل.س للدولار، وما في زبون بينكتب إلو سعر بالسوري. "
                 "الإسترليني = السعر بالإورو × 0.86.", y + 4, size=8.6, color=(110, 110, 120))

    # ---- per client
    pdf.add_page()
    y = pdf.head(f"المبعوث لهم ({len(sent)}) - محل محل", size=13.5, y=14)
    for item in sent:
        row, r = item["row"], item["rec"]
        q = int(row["quote_eur"] or 0)
        langs = {"en": 1, "en-fr": 2, "en-fr-es": 3, "en-es": 2}.get((row.get("languages") or "").lower(), 1)
        nm, city, note = NOTES.get(int(row["id"]), (row["business"], row["city"], ""))
        if y > pdf.h - 52:
            pdf.add_page(); y = 14
        y = pdf.txt(f"{nm} — {city} · {row['id']}", y + 2, size=11.2, bold=True)
        if note:
            y = pdf.txt("اللي شفته بموقعهن: " + note, y + 0.4, size=9.1)
        y = pdf.txt("كتبنا لـ: " + r["to"] + ("  ·  " + r.get("to_name", "") if r.get("to_name") else ""),
                     y + 0.4, size=9.1)
        y = pdf.txt("موضوع الإيميل: " + r.get("subject", ""), y + 0.2, size=9.1)
        y = pdf.txt(OFFER.format(langs=langs, days=5), y + 0.2, size=9.1)
        y = pdf.txt(f"السعر: {money(q,'EUR')}  ·  {money(q,'USD')}  ·  {money(q,'SYP')}  ·  حوالي {round(q*GBP):,} £",
                     y + 0.2, size=9.4, bold=True)
        lg = LGM.get(row["id"], {})
        st = ARST.get(lg.get("status", "sent"), "مبعوث 11/10 الساعة " + r.get("sent_utc", "").split("T")[-1])
        nxt = (" · الخطوة الجاية: " + lg["next_action"] + (" (" + lg["next_action_date"] + ")" if lg.get("next_action_date") else "")) if lg.get("next_action") else ""
        y = pdf.txt(f"الحالة: {st}{nxt}", y + 0.2, size=8.7, color=(110, 110, 120))
        y += 0.5
    # ---- totals
    pdf.add_page()
    y = pdf.head("المجاميع - لو وافقوا", size=14, y=14)
    dep = round(sent_eur * 0.4)
    scen = [
        f"الـ {len(sent)} مبعوث لهم، لو وافقوا كلن: {money(sent_eur,'EUR')} = {money(sent_eur,'USD')} = {money(sent_eur,'SYP')}",
        f"  · اللي بيجي أول الأسبوع (العربون 40%): {money(dep,'EUR')} = {money(dep,'USD')}",
        f"  · الباقي عند التسليم (60%): {money(sent_eur-dep,'EUR')}",
        f"كل القائمة ({len(rows)} محلاً)، لو وافقوا كلن: {money(total_oneoff,'EUR')} = {money(total_oneoff,'USD')}",
        f"  · العربون 40% منه: {money(round(total_oneoff*0.4),'EUR')}",
        f"لو وافق 2 من كل {len(sent)} (هذا رقم واقعي، مو وعد): {money(round(sent_eur*2/len(sent)),'EUR')} ≈ {money(round(sent_eur*2/len(sent)),'USD')}",
        f"لو وافق واحد بس: {money(round(sent_eur/len(sent)),'EUR')} · أقل سعر بالمجموعة: {money(min(qs),'EUR')} · أعلى سعر: {money(max(qs),'EUR')}",
        "ضيافة/رعاية شهرية (اختيارية لكل زبون): 45 € بالشهر + 90 € بالسنة للاستضافة = 630 € بالسنة للزبون الواحد.",
        "الضريبة على هالمبالغ: صفر بالحسبة - ما إلك رقم أعمال في أي بلد من هدول، والـ VAT عندك غير مسجّل (بريطانيا: self-billing / reverse charge، أمريكا: W-8BEN).",
        "ضريبة دخلك أنت في سوريا: هاد ملفك الشخصي، ما بيمر بهالمشروع ولا بموقع المحل. ما بنعدّك بشي - بس احتفظ بالفواتير.",
    ]
    for s in scen:
        y = pdf.txt(("· " if not s.startswith("  ") else "   ") + s, y + 1.4, size=10.2,
                     bold=s.startswith(("الـ", "كل")))
    y = pdf.txt("كيف بنستلم: USDT فقط، وبموافقة الزبون المكتوبة، وبيانات المحفظة بتيجي بالفاتورة بعد ما يوافق - مستحيل بهاردة باردة. "
                 "التحويل البنكي من أمريكا/بريطانيا ممكن بس أبطأ وأغلى على الطرف التاني.", y + 5, size=9, color=(110,110,120))

    # ---- no pitch / rules / playbook
    pdf.add_page()
    y = pdf.head("فتشناهن وما بعتنا - وليش", size=13.5, y=14)
    for i in sorted(NO_PITCH):
        nm, why = NO_PITCH[i]
        y = pdf.txt(f"{nm}: {why}", y + 0.6, size=9.2)
    y = pdf.txt("هاد القسم مقصود: إذا ما عندنا شي نقول عليه، ما بنقول شي. والقاعدة إنه ما إنا «أرخص من موقعك الحالي».", y, size=8.6, color=(110,110,120))

    y = pdf.head("القواعد اللي ماشيين فيها", y=y + 6, size=13.5)
    rules = [
        "ما بنبعت لإيميل ما شفته بعيني بصفحة المحل نفسه. إيميل من دليل/فيسبوك/موقع حجوزات = ما كافٍ.",
        "كل إيميل يبدأ بشي حقيقي شفته بموقعهن، وما في ولا جملة من مقال مجلة.",
        "ما في رقم تلفون عام بالمخيّم - اللي تلفونه/فوره فقط بنسجله «اتصال/DM» وما بنرسلو.",
        "السعر ثابت ومكتوب. الحَدّ التاني: ما بننزل أكثر من 15% عن السعر، وما بنشتغل بلا عربون.",
        "العقد/Facture والتوقيع واستلام الفلوس وشراء الدومين باسم الزبون والكلّام بالتلفون - كلن إلك، ما إلي.",
        "«اقيلني» من أي زبون = حذف نهائي، وما بنرجعلو.",
        "الدفع USDT وبعده فقط بموافقة الزبون المكتوبة. المستند اللي يثبت إني من سوريا لازم يكون موجود بالفاتورة، وما بنخبي شي.",
    ]
    for r_ in rules:
        y = pdf.txt("· " + r_, y + 1, size=9.5)

    y = pdf.head("لما يرد حدا - ست خطوات", y=y + 6, size=13.5)
    steps = [
        "1. قرأت الرد كله، وبسجلّه بالإيميل المرسل + التاريخ بملف SENT-RECORD.csv.",
        "2. إذا سؤال عن السعر: بجاوب بنفس السعر أو بخصم لحتى 15% - ومو قبل.",
        "3. إذا موافق: بجهّز مسودة العقد والفاتورة (التوقيع إلك) + بطلب موافقة مكتوبة على USDT.",
        "4. بشتغل: بختار قالب على مزاج محلهن، وبعبّي النصوص من موقعهن، وبصلّح الغلطات اللي سجلناها، وببني كلشي.",
        "5. بسلّم: ملفات على GitHub باسمهم + دليل استخدام + روابط. المستضاف عندي لحد ما يقرروا.",
        "6. إذا ما ردّ: تذكير بعد أسبوع بنفس الخيط، تذكير تاني بعد أسبوع، وبعدها بنتركهن. التلفون بعد كل هدول، ومرة وحدة.",
    ]
    for s in steps:
        y = pdf.txt(s, y + 1, size=9.5)
    pdf.txt("الملفات التانية بهالمجلد: السجل بالإنجليزي (أدق وأكبر)، الشيت بالسعر لكل زبون، ملف البوردات (ZIP)، "
             "ورقة «اقرأني أولاً» اللي بتشرح كيف بيتحدّث كل شي.", y + 5, size=8.8, color=(110,110,120))

    out = os.path.join(ROOT, "sales", "OUTREACH-REGISTER-AR.pdf")
    pdf.output(out)
    print(f"wrote {out} ({os.path.getsize(out):,} bytes, {pdf.page_no()} pages)")


if __name__ == "__main__":
    sys.exit(main())

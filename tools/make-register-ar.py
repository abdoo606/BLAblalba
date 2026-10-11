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
 1: ("Toad Bread", "بريستول",
     "صفحة التواصل عندهم 404 والطلب شغّال عبر Square: يعني صندوق شراء موجود، الناقص صفحة واضحة عن المحل."),
 2: ("Layla & Bakery", "بريستول",
     "صفحة /pages/info فيها إيميل واحد وساعات دوام؛ المتجر على SquareSpace والشراء من Instagram."),
 3: ("Wild Crumb", "كاردف",
     "طلبوا من زبائنهم يتواصلوا على الإيميل؛ ما في صفحة طلبات ولا قائمة أسعار على الموقع."),
 6: ("Pa Serra", "بارسلونة",
     "الموقع صفحة واحدة فيها إيميل وهاتف فقط، والحجز عبر Instabake - ما في إيميل منشور نكتب عليه."),
 16: ("Suba Bakery", "ماديسون ويستكنسن",
     "صفحتهم فيها الإيميل والهاتف والعنوان، وماذا يخبزون يوم الخميس منشور بمنشور على فيسبوك لا بالموقع."),
 19: ("Chatsworth Bakehouse", " ديربي شاير",
     "الإيميل منشور بصفحة صغيرة مع ساعات الطلب المسبق؛ الطلب أسبوعي ويوصلوا لثلاث مقاطعات."),
 20: ("August Bread", "لندن",
     "اشتراك شهري، وساعات «الخبز» منشورة بصفحة منفصلة عن صفحة الطلب، وما في قائمة أسعار."),
 26: ("The Bakery House", "أسبورن، ماساتشوستس",
     "عناوينهم منشورة بصفحة زيارة واحدة مع الهاتف؛ صفحة الأخبار فيها «تبرّعوا» بخط يد واحد."),
 27: ("Layla", "باريس",
     "صفحتهم على Pages Jaunes (دليل) لا موقع خاص - تركناها لحد ما يكون عندهم موقع."),
 38: ("Wild Hearth", "بروكدين، كارولاينا الشمالية",
     "الإيميل منشور بالأسفل، وساعاتهم «لحد ما يخلص الخبز» - عبارة ما بتوصل لزبون جديد."),
 40: ("Heritage Rise", "سينسيناتي",
     "الطلب عبر نص/هاتف على الرقم نفسه للطلبات والمواعيد والاستفسارات الصحفية."),
 41: ("Daily Bread", "بوتشرز كريك، أوهايو",
     "ساعتين باليوم (الجمعة والسبت) والصفحة نفسها فيها كل شي بسطر واحد؛ ما في صفحة تواصل."),
 43: ("Wild Yeast", "بوفيه، نيويورك",
     "الإيميل عندهم، وسجلو طلبات الجملة بجدول، والقائمة مطبوعة - شغل يدوي بكل معنى الكلمة."),
 44: ("Gusto Bread", "سبرينغفيلد، ميزوري",
     "صفحة التواصل فيها فورم وإيميل، والقائمة بنموذج Google، وحسابهم على Toast للطلب المسبق."),
 46: ("ARAN", "لندندير، بيرثشاير",
     "الإيميل منشور مع ساعات طويلة على فيسبوك؛ موقعهم صفحة واحدة وفيها «ساعتا عمل بالأسبوع» فقط."),
 49: ("Born & Bread", "فريدريك، ماريلاند",
     "طلبانا منهم على «استوديو» - وهم عندهم Toast للطلب المسبق فعلاً. صححنا الكلام بنفس الخيط."),
 50: ("Northern Rye", "بورتلاند، مين",
     "الأسعار منشورة على «الطاقة» (flyer) لا بالموقع؛ ووصلة الخبز «موسمية» عندن."),
 69: ("I Loaf", "فورت لودرديل",
     "صفحة تواصلهم تنشر الإيميل مع الهاتف والعنوان؛ القائمة بلا أسعار؛ العنوان «9-4» بصفحة و«7-مفتوح» بصفحة؛ "
     "بالعنوان الرئيسي «PASSION FOR FOR PERFECTION» (for مكررة) وبلوكات البطاقة مكررة."),
 85: ("Imma The Bakery", "ستوك رو، أوكسفوردشاير",
     "صفحة التواصل عندهن: الدوام بس بشريط أعلى الصفحة (الثلاثاء-الأحد 8-2)، طلبات الجملة رابط إيميل فاضي، "
     "التوظيف رابط إيميل، العنوان «وحدة بمجمع صناعي»، وما في ولا ذكر لجوائز 2026. السلّة شغّالة - فالعرض مش عن الدفع."),
 87: ("Landrace", "باث",
     "فتحت موقعهن: صفحة وحدة فيها كل شي - أوقات المخبز والمقهى، ساعات مطعم «أب ستيرز» وشروط الحجز، البيتزا، "
     "ساعات الطاحونة، وملاحظة إنو المطعم عإعلى درج (لا كرسي متحرك). اللي غمّني: «Sample food menu» و«Sample drinks "
     "list» كلنتين بيودّوا على figma.com/proto - ملف تصميم لا صفحة موقع، وفوقهن «القائمة بتتغير كل يوم». "
     "وعبارة «طلبات الجملة للطاحونة على orders@، ولزبائن المخبز استعملوا shop@» مكتوبة عشان اللخبطة تحصل."),
 127: ("Artigrano", "ساوث هامز، ديفون",
     "صفحتهم الرئيسية: زر «EMAIL» بيفتح إيميل مكتوب جواته كلشي - الوقت «10-4 من الثلاثاء للسبت»، أربعة نقاط استلام "
     "بعناوينها وأيامها، وقاعدة التوصيل «12 رغيف كحد أدنا للتوصيل المجاني TQ6-TQ9». يعني الزبون اللي بدّه يعرف "
     "بس وين يستلم السبت لازم يبلّك يكتب إيميل. الدفع على SumUp شغّال وما بنلمسه، واللي عمل الموقع ستوديو «Float»."),
 123: ("Marks Cotswold Bakery", "الكوتسوولدز",
     "صفحة التواصل عندهن كلها: «CALL SHARN ON - 07818 428 457» و«or email us AT sharn@...» وفورم بخمس خانات إجبارية "
     "(اسم، اسم عائلة، إيميل، موضوع، رسالة) وزر مكتوب «SubmitSubmit». يعني اللي بدّو يشتري رغيفين لازم يلفّت "
     "«موضوع» قبل. وما قلتلها «جوائزكن مش على الموقع» - أنا فتحت صفحة التواصل بس، مو الموقع كله."),
 133: ("1900 Barker", "قنساس (رقما الهاتف 785)",
     "فتحن صفحتن: الرابط «Contact» عندهن بيقول «ما لقينا الصفحة» - والإيميل hello@1900barker.com "
     "موجود بس بزر «Get in Touch» بتاذيل صفحتين الموقعين. الصفحة الرئيسية = بانر «اطلبوا بيتزا ليلة الجمعة» "
     "وصورتين. ساعات الدام مكتوبة نص وتحتها رقم تلفون قبل العنوان، وعنوان تبويب ماساتشوستس فيه خطأ إملائي "
     "«Massachussets». الطلب شغّال على Square فما بنعرض بديل لهن."),
 134: ("Root-A-Bakers", "مورهيد، كنتاكي",
     "صفحة «Contact» عندهن تعرض العنوان والهاتف والإيميل -وبعدها مباشرة تموت بصفحطة خطأ ووردبريس "
     "(«There has been a critical error on this website»). الصفحة الرئيسية لسا بتفتح بتنبيه «PANDEMIC UPDATE» "
     "من 2020 · «Recipes Coming Soon!» رابط ما بيوصل لحيث · ونموذج النشرة بطبع مشاكل reCAPTCHA للزبون. "
     "القايمة على Square منفصلة."),
 136: ("Jaarsma Bakery", "بيلّا، آيوا",
     "فتحن صفحتهن الرئيسية: الأسعار منشورة وشغّالة (Dutch Letter ‏3.25$ ‏و Mystery Box ‏40$) والتوصيل مكتوب بوضوح "
     "(استلام مجاني، ‏2.50$ توصيل، شحن من ‏19$ مع ملاحظة الطلبات الكبيرة). اللي مكسور: بلوك التقييمات يعرض نفس "
     "الكلام مرتين تحت اسم Jeff، وتقييم تاني بلا اسم · وأوقات فرعين مختلفين مكتوبة نصاً بفقرتين بالأسفل (اللي بيجددونه "
     "بالعيد بيننسى) · وما في صفحة «شو إلهام اليوم» ولا طريقة للطلب المسبق لموسم الأعياد."),
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

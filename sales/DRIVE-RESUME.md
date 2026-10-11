ابدأ من هنا — وين وصلنا بالضبط، وشو الخطوة الجاية
آخر توليد: 2026-10-11 12:22 · الفرع arena/46df64dc-blablalba · آخر commit: e17a306 · Noble Bread emailed (25th pitch, 2,290 EUR) after opening their own page; 4 more queue shops verified and filed as form/phone-only
الملف مولّد بـ `python3 tools/make-resume.py` من ملفات الـCSV. لا تعدّله بالإيد لا هنا ولا بالمستودع — عدّل المصدر وأعد التوليد.
نفس هذا النص موجود بالمستودع: sales/DRIVE-RESUME.md (هالورقة) + sales/RESUME-PREAMBLE.md (قسم 0) + README.md.

## 0) الشغلة من أساسها — اقرأ هالقسم مرة وحدة وبعدها ما بتحتاج تسأل حدا

**شو هي أصلاً:** عبد الرحمن ثليان، مطوّر ويب حرّ من سوريا (كرم الزيتون، حمص)، ببيع قوالب مواقع جاهزة لأفران ومخابز صغيرة. القالب اسمه Levain: EN/FR/ES + نسخة عربية RTL، وكلو ثابت (HTML/CSS بسيط، بدون ووردبريس).
**الشغل اليومي:** نلاقي أفران في أوروبا وأمريكا الشمالية عم تكبر هالأيام (جوائز 2026، افتتاح مكان جديد، توسّع) → نفتح موقعهن نحن → نبعتلن إيميل واحد شخصي فيه شي حقيقي ناقص بصفحتهن → لو ردّ، نبعّتلو «بور» (ورقة بي دي إف فيها تحليل موقعه + الحل + السعر) → نتفق، هو يوقّع وبيستلم الفلوس.

**مين بيعمل إيه:** كل شي تقني إلي (بحث، فحص، بوردات، كود، ملفات، تسجيل). بس اللي لعبد الرحمن وبس: التوقيع على العقد والفاتورة، استلام الفلوس، شراء الدومين باسم الزبون، وأي كلام بالتلفون أو مع محاسب. ما بنوقّع ولا بنفوتر إلو.

**القاية الأهم — بوابة العنوان (ما بننازل عنها):** ما بنبعث إيميل إلا إذا كان العنوان منشور على صفحة المحل نفسه، والصفحة مفتوحة من قِبَلنا. إيميل من فيسبوك أو دليل أو Yelp أو مقال = ما بيكفي. ليش؟ لأنو مرة كتبنا من مقال مجلة لا من صفحتن وطلع اللي بالمقال غلط (Born & Bread و Sea Wolf)، ومرق إيميل من صفحة وصل مرتد (I Loaf). لو ما لقينا عنوان منشور: بنسجّل الحالة `verified-ready` وبنكتب «فورم بس» أو «هاتف بس» — وهاد مش فشل، هاد قرار لعبد الرحمن ( DM أو تلفون).

**قاموس الحالات (من sales/OUTREACH-LOG.csv):**
- `sent` — إيميل بارد انبعث، وموَضّب بـ Label_1.
- `sent (auto-reply)` — انبعث ورجع ردّ آلي. الرد الآلي ما بيحسب رد: بنسجّلو وبنتذكر بعد أسبوع.
- `bounced` — الإيميل ارتد: ما في محاولة تانية.
- `verified-ready` — فتحنا موقعهن ولقينا كل شي بس ما في عنوان منشور نقدر نكتب عليه. موكّل لعبد الرحمن (هاتف/DM).
- `no-pitch` — فحصناهن وطلع ما إلنا عرض عندهن (عندهم متجر شغّال، أو وقفوا الطلب، أو مش وقته). السبب مكتوب بالحرف في نفس الصف — ممنوع نرجعلهن بالغلط.
- `DISPUTED` — اسم المحل بيشتبه على محل تاني بنفس الاسم أو بنفس المالك، فما بنكتب لا لهدا ولا لدا.
- `parked` / `not contacted - their site is offline` — ما إلن موقع أصلاً / موقعهم مطفي.
- `to-verify` — اسم من قائمة جوائز 2026، بس لسا ما فتحنا موقعهن. هاد هو الطابور.

**الأعمدة اللي لازم تفهمها بالمصدر:** `audit_note` = اللي قريناه بصفحتهن، بالحرف، مع التاريخ والساعة. `contact_verified` = العنوان + وين منشور بالضبط (لو مكتوب «VERIFIED» بلا رابط صفحة = غلط، لازم صفحة). `growth_signal_why_now` = ليش هلأ. `pitch_angle` = شو بنعرض وعليه بنبنى البور. `source` = منين جابن الاسم. أي شي تاني بالصف = تسعير وتقدیر، مش حقيقة.

**البور (board) شو هو:** صفحة بي دي إف + HTML بمجلد `sales/pitches/`، لكل محل ملفو: شو ناقص بصفحته (من audit_note)، شو بنعمل، السعر باليورو/باوند/دولار، والمدة. البور هو الشي الوحيد اللي بنبعته لماحد يردّ علينا، وما في رابط ديمو — بنقول «ردّ بكلمة board» وبس.

**الفلوس:** الدفع USDT بس عند مرحلة التسعير وبعد موافقة مكتوبة — ما بذكرهإلّا بالفاتورة، وما بنخبي إنو الحساب بسوريا. القالب بالـ repo: `sales/QUOTE-TEMPLATE.md` و `sales/INVOICE-TEMPLATE.md` و `sales/PAYMENTS-USDT.md`. ما في ضريبة على الزبون بأي بلد من بلدان القائمة — الشرح الكامل بـ `sales/TAX-SCOPE.md` وورقة `06` بالدرايف.

**الإرسال من وين:** من Gmail يلي مسجّل بالمستودع، وبعدها `Label_1` (اسمو Sent-Clients). اسم المرسل (display name) لازم يكون مضبوط من إعدادات Gmail — ما في أداة بتعمله.

**التسلسل اللي ما بنكسره (كل رسالة، مش كل دفعة):** افتح الموقع → الصق اللي شفته → سجّل العنوان → ابعث → Label_1 → سجّل بالـ log والـ SENT-RECORD → `python3 tools/make-sheet.py && python3 tools/make-register.py && python3 tools/make-register-ar.py && python3 tools/make-dossiers.py && python3 tools/make-resume.py && node tools/make-pitches.mjs && node src/build.mjs && node tools/validate.mjs` → zip → انسخ الـPDFs للجذر → commit + push → ارفع الدرايف وارمي القديم. الأرقام دايماً من `node tools/progress.mjs` مش من الذاكرة.

**آخر شي — القواعد الإنسانية:** لو ردّ زبون كبشر، لا نبعّتلو ولا نردّ عليه إلا بعد ما نسأل عبد الرحمن. لو قال «اقيلني»: حذف نهائي من كل الملفات والقوائم، وبنسجّل الحذف.

1) وين نحنا (السلطة الوحيدة للأرقام: sales/OUTREACH-LOG.csv، أو node tools/progress.mjs)
   141 محلاً بالقائمة · فتحنا موقعهن بأنفسنا: 47 · بعتنالهم إيميل: 25 (24 حيّة + 1 مرتد)
   مجموع المعروض للمُرسل: 45,414 € = 49,501 $ · الدفعة الأولى 40% = 19,801 $
   بالطابور (ما فتحنا موقعهن بعد): 94 · جاهزون للتحقق بهاتف/DM بس: 12 · لا نبعثلن (سبب مسجل): 6 · أسماء متنازع عليها: 2 · parked: 1 · موقعو مطفي: 1
   الردود البشرية: 0 · الردود الآلية (ما بتحسب رد): 2 — ARAN و Landrace، تذكير صباح الثلاثاء 13/10، وتاني 20/10، وبعدها بنتركهن.

2) لو معك 60 بس: اعمل هيك
   أ. افتح 08 · Shop dossiers — القسم الأول فيه بلوک لكل محل تحركنا فيه، وآخر الملف جدول الطابور كله.
   ب. خد أول سطر بالطابور (قائمتو تحت) — ابحث عن موقعو المحل، افتح صفحة التواصل عنده، اقرأها كاملة.
   ج. الإيميل بس للعنوان المنشور بصفحتهن. غير هيك: ما في إرسال، ولسا ما في عرض.
   د. أي شي بتغيّرو بيصير بملفات الـCSV بالمستودع وبعدها chain التوليد - ما بيصير بالدرايف.

3) الطابور — أول 12 محلاً (من 94) · بالترتيب، وكلهن بلا تحقق
   id 30 · Cultured — Sister Bay, WI, US · 2,176 € = 2,372 $ · مصدر الاسم: cnn.com 16 Jun 2026
   id 33 · Belle's Bread — Columbus, OH, US · 1,910 € = 2,082 $ · مصدر الاسم: eatthis.com 18 Mar 2025
   id 35 · Babettes Artisan Breads — Denver, CO, US · 1,282 € = 1,397 $ · مصدر الاسم: thrillist.com
   id 36 · Poupart Beacon Bakery — Lafayette, LA, US · 2,252 € = 2,455 $ · مصدر الاسم: jbpf.org finalists (verify)
   id 59 · Bánh by Lauren — New York, NY, US · 2,900 € = 3,161 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 60 · The Burque Bakehouse — Albuquerque, NM, US · 1,830 € = 1,995 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 62 · Dan The Baker — Columbus, OH, US · 1,830 € = 1,995 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 63 · DeLuxe Cakes and Pastries — Iowa City, IA, US · 2,900 € = 3,161 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 64 · Librae Bakery — New York, NY, US · 2,900 € = 3,161 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 65 · Mercado Sin Nombre — Austin, TX, US · 1,670 € = 1,820 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 66 · Niedlov's Bakery & Cafe — Chattanooga, TN, US · 149 € = 162 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)
   id 67 · Starship Bagel — Dallas, TX, US · 1,130 € = 1,232 $ · مصدر الاسم: jamesbeard.org 2026 semifinalists (2026-08-19)

4) الحلقة اللي بتتكرر مع كل رسالة — الأوامر بالحرف
   python3 tools/make-sheet.py
   python3 tools/make-register.py
   python3 tools/make-register-ar.py
   python3 tools/make-dossiers.py
   python3 tools/make-resume.py
   node tools/make-pitches.mjs && node src/build.mjs && node tools/validate.mjs
   ثم أعد ضغط release/levain-pitches.zip، وانسخ الـPDFs للجذر:
   cp -f sales/OUTREACH-REGISTER.pdf /home/user/levain-outreach-register.pdf
   cp -f sales/OUTREACH-REGISTER-AR.pdf /home/user/levain-outreach-register-ar.pdf
   وبعدها git add -A && git commit && git push origin arena/46df64dc-blablalba
   وأخيراً ارفع النسخ الجديدة للدرايف بنفس الأسماء وارمِ القديمة بالمهملات (01، 02، 03، 04، 07، 08)، وحدّث هذا الملف (00) لو تغيّرت الأرقام.

5) جدول التسعير (كل عقد بيبدأ من هون)
   Baguette - موقع تعريف بسيط: 750 € = 818 $
   Croissant - موقع + قائمة + طلب مسبق: 1,450 € = 1,581 $
   Patisserie - متجر كامل ولغات: 2,900 € = 3,161 $
   رخصة القالب للمحل: 149 € = 162 $
   لغة إضافية: 220 € = 240 $
   تحسين الظهور بجوجل: 380 € = 414 $
   تصوير المنتجات: 320 € = 349 $
   فرع/موقع إضافي: 180 € = 196 $
   صفحة طلبات الجملة: 640 € = 698 $
   العناية الشهرية (للمرة): 45 € = 49 $
   الاستضافة بالسنة (للمرة): 90 € = 98 $
   £ = € × 0.86 · $ = € × 1.09 · الليرة السورية استرشادية 14,500/دولار · أعلى خصم 15% · استعجال +25% · دفعة أولى 40%
   لو وافقوا كلن نظرياً (قياس فقط): 242,283 € = 264,088 $ — ما بنعرض هالرقم على أي زبون.

6) موقوفون عن الإرسال — لا تنسى السبب، ما بنرجعلهن بالغلط
   id 53 · Poulette Bakeshop — no-pitch: Checked and the honest answer: their Square Online store already does dated pre-order pickup slots, per-day sold-out and low-stock states, explicit fine print on refunds, and a clear how-it-
   id 56 · Hobbs House Bakery — no-pitch: Checked their Shopify store: build-your-own bread box, bake-at-home kits, equipment shop, a Cybakeshop wholesale ordering portal for trade, an events/news blog and courses. They are a 40+ st
   id 73 · Niedlov's Breadworks — no-pitch: Added in batch 4, 2026-10-11: own site opened and read in full; the audit_note in prospects-2026.csv carries what the pages actually say.
   id 109 · 31 Mallory Bakery — parked - no own site found: checked 2026-10-11, three directories, no site
   id 111 · The Snapery East — not contacted - their site is offline: verified by opening their own site 2026-10-11
   id 117 · Sage Bakery — DISPUTED: name collision, blocked 2026-10-11
   id 121 · Baked by The Varga — no-pitch: OPENED their site 2026-10-11: the homepage says 'Baked by the Varga is taking a short pause from regular baking and orders' after winning GOLD (Pharaoh's Loaf) and BRONZE (Golden Loaf) at Br
   id 125 · Welch Bakes — no-pitch: OPENED welchbakes.co.uk 2026-10-11: the homepage IS a working Square online shop (Order now, cart, Apple/Google Pay, secure checkout by Square) plus a three-sentence Our Story. No email on t
   id 126 · Balé Artisano — DISPUTED: CHECKED 2026-10-11: the medal list gives no town and the name returns an unrelated Ba Le Bakery in Philadelphia (philly@balebakery.com). Blocked by the same guard that stopped the Sage Baker
   id 129 · Sea Wolf Bakers — no-pitch: NO PITCH. Verified their own pages: Squarespace + wholesale portal + portal guide + closure-dates page + gift cards + careers + donations. My first pass (from the magazine article alone) wro

7) الشي اللي ما صار بعد (حتى ما ينحسب تمام)
   أ. طابور التحقق (94 محلاً) لسا ما فتحنا موقعهن واحد واحد — هاي الشغلة الشغالة.
   ب. وعد «قائمة 100 محل جديدة» لسا ما انسلم: آخر دفعة زادت 3 محلات بس. المصادر الجاهزة: Food Republic أجزاء 2-5 و Britain's Best Loaf 2026 أجزاء 1-3.
   ج. محلات فرنسا واسبانيا بالقائمة ما بعتنالهن ولا صف — مستنين الإشارة منك لأنو فيهما TVA/autónomo (ورقة 06).
   د. أي محل يردّ علينا انسان: بنسأل عبد الرحمن قبل ما نبعتلو أي شي — القاعدة مكتوبة بـ 07.

8) خريطة الدرايف — نسخة حية وحدة لكل ملف (لا تكاوير)
   00 · ابدأ من هنا — هذا الملف نفسه، وأحدث نسخة إلو بمجلد Levain Kit (لا تبحث عن رابط قديم)
   01 · Register EN — سجل الإرسال
        https://drive.google.com/file/d/15HLKSl4-d6db9t64x2VPwLc_Hbo8gvBW/view
   02 · السجل بالعربي
        https://drive.google.com/file/d/17ox4Ib0UvIUnQ_7k-sV-noyvBi6rcEB0/view
   03 · Pitch Boards (141) · zip
        https://drive.google.com/file/d/1BxNVZJEWZ2UmjQR0cFAtkOjjzYWD8T6j/view
   04 · Clients & Pricing · جدول 141×26
        https://docs.google.com/spreadsheets/d/1rHlCeF-in6d_OmDziplUVm8O-K0hMj_dquUgRB5DQ9I/edit
   05 · Sales pack — التسعير والقوالب
        https://docs.google.com/document/d/1s5locBBaIyQmL-xylxESO_eTZ7bUva-14l8X3CY6txU/edit
   06 · Compliance — لماذا بلا ضريبة على الزبون
        https://docs.google.com/document/d/1-cHQByvBH2V2uAlamMXRVKG5ERbw1ajXM6pfLbOtSJ0/edit
   07 · TODO لكل رسالة
        https://docs.google.com/document/d/1goQ3qcHVfcrv9lrQlkngCaGMMNCHXJRZmFkYrexNlBM/edit
   08 · Shop dossiers — ملف لكل محل
        https://docs.google.com/document/d/14_65Xl2k7nfIHnRy5jPmUdLTjfgZovsVP2YtymI9OuA/edit
   المستودع: github.com/abdoo606/BLAblalba — الفرع arena/46df64dc-blablalba
   الملفات المصدّرة: sales/prospects-2026.csv (القائمة) · sales/OUTREACH-LOG.csv (الحالة، السلطة للأرقام) · sales/SENT-RECORD.csv (مين انبعثلو) · sales/SHOP-DOSSIERS.md (08) · sales/EVERY-MESSAGE-CHECKLIST.md (07)

9) باقي ورقة التسليم — القواعد والتفصيل

اقرأني أولاً — كيف يشتغل هالمجلد
(نسخة 2026-10-11 · عبد الرحمن ثليان · مطوّر ويب حر ·كرم الزيتون، حمص، سوريا)

هدفي من هالملفات: إني أعرف أكمّل الشغل من أي جلسة جديدة، وأنا أو غيري، بدون ما نعيد تحقيق شي.

1) المصدر الوحيد للحقيقة = المستودع، لا الدرايف
   GitHub: abdoo606/BLAblalba  ·  الفرع: arena/46df64dc-blablalba
   كل ملف بهالمجلد هو نسخة مولّدة. ما حدا يكتب بإيده على ملف بالدرايف — بيولّد من جديد.
   إذا صار فرق بين الدرايف والمستودع: المستودع هو الصح، والدرايف لازم يتحدّث.

2) ملف لملف
   00 · ابدأ من هنا — هذا الملف نفسه: وين وصلنا بالأرقام، أول 12 محلاً بالطابور، الأوامر بالحرف، جدول التسعير، الموقوفين والسبب، وروابط كل ملف. مولّد من الـCSV بـ `python3 tools/make-resume.py` فما بيقدر يضل قديم.
   01 · Register EN  — سجلّ تفصيلي بالإنجليزي: لكل محل: العنوان وين منشور، موضوع الإيميل، العرض، السعر بثلاث عملات، الحالة، والشو اللي لازم يوقعه عبد الرحمن.
   02 · السجل بالعربي — نفس المعلومات، مكتوبة بالعربي للقراءة البشرية.
   03 · Boards zip    — 141 بور: بور واحد لكل محل (شو ناقص موقعه، شو بنعمل، السعر). البورد هو الشي الوحيد اللي بنبعته لماحد يردّ علينا.
   04 · Clients & Pricing (Google Sheet) — الصف × السعر لكل محل. لا تعدّل الأسعار هنا.
   05 · Sales pack     — التسعير والقوالب وطريقة الكلام (EN/FR/ES/AR).
   06 · Compliance — ورقة الالتزام (فرنسي): لماذا ما في ضريبة على الزبون، وكيف بنبلّغ عن بلدنا بالفاتورة.
   07 · TODO لكل رسالة — الخطوات اللي بتنعمل مع كل برid منك، بينها قاعدة الدوسيهات وقائمة الأسعار (نفسها بالمستودع: sales/EVERY-MESSAGE-CHECKLIST.md).
   08 · Shop dossiers — ملف لكل محل تحركنا فيه: وين إحنا، شو لقينا بصفحته بالحرف، اتجاهنا، السعر، الخطوة الجاية، ومين بعتناله. ثم جدول باللي لسا ما فتحنا موقعهن. مولّد من الـCSV: python3 tools/make-dossiers.py

3) الأرقام اليوم (141 = العدد الكلي)
   شُفت مواقعهم بنفسي: 42  ·  بعتنالهم إيميل: 24 (23 حيّة + 1 مرتد)  ·  مجموع المعروض: 43,124 €
   لسه ما انفتح موقعه: 99 (كلهن من قوائم جوائز 2026، ما بنعتبرها صالحة للتواصل لحد ما نفتح الموقع)
   الردود البشرية: 0  ·  رد آلي: 2 (ARAN، Landrace)  ·  إيميلات مرتدة: 1 (I Loaf)
   لو وافقوا كلن (قياس فقط): 242,283 € = 264,088 $ لمرة وحدة، وبالدولار: مجموع المُرسَل 43,124 € = 47,005 $.

4) القواعد — لا تنازل عنها
   · ما بنبعت لإيميل ما قريناه على صفحة المحل نفسه. إيميل من دليل أو فيسبوك أو Yelp = ما كافٍ.
   · كل إيميل لازم يبدأ بشي شافه واحد منّا بالصفحة. ما بنحكّي من مقال مجلة (صار مرتين وغلطنا: Born & Bread و Sea Wolf).
   · المحل اللي عنده موقع/بوابة شغّالة وما ناقصه شي = ما بنبعتلن، وبنسجّل السبب.
   · الدفع USDT بس، وبموافقة الزبون المكتوبة، بالفاتورة — مستيح بهاردة باردة.
   · ما بنخبي إنو المقصي من سوريا، وما بندّعي وجود في بلد الزبون.
   · التوقيع، الفاتورة، استلام الفلوس، شراء الدومين باسم الزبون، والكلّام بالتلفون: لعبد الرحمن. كل شي تاني إلي.
   · «اقيلني» = حذف نهائي من كل القوائم.
   · كل محل فتحنا موقعه أو بعتناله: لازم بلوکو في 08 يکون محدّث بنفس الرسالة - والقائمة نفسها (07) کمان.
   · لو ردّ إنسان (مش ردّ آلي): اسأل عبد الرحمن قبل ما نبعتلن أي شي.

5) الحلقة اللي بتتكرر مع كل رسالة (مو كل دفعة بس)
   ملف كامل بالخطوات السبع: sales/EVERY-MESSAGE-CHECKLIST.md - وفيه أوامر التنفيذ بالحرف،
   وقالب «جدول الأسعار المتوقعة» اللي لازم ييجي آخر كل رسالة.

6) خطوات الدفعة الجوا القائمة:
   1. أفتح موقع المحل وأقرأ صفحة التواصل كاملة.
   2. ألصّق اللي بيقوله الصفحة بحرفه في audit_note، وأسجّل الإيميل المنشور بـ contact_verified، وأحط verification = VERIFIED + التاريخ.
   3. إذا الإيميل منشور عندهن: بنفس اليوم ببعث الإيميل من Gmail، وبعملّه Label_1.
   4. أعيد التوليد:
      python3 tools/make-sheet.py
      python3 tools/make-register.py
      python3 tools/make-register-ar.py
      node tools/make-pitches.mjs
      node src/build.mjs && node tools/validate.mjs
      python3 tools/make-dossiers.py
      python3 tools/make-resume.py   # الورقة اللي بتقول وين نحنا — بترفع على الدرايف 00
   5. أرفع النسخ الجديدة للدرايف وأسمّي القديمة «SUPERSEDÉ»، وبعدها commit + push.

7) معلّق — لا تنساه
   · ARAN: إذا ما ردّ، تذكير بنفس الخيط صباح الثلاثاء 13/10. وبعدها الثلاثاء 20/10، وبعدها بنتركهن.
   · The Snapery East (لندن): موقعهم مطفيّ اليوم — النطاق الأول بيقول WordPress «Active domain connection not found» والتاني «Website Expired». أهم حالة بالقائمة، وما في إيميل منشور نقدر نكتب عليه: لازم اتصال بشري (DM على إنستغرام أو تلفون) من عبد الرحمن.
   · مستودع عام نظيف (القوالب بس): التحضير جاهز بـ levain-kit-public — الرفع وجعل abdoo606/BLAblalba خاص إلك.
   · اسم المرسل بالإيميلات (Gmail display name) لازم تعيّته إنت من إعدادات Gmail؛ ما في أداة بتعمله.

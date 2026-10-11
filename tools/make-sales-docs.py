#!/usr/bin/env python3
"""Regenerate the sales policy documents from the smaller, location-free campaign policy."""
from pathlib import Path
from outreach_policy import ROOT, load_policy, money


def main():
    p = load_policy()
    packages = p['packages']
    table = '| Package | One-time EUR | Approx. USD | Scope |\n|---|---:|---:|---|\n' + '\n'.join(
        f"| {v['name']} | {v['price_eur']:,} | {money(v['price_eur'], p):,} | {v['scope']} |" for v in packages.values())
    exclusions = '\n'.join('- ' + item for item in p['excluded_by_default'])
    signature = p['sender']['display_name'] + '\n' + p['sender']['role'] + '\n' + p['sender']['reply_to']
    legal = '''# Compliance review — conditional, not a guarantee · 2026-10-11

**Status: sending paused.** This is a working review of official published guidance, not a legal opinion, approval of previous sends, or a promise that a message is lawful in every jurisdiction. Rules can depend on the actual sender, recipient, routing, entity, consent, data processing and transaction. No substitute nationality, city, company, phone or address is allowed.

## What changed

- Marketing signatures no longer contain provider locality. Real identity and a working reply/opt-out route remain. Where lawful disclosure is required in billing, contracts, tax, privacy or payment/KYC, provide truthful information or decline the transaction; do not conceal it.
- US recipients are permanently removed from this campaign by the user's instruction. Canada is permanently blocked from future imports. These are **user exclusions**, not invented recipient opt-outs.
- Remaining markets are research/draft-only until recipient entity/consent, contact purpose, privacy information and sender-side obligations are documented. A business-looking email address is not proof of corporate status.
- Old sent copies were moved to Gmail trash at the user's request. This does not edit, recall or erase recipients' copies, or establish retroactive compliance. New copy is draft-only and must not be replayed as a fresh first contact.

## Official rules relevant to the decisions

| Market | Published guidance | Campaign action |
|---|---|---|
| US | CAN-SPAM covers commercial messages including B2B, requires truthful headers/subjects, advertisement identification, a valid physical postal address and opt-out. The address rule is not a requirement to state nationality. [1](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) | Permanently excluded; do not remove a mandatory footer or invent a local mailbox. |
| Canada | CASL generally requires consent, identifying information and unsubscribe; its mailing-address guidance permits real alternatives such as a PO box. Public publication is not a broad licence to send, and requirements must be assessed case by case. [1](https://crtc.gc.ca/eng/com500/faq500.htm) | Permanently excluded from this no-address campaign, including future imports. |
| UK | Corporate-subscriber email differs from sole traders/ordinary partnerships. Unknown subscriber status should be treated as individual; public contact details alone do not supply the consent required for individuals. Identity and a valid opt-out contact remain required. Named contact data may engage UK GDPR. ICO also flags that guidance is under review after legislative changes. [2](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/) | Hold until corporate status or appropriate consent and privacy/source review are documented. No blanket UK/B2B exemption. |
| France | CNIL distinguishes professional relevance/information/objection from prior consent for consumer marketing; sender identity and a simple objection route remain necessary. [2](https://www.cnil.fr/en/node/14686) | Hold pending a documented lawful route, information, relevance and privacy review. Do not extrapolate to all Europe. |
| Spain | Article 21 generally prohibits unrequested/unauthorised electronic promotions, with a limited previous-contract/similar-product exception. [3](https://www.aepd.es/documento/2018-0173.pdf) | Hold without documented prior authorisation or an applicable reviewed exception. A public email is not enough. |

Excluding a recipient country **does not prove** that sender-side or other applicable laws disappear. The actual sender-side jurisdictions are not verified in this project. Do not use a phone, DM, intermediary or a second address to bypass a blocked marketing route.

## Billing, tax and payments are separate checks

- EU guidance lists supplier and customer full name/address on a full VAT invoice. The applicable invoice type and obligations require transaction-specific review. [1](https://taxation-customs.ec.europa.eu/taxation/vat/vat-businesses/invoicing_en)
- UK place-of-supply/reverse-charge rules depend on where the parties belong and what is supplied. They do not establish that everybody owes no tax. [1](https://www.gov.uk/guidance/vat-place-of-supply-of-services-notice-741a)
- OFAC's updated guidance reports changes to comprehensive country sanctions while preserving targeted restrictions. This is not an approval of a particular person, bank, transfer, payment provider or contract. [2](https://ofac.treasury.gov/faqs/topic/1571)
- No blanket “no VAT anywhere”, “legal for sure”, unsupported payment-availability assertion, or automatic tax-form selection remains authorised. Sender identity, applicable jurisdictions, tax treatment and a supported lawful payment route must be reviewed before sending a priced proposal or taking a deposit.

## Storage and public history

Repository visibility and Drive sharing must be reviewed before publishing new compiled contact data. A public repository can expose both present records and older Git revisions. Making it private reduces exposure but does not erase earlier public copies, recipients' messages, caches or trash. Technical visibility/ACL checks do not by themselves prove compliance with privacy law. No privacy-storage approval is recorded yet.

## Enforced workflow

`python3 tools/suppression.py` blocks opt-outs, user exclusions and excluded recipient countries. `python3 tools/outreach_policy.py check-send ID` fails closed if any required evidence or approval is missing. An earlier recipient needs separate follow-up approval. The gate is an operational safeguard, not a legal certificate.

If a prospective client makes provider-locality disclosure a condition and the user declines it: exclude that client with reason `user-exclusion`; do not invent an answer or work around the requirement. An opt-out is acted on immediately, without re-pitch or a second confirmation.
'''
    docs = {
        'sales/COMPLIANCE.md': legal,
        'sales/TAX-SCOPE.md': '''# Tax scope — unverified; no exemption claim authorised

The old location-dependent assumptions and universal tax-free statements are withdrawn from this working edition. Actual legal identity, tax residence, business establishment, registrations and payment route are not verified. Do not infer them from an old signature, an IP location, a nickname or the recipient's country.

Before a quote or invoice: identify the genuine contracting supplier, applicable jurisdictions, customer business status, relevant registrations, service classification, place of supply, invoice requirements and any reverse charge with a qualified adviser. No automatically selected W-8/W-9, fictitious entity, borrowed account or false tax address.

The published UK guidance makes place-of-supply/reverse-charge treatment conditional on the parties and supply. [1](https://www.gov.uk/guidance/vat-place-of-supply-of-services-notice-741a) EU guidance lists supplier/customer full name and address on a full VAT invoice. [1](https://taxation-customs.ec.europa.eu/taxation/vat/vat-businesses/invoicing_en)

Marketing omits optional provider locality; legally necessary disclosures are not optional. If required truthful information will not be provided, decline that transaction rather than hide it. Price drafts say tax is confirmed before agreement, not that it is zero. See COMPLIANCE.md and OUTREACH-POLICY.json; tax review remains pending.
''',
        'docs/PRICING.md': '# Smaller bakery projects — draft price catalogue · 2026-10-11\n\n' + table + '''

All fees are for the specified scope **once**, not per month and not the previous larger package at a discount. EUR is the planning currency; USD/GBP conversions are indicative only. No fee here is a sent quote, contract, revenue or verified customer budget. Tax and feasibility are confirmed before agreement.

Client supplies approved text, hours, prices, images and necessary access. Commissioned packages include one revision round and 14 days of fixes for defects in the agreed work, not new features. Time estimates run after scope, content and access are confirmed. Deposit: 40% after approval of a written scope; balance at delivery. Licence is self-installation, not a build service.

**No required subscription.** Care is optional at EUR 25/month (about USD 27), agreed separately for one small content update/month and agreed technical upkeep. Domains/hosting are in the client's own account and paid by the client. No hosting charge is automatically included in a project or first-year total.

## Not included in the lower fee
''' + exclusions + '''

The kit demos may demonstrate more technical capabilities than a purchased scope includes. They are concepts with sample content, not client work, real menus, or promises of an entire store for a one-page fee. Extra work requires a separately approved quote; no silent add-ons or misleading upsell.
''',
        'sales/PITCH-VOICE.md': '''# نبرة الإيميل — منفعة واضحة، نطاق صغير، وهوية حقيقية

## قاعدة 2026-10-11 الجديدة
لا مدينة ولا بلد ولا جنسية في التوقيع التسويقي. لا نستبدلها ببلد آخر، وكالة وهمية أو رقم محلي غير حقيقي. الاسم الحقيقي + الصفة + إيميل الرد فقط. بيانات مطلوبة قانونياً في فاتورة أو عقد أو تحقق مالي لا نخفيها؛ إن لم تُقدَّم نرفض المعاملة.

## البنية — تقريباً 100–170 كلمة
1. موضوع قصير يوضح المنفعة، بلا فضح عيوب ولا Re: مزيفة.
2. هدف عملي للزبون: اختيار المحل الصحيح، قراءة المنيو، الوصول لرابط الطلب الحالي.
3. تعريف مهني بجملة، ثم نطاق واحد صغير ومحدد. لا إعادة بناء كاملة افتراضياً.
4. سعر **مرة واحدة** مع زمن تقديري بعد اعتماد النطاق واستلام المحتوى، مراجعة واحدة و40% عربون.
5. لا إعفاء ضريبي مزعوم؛ أي ضريبة واجبة تتأكد قبل الاتفاق. لا رعاية شهرية تلقائية.
6. طلب واحد: Reply "outline". توقيع حقيقي وReply "remove me" للخروج الدائم.

## ممنوع
- سخرية، أخطاء إملائية منسوخة من موقعهم، أو افتتاح بتقرير عيوب.
- ادّعاء خسارة مبيعات، عوائد مضمونة، شراكة بجائزة، أعمال سابقة أو موعد محدود غير موثّق.
- الجزم بميزانية المحل أو غناه/فقره، أو تسعير العمل على راتب مفترض بأي بلد.
- ملاحق وروابط ديمو غير منشورة، بوابة دفع جديدة أو تصوير/ترجمة/SEO شامل ضمن سعر الصفحة.
- عنوان من دليل، أو صندوق توظيف/طلبات منتجات/ميرش يُستخدم لعرض مورد مواقع.
- إعادة الرسالة القديمة كأنها أول تواصل. النسخ الجديدة مسودات، لا تعديل للإيميلات المستلمة.

## التوقيع
''' + signature + '''

## قبل الإرسال — بدون استثناء
اقرأ COMPLIANCE.md وOUTREACH-POLICY.json. شغّل suppression.py ثم outreach_policy.py check-send ID. البيانات المنشورة لا تكفي وحدها لإذن التسويق. الوضع الآن: إرسال موقوف. الرد البشري يحتاج موافقة عبد الرحمن، والمراسَل سابقاً يحتاج موافقة منفصلة على متابعة. أي حذف/رفض واضح = إزالة ومنع دائم، بلا عرض آخر أو تأكيد ثانٍ.
''',
        'sales/EVERY-MESSAGE-CHECKLIST.md': '''# قائمة كل رسالة — النسخة الجديدة · 2026-10-11

## 1. السلامة قبل الحجم
- طلب تعديل/حذف/مراجعة قانونية لا يتضمن إرسالات جديدة تلقائياً. لا حد أدنى للإرسال يتجاوز المنع القانوني.
- لا ذكر اختياري لموقع المرسل بالتسويق؛ لا بلد بديل ولا هوية أو عنوان وهمي. البيانات اللازمة قانونياً لا نخفيها.
- أميركا وكندا مستبعدتان دائماً من هذه الحملة؛ لا إعادة إدخال أو التفاف بقناة أخرى.
- أي remove me أو رفض واضح: حذف الحالي ومنع ببصمات، بلا إعادة عرض. السبب user-exclusion منفصل عن opt-out الحقيقي.

## 2. شيّك الردود
- اقرأ الجديد من Gmail. الرد الآلي ليس اهتماماً، ولا هوية شركة، ولا موافقة تسويق.
- إنسان مهتم/سؤال: بلّغ عبد الرحمن؛ لا رد أو بور أو تفاوض قبل موافقته.
- إذا العميل يشترط معرفة موقع المزود والمستخدم يرفض الإفصاح: استبعده، ولا تكذب.
- حذف نسخة المرسل لا يسحب رسالة من المستلم. لا محو لتاريخ Git أو المهملات أو النسخ الخارجية.

## 3. البحث والتأهيل
- الميزانية غير معروفة حتى يصرّحوا فيها. جائزة أو موقع ضعيف لا يثبت القدرة على الدفع.
- افتح موقع المحل نفسه، وسجّل رابط صفحة النشر والغرض من صندوق البريد. لا عنوان من دليل ولا توظيف/ميرش/طلبات منتجات كصندوق عام.
- ثبّت نوع الكيان/الموافقة والأساس القانوني وبيانات الخصوصية. مجهول النوع يبقى موقوفاً، لا يُعامل كشركة تلقائياً.
- لا مشكلة مؤكدة أو حاجة مناسبة؟ no-pitch. لا نخترع حاجة لنبيع.

## 4. الرسائل
- اقرأ PITCH-VOICE.md. منفعة، نطاق صغير، سعر مرة واحدة، طلب outline، اسم حقيقي وإيميل رد، remove me.
- السعر والخدمات من OUTREACH-POLICY.json؛ لا تصوير/ترجمة/بوابة دفع/SEO واسع أو اشتراك ضمن السعر الصغير.
- قبل أي إرسال: `python3 tools/outreach_policy.py check-send ID` (للمتابعة: --follow-up وموافقة منفصلة).
- الوضع الحالي `send_paused=true`؛ لا إرسال ولا إعادة إرسال. مستندات المسودات ليست إيميلات مبعوثة.

## 5. التوليد والفحص
```
python3 tools/suppression.py
python3 tools/outreach_policy.py audit
python3 tools/make-sales-docs.py
python3 tools/make-emails.py
python3 tools/make-sheet.py
python3 tools/make-register.py
python3 tools/make-register-ar.py
python3 tools/make-dossiers.py
python3 tools/make-resume.py
node tools/make-pitches.mjs
node src/build.mjs
node tools/validate.mjs
node tools/progress.mjs
python3 -m unittest discover -s tests -p 'test_*.py'
```
- طابق CSV/JSON، الرسائل والباقة والسعر، ولا تكتب مجموع المسودات كإيراد أو عرض قائم.
- أعد ضغط release/levain-pitches.zip من الملفات الحالية فقط، وانسخ السجلين للعارض.
- ثم `git add -A && git commit && timeout 60 git push origin arena/46df64dc-blablalba`.

## 6. الدرايف
- اقرأ قائمة المجلد، وارفع النسخ النظيفة 00–09، ثم ارْمِ القديمة للمهملات بعد التحقق من الرفع. 09 هي إعادة صياغة الرسائل.
- 05 التسعير/القوالب و06 الالتزام يتحدثان أيضاً؛ لا تترك قواعد الهوية أو الإعفاء الضريبي القديمة.
- لا تلمس ملفات Nabd أو Formation Trading. نسخة واحدة نشطة لكل رقم.

## 7. آخر الرد
- عربي قصير: ما تغيّر، ما لم يحدث، وما يزال موقوفاً. أرفق هذه القائمة.
- سلّم جدول الأسعار الجديد في الآخر؛ USD تقريبي مع EUR الأساسي. التفاصيل في الملفات.

## بوابة الحذف
`python3 tools/suppression.py remove ID --date YYYY-MM-DD --reason opt-out`
أو `--reason user-exclusion` إذا قرار المستخدم/شرط إفصاح مرفوض، وليس طلب حذف من المستلم.
للحملة الحالية: `exclude-countries US CA --date YYYY-MM-DD` نفّذت بالفعل. لا تكرر حذفاً لتصنع أرقاماً.
البصمات مستعارة الهوية لا مجهولة الهوية. لا نحظر gmail.com أو مزود مشترك كله بسبب عنوان واحد.
''',
        'sales/RESUME-PREAMBLE.md': '''## أساس النسخة الجديدة
عبد الرحمن ثليان مطوّر ويب مستقل للمخابز. التوقيع التسويقي: الاسم والصفة وإيميل الرد؛ لا موقع جغرافي اختياري ولا بلد بديل. الهوية والبيانات اللازمة قانونياً للتعاقد/الفوترة/الدفع تبقى حقيقية، أو لا تتم المعاملة.

المصدر: OUTREACH-POLICY.json للنطاق والسعر والبوابة، prospects-2026.csv للبحث، OUTREACH-LOG.csv للحالة، SUPPRESSION-LIST.json للمنع، CAMPAIGN-ACTIVITY.json لأعداد الحذف السابقة وبصمات منع التكرار فقط.

كل الرسائل القديمة في الإصدار النشط أُزيلت، ولم تُعدَّل نسخة أي مستلم. توجد صياغة جديدة للمراجعة فقط؛ لا إرسال آلي أو ملاحقة بالمواعيد القديمة. الوضع إرسال موقوف إلى أن تتوثّق الوقائع القانونية والمصدر وغرض العنوان. الإيميل المنشور لا يثبت وحده إذن التسويق أو نوع الكيان.

دوري: البحث والكود والمسودات والسجل. لعبد الرحمن: الموافقات البشرية، توقيع العقد، استلام المال، شراء/ملكية النطاق، والمحاسب/المستشار. لا توقيع ولا بيانات مالية مختلقة بالنيابة عنه.
''',
        'sales/DRIVE-HANDOVER.txt': '''اقرأني أولاً — نسخة إعادة الصياغة 2026-10-11

المستودع هو مصدر البيانات، والدرايف نسخة مولّدة. كل الأرقام الحية في 00؛ لا نسخ ثابتة متعارضة.
00 حالة العمل والقواعد. 01 سجل EN. 02 سجل عربي. 03 البوردات النظيفة zip. 04 الأسعار والنطاق.
05 باقة التسويق الصغيرة. 06 مراجعة الالتزام المشروطة. 07 قائمة كل رسالة. 08 دوسيهات البحث. 09 الرسائل الجديدة للمراجعة.

لا منشأ اختياري في الرسائل ولا منشأ بديل. لا إرسال حتى تمر بوابة suppression وoutreach_policy، ولا يُعاد مراسلة عنوان سابق تلقائياً. لا blanket no VAT ولا 100% legal. الفواتير والعقود النهائية تحتاج بيانات حقيقية ومراجعة مستقلة.
توليد ثم فحص ثم commit/push ثم رفع واستبدال النسخ القديمة. لا نلمس Nabd وFormation Trading.
''',
        'sales/OUTREACH.md': '''# Outreach — replacement-copy edition

Campaign sending is paused. Read OUTREACH-POLICY.json, COMPLIANCE.md and PITCH-VOICE.md. US/CA markets are permanently excluded, not merely hidden from a view. Research the business's own page; document publication, contact purpose, entity/consent and privacy requirements. No directory address, purpose-restricted inbox or unsupported legal exemption.

New letters are in EMAIL-REWRITES.md and email-drafts/. They are review-only and must not be sent as a replay of an earlier email. A fresh own-page check and legal gate are necessary; a prior recipient also needs separate follow-up approval. There is no automatic day-9/day-21 chase queue.

Use the small fixed scope and one-time fee from the policy. Keep the real identity/reply address, but no optional city/country in marketing. Necessary legal disclosures are truthful or the transaction is declined. No substitute address/entity, fake portfolio, guaranteed ROI or hidden recurring fee.
''',
        'sales/PROGRESS-CHECKLIST.md': '''# Progress checklist — restart safely

- [x] Location omitted from marketing policy; no substitute location authorised.
- [x] Old sender copies moved to Gmail trash; no recipient recall claimed.
- [x] US leads permanently removed; Canada blocked for future imports.
- [x] Smaller prices replace bigger scopes, not the same work at an arbitrary discount.
- [ ] Verify the genuine contracting identity and applicable sender-side jurisdictions privately with a qualified adviser.
- [ ] Verify tax/invoice treatment and a lawful supported payment route; no borrowed account or automatic tax form.
- [ ] Document each recipient's entity/consent, own-page source, relevant contact purpose and privacy information.
- [ ] Recheck that a small proposed change is useful and feasible; budget stays unknown until supplied.
- [ ] Obtain approval for any human reply/follow-up and pass check-send. No new send occurred during this reset.

A published general email is not proof of corporate-subscriber status; a named/purpose-restricted inbox needs special care. Do not use a phone/DM or a different address to work around a block. See COMPLIANCE.md for official guidance and its limits.
''',
        'sales/REPLY-PLAYBOOK.md': '''# Reply playbook — real identity, smaller scope, no automatic reply

1. A new human response is read and reported to Abdulrhman. Prepare a draft only; approval precedes sending.
2. remove me / unsubscribe / clear refusal: remove current records and block permanently, no re-pitch or repeat confirmation.
3. A request for an outline is not unlimited marketing consent. Provide only the requested scope after approval and the relevant checks.
4. A price objection can lead to a **different, smaller** scope, not an invented discount on the same deliverables or a recurring fee hidden as one-time.
5. A question about provider locality is not answered with a fake country. If locality disclosure is a condition and the user declines, record user-exclusion and close the contact. Legally necessary invoice/KYC details cannot be hidden.
6. A commercial yes is not a signed contract or received money. Verify the contracting parties, law, tax and payment route before an agreement/deposit. A qualified professional must address legal certainty.
7. Silence does not trigger automatic follow-ups in this campaign. Previous recipients require separate approval and check-send --follow-up.
''',
        'sales/QUOTE-TEMPLATE.md': '''# Written scope / quote template — DO NOT ISSUE UNTIL REVIEWED

Draft only. A marketing sketch is not this quote. Do not substitute an old delivered fee with new text after the fact.

- Genuine supplier legal name/entity: [verified]
- Required real contact, billing address and registration details: [verified under applicable law]
- Customer legal name/entity, address and relevant tax ID: [verified]
- Approved scope/package and exact deliverables: [from policy plus agreed content limits]
- One-time project fee and invoice currency: [agreed amount]
- Tax treatment, invoice wording and total payable: [reviewed, not assumed zero]
- Access/content due before the estimate starts: [agreed]
- Estimated build window: [3 / 5 / 7 working days after content/access/scope are ready]
- Revisions: one agreed round; defects in agreed work fixed for 14 days after delivery.
- Deposit: 40% after a valid signed scope; remaining balance at delivery.
- Hosting/domain: client account, paid by client. No mandatory subscription or recurring care.
- Optional separate care: EUR 25/month if actually chosen, described and agreed.
- Exclusions: payments/checkout, inventory, custom CMS, translation, photography, marketing/SEO campaign, ongoing hosting/care, unlimited revisions unless separately quoted.
- Ownership/licence/handover and dispute terms: [reviewed and accepted]
- Quote expiry: [agreed date], not a fake marketing urgency device.
- Signatures: only the actual parties; the agent does not sign.

If required supplier details will not be disclosed, decline the transaction. No fake local entity, address, tax ID or payment recipient. See COMPLIANCE.md/TAX-SCOPE.md.
''',
        'sales/INVOICE-TEMPLATE.md': '''# Invoice template — BLOCKED UNTIL IDENTITY AND TAX REVIEW

Not an issued invoice. No assumed country, tax residence, exemption, reverse charge or financial route.

Invoice number: [unique actual number] · Issue date: [actual date] · Currency: [agreed]
Supplier: [verified legal name/entity]
Supplier contact / full real address / applicable registration and tax details: [as legally required]
Customer: [verified legal name/entity, real address, applicable tax ID]
Supply: [actual agreed small scope, date and description]
Subtotal: [one-time agreed fee]
Tax treatment/rate/amount/required wording: [reviewed for actual transaction]
Total payable: [unambiguous amount]
Deposit/balance and due date: [agreed]
Payment recipient and supported payment route: [verified actual supplier]

No automatic tax-law citation, tax-free line, borrowed bank account, false address, backdating or anonymous crypto substitution. Keep mandatory truthful data or do not issue. EU guidance lists full supplier/customer names and addresses on a full VAT invoice. [1](https://taxation-customs.ec.europa.eu/taxation/vat/vat-businesses/invoicing_en) Applicability and other jurisdictions need review, not a universal rule invented by this template.
''',
        'sales/TERMS.md': '''# Service terms skeleton — not an executable legal contract

Pending legal identity, jurisdiction, tax and payment review. No automatically chosen governing law or invented contracting entity. Only the parties can approve/sign final terms.

Specify the actual supplier/customer, required contact/billing details, the small scope and client-supplied content/access. Specify one revision round, the estimated window after readiness, 40% deposit and balance at delivery, ownership/licence, handover, cancellation/refunds, defect handling, liability and dispute resolution appropriate to the actual law.

The project fee is one-time. Care is separate and optional; no hosting or subscription bundled by default. Additional work is separately scoped/approved. The client owns its domain/hosting account. An enquiry form is not an inventory or confirmed-order/payment system.

Do not reuse press photos, invented customer quotes or fabricated portfolio claims. Customer-data handling, processing roles, security and privacy must be reviewed before collecting live data; a no-backend form is not automatically exempt from privacy obligations.

Marketing does not force provider locality in its signature. Legally necessary identity/address/tax/KYC data stays truthful; if it cannot be supplied, decline the transaction. Final legal terms require qualified advice.
''',
        'sales/PRIVACY-NOTICE.md': '''# Privacy notice working template — review before live use

Controller: Abdulrhman Thali · Contact: abdulrhmant948@gmail.com. Legal identity, applicable jurisdictions, any required representative/contact disclosures and a publication route still need review. This is not a completed compliance notice or permission to send marketing.

Proposed processing: limited public professional contact data and objective website research to assess a relevant small website service. Source must be the business's own page, and channel purpose/entity/consent and the applicable lawful basis must be recorded. Public publication alone does not establish permission. Do not buy lists or treat a purpose-limited address as a general vendor inbox.

No sales/wealth profiling, resale, hidden tracking pixel or address transfer. Give recipients an accessible objection/rights route, identify the actual controller, and review required information, lawful basis, retention, security, processors/transfers and complaint authority for the actual jurisdiction. Do not promise a universal three-year rule or that every generic address is outside privacy law.

A refusal removes current marketing records and leaves only minimal pseudonymous prevention fingerprints. Hashes are not guaranteed anonymity. User-directed market exclusions are separate from recipient opt-outs. Old sender copies and superseded Drive files were trashed, not recalled from recipients or erased from Git history. Minimum aggregate history/duplicate-prevention hashes remain, with no old email body or historical fee in the reset activity file.

For commissioned live forms, clarify who controls/processes submissions and where the real recipient stores them before deployment. Do not quietly move customers' data to the developer.
''',
        'sales/PAYMENTS-USDT.md': '''# Payments — no route chosen; old crypto-only assumption retired

The filename is retained for compatibility, not a recommendation to use USDT. No payment route is verified and no deposit is requested during this reset.

Before payment, verify the actual contracting identity, relevant jurisdictions, sanctions/other restrictions on parties/banks, provider country and service eligibility, fees, refund handling and tax records. A supported lawful bank/payment route in the supplier's own name is preferred if available. A crypto route needs its own lawful/operational review and client agreement; it is not a workaround for legal or KYC restrictions.

No fake residence, borrowed IBAN/account, false local entity, concealment from a bank/payment provider, or third party presented as the real contractor. Never promise a payment provider serves or bans a person based on an old blanket country statement.

Current OFAC guidance reports changes to comprehensive country sanctions while preserving targeted restrictions; a change is not approval of a specific transfer, person, bank or provider. [2](https://ofac.treasury.gov/faqs/topic/1571) Other applicable regimes and current provider terms remain separate checks. Final decisions/receiving money belong to Abdulrhman, not the agent.
''',
        'sales/DATA-QUALITY-NOTES.md': '''# Reset / data-quality notes · 2026-10-11

The user requested location-free professional copy, removal of incompatible markets, smaller prices/scopes and clearing old sent-copy material. The 55 freshly listed campaign-only sender message IDs were checked against the recorded sends before Gmail trashing. No unrelated email or draft was deleted. No recipient copy was changed or recalled, and no new email was sent.

Seventy US prospect records were permanently removed from CSV/JSON/log/boards; Canada had no current rows but is blocked for future imports. These are user exclusions, not recipient opt-outs. The earlier true opt-out remains protected. Hashes never apply to all of a shared mail provider; business-domain prevention excludes shared roots such as Gmail.

Old active SENT-RECORD entries, subject/body narratives, historical fee totals and automatic chase dates were cleared. Minimal aggregate history and message/prevention fingerprints remain in CAMPAIGN-ACTIVITY.json/SUPPRESSION-LIST.json, not old contact dossiers. Previous contact dates remain on retained leads to stop accidental first-touch replay. Git/Drive/Gmail trash and external copies are not erased.

A shared-mailbox index previously mis-matched a contacted discovery row to a different placeholder. That resolver's regressions remain. No old financial figure is carried forward as a new quote, contract or revenue.

ARAN's research row was cross-contaminated with an unrelated business. Its wrong audit was discarded and its own homepage re-read; only displayed opening times/cart summary are recorded. Address publication and entity still need review. Hiring/merchandise/order-specific inboxes in other retained rows remain blocked for vendor proposals.

New fees represent new smaller scopes, not retroactive edits to delivered offers. All recipient entity/consent/source/privacy fields are pending review, and the sender-side/tax/payment reviews are also pending. There are zero send-ready leads. No certainty about past legality, future legality, customer budget or sales outcome is claimed.
''',
    }
    docs['sales/DRIVE-SALES-PACK.md'] = '# Smaller-scope sales pack · 2026-10-11\n\n**Review-only; campaign sending paused.**\n\n' + table + '''

Professional signature:

''' + signature + '''

One outcome, one small scope, one-time fee, one revision, no obligatory subscription, one reply CTA. Client supplies text/images; timeframe starts after readiness. No optional provider locality, no substitute country, no false identity, tax exemption or guaranteed sales. Applicable taxes and contract feasibility are confirmed before agreement. Required legal disclosures are truthful or the transaction is declined.

Optional care EUR 25/month (about USD 27); hosting/domain are client-owned and paid directly. See docs/PRICING.md for exclusions and COMPLIANCE.md for limits. The replacement letters are in 09 / EMAIL-REWRITES.md, not a new send log.
'''
    storage_note = '''\n\n## تخزين بيانات العملاء\nالمستودع يبقى عاماً، لكن القوائم والمسودات والبوردات والسجلات الحالية مستبعدة من Git. تبقى بمساحة العمل ونسخة 10 الخاصة بالدرايف. لا رفع لبيانات عملاء جديدة على Git؛ تاريخ البيانات العامة القديم لم يُمحَ. قبل تشغيل الأدوات من clone جديد: استرجع النسخة الخاصة، ولا تنشئ سجل منع فارغاً. راجع docs/OUTREACH-STORAGE.md. فحص صلاحيات المجلد (مالك فقط) لا يساوي ضماناً قانونياً.\n'''
    for key in ('sales/EVERY-MESSAGE-CHECKLIST.md', 'sales/DRIVE-HANDOVER.txt', 'sales/RESUME-PREAMBLE.md'):
        docs[key] += storage_note
    for name, text in docs.items():
        path = ROOT / name
        path.write_text(text.rstrip() + '\n', encoding='utf-8')
    print(f"wrote {len(docs)} policy/pricing/templates; no forced-location signature or blanket tax assurance")


if __name__ == '__main__':
    main()

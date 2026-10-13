#!/usr/bin/env python3
"""Shared, current-edition outreach reporting. Past deliveries are not rewritten as new sends."""
import argparse
import csv
import datetime
import json
import subprocess
from collections import Counter
from pathlib import Path
from outreach_policy import ROOT, load_policy, package_for, money, send_blocks
from suppression import check_sources, load_registry


def read_csv(name):
    with (ROOT / 'sales' / name).open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def state():
    check_sources()
    policy, registry = load_policy(), load_registry()
    rows, logs = read_csv('prospects-2026.csv'), read_csv('OUTREACH-LOG.csv')
    log = {r['id']: r for r in logs}
    if {r['id'] for r in rows} != set(log):
        raise ValueError('Prospect/log ID sets differ.')
    for row in rows:
        if row['package'] not in policy['packages']:
            raise ValueError('Unknown package in current data.')
        expected = 0 if row['offer_state'] == 'no-offer' else package_for(row, policy)['price_eur']
        if int(row['quote_eur']) != expected or int(row['care_eur_per_month']) != 0:
            raise ValueError('Stale fee or hidden recurring care in source data.')
    activity = json.loads((ROOT / 'sales/CAMPAIGN-ACTIVITY.json').read_text(encoding='utf-8'))
    letters_path = ROOT / 'sales/EMAIL-REWRITES.json'
    letters = json.loads(letters_path.read_text(encoding='utf-8'))['messages'] if letters_path.exists() else []
    new_sends = [r for r in read_csv('SENT-RECORD.csv') if r['kind'] == 'cold pitch']
    stats = {
        'active': len(rows), 'countries': Counter(r['country'] for r in rows),
        'statuses': Counter(r['status'].strip() for r in logs),
        'previously_contacted': sum(bool(r['already_contacted_at']) for r in rows),
        'rewrites': len(letters), 'new_sent': len(new_sends),
        'send_ready': sum(not send_blocks(r, policy, registry) for r in rows),
        'opt_outs': sum(e['reason'] == 'opt-out' for e in registry['entries']),
        'user_exclusions': sum(e['reason'] == 'user-exclusion' for e in registry['entries']),
        'standing_eur': sum(int(r['quoted_eur'] or 0) for r in logs if r['status'].strip().startswith('sent')),
        'draft_total_eur': sum(int(r['quote_eur']) for r in rows),
    }
    return rows, log, policy, registry, activity, letters, stats


def sheet():
    rows, log, policy, _, _, _, stats = state()
    fields = ['ID', 'Client / العميل', 'Client city', 'Recipient country', 'Research status',
              'Legal status / NOT approval', 'Offer state', 'Contact purpose', 'Unapproved contact record',
              'Draft package', 'Draft fee EUR / not a sent quote', 'Approx USD', 'Scope', 'Included languages',
              'Default monthly care', 'Tax status', 'Previous contact / no replay', 'Next action']
    with (ROOT / 'sales/drive-clients-pricing.csv').open('w', newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh, lineterminator='\n')
        writer.writerow(fields)
        for row in sorted(rows, key=lambda r: (r['country'], int(r['id']))):
            pack = package_for(row, policy)
            writer.writerow([row['id'], row['business'], row['city'], row['country'], row['verification'],
                row['legal_status'], row['offer_state'], row['contact_purpose'], row['contact_verified'],
                pack['name'] if row['offer_state'] != 'no-offer' else 'NO OFFER', row['quote_eur'],
                money(int(row['quote_eur']), policy), row['planned_scope'], row['languages'], 0,
                'Pending transaction-specific review', row['already_contacted_at'], log[row['id']]['next_action']])
        writer.writerow(['SUMMARY', f"{stats['active']} active research rows; {stats['send_ready']} send-ready; {stats['new_sent']} new sends",
                         '', '', '', '', 'DRAFTS ONLY', '', '', '', '', '', '', '', '', '', '', 'No revenue or signed contracts inferred'])
    (ROOT / 'sales/prospects-2026.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"sheet: {stats['active']} active rows · {stats['send_ready']} ready · {stats['new_sent']} new sends · default recurring=0")


def dossiers():
    rows, log, policy, _, _, _, stats = state()
    lines = ['# ملف لكل محل — الإصدار الصغير الموقوف · 2026-10-11', '',
        f"{stats['active']} محلاً للبحث والمراجعة، {stats['previously_contacted']} منها تواصلنا معها سابقاً. "
        'إعادة الصياغة ليست إرسالاً جديداً ولا محواً لنسخة المستلم. كل السعر أدناه خطة لنطاق جديد صغير، لا عرضاً قائماً أو دخلاً.', '',
        '**مهم:** الأسماء والمدن هنا للمحلات. توقيع المرسل لا يحمل موقعاً جغرافياً اختيارياً. الإرسال موقوف، والأسواق المستبعدة غير موجودة هنا.', '']
    for row in sorted(rows, key=lambda r: (r['country'], int(r['id']))):
        lg, fee = log[row['id']], int(row['quote_eur'])
        lines.extend([f"## {row['business']} · id {row['id']} · {row['city']}, {row['country']}", '',
            f"**الحالة:** {lg['status']} · **المراجعة القانونية:** {row['legal_status']} · **الميزانية:** غير معروفة",
            f"**البحث:** {row['verification'].strip()}", f"**الموقع المسجّل:** {row['site_found'] or 'غير موثّق بعد'}",
            f"**تواصل للبحث لا إذن إرسال:** {row['contact_verified'] or 'لا عنوان موثّق'}",
            f"**غرض العنوان:** {row['contact_purpose']} · توثيق صفحة النشر: {row['contact_source_verified']}"])
        if row['already_contacted_at']:
            lines.append('**مراسَل سابقاً:** ممنوع اعتباره أول تواصل أو إعادة رسالة تلقائياً.')
        lines.extend([f"**النطاق الجديد:** {row['planned_scope'] or 'لا عرض — نحتفظ بقرار no-pitch'}",
            f"**رسم المسودة:** {fee:,} € ≈ {money(fee, policy):,} $ · مرة واحدة · رعاية تلقائية 0",
            '**موانع الإرسال:** ' + '; '.join(send_blocks(row, policy, load_registry())),
            f"**الخطوة التالية:** {lg['next_action']}",
            f"**نتائج البحث الداخلية (ليست نص الرسالة):** {row['audit_note'] or 'لم تُسجّل قراءة موثقة بعد'}",
            f"**مصدر الاسم فقط:** {row['source']}", ''])
    (ROOT / 'sales/SHOP-DOSSIERS.md').write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
    print(f"dossiers: {len(rows)} current research records; removed markets absent")


def resume():
    rows, log, policy, registry, activity, _, stats = state()
    head = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    lines = ['# ابدأ من هنا — نسخة إعادة الصياغة · 2026-10-11', '',
        f"نسخة الكود قبل حفظ هذا التوليد: {head} · الفرع arena/46df64dc-blablalba", '',
        (ROOT / 'sales/RESUME-PREAMBLE.md').read_text(encoding='utf-8').strip(), '',
        '## 1. الحالة الحقيقية',
        f"- {stats['active']} محلاً بالقائمة الحالية: " + ' · '.join(f'{country} {count}' for country, count in sorted(stats['countries'].items())),
        f"- {activity['gmail_sender_copies_moved_to_trash']} نسخة إرسال قديمة إلى مهملات Gmail؛ ليست سحباً من المستلمين."
        f" السجل السابق كان {activity['pre_reset_tracked_pitch_messages']} رسالة عرض + {activity['pre_reset_tracked_corrections']} تصحيحاً.",
        f"- {stats['previously_contacted']} مراسَلاً سابقاً باقياً بالقائمة، و{stats['rewrites']} مسودة جديدة؛ لم تُرسل.",
        f"- إرسالات الحملة الجديدة {stats['new_sent']} · جاهزون قانونياً وفق البوابة {stats['send_ready']} · الإرسال موقوف={policy['send_paused']}.",
        f"- عروض جديدة قائمة حسب السجل: {stats['standing_eur']:,} € ≈ {money(stats['standing_eur'], policy):,} $؛ لا مسودات تُحسب كدخل أو عقود.",
        f"- {stats['user_exclusions']} استبعاداً بقرار المستخدم + {stats['opt_outs']} طلب حذف حقيقياً. "
        + 'أسواق ممنوعة دائماً: ' + ', '.join(sorted(registry.get('blocked_countries', {}))) + '.',
        '- لا مصدر قانوني/كيان/موافقة/غرض بريد/خصوصية/هوية ضريبية موثّق بعد يسمح بالإرسال. لا ادعاء بأن القديم كان قانونياً أو أن المستقبل مضمون قانونياً.', '',
        '## 2. الخطوة التالية — بحث ومراجعة فقط',
        '- افتح 09 للرسائل الجديدة، ثم 08 لنتائج البحث. لا تستخدمها كأول تواصل لمن سبق مراسلته.',
        '- ثبّت نوع الكيان أو الموافقة والأساس المحلي، صفحة نشر العنوان والغرض، بيانات الخصوصية والهوية/الضريبة/الدفع. التفاصيل والمصادر في 06.',
        '- صندوق توظيف/ميرش/طلبات منتجات ليس صندوق عروض موردين؛ لا التفاف بفورم أو DM أو عنوان من دليل.',
        '- إذا العميل يشترط معرفة موقع المزود والمستخدم يرفض: استبعاد user-exclusion، لا جواب مختلق.', '',
        '## 3. الأسعار الجديدة — مرة واحدة ونطاق أصغر']
    for pack in policy['packages'].values():
        lines.append(f"- {pack['name']}: {pack['price_eur']:,} € ≈ {money(pack['price_eur'], policy):,} $ · {pack['scope']}")
    lines.extend(['- لغة واحدة ومراجعة واحدة للمشاريع المنفّذة. لا تصوير/ترجمة/SEO حملة/دفع/مخزون/CMS أو استضافة افتراضية.',
        f"- العناية اختيارية {policy['optional_care_eur_per_month']} €/شهر ≈ {money(policy['optional_care_eur_per_month'], policy)} $؛ الافتراضي 0. النطاق/الاستضافة بحساب العميل.",
        '- الضريبة والمبلغ النهائي والإمكانية تتأكد قبل الاتفاق. العربون 40% بعد اعتماد نطاق صالح، لا قبله.', '',
        '## 4. الحلقة', '```', 'python3 tools/suppression.py', 'python3 tools/outreach_policy.py audit',
        'python3 tools/make-sales-docs.py', 'python3 tools/make-emails.py', 'python3 tools/make-sheet.py',
        'python3 tools/make-register.py', 'python3 tools/make-register-ar.py', 'python3 tools/make-dossiers.py',
        'python3 tools/make-resume.py', 'node tools/make-pitches.mjs', 'node src/build.mjs',
        'node tools/validate.mjs && node tools/progress.mjs', "python3 -m unittest discover -s tests -p 'test_*.py'", '```',
        '- أعد zip من الحالي، انسخ PDF، commit/push، ارفع 00–09 وتحقق ثم ارمِ القديم. لا تمس Nabd/Formation Trading.', '',
        '## 5. طابور لم يُفتح — لا رسائل له'])
    queue = [row for row in rows if log[row['id']]['status'] == 'to-verify']
    for row in queue[:12]:
        lines.append(f"- id {row['id']} · {row['business']} · {row['country']} · بحث فقط، لا موافقة تسويق")
    lines.extend(['', '## 6. ملفات الدرايف',
        '00 الحالة · 01 EN · 02 العربي · 03 zip · 04 جدول النطاق والسعر · 05 التسويق · 06 الالتزام المشروط · 07 TODO · 08 دوسيهات · 09 رسائل المراجعة · 10 نسخة مصادر خاصة لاستعادة القوائم.',
        'المجلد: https://drive.google.com/drive/folders/0ACdYKa5qpuxEUk9PVA',
        'الأرقام والأسماء ثابتة؛ اقرأ القائمة قبل الاستبدال. لا ids قديمة في الروابط الداخلية.', '',
        '## 7. حدود الحذف',
        'الملفات الحالية نظيفة من النسخ القديمة والأسواق المستبعدة؛ بقيت بصمات وأعداد منع فقط. تاريخ Git ومهملات Gmail/Drive ونسخ المستلمين لم تُمحَ.', '',
        (ROOT / 'sales/DRIVE-HANDOVER.txt').read_text(encoding='utf-8').strip()])
    check = activity.get('latest_mail_check')
    if check:
        lines.extend(['', '## 8. آخر فحص للإيميلات',
            f"- وقت الفحص: {check['checked_at']} · بحث كامل مع المهملات/السبام؛ لا رد قديم يُحسب كجديد.",
            f"- ردود بشرية جديدة: {check['new_human_campaign_replies']} · اهتمام مؤكد: {check['confirmed_positive_campaign_replies']}.",
            f"- ردود استلام آلية قديمة: {len(check['known_automatic_acknowledgements'])} · ارتداد قديم: {check['known_old_delivery_failures']}؛ لا إعادة إرسال.",
            f"- رسائل إرسال جديدة خارج المهملات: {check['active_gmail_sent_since_reset']} · مسودات Gmail: {check['gmail_drafts']}. الـ25 صياغة الخاصة ليست مسودات Gmail ولا رسائل مبعوثة.",
            '- لا بيانات تتبع فتح/قراءة للمستلمين. الفحص لم يرسل أو يحذف أو يغيّر UNREAD.',
            '- تنبيه أمان مستقل من LinkedIn بتاريخ 11/10 يبلغ عن محاولات دخول مريبة؛ راجع التطبيق/الموقع الرسمي مباشرة وكلمة مرور فريدة والتحقق بخطوتين. لم تُعدَّل إعدادات الحساب.',
            '- التقرير الخاص: sales/MAIL-CHECK.md · النسخة 11 بالدرايف. أعداد وبصمات فقط، بلا روابط استعادة أو رموز حسابات.'])
    (ROOT / 'sales/DRIVE-RESUME.md').write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')
    print(f"resume: {stats['active']} active · {stats['rewrites']} rewrites · {stats['new_sent']} new sends · {stats['send_ready']} ready")


def register(arabic=False):
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
    if arabic:
        import arabic_reshaper
        from bidi.algorithm import get_display
        visual = lambda text: get_display(arabic_reshaper.reshape(str(text)))
    else:
        visual = str
    rows, log, policy, _, activity, _, stats = state()
    pdf = FPDF()
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(True, margin=14)
    fonts = Path('/usr/share/fonts/truetype/dejavu')
    pdf.add_font('D', '', str(fonts / 'DejaVuSans.ttf'))
    pdf.add_font('D', 'B', str(fonts / 'DejaVuSans-Bold.ttf'))
    pdf.add_page()
    width = pdf.w - pdf.l_margin - pdf.r_margin

    def para(text, size=9, bold=False, color=(40, 44, 50), gap=1):
        pdf.set_font('D', 'B' if bold else '', size)
        pdf.set_text_color(*color)
        # Wrap in logical order first, then shape each Arabic visual line.
        for paragraph in str(text).split('\n'):
            lines, current = [], ''
            for word in paragraph.split():
                trial = (current + ' ' + word).strip()
                if current and pdf.get_string_width(visual(trial)) > width - 1:
                    lines.append(current)
                    current = word
                else:
                    current = trial
            lines.append(current)
            for line in lines:
                pdf.multi_cell(0, size * 0.48 + 1, visual(line), align='R' if arabic else 'L',
                               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(gap)

    title = 'السجل الجديد — مسودات أصغر، إرسال موقوف' if arabic else 'Outreach restart — smaller scopes, paused sending'
    para(title, 16, True, (100, 61, 32), 3)
    para('Abdulrhman Thali · Independent web developer for bakeries · abdulrhmant948@gmail.com', 9)
    if arabic:
        facts = [f"القائمة الحالية {stats['active']} · سابقاً تواصلنا مع {stats['previously_contacted']} منهم.",
                 f"مسودات جديدة {stats['rewrites']} · إرسالات جديدة {stats['new_sent']} · جاهزون عبر البوابة {stats['send_ready']}.",
                 f"نسخ إرسال قديمة بالمُهملات {activity['gmail_sender_copies_moved_to_trash']}؛ لم تُسحب من المستلمين.",
                 f"استبعاد مستخدم {stats['user_exclusions']} · حذف حقيقي {stats['opt_outs']} · أسواق US/CA ممنوعة.",
                 'كل الرسوم خطط لنطاق أصغر، لا تعديلات بأثر رجعي ولا عقود أو إيرادات. لا ضمان قانوني؛ الهوية والكيان/الموافقة والمصدر والخصوصية والضريبة والدفع تحتاج مراجعة.']
    else:
        facts = [f"{stats['active']} active research leads; {stats['previously_contacted']} were contacted before this reset.",
                 f"{stats['rewrites']} new review-only letters; {stats['new_sent']} new sends; {stats['send_ready']} send-ready.",
                 f"{activity['gmail_sender_copies_moved_to_trash']} old sender copies moved to recoverable trash, not recalled from recipients.",
                 f"{stats['user_exclusions']} user exclusions and {stats['opt_outs']} real opt-out; US/CA markets permanently blocked.",
                 'Fees below are smaller-scope plans, not retroactive edits, delivered quotations, contracts or revenue. No legal guarantee; sender-side, entity/consent, source, privacy, tax and payment reviews are pending.']
    for text in facts:
        para(text, 10, gap=2)
    para('الأسعار — مرة واحدة' if arabic else 'Catalogue — one-time fees', 12, True, gap=3)
    for pack in policy['packages'].values():
        para(f"{pack['name']}: {pack['price_eur']} EUR ≈ {money(pack['price_eur'], policy)} USD", 10, True)
        para(pack['scope'], 8.5)
    para('لا اشتراك افتراضي. العناية 25 EUR/شهر اختيارية، والاستضافة بحساب العميل. انظر 06 للالتزام و09 للرسائل.' if arabic else
         'No default subscription. Care EUR 25/month is optional; hosting/domain belong to the client. See 06 for conditional compliance and 09 for replacement letters.', 9)
    pdf.add_page()
    for row in sorted(rows, key=lambda r: (not bool(r['already_contacted_at']), r['country'], int(r['id']))):
        if pdf.get_y() > pdf.h - 75:
            pdf.add_page()
        fee, pack = int(row['quote_eur']), package_for(row, policy)
        para(f"{row['id']} · {row['business']} — {row['city']}, {row['country']}", 10.5, True, (100, 61, 32))
        para(('رسم مسودة' if arabic else 'Draft fee') + f": {fee} EUR ≈ {money(fee, policy)} USD · "
             + ('مرة واحدة، لم يُرسل' if arabic else 'one-time, not sent'), 9, True)
        para(row['planned_scope'] or ('لا عرض، نحتفظ بقرار no-pitch.' if arabic else 'No offer; preserve no-pitch decision.'), 8.3)
        para(('الحالة' if arabic else 'State') + ': ' + log[row['id']]['status'] + ' · ' + row['legal_status'], 8)
        para(('غرض العنوان' if arabic else 'Contact purpose') + ': ' + row['contact_purpose'] + ' · '
             + ('ميزانية غير معروفة. لا موافقة إرسال.' if arabic else 'Budget unknown. No permission to send.'), 8)
        if row['already_contacted_at']:
            para('مراسَل سابقاً؛ ممنوع إعادة أول تواصل تلقائياً.' if arabic else 'Previously contacted; no automatic first-touch replay.', 8)
        para(('البحث' if arabic else 'Research') + ': ' + row['verification'], 8, gap=3)
    out = ROOT / 'sales' / ('OUTREACH-REGISTER-AR.pdf' if arabic else 'OUTREACH-REGISTER.pdf')
    pdf.output(str(out))
    print(f"wrote {out.name}: {pdf.page_no()} pages · {out.stat().st_size:,} bytes")


def progress():
    _, _, policy, registry, activity, _, stats = state()
    print(f"\nLevain restart — {stats['active']} active research leads")
    for status, count in sorted(stats['statuses'].items()):
        print(f"{status:56} {count:3}")
    print(f"previous recipients : {stats['previously_contacted']} (no replay)")
    print(f"rewritten drafts    : {stats['rewrites']} (not sent)")
    print(f"new sends           : {stats['new_sent']}")
    print(f"send ready          : {stats['send_ready']}; paused={policy['send_paused']}")
    print(f"standing offers     : {stats['standing_eur']} EUR = {money(stats['standing_eur'], policy)} USD; not draft valuations")
    print(f"old sender copies   : {activity['gmail_sender_copies_moved_to_trash']} trashed; recipients unchanged")
    print(f"permanent prevention: {stats['user_exclusions']} user exclusions + {stats['opt_outs']} opt-out")
    print('excluded markets    : ' + ', '.join(sorted(registry.get('blocked_countries', {}))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=['sheet', 'dossiers', 'resume', 'register', 'register-ar', 'progress'])
    kind = parser.parse_args().kind
    if kind == 'register-ar':
        register(True)
    else:
        globals()[kind]()

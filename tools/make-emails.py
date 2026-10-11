#!/usr/bin/env python3
"""Write new professional review-only letters; never edit/re-send a delivered email."""
import csv
import json
import re
import unicodedata
from pathlib import Path
from outreach_policy import ROOT, load_policy, package_for, money, send_blocks, validate_email
from suppression import EMAIL, check_sources, load_registry


def slug(value):
    value = unicodedata.normalize('NFD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', value).strip('-')


def body_for(row, brief, policy):
    pack = package_for(row, policy)
    eur, gbp = pack['price_eur'], money(pack['price_eur'], policy, 'GBP')
    return (f"Hello {row['business']} team,\n\n"
            f"{brief['benefit']}\n\n"
            "I'm Abdulrhman Thali, an independent web developer for bakeries. "
            f"As a small starting point, I can build {brief['focus']} using the text, prices and images you approve. "
            "You receive the editable files and a short handover guide; no checkout replacement or compulsory monthly plan.\n\n"
            f"The one-time project fee is EUR {eur:,} (about GBP {gbp:,}). "
            f"Estimated build: {pack['days']} working days after scope, content and access are confirmed, "
            "with one revision round and a 40% deposit. Any applicable tax is confirmed before agreement.\n\n"
            "Reply \"outline\" if you'd like a one-page plan before deciding.\n\n"
            f"{policy['sender']['display_name']}\n{policy['sender']['role']}\n{policy['sender']['reply_to']}\n\n"
            "This is a business proposal. Reply \"remove me\" and I will not contact you again.")


def main():
    check_sources()
    policy, registry = load_policy(), load_registry()
    with (ROOT / 'sales/prospects-2026.csv').open(newline='', encoding='utf-8') as fh:
        rows = {r['id']: r for r in csv.DictReader(fh)}
    briefs = json.loads((ROOT / 'sales/EMAIL-REWRITE-BRIEFS.json').read_text(encoding='utf-8'))['briefs']
    out = ROOT / 'sales/email-drafts'
    out.mkdir(exist_ok=True)
    active_keys = {f"{key}-{slug(rows[key]['business'])}" for key in briefs if key in rows}
    for path in out.glob('*.txt'):
        if re.match(r'^\d+-', path.name) and path.stem not in active_keys:
            path.unlink()
    messages, document = [], [
        '# الرسائل الجديدة — مسودات للمراجعة، لم تُرسل · 2026-10-11', '',
        'هذه إعادة كتابة للنطاقات الأصغر، وليست تعديل رسائل وصلت للمستلمين. لا إعادة إرسال تلقائية. '
        'العناوين والنوع القانوني والغرض والخصوصية ما زالت بحاجة للمراجعة. الأسماء أدناه تخص المحلات، لا موقع المرسل.', '',
        'الأسواق المستبعدة غير موجودة هنا. لا رسائل إلى صناديق توظيف أو طلبات ميرش/منتجات؛ '
        'حين يكون الغرض محدوداً، العنوان محجوب من المسودة ويبقى النص للتخطيط فقط.', ''
    ]
    for key, brief in briefs.items():
        if key not in rows:
            continue
        row = rows[key]
        if row['package'] != brief['package']:
            raise ValueError('Rewrite brief/package mismatch; do not generate stale prices.')
        body, subject = body_for(row, brief, policy), brief['subject']
        words = validate_email(subject, body)
        blocks = send_blocks(row, policy, registry)
        address = EMAIL.search(row.get('contact_verified') or '')
        suitable = row['contact_purpose'] in {'general-business', 'owner-business', 'vendor-proposals'}
        recipient = address.group(0) if address and suitable else None
        message = {
            'id': key, 'business': row['business'], 'country': row['country'],
            'subject': subject, 'body': body, 'unapproved_recipient': recipient,
            'planned_quote_eur': int(row['quote_eur']), 'package': row['package'],
            'review_only': True, 'sent': False, 'send_ready': not blocks,
            'contact_purpose': row['contact_purpose'], 'blocks': blocks, 'word_count': words,
        }
        messages.append(message)
        label = recipient or 'WITHHELD — contact purpose/source unsuitable or unverified'
        text = f"DRAFT ONLY — NOT SENT\nLead ID: {key}\nRecipient for review only: {label}\nSend ready: NO\nSubject: {subject}\n\n{body}\n"
        (out / f"{key}-{slug(row['business'])}.txt").write_text(text, encoding='utf-8')
        document.extend([
            f"## {row['business']} · id {key} · {row['quote_eur']} € ≈ {money(int(row['quote_eur']), policy)} $", '',
            f"**الحالة:** مسودة فقط؛ لم تُرسل. **غرض العنوان:** {row['contact_purpose']}",
            f"**عنوان للمراجعة لا للإرسال:** {label}",
            '**موانع الإرسال:** ' + '; '.join(blocks), '',
            '**Subject:** ' + subject, '', '```text', body, '```', ''
        ])
    (ROOT / 'sales/EMAIL-REWRITES.json').write_text(json.dumps({'version': 1, 'updated_on': '2026-10-11',
        'messages': messages, 'new_messages_sent': 0}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (ROOT / 'sales/EMAIL-REWRITES.md').write_text('\n'.join(document).rstrip() + '\n', encoding='utf-8')
    print(f"wrote {len(messages)} fresh, location-free smaller-scope letters; sent=0; ready={sum(m['send_ready'] for m in messages)}")


if __name__ == '__main__':
    main()

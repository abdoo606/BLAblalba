#!/usr/bin/env python3
"""Package current review-only deliverables and a private, restorable source bundle.

Never publish either archive in a public repository. Source suppression files are
mandatory; do not restore a trusted source archive by creating an empty registry.
"""
import csv
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from outreach_policy import ROOT, load_policy, validate_email
from suppression import check_sources

PRIVATE_SOURCE_FILES = [
    'sales/prospects-2026.csv', 'sales/prospects-2026.json', 'sales/OUTREACH-LOG.csv',
    'sales/SENT-RECORD.csv', 'sales/SUPPRESSION-LIST.json', 'sales/CAMPAIGN-ACTIVITY.json',
    'sales/OUTREACH-POLICY.json', 'sales/EMAIL-REWRITE-BRIEFS.json', 'sales/EMAIL-REWRITES.json',
]


def main():
    check_sources()
    policy = load_policy()
    with (ROOT / 'sales/prospects-2026.csv').open(newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    assert rows == json.loads((ROOT / 'sales/prospects-2026.json').read_text(encoding='utf-8'))
    assert all(r['country'] not in ('US', 'CA') for r in rows)
    messages = json.loads((ROOT / 'sales/EMAIL-REWRITES.json').read_text(encoding='utf-8'))['messages']
    for msg in messages:
        validate_email(msg['subject'], msg['body'])
        assert msg['sent'] is False and msg['review_only'] is True
    active_ids = {r['id'] for r in rows}
    pitches, drafts = ROOT / 'sales/pitches', ROOT / 'sales/email-drafts'
    assert len(list(pitches.glob('*.md'))) - 1 == len(list((pitches / 'html').glob('*.html'))) == len(rows)
    for path in list(pitches.rglob('*')) + list(drafts.rglob('*')):
        if path.is_file() and re.match(r'^\d+-', path.name):
            assert path.name.split('-', 1)[0] in active_ids, 'Orphaned/deleted client in package'
    release = ROOT / 'release'
    release.mkdir(exist_ok=True)
    with zipfile.ZipFile(release / 'levain-pitches.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for folder in (pitches, drafts):
            for path in sorted(folder.rglob('*')):
                if path.is_file():
                    archive.write(path, path.relative_to(ROOT / 'sales'))
        archive.write(ROOT / 'sales/EMAIL-REWRITES.md', 'EMAIL-REWRITES.md')
    with zipfile.ZipFile(release / 'levain-outreach-private-sources.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        manifest = {'version': 1, 'purpose': 'PRIVATE CRM restore only; not a public release', 'files': {}}
        for name in PRIVATE_SOURCE_FILES:
            path = ROOT / name
            manifest['files'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
            archive.write(path, name)
        archive.writestr('PRIVATE-SOURCE-MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
    for name in ('levain-pitches.zip', 'levain-outreach-private-sources.zip'):
        path = release / name
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
        print(f'{name}: {path.stat().st_size:,} bytes; current data only')
    # Committing code must never re-publish the compiled contact/letter records.
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    forbidden = [name for name in tracked if name in PRIVATE_SOURCE_FILES and name != 'sales/OUTREACH-POLICY.json']
    forbidden += [name for name in tracked if name.startswith(('sales/pitches/', 'sales/email-drafts/'))
                  or name in ('sales/EMAIL-REWRITES.md', 'sales/SHOP-DOSSIERS.md', 'sales/drive-clients-pricing.csv')]
    assert not forbidden, 'Current CRM data is still tracked in public Git'


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Restore trusted private Drive source data after a fresh checkout/sandbox reset.

Only expected data paths are accepted; no code, absolute paths, traversal or
symlinks are extracted. Manifest hashes detect corruption, not malicious provenance.
Existing different local data is never overwritten without an explicit flag.
"""
import argparse
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path
from suppression import ROOT, check_sources

CORE = {
    'sales/prospects-2026.csv', 'sales/prospects-2026.json', 'sales/OUTREACH-LOG.csv',
    'sales/SENT-RECORD.csv', 'sales/SUPPRESSION-LIST.json', 'sales/CAMPAIGN-ACTIVITY.json',
    'sales/OUTREACH-POLICY.json', 'sales/EMAIL-REWRITE-BRIEFS.json', 'sales/EMAIL-REWRITES.json',
}
OPTIONAL = {'sales/MAIL-CHECK.json', 'sales/MAIL-CHECK.md'}
MANIFEST = 'PRIVATE-SOURCE-MANIFEST.json'


def restore(bundle, root=ROOT, overwrite=False, validate=True):
    root = Path(root).resolve()
    with zipfile.ZipFile(bundle) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)) or MANIFEST not in names:
            raise ValueError('Invalid or duplicated source archive members.')
        if sum(info.file_size for info in infos) > 25 * 1024 * 1024:
            raise ValueError('Source archive exceeds the expected size bound.')
        for info in infos:
            if info.filename not in CORE | OPTIONAL | {MANIFEST} or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Unexpected path or symlink in source archive.')
        manifest = json.loads(archive.read(MANIFEST))
        files = manifest.get('files')
        if manifest.get('version') != 1 or not isinstance(files, dict) or not CORE.issubset(files):
            raise ValueError('Incomplete private source manifest; never create an empty safety registry.')
        if set(files) != set(names) - {MANIFEST}:
            raise ValueError('Manifest/member set differs.')
        payloads = {}
        for name, digest in files.items():
            if not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
                raise ValueError('Invalid manifest digest.')
            payload = archive.read(name)
            if hashlib.sha256(payload).hexdigest() != digest:
                raise ValueError('Source checksum mismatch.')
            destination = root / name
            if not destination.resolve().is_relative_to(root):
                raise ValueError('Destination escapes repository root.')
            if destination.exists() and destination.read_bytes() != payload and not overwrite:
                raise ValueError(f'Existing local data differs: {name}; review before explicit overwrite.')
            payloads[name] = payload
    for name, payload in payloads.items():
        destination = root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
    if validate:
        check_sources(root)
    return len(payloads)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        count = restore(args.bundle, overwrite=args.overwrite)
        print(f'Restored {count} trusted private data files; suppression gate passed. No email sent.')
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'{exc}\n')

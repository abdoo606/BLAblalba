import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location('restore_outreach', TOOLS / 'restore-outreach.py')
restore_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(restore_module)


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.destination = self.base / 'work'
        self.destination.mkdir()
        self.bundle = self.base / 'trusted.zip'

    def archive(self, extra=None, bad_digest=False):
        payloads = {name: b'{}\n' for name in restore_module.CORE}
        manifest = {'version': 1, 'files': {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()}}
        if bad_digest:
            manifest['files']['sales/SUPPRESSION-LIST.json'] = '0' * 64
        with zipfile.ZipFile(self.bundle, 'w') as archive:
            for name, data in payloads.items():
                archive.writestr(name, data)
            if extra:
                archive.writestr(extra, b'not an allowed data path')
            archive.writestr(restore_module.MANIFEST, json.dumps(manifest))

    def test_known_data_paths_and_hashes_restore(self):
        self.archive()
        count = restore_module.restore(self.bundle, self.destination, validate=False)
        self.assertEqual(count, len(restore_module.CORE))
        self.assertEqual((self.destination / 'sales/SUPPRESSION-LIST.json').read_bytes(), b'{}\n')

    def test_unexpected_or_traversal_path_rejected_before_writes(self):
        for name in ('../outside.json', '/tmp/outside.json', '.git/config', 'tools/evil.py'):
            with self.subTest(name=name):
                self.archive(extra=name)
                with self.assertRaises(ValueError):
                    restore_module.restore(self.bundle, self.destination, validate=False)
                self.assertEqual(list(self.destination.iterdir()), [])

    def test_bad_checksum_is_rejected_before_writes(self):
        self.archive(bad_digest=True)
        with self.assertRaisesRegex(ValueError, 'checksum'):
            restore_module.restore(self.bundle, self.destination, validate=False)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_different_local_data_is_not_overwritten(self):
        self.archive()
        existing = self.destination / 'sales/SUPPRESSION-LIST.json'
        existing.parent.mkdir()
        existing.write_text('important existing data')
        with self.assertRaisesRegex(ValueError, 'Existing local data differs'):
            restore_module.restore(self.bundle, self.destination, validate=False)
        self.assertEqual(existing.read_text(), 'important existing data')


if __name__ == '__main__':
    unittest.main()

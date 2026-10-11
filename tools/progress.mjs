#!/usr/bin/env node
// Reuse the canonical reporting/gate logic: 'not sent' must never count as sent.
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const result = spawnSync('python3', [join(ROOT, 'tools', 'outreach_reports.py'), 'progress'], {
  cwd: ROOT, stdio: 'inherit', shell: false,
});
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);

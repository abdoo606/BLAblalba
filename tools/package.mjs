/* npm run package — build the site and drop a handover zip in release/:
   dist/ (client-ready), src/data (content), docs. No node_modules needed. */
import { spawnSync } from 'node:child_process';
import { mkdirSync, existsSync, rmSync, statSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'release');
const ZIP = join(OUT, 'levain-kit.zip');
mkdirSync(OUT, { recursive: true });
if (existsSync(ZIP)) rmSync(ZIP);

const run = (cmd, args) => {
  const r = spawnSync(cmd, args, { cwd: ROOT, stdio: 'inherit', shell: false });
  if (r.error) console.error(cmd + ' unavailable: ' + r.error.message);
  return !r.error && r.status === 0;
};

if (!run(process.execPath, [join(ROOT, 'src', 'build.mjs')])) process.exit(1);
const include = ['dist', 'src/data', 'src/styles', 'src/js', 'docs', 'sales', 'README.md', 'package.json'];
const ok = run('zip', ['-rq', join(OUT, 'levain-kit.zip'), ...include]);
if (!ok) run('tar', ['-czf', join(OUT, 'levain-kit.tar.gz'), ...include]);
const made = existsSync(ZIP) ? ZIP : join(OUT, 'levain-kit.tar.gz');
if (existsSync(made)) console.log(`✓ handover archive → ${made.replace(ROOT + '/', '')} (${(statSync(made).size / 1024 / 1024).toFixed(1)} MB)`);
else console.log('archive step skipped (no zip/tar available)');

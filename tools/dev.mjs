/* npm run dev — build once, serve, then rebuild on change in src/. */
import { watch, existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'src');
let child = null;
let timer = 0;

const start = () => {
  if (child) return;
  child = spawn(process.execPath, [join(ROOT, 'tools', 'serve.mjs')], { stdio: 'inherit', cwd: ROOT });
  child.on('exit', () => (child = null));
};

const build = (why = '') => {
  const p = spawn(process.execPath, [join(ROOT, 'src', 'build.mjs')], { stdio: 'inherit', cwd: ROOT });
  p.on('exit', (code) => {
    if (code) console.error('build failed' + why);
    else if (why) console.log('rebuilt' + why);
    start();
  });
};

if (!existsSync(join(ROOT, 'dist'))) await new Promise((r) => build(), 1200);
build();
setTimeout(start, 900);

watch(SRC, { recursive: true }, (_e, file) => {
  if (!file || /\.DS_Store$/.test(file)) return;
  clearTimeout(timer);
  timer = setTimeout(() => build(` (${file})`), 160);
});
console.log('watching src/ … ctrl-c to stop');

/* npm run validate — parity of locales, JSON health, and every local
   href/src in dist/ must resolve to a real file. Run before every delivery. */
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = join(ROOT, 'dist');
const DATA = join(ROOT, 'src', 'data');
const problems = [];

/* 1. locales parse + key parity + no untranslated leftovers */
const locales = {};
for (const f of readdirSync(join(DATA, 'locales'))) {
  if (!f.endsWith('.json')) continue;
  try {
    locales[f.replace('.json', '')] = JSON.parse(readFileSync(join(DATA, 'locales', f), 'utf8'));
  } catch (e) {
    problems.push(`locales/${f}: invalid JSON — ${e.message}`);
  }
}
const flat = (o, p = '') => Object.entries(o).flatMap(([k, v]) => (v && typeof v === 'object' ? flat(v, `${p}${k}.`) : [[`${p}${k}`, v]]));
const codes = Object.keys(locales);
const base = codes.length ? new Map(flat(locales[codes[0]])) : new Map();
for (const code of codes) {
  const map = new Map(flat(locales[code]));
  for (const [k, v] of base) {
    if (!map.has(k)) problems.push(`${code}: missing key ${k}`);
    else if (typeof v === 'string' && !String(map.get(k)).trim()) problems.push(`${code}: empty value at ${k}`);
  }
  for (const k of map.keys()) if (!base.has(k)) problems.push(`${code}: extra key ${k}`);
}
/* 2. data */
let site = {};
try {
  site = JSON.parse(readFileSync(join(DATA, 'site.json'), 'utf8'));
} catch (e) {
  problems.push(`site.json: ${e.message}`);
}
/* 3. links & assets inside dist */
const walk = (dir) => readdirSync(dir).flatMap((f) => (statSync(join(dir, f)).isDirectory() ? walk(join(dir, f)) : [join(dir, f)]));
const files = existsSync(DIST) ? walk(DIST) : [];
if (!files.length) problems.push('dist/ is empty — run `npm run build` first');
for (const file of files) {
  if (!file.endsWith('.html')) continue;
  const html = readFileSync(file, 'utf8');
  for (const m of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const raw = m[1];
    if (/^(https?:|mailto:|tel:|data:|#)/.test(raw) || raw.includes('{{')) continue;
    const clean = raw.split('?')[0].split('#')[0];
    if (!clean) continue;
    const target = resolve(dirname(file), clean);
    if (!existsSync(target) && !existsSync(join(target, 'index.html'))) problems.push(`${file.replace(ROOT + '/', '')}: broken ref → ${raw}`);
  }
  if (!/lang="[a-z]{2}"/.test(html)) problems.push(`${file.replace(ROOT + '/', '')}: missing html lang`);
  if (!/<meta name="viewport"/.test(html)) problems.push(`${file.replace(ROOT + '/', '')}: missing viewport`);
  if (!file.endsWith('404.html') && !/data-i18n=/.test(html)) problems.push(`${file.replace(ROOT + '/', '')}: no i18n hooks`);
}
/* 4. every product image referenced in site.json exists on disk */
for (const p of [...(site.products || []), ...(site.gallery || [])]) {
  const img = join(ROOT, 'src', 'assets', p.image);
  if (!existsSync(img)) problems.push(`missing image: src/assets/${p.image}`);
}
for (const t of site.templates || []) {
  if (!existsSync(join(ROOT, 'src', 'assets', t.hero))) problems.push(`missing hero: src/assets/${t.hero}`);
}
/* 5. a11y-ish smoke test */
for (const file of files.filter((f) => f.endsWith('index.html'))) {
  const html = readFileSync(file, 'utf8');
  const imgs = [...html.matchAll(/<img\b[^>]*>/g)].filter((t) => !/\balt=/.test(t[0]));
  if (imgs.length) problems.push(`${file.replace(ROOT + '/', '')}: ${imgs.length} <img> without alt`);
  const btns = [...html.matchAll(/<button\b[^>]*>(?:(?!<\/button>).)*<\/button>/gs)].filter(
    (t) => !/\baria-label=|\bdata-i18n-aria=|[\p{L}]/u.test(t[0].replace(/<[^>]+>/g, '')) && !/aria-label/.test(t[0])
  );
  if (btns.length > 3) problems.push(`${file.replace(ROOT + '/', '')}: ${btns.length} buttons without an accessible name`);
}
console.log(`${codes.length} locales · ${base.size} keys · ${files.length} files in dist/`);
if (problems.length) {
  console.error('\n✗ ' + problems.length + ' problem(s):');
  for (const p of [...new Set(problems)].slice(0, 60)) console.log('  - ' + p);
  process.exit(1);
}
console.log('✓ all checks passed');

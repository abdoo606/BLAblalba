#!/usr/bin/env node
// tools/progress.mjs — where the pipeline stands, and what the next action is for each lead.
import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const LOG = join(ROOT, 'sales', 'OUTREACH-LOG.csv');
const PRO = process.argv.includes('--prose');

const rows = parseCSV(readFileSync(LOG, 'utf8'));
const order = ['to-verify', 'DISPUTED', 'verified-ready', 'draft-in-gmail', 'sent', 'replied-interested',
  'call-booked', 'scoped', 'quoted', 'negotiated', 'won', 'parked', 'lost', 'do-not-contact'];
const count = {};
for (const r of rows) count[r.status] = (count[r.status] ?? 0) + 1;

const money = (rs) => rs.reduce((n, r) => n + (+r.quoted_eur || 0), 0);
const sent = rows.filter((r) => /sent|replied|call|scoped|quoted|negotiated|won/.test(r.status));
const won = rows.filter((r) => r.status === 'won');

console.log(`\nLevain Kit — pipeline ${new Date().toISOString().slice(0, 10)}  (${rows.length} leads)\n`);
for (const s of order.filter((k) => count[k])) {
  const bar = '█'.repeat(Math.max(1, Math.round(count[s] / 2)));
  console.log(`${s.padEnd(19)} ${String(count[s]).padStart(3)}  ${bar}`);
}
const hasEmail = (r) => /^\s*email\b/i.test(r.channel || '') && !/NOT an email/i.test(r.channel || '');
const emailReady = rows.filter((r) => (r.status === 'verified-ready' || r.status === 'draft-in-gmail') && hasEmail(r));
const callOnly = rows.filter((r) => r.status === 'verified-ready' && !hasEmail(r));
const noPitch = rows.filter((r) => r.status === 'no-pitch');
console.log(`\nready to send now  : ${emailReady.map((r) => r.business).join(', ') || '— (no verified email address left unsent)'}`);
console.log(`call / DM today    : ${callOnly.map((r) => r.business).join(', ') || '—'}`);
console.log(`looked, no pitch   : ${noPitch.length ? noPitch.map((r) => r.business).join(', ') : '—'}`);
console.log(`sent               : ${sent.length} leads${money(sent) ? ` · ${money(sent).toLocaleString()} € quoted` : ''}`);
console.log(`won                : ${won.length}${won.length ? ` · ${money(won).toLocaleString()} €` : ''}`);
console.log(`needs verification : ${count['to-verify'] ?? 0}`);
console.log(`disputed rows      : ${count['DISPUTED'] ?? 0}  ← fix or delete before anything else`);
console.log(`do-not-contact     : ${count['do-not-contact'] ?? 0}  (suppression list — never re-add)`);

if (PRO) {
  console.log(`\nNext 6 actions\n`);
  const prio = { 'draft-in-gmail': 0, 'verified-ready': 1, DISPUTED: 2, 'to-verify': 3 };
  [...rows]
    .sort((a, b) => (prio[a.status] ?? 9) - (prio[b.status] ?? 9) || (b.quoted_eur || 0) - (a.quoted_eur || 0))
    .slice(0, 6)
    .forEach((r) => {
      const file = `sales/pitches/${r.id}-${slug(r.business)}.md`;
      const next = r.status === 'draft-in-gmail'
        ? 'open Gmail, fill the demo link, read it out loud once, send'
        : r.status === 'DISPUTED'
          ? 'find the real business or delete the row — the pitch stays locked'
          : r.status === 'verified-ready'
            ? '§4 of the pitch file → send 1:1'
            : '4-minute check: open their site, their Instagram bio, their Google listing; write the date';
      console.log(`• ${r.business} ${r.status}${r.channel !== 'unknown' ? ` via ${r.channel}` : ' — no channel yet'}\n  → ${next}${existsSync(join(ROOT, file)) ? `\n  → ${file}` : ''}`);
    });
  console.log(`\nSay-this reminders: no invented urgency · price only from sales/drive-clients-pricing.csv ·
  every message carries a real sender and a free opt-out · after a "no", the address never comes back on.\n`);
}

function slug(s) {
  return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}
function parseCSV(text) {
  const out = []; let row = [], cur = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') { if (q && text[i + 1] === '"') { cur += '"'; i++; } else q = !q; }
    else if (c === ',' && !q) { row.push(cur); cur = ''; }
    else if ((c === '\n' || c === '\r') && !q) {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cur); if (row.length > 1 || row[0] !== '') out.push(row); row = []; cur = '';
    } else cur += c;
  }
  const [head, ...body] = out;
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.replace(/^\uFEFF/, ''), (r[i] ?? '').trim()])));
}

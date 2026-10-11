#!/usr/bin/env node
// Current-edition scope boards. No old delivered-email body or invented client menu.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, unlinkSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const gate = spawnSync('python3', [join(ROOT, 'tools', 'outreach_policy.py'), 'audit'], { cwd: ROOT, encoding: 'utf8' });
if (gate.error || gate.status !== 0) {
  console.error(gate.error?.message || gate.stderr || 'Policy audit failed.');
  process.exit(1);
}
const OUT = join(ROOT, 'sales', 'pitches');
mkdirSync(join(OUT, 'html'), { recursive: true });
const rows = parseCSV(readFileSync(join(ROOT, 'sales', 'prospects-2026.csv'), 'utf8'));
const policy = JSON.parse(readFileSync(join(ROOT, 'sales', 'OUTREACH-POLICY.json'), 'utf8'));
const emails = JSON.parse(readFileSync(join(ROOT, 'sales', 'EMAIL-REWRITES.json'), 'utf8'));
const letters = new Map(emails.messages.map((m) => [m.id, m]));
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const slug = (s) => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const active = new Set(rows.map((r) => `${r.id}-${slug(r.business)}`));
for (const [dir, ext] of [[OUT, '.md'], [join(OUT, 'html'), '.html']]) {
  for (const name of readdirSync(dir)) {
    if (/^\d+-/.test(name) && name.endsWith(ext) && !active.has(name.slice(0, -ext.length))) unlinkSync(join(dir, name));
  }
}
const index = [];
for (const row of rows) {
  const key = `${row.id}-${slug(row.business)}`;
  const pack = policy.packages[row.package];
  const fee = +row.quote_eur;
  const usd = Math.round(fee * policy.rates.USD);
  const letter = letters.get(row.id);
  const noOffer = row.offer_state === 'no-offer';
  const scope = noOffer ? 'No proposal: preserve the no-pitch research decision.' : pack.scope;
  const state = 'DRAFT / RESEARCH ONLY — NOT SENT — LEGAL AND SOURCE REVIEW PENDING';
  const md = `# ${row.business} — smaller-scope concept\n\n${state}\n\n` +
    `Client area: ${row.city}, ${row.country}. This is the client's area, not the provider's location.\n\n` +
    `## Proposed scope\n${scope}\n\n` +
    `Planning fee: ${fee} EUR ≈ ${usd} USD, once. Not a delivered quote, retrospective replacement, contract or revenue.\n` +
    `No default subscription. Estimated ${pack.days} working days after scope/content/access confirmation; one revision round for a commissioned build.\n` +
    `Client supplies approved text and images. Hosting/domain are client-owned. Tax treatment is confirmed before agreement.\n\n` +
    `## Excluded unless separately approved\n${policy.excluded_by_default.map((s) => '- ' + s).join('\n')}\n\n` +
    `## Research / contact hold\n${row.verification}\nContact purpose: ${row.contact_purpose}. Publication proof: ${row.contact_source_verified}.\n` +
    `Budget: unknown. Entity/consent/privacy and sender-side/tax/payment reviews are incomplete. Previous recipient: ${row.already_contacted_at ? 'YES — no automatic replay' : 'no recorded prior contact'}.\n\n` +
    `## Review-only letter\n${letter ? 'Subject: ' + letter.subject + '\n\n' + letter.body : 'No email prepared: do the source, need and legal review first.'}\n\n` +
    `No sending from this board. Run the suppression and check-send gates and obtain the applicable approval.\n`;
  writeFileSync(join(OUT, `${key}.md`), md);
  const color = row.recommended_template.toLowerCase().includes('patisserie') ? '#875069' : '#8b542e';
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(row.business)} — small-scope concept</title><style>
:root{--accent:${color};--ink:#242421;--paper:#faf7f0}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,sans-serif}.wrap{max-width:940px;margin:auto;padding:36px 22px 64px}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase}header{padding:38px;border-radius:22px;background:var(--ink);color:var(--paper)}h1{font:clamp(32px,6vw,58px)/1.12 Georgia,serif;margin:12px 0}h2{margin-top:34px;font:25px/1.3 Georgia,serif}.hold{background:#fff1cf;border:1px solid #cba557;border-radius:12px;padding:16px;margin-top:22px}.fee{color:var(--accent);font-size:32px;font-weight:700}.muted{opacity:.72}.card{background:#fff;border:1px solid #e7e2d7;border-radius:16px;padding:24px;margin-top:18px}pre{font:15px/1.7 system-ui,sans-serif;white-space:pre-wrap;overflow-wrap:anywhere}li{margin:7px 0}@media print{header{background:none;color:var(--ink);padding:10px}.hold,.card{break-inside:avoid}.wrap{padding:0}}
</style></head><body><main class="wrap"><header><span class="eyebrow">Independent concept · not client work · review only</span><h1>${esc(row.business)}</h1><p>${esc(noOffer ? 'Research record — no offer' : pack.name)}</p></header>
<div class="hold">${esc(state)}. No new email has been sent. Previous deliveries cannot be edited from this document.</div>
<section class="card"><h2>The small starting point</h2><p>${esc(scope)}</p><p class="fee">${fee.toLocaleString()} EUR <span style="font-size:16px">≈ ${usd.toLocaleString()} USD · one-time</span></p><p class="muted">Planning fee only. Tax and feasibility are confirmed before agreement. No mandatory monthly plan; optional care is separate. Client owns and pays hosting/domain.</p></section>
<h2>Precisely bounded</h2><ul>${(noOffer ? ['No commissioned work proposed.'] : pack.deliverables).map((s) => `<li>${esc(s)}</li>`).join('')}</ul><p>${pack.days} working days estimated after content/access/scope readiness · one revision for commissioned work · 40% deposit after approved written scope.</p>
<h2>Not included</h2><ul>${policy.excluded_by_default.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
<section class="card"><h2>Review status</h2><p>${esc(row.verification)}</p><p>Contact purpose: ${esc(row.contact_purpose)} · Budget unknown · Entity/consent, source and privacy review pending.</p><p>${row.already_contacted_at ? 'Previously contacted — do not replay a first-touch email.' : 'No earlier contact recorded; no permission to send inferred.'}</p></section>
${letter ? `<section class="card"><h2>Replacement-copy draft — not sent</h2><p><b>${esc(letter.subject)}</b></p><pre>${esc(letter.body)}</pre></section>` : '<p>No email prepared until the need, publication and legal checks are documented.</p>'}
<footer class="muted"><p>${esc(policy.sender.display_name)} · ${esc(policy.sender.role)}</p><p>Private planning concept. No affiliation, real-menu claim, invented portfolio or guaranteed result.</p></footer></main></body></html>`;
  writeFileSync(join(OUT, 'html', `${key}.html`), html);
  index.push(`| [${key}](./${key}.md) | ${row.business.replaceAll('|', '\\|')} | ${row.country} | ${fee} | ${usd} | ${row.offer_state} | ${row.contact_purpose} |`);
}
writeFileSync(join(OUT, 'INDEX.md'), `# Smaller-scope concepts — ${rows.length} active research records\n\nReview only. No new sends, no automatic replay, no source/legal permission inferred. Excluded markets are absent.\n\n| Board | Business | Client country | Draft EUR | Approx USD | Offer state | Contact purpose |\n|---|---|---|---:|---:|---|---|\n${index.join('\n')}\n`);
console.log(`${rows.length} smaller-scope boards · ${letters.size} replacement-copy drafts · sent=0 · review-only`);

function parseCSV(text) {
  const out = []; let row = [], current = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') { if (quoted && text[i + 1] === '"') { current += '"'; i++; } else quoted = !quoted; }
    else if (c === ',' && !quoted) { row.push(current); current = ''; }
    else if ((c === '\n' || c === '\r') && !quoted) {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(current); if (row.length > 1) out.push(row); row = []; current = '';
    } else current += c;
  }
  if (current || row.length) { row.push(current); out.push(row); }
  const [head, ...body] = out;
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.replace(/^\uFEFF/, ''), (r[i] ?? '').trim()])));
}

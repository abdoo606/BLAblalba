#!/usr/bin/env node
// tools/make-pitches.mjs — one design board + pitch + checklist per prospect.
// Reads sales/prospects-2026.csv, writes sales/pitches/*.md + sales/pitches/html/*.html + INDEX.md.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'sales', 'pitches');
mkdirSync(join(OUT, 'html'), { recursive: true });

const site = JSON.parse(readFileSync(join(ROOT, 'src', 'data', 'site.json'), 'utf8'));
const en = JSON.parse(readFileSync(join(ROOT, 'src', 'data', 'locales', 'en.json'), 'utf8'));
const pname = (id) => (en.product?.[id]?.name ?? en.menu?.[id]?.name ?? en.products?.[id]?.name ?? id)
  .replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
const rows = parseCSV(readFileSync(join(ROOT, 'sales', 'prospects-2026.csv'), 'utf8'));
const TPL = Object.fromEntries(site.templates.map((t) => [t.id, t]));

const CUR = { US: ['$', 'USD'], GB: ['£', 'GBP'], FR: ['€', 'EUR'], ES: ['€', 'EUR'], RE: ['€', 'EUR'], GR: ['€', 'EUR'], CA: ['CA$', 'CAD'] };
const LANG = { US: ['en'], GB: ['en'], FR: ['fr'], ES: ['es'], RE: ['fr'], CA: ['fr', 'en'] };
const SECOND = { GB: 'FR · PL · RO · ES — pick the one your street actually speaks', US: 'ES · FR · ZH · KO',
  FR: 'EN · ES · DE · IT', ES: 'EN · FR · DE (plus Catalan/Valencian where it is the street language)', RE: 'EN', CA: 'EN' };
const DAYS = { baguette: 5, croissant: 7, patisserie: 14, licence: 3 };
const CAT = new Set(['Barcelona', 'València']); // cities where a Catalan menu line is a real plus
const PALETTES = {
  artisan: [['#2f1c12', '#b4530a', '#f6ece0', '#7d5a3c', 'Flour, crust, burnt sugar'],
            ['#22201c', '#8a6d3b', '#f3efe6', '#5d5340', 'Rye, linen, walnut'],
            ['#2a1f1a', '#a8562a', '#f7ece1', '#6b4b36', 'Cocoa nib, ember, cream']],
  patisserie: [['#1c1a24', '#b4708c', '#f8f2f4', '#6d5a7a', 'Plum, meringue, lilac'],
               ['#141b1a', '#3f8f7a', '#f2f7f4', '#4a6b62', 'Pistachio, cream, mint'],
               ['#20141c', '#c2496b', '#fdf4f6', '#7a4256', 'Raspberry, buttercream']],
  moderno: [['#101314', '#e2622a', '#f4f5f4', '#40535c', 'Concrete, ember, steel'],
            ['#0f1113', '#2f80c4', '#f1f5f8', '#3a5a72', 'Glaze, blueberry, ice'],
            ['#12100f', '#c9a227', '#f5f2ea', '#5b5340', 'Burnt honey, brass']],
};
const hash = (s) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const slug = (s) => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const money = (eur, c) => {
  const r = { USD: 1.09, GBP: 0.86, CAD: 1.5, EUR: 1 }[CUR[c][1]] ?? 1;
  return Math.round((eur * r) / 5) * 5;
};
// Menu items: the kit's own products, filtered by the words that appear in the lead's own story.
function menuFor(r) {
  const text = `${r.business} ${r.growth_signal_why_now} ${r.audit_note ?? ''}`.toLowerCase();
  const score = (p) => (p.tags || []).reduce((n, t) => n + (text.includes(t) ? 2 : 0), 0)
    + (text.includes(String(p.id).replace(/-/g, ' ')) ? 3 : 0);
  const cur = CUR[r.country]?.[0] ?? '€';
  return [...site.products].sort((a, b) => score(b) - score(a)).slice(0, 6)
    .map((p) => ({ name: pname(p.id), note: p.weight ?? '', price: `${cur}${(+p.price).toFixed(2)}${p.category ? ` · ${p.category}` : ''}` }));
}
const firstLine = (r) => {
  const facts = [];
  if (r.verification_2026_10_10?.startsWith('VERIFIED')) facts.push(r.audit_note);
  else facts.push(`public notes say: “${r.web_presence_note}” — open their site before you use this sentence`);
  return facts[0].trim();
};
function priceBlock(r) {
  const cur = CUR[r.country]?.[0] ?? '€';
  const add = r.addons ? ` Includes ${r.addons.split('+').map((x) => x.trim()).join(' + ')}.` : '';
  const vat = r.tax_wave?.startsWith('1')
    ? `No VAT on my invoice: you account for local VAT yourself (reverse charge), and it nets off if you are VAT-registered.`
    : r.tax_wave?.startsWith('2')
      ? `Billed without VAT under the reverse charge (art. 196 Directive 2006/112) — send me your VAT number. If you are not VAT-liable (franchise en base / módulos), you self-account 21 % you cannot recover, so budget about ${money(+r.quote_eur * 1.21, r.country)} ${cur}.`
      : 'VAT treatment to be confirmed — I invoice from outside the EU.';
  return { eur: r.quote_eur, local: `${money(+r.quote_eur, r.country)} ${cur}`, vat, add, care: `Care plan ${money(45, r.country)} ${cur}/month (prices, hours, seasonal menu, updates).` };
}

const boards = [];
for (const r of rows) {
  const t = TPL[r.recommended_template] ?? TPL.artisan;
  const pal = PALETTES[t.theme] ?? PALETTES.artisan;
  const [ink, accent, paper, muted, palName] = pal[hash(r.business) % pal.length];
  const want = Math.max(1, parseInt(r.languages, 10) || 1);
  const langs = (LANG[r.country] ?? ['en']).slice(0, want);
  if (want > langs.length) langs.push(`${want - langs.length} more: ${SECOND[r.country] ?? 'EN'}`);
  if (CAT.has(r.city)) langs.push('ca/valencià — same layout, RTL-safe code is already in the kit');
  const days = DAYS[r.package] ?? 7;
  const menu = menuFor(r);
  const p = priceBlock(r);
  const demo = `dist/templates/${t.id}/index.html?lang=${langs[0]}`;
  const id = `${r.id}-${slug(r.business)}`;
  const verified = r.verification_2026_10_10?.startsWith('VERIFIED');
  const hasEmail = /\S+@\S+\.\w/.test((r.contact_verified ?? '').replace(/Instagram\s*@\S+/, ''));
  const channel = verified && hasEmail ? 'email' : verified ? 'phone / counter / DM (no public email)' : 'to be found during verification';
  const md = `# ${r.business} — design board & pitch

${r.city}, ${r.country} · ${r.priority} · template **${t.id}** · ${r.package} · ${p.eur} €
Verified 2026-10-11: **${verified ? 'YES' : 'NO — do the 4-minute check before anything is sent'}**

## 1. Why them, now
${r.growth_signal_why_now}
Source on file: ${r.source}${r.source_date ? ` (${r.source_date})` : ''}.

## 2. What their web presence actually is
${firstLine(r)}
${verified ? `Found live: ${r.site_found || '—'}\nContact: ${r.contact_verified}` : `Claimed earlier (press/aggregator): ${r.web_presence_note}`}

## 3. The design I'd ship
- **Template:** ${t.id} · **palette:** ${palName} — \`${ink} ink / ${accent} accent / ${paper} paper / ${muted} muted\`
- **Sections, in order:** ${t.sections.join(' → ')}${/wholesale/.test(r.addons) ? ' → **wholesale order page**' : ''}${/preorder|pre-order/.test(r.addons) ? ' → **pre-order basket → WhatsApp**' : ''}${/multi/.test(r.addons) ? ' → **per-location hours & stock**' : ''}${/photo/.test(r.addons) ? ' → **gallery: 9 shots, client-shot, I direct remotely**' : ''}
- **Languages:** ${langs.join(', ')}${CAT.has(r.city) ? ' (Spanish + Catalan is what sells in this city; Arabic RTL is already in the codebase if you want a halal/wedging crowd served)' : ''}
- **Menu to enter (their real items, from their own posts):** ${menu.map((m) => `${m.name} ${m.price}`).join(' · ')}
- **Hero line:** “${r.business} — ${/sourdough|rye|loaf/i.test(r.growth_signal_why_now + r.business) ? 'the loaf people queue for' : 'what the whole street talks about'}” — ${langs.length > 1 ? 'written once, mirrored in the second language, never machine-translated.' : 'one language, so it stays human.'}
- **Hours block:** as published by *them*, not as on Google — and we fix the Google listing in the SEO pass so the two agree. That single mismatch is why ${/hours/i.test(r.audit_note ?? '') ? 'this is clause 1 of this project' : 'we check it on day 1'}.
- **Live preview:** \`${demo}\` (open it on your phone first — that's the only screen they will judge it on)

## 4. What I would say (first touch, ${channel})
> Hi ${r.business.replace(/^(Boulangerie[- ]|Forn |Panadería |Panaderia |La |Le |El )/g, '')} team — ${/^[a-z]/.test(r.business) ? '' : `I looked at ${r.site_found || 'your online presence'} this morning. `}${firstLine(r).replace(/\.$/, '')}.
> That's exactly the part I build: ${t.sections.slice(0, 4).join(', ')} — ${p.local} delivered in ${days} days, and the files and repository are yours, no subscription, no Shopify fees.${p.add}
> ${p.vat}
> If this isn't the right conversation, say so once and I won't write again.
>
> Abdulrhman Thali · freelance web developer · Karm El-Zeitoun, Homs, Syria
> You're getting this because your contact details are published by you / in public listings. Reply “remove me” and I delete you from my list permanently.

*(If the first sentence in that quote is not true today, do not send the quote. Fix it, then send.)*

## 5. Before you press send — this lead's checklist
- [ ] Opened their site / Instagram / Google listing **today**
- [ ] Confirmed the sentence in §4 is a fact, not an assumption (write what you saw)
- [ ] Contact address is one *they* published (never guessed, never bought)
- [ ] Package + price match \`sales/drive-clients-pricing.csv\` — nothing renegotiated in a cold email
- [ ] Signature has the real name and a real postal address
- [ ] Opt-out line present, and the reply goes straight into the suppression list
- [ ] 1:1 send from a normal mailbox (no Mailchimp/Brevo broadcast, max 5–10/day)
- [ ] Log updated in \`sales/OUTREACH-LOG.csv\` (status + date + source of address)

## 6. If they reply yes
1. 12 scoping questions on one 10-min call (\`sales/REPLY-PLAYBOOK.md\` §4)
2. Quote from §3 + the 40 % deposit invoice (payment route agreed **first** — see the note at the bottom of \`sales/PROGRESS-CHECKLIST.md\`)
3. Domain **in their name**, on their email, their 2FA (RDAP check first: \`curl https://rdap.org/domain/<name>\`)
4. Content deadline 7 days · build in this kit on branch \`client/${id}\` · staging link · 2 revision rounds
5. Go-live: DNS + HTTPS + Google listing hours fixed + printed counter sheet
6. Handover doc + care plan signed the same week
`;
  writeFileSync(join(OUT, `${id}.md`), md);

  const html = `<!doctype html><html lang="${langs[0].slice(0, 2)}" data-theme="${t.theme}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(r.business)} — design board · Levain Kit</title>

<style>
:root{--ink:${ink};--accent:${accent};--paper:${paper};--muted:${muted}}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 var(--font)}
[data-theme="patisserie"]{--font:"Didot","Playfair Display",Georgia,serif}
[data-theme="moderno"]{--font:ui-sans-serif,system-ui,"Helvetica Neue",Arial,sans-serif}
[data-theme="artisan"]{--font:Georgia,"Iowan Old Style",serif}
.wrap{max-width:960px;margin:0 auto;padding:28px 20px 64px}
.hero{border:1px solid #0002;border-radius:22px;padding:34px 26px;background:
radial-gradient(120% 140% at 100% 0,${accent}22,transparent 60%),${ink};color:${paper}}
.hero h1{font-size:clamp(30px,6vw,54px);margin:0 0 10px;line-height:1.05}
.hero p{margin:0;opacity:.86}
.sw{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 0}
.sw i{width:64px;height:40px;border-radius:10px;display:block;border:1px solid #0002}
h2{font-size:14px;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin:34px 0 10px}
ul{margin:0;padding-left:20px}
.menu{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.mi{border:1px solid #0002;border-radius:14px;padding:12px 14px;background:#fff6;display:flex;justify-content:space-between;gap:12px;align-items:baseline}
.mi b{font-weight:600}.mi s{opacity:.6;text-decoration:none;font-size:14px}
.tag{display:inline-block;border:1px solid ${accent};color:${accent};border-radius:999px;padding:3px 10px;font:12px/1 system-ui;margin:4px 6px 0 0}
.box{border:1px dashed #0003;border-radius:16px;padding:16px 18px;background:#fff5}
pre{white-space:pre-wrap;font:13px/1.6 ui-monospace,monospace;margin:0}
a{color:${accent}}
</style></head><body><div class="wrap">
<div class="hero"><p style="letter-spacing:.16em;text-transform:uppercase;font-size:12px;opacity:.7">${esc(r.city)} · ${esc(r.country)} · ${t.id} template</p>
<h1>${esc(r.business)}</h1>
<p>${esc(r.business)} — ${/sourdough|rye|loaf/i.test(r.growth_signal_why_now + r.business) ? 'the loaf people queue for' : 'what the whole street talks about'}</p>
<div class="sw">${[ink, accent, paper, muted].map((c) => `<i style="background:${c}" title="${c}"></i>`).join('')}</div>
<p style="font-size:13px;opacity:.7;margin-top:12px">palette: ${palName}</p></div>

<h2>Sections, in order</h2><p>${t.sections.map((s) => `<span class="tag">${esc(s)}</span>`).join('')}${/wholesale/.test(r.addons) ? '<span class="tag">wholesale order</span>' : ''}${/preorder|pre-order/.test(r.addons) ? '<span class="tag">pre-order → WhatsApp</span>' : ''}${/multi/.test(r.addons) ? '<span class="tag">2 locations</span>' : ''}</p>

<h2>Menu, entered from their own posts</h2><div class="menu">${menu.map((m) => `<div class="mi"><b>${esc(m.name)}</b><s>${esc(m.price ?? '')}</s></div>`).join('')}</div>

<h2>Languages</h2><p>${langs.map((l) => `<span class="tag">${esc(l)}</span>`).join('')} <span style="opacity:.7;font-size:14px">— second language is a real menu, not a Google-translate banner.</span></p>

<h2>What I'd say first</h2><div class="box"><pre>${esc(md.split('## 4. What I would say')[1].split('\n\n## 5')[0].replace(/^[^\n]*\n>\s*/, '').split('\n> ').join('\n'))}</pre></div>

<h2>Numbers</h2><p><b>${p.local}</b> — ${esc(r.package)}${esc(p.add)}<br><span style="opacity:.8;font-size:14px">${esc(p.vat)}</span><br><span style="opacity:.8;font-size:14px">${esc(p.care)}</span></p>

<h2>Verified?</h2><p>${verified ? `<b>Yes</b> — ${esc(r.site_found || '')} · ${esc(r.contact_verified || '')}` : '<b>No</b> — do the 4-minute check (site, Google listing, Instagram bio, WHOIS) before this page is sent to anyone.'}</p>
<p style="margin-top:26px;font-size:13px;opacity:.7">Generated 2026-10-11 by <code>tools/make-pitches.mjs</code> · full brief in <code>sales/pitches/${id}.md</code></p>
</div></body></html>`;
  writeFileSync(join(OUT, 'html', `${id}.html`), html);
  boards.push({ id: r.id, key: id, business: r.business, city: r.city, country: r.country, tpl: t.id, price: p.eur, verified: verified ? '✅' : '⬜', channel, wave: r.tax_wave?.slice(0, 1) ?? '?' });
}

const idx = `# Design boards — 36 bakeries, one file each

Generated by \`node tools/make-pitches.mjs\`. Per lead: \`sales/pitches/<file>.md\` (the brief you read)
and \`sales/pitches/html/<file>.html\` (the design board — open it in a browser, it uses the kit's own
\`core.css\` and theme, so what you see is what the client gets).

| Lead | Business | City | Wave | Template | € | Verified | Channel |
|---|---|---|---|---|---|---|---|
${boards.map((b) => `| [${b.key}](./${b.key}.md) | ${b.business} | ${b.city} | ${b.wave} | ${b.tpl} | ${b.price} | ${b.verified} | ${b.channel} |`).join('\n')}

**Reading the ⬜**: the design is real and shippable; the *reason* in §4 of that file is not yet confirmed,
so the message stays undelivered until someone opens their site. ${boards.filter((b) => b.verified === '✅').length} of ${boards.length} are ✅.
`;
writeFileSync(join(OUT, 'INDEX.md'), idx);
console.log(`${boards.length} design boards · ${boards.filter((b) => b.verified === '✅').length} verified · ${boards.filter((b) => b.channel === 'email').length} with a real email`);

function parseCSV(text) {
  const rows = []; let row = [], cur = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') { if (q && text[i + 1] === '"') { cur += '"'; i++; } else q = !q; }
    else if (c === ',' && !q) { row.push(cur); cur = ''; }
    else if ((c === '\n' || c === '\r') && !q) {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cur); if (row.length > 1 || row[0] !== '') rows.push(row); row = []; cur = '';
    } else cur += c;
  }
  if (cur || row.length) { row.push(cur); rows.push(row); }
  const [head, ...body] = rows;
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.replace(/^\uFEFF/, ''), (r[i] ?? '').trim()])));
}

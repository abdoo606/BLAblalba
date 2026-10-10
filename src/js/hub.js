/* ==========================================================================
   Levain Kit — hub extras: live template showcase, viewport emulator,
   quote calculator, copy-to-clipboard. All optional, all vanilla.
   ========================================================================== */
(() => {
  'use strict';
  const D = document;
  const $ = (s, r = D) => r.querySelector(s);
  const $$ = (s, r = D) => Array.from(r.querySelectorAll(s));
  const CFG = window.LEVAIN_CFG || {};
  const t = (k, v) => (window.LevainKit?.t ? window.LevainKit.t(k, v) : k);

  /* -------------------------------------------------- showcase switcher */
  function showcase() {
    const frame = $('[data-frame]');
    if (!frame) return;
    const iframe = $('iframe', frame);
    const tabs = $$('[data-tpl]');
    const pick = $$('[data-quote-tpl]');
    const viewport = $('[data-viewport]');
    const url = $('[data-frame-url]');
    const base = CFG.base || '.';
    const lang = () => (window.LevainKit?.lang || 'en');

    const load = (id) => {
      tabs.forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tpl === id)));
      pick.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.quoteTpl === id)));
      const tpl = (CFG.templates || []).find((x) => x.id === id) || { path: 'templates/' + id };
      const src = `${base}/${tpl.path}/index.html?embed=1&lang=${lang()}`;
      if (iframe.dataset.src !== src) {
        iframe.dataset.src = src;
        iframe.src = src;
      }
      if (url) url.textContent = `https://${(CFG.brandSlug || 'boulangerie')}.example/${id === 'artisan' ? '' : id + '/'}`;
      D.dispatchEvent(new CustomEvent('levain:toast', { detail: t('hub.open') + ' · ' + id }));
    };
    tabs.forEach((b) => b.addEventListener('click', () => load(b.dataset.tpl)));
    pick.forEach((b) => b.addEventListener('click', () => load(b.dataset.quoteTpl)));
    $$('[data-size]').forEach((b) =>
      b.addEventListener('click', () => {
        const size = b.dataset.size;
        viewport.dataset.size = size;
        $$('[data-size]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      })
    );
    // hub language change → re-announce to the live iframe
    D.addEventListener('levain:lang', () => {
      const active = tabs.find((b) => b.getAttribute('aria-selected') === 'true');
      if (active && iframe.contentWindow) {
        iframe.contentWindow.postMessage({ type: 'levain:lang', code: lang() }, '*');
      }
    });
    iframe.addEventListener('load', () => {
      iframe.contentWindow?.postMessage({ type: 'levain:lang', code: lang() }, '*');
    });
  }

  /* -------------------------------------------- quote calculator (pricing) */
  const state = { pkg: 'croissant', langs: 2, opts: new Set(['seo']), client: '' };

  function calc() {
    const root = $('[data-calc]');
    if (!root) return;
    const pkgs = CFG.packages || [];
    const opts = CFG.options || [];

    const render = () => {
      const pkg = pkgs.find((p) => p.id === state.pkg) || pkgs[0];
      const extraLangs = Math.max(0, state.langs - (pkg.languages || 1));
      const langPrice = extraLangs * (opts.find((o) => o.id === 'language')?.price || 0);
      const chosen = opts.filter((o) => o.id !== 'language' && state.opts.has(o.id) && !o.recurring);
      const recurring = opts.filter((o) => o.id !== 'language' && state.opts.has(o.id) && o.recurring);
      const total = (pkg.price || 0) + langPrice + chosen.reduce((s, o) => s + o.price, 0);
      const monthly = recurring.reduce((s, o) => s + o.price, 0);
      const money = (n) => (window.LevainKit?.money ? window.LevainKit.money(n) : n.toFixed(2));

      $('[data-calc-total]', root).textContent = money(total);
      const rows = $('[data-calc-rows]', root);
      if (rows) {
        const list = [[t('hub.calcPackage') + ' · ' + t('hub.pkg.' + pkg.id), money(pkg.price)]];
        if (extraLangs > 0) list.push([`${t('hub.opt.language')} × ${extraLangs}`, money(langPrice)]);
        chosen.forEach((o) => list.push([t('hub.' + o.labelKey.replace('calc.opt.', 'opt.')), money(o.price)]));
        list.push([t('hub.calcLangs'), String(state.langs)]);
        rows.innerHTML = list.map(([a, b]) => `<div class="calc__row"><span>${a}</span><span class="num">${b}</span></div>`).join('');
      }
      $('[data-calc-monthly]', root).textContent = monthly ? money(monthly) + ' / mo' : '—';
      $('[data-calc-days]', root).textContent = pkg.days ? t('hub.calcDaysValue', { n: pkg.days }) : t('hub.pkg.licence');
      const bullets = $('[data-calc-list]', root);
      if (bullets) {
        const items = [
          t('hub.f1t') + ' — ' + t('hub.f1d'),
          t('hub.f3t') + ' — ' + t('hub.f3d'),
          t('hub.f6t') + ' — ' + t('hub.f6d'),
        ];
        if (state.opts.has('seo')) items.push(t('hub.opt.seo'));
        if (state.opts.has('photo')) items.push(t('hub.opt.photo'));
        if (state.opts.has('preorder')) items.push(t('hub.opt.preorder'));
        if (state.pkg === 'patisserie') items.push(t('hub.f7t'), t('hub.f5t'));
        bullets.innerHTML = items.map((i) => `<li>${i}</li>`).join('');
      }
      state.total = total;
      state.monthly = monthly;
    };

    $$('[data-pkg]', root).forEach((b) =>
      b.addEventListener('click', () => {
        state.pkg = b.dataset.pkg;
        const pkg = (CFG.packages || []).find((p) => p.id === state.pkg);
        if (pkg) state.langs = Math.max(state.langs, pkg.languages || 1);
        $$('[data-pkg]', root).forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        const langBtns = $$('[data-langs] button', root);
        langBtns.forEach((x) => x.setAttribute('aria-pressed', String(Number(x.dataset.langs) === state.langs)));
        render();
      })
    );
    $$('[data-langs] button', root).forEach((b) =>
      b.addEventListener('click', () => {
        state.langs = Number(b.dataset.langs);
        $$('[data-langs] button', root).forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        render();
      })
    );
    $$('[data-opt] input', root).forEach((inp) =>
      inp.addEventListener('change', () => {
        const id = inp.closest('[data-opt]').dataset.opt;
        inp.checked ? state.opts.add(id) : state.opts.delete(id);
        render();
      })
    );
    $('[data-client]', root)?.addEventListener('input', (e) => { state.client = e.target.value.trim(); });
    $('[data-copy-quote]', root)?.addEventListener('click', async () => {
      const lines = [
        `Levain Kit — ${t('hub.calcTitle')}`,
        state.client ? `Client: ${state.client}` : '',
        `Template: ${$('[data-quote-tpl][aria-pressed="true"]')?.dataset.quoteTpl || 'any'}`,
        `Package: ${state.pkg} · Languages: ${state.langs}`,
        `Add-ons: ${[...state.opts].join(', ') || '—'}`,
        `Total: ${window.LevainKit?.money(state.total) || state.total}`,
        state.monthly ? `Care: ${window.LevainKit?.money(state.monthly)}/month` : '',
        `Repo: ${CFG.repo || ''}`,
      ].filter(Boolean);
      try {
        await navigator.clipboard.writeText(lines.join('\n'));
        D.dispatchEvent(new CustomEvent('levain:toast', { detail: t('hub.calcCopied') }));
      } catch {
        D.dispatchEvent(new CustomEvent('levain:toast', { detail: lines.join(' · ') }));
      }
    });
    render();
    D.addEventListener('levain:lang', render);
  }

  /* ------------------------------------------------------- copy buttons */
  function copyButtons() {
    $$('[data-copy]').forEach((btn) =>
      btn.addEventListener('click', async () => {
        const text = btn.dataset.copy || $('code', btn.parentElement)?.textContent || '';
        try { await navigator.clipboard.writeText(text.trim()); btn.textContent = t('common.copied'); }
        catch { btn.textContent = '⌘C'; }
        setTimeout(() => (btn.textContent = t('common.copy')), 1600);
      })
    );
  }

  const boot = () => { showcase(); calc(); copyButtons(); };
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

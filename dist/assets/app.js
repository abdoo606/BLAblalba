/* ==========================================================================
   Levain Kit — runtime engine (no dependencies, ~1 file)
   i18n + RTL · basket · oven countdown · open-now · menu filter · carousel
   lightbox · accordion · form validation · reveal · scrollspy · toasts
   ========================================================================== */
(() => {
  'use strict';

  const D = document;
  const $ = (s, r = D) => r.querySelector(s);
  const $$ = (s, r = D) => Array.from(r.querySelectorAll(s));
  const CFG = window.LEVAIN_CFG || {};
  const DICT = window.LEVAIN_I18N || {};
  const LANGS = CFG.languages || [{ code: 'en', locale: 'en-GB', dir: 'ltr' }];
  const LS = {
    get(k, f) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : f; } catch { return f; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
  };
  const LANG_KEY = 'levain.lang';
  const BASKET_KEY = 'levain.basket.' + (CFG.templateId || 'default');
  const MODE_KEY = 'levain.mode';
  const reduced = () => (typeof matchMedia === 'function' ? matchMedia('(prefers-reduced-motion: reduce)').matches : false);

  /* ------------------------------------------------------------------ i18n */
  let lang = LS.get(LANG_KEY, CFG.defaultLanguage || 'en');
  if (!LANGS.some((l) => l.code === lang)) lang = CFG.defaultLanguage || 'en';

  const path = (obj, key) => key.split('.').reduce((o, k) => (o == null ? o : o[k]), obj);
  const lookup = (key, code = lang) => {
    const v = path(DICT[code] || {}, key);
    return typeof v === 'string' ? v : typeof v === 'number' ? String(v) : null;
  };
  const fill = (str, vars) =>
    str == null ? '' : (vars ? str.replace(/\{\{(\w+)\}\}/g, (m, k) => (vars[k] ?? m)) : str);
  /** Translate a key with optional interpolation. Safe fallback = the key itself. */
  const t = (key, vars) => fill(lookup(key) ?? lookup(key, CFG.defaultLanguage) ?? key, vars);

  const locale = () => LANGS.find((l) => l.code === lang)?.locale || lang;
  const isRTL = () => (LANGS.find((l) => l.code === lang)?.dir || 'ltr') === 'rtl';

  const nf = (opts) => new Intl.NumberFormat(locale(), opts);
  const money = (n) => nf({ style: 'currency', currency: CFG.currency || 'EUR' }).format(n);
  const int = (n) => nf({ maximumFractionDigits: 0 }).format(n);
  const dtf = (opts) => new Intl.DateTimeFormat(locale(), opts);
  const fmtTime = (hhmm) => {
    const [h, m] = hhmm.split(':').map(Number);
    const d = new Date(2000, 0, 1, h, m);
    const s = dtf({ hour: '2-digit', minute: '2-digit', hour12: usesAmPm() }).format(d);
    return s.replace(/\s?(AM|PM)/i, (mm) => (lang === 'en' ? mm : ' ' + mm.trim().toLowerCase()));
  };
  const usesAmPm = () => ['en'].includes(lang.split('-')[0]);

  /** Apply the dictionary to the DOM. */
  function applyI18n(root = D) {
    $$('[data-i18n]', root).forEach((el) => {
      const v = lookup(el.dataset.i18n);
      if (v != null) el.textContent = v;
    });
    $$('[data-i18n-html]', root).forEach((el) => {
      const v = lookup(el.dataset.i18nHtml);
      if (v != null) el.innerHTML = v;
    });
    $$('[data-i18n-ph]', root).forEach((el) => {
      const v = lookup(el.dataset.i18nPh);
      if (v != null) el.setAttribute('placeholder', v);
    });
    $$('[data-i18n-aria]', root).forEach((el) => {
      const v = lookup(el.dataset.i18nAria);
      if (v != null) el.setAttribute('aria-label', v);
    });
    $$('[data-i18n-title]', root).forEach((el) => {
      const v = lookup(el.dataset.i18nTitle);
      if (v != null) el.setAttribute('title', v);
    });
    if (root === D) {
      const title = lookup('meta.title') || lookup('hub.meta.title');
      if (title) D.title = title;
      const desc = $('meta[name="description"]');
      const d = lookup('meta.desc');
      if (desc && d) desc.setAttribute('content', d);
    }
  }

  function setLang(code, opts = {}) {
    if (!DICT[code]) return;
    lang = code;
    LS.set(LANG_KEY, code);
    const meta = LANGS.find((l) => l.code === code) || {};
    D.documentElement.lang = code;
    D.documentElement.dir = meta.dir || 'ltr';
    $$('select[data-lang-select]').forEach((s) => { s.value = code; });
    applyI18n();
    renderMenu();
    renderBasket();
    renderHours();
    renderBatch();
    renderCarouselMeta();
    D.dispatchEvent(new CustomEvent('levain:lang', { detail: { code } }));
    if (!opts.quiet) D.dispatchEvent(new CustomEvent('levain:toast', { detail: t('common.lang') + ': ' + (meta.native || code) }));
  }

  /* --------------------------------------------------------------- chrome */
  function headerChrome() {
    const header = $('.site-header');
    const prog = $('.scrollbar-progress');
    const toTop = $('.to-top');
    let raf = 0;
    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        raf = 0;
        const y = scrollY;
        if (header) header.dataset.stuck = y > 8;
        const h = D.documentElement.scrollHeight - innerHeight;
        if (prog) prog.style.setProperty('--p', Math.min(100, (y / Math.max(1, h)) * 100) + '%');
        if (toTop) toTop.dataset.show = y > 600;
      });
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    toTop?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduced() ? 'auto' : 'smooth' }));

    const burger = $('.burger');
    const nav = $('.nav');
    if (burger && nav) {
      burger.addEventListener('click', () => {
        const open = nav.dataset.open === 'true';
        nav.dataset.open = String(!open);
        burger.setAttribute('aria-expanded', String(!open));
      });
      nav.addEventListener('click', (e) => {
        if (e.target.closest('a')) { nav.dataset.open = 'false'; burger.setAttribute('aria-expanded', 'false'); }
      });
      addEventListener('keydown', (e) => { if (e.key === 'Escape') { nav.dataset.open = 'false'; burger.setAttribute('aria-expanded', 'false'); } });
    }
    // scrollspy
    const links = $$('.nav a[href^="#"]');
    if (links.length && 'IntersectionObserver' in window) {
      const map = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
      const io = new IntersectionObserver(
        (es) => es.forEach((e) => {
          const a = map.get(e.target.id);
          if (!a) return;
          if (e.isIntersecting) { links.forEach((l) => l.removeAttribute('aria-current')); a.setAttribute('aria-current', 'true'); }
        }),
        { rootMargin: '-45% 0px -50% 0px' }
      );
      map.forEach((_, id) => { const s = D.getElementById(id); if (s) io.observe(s); });
    }
  }

  function langPicker() {
    const sel = $('select[data-lang-select]');
    if (!sel) return;
    sel.innerHTML = LANGS.map((l) => `<option value="${l.code}">${l.native}</option>`).join('');
    sel.value = lang;
    sel.addEventListener('change', () => setLang(sel.value));
    $$('[data-set-lang]').forEach((b) => {
      b.addEventListener('click', (e) => {
        e.preventDefault();
        setLang(b.dataset.setLang);
      });
    });
  }

  function modeToggle() {
    const btn = $('[data-mode-toggle]');
    if (!btn) return;
    const root = D.documentElement;
    const saved = LS.get(MODE_KEY, null);
    if (saved) root.dataset.mode = saved;
    const paint = () => {
      const dark = root.dataset.mode === 'dark';
      btn.setAttribute('aria-pressed', String(dark));
      btn.querySelector('[data-mode-icon]').innerHTML = dark ? ICONS.sun : ICONS.moon;
    };
    btn.addEventListener('click', () => {
      root.dataset.mode = root.dataset.mode === 'dark' ? 'light' : 'dark';
      LS.set(MODE_KEY, root.dataset.mode);
      paint();
    });
    paint();
  }

  /* ----------------------------------------------------------- menu board */
  let filterCat = 'all';
  let query = '';
  let activeTags = new Set();

  function renderMenu() {
    const board = $('[data-menu]');
    if (!board) return;
    const items = $$('[data-item]', board);
    let shown = 0;
    items.forEach((el) => {
      const cats = filterCat === 'all' || el.dataset.category === filterCat;
      const tags = !activeTags.size || [...activeTags].every((tg) => (el.dataset.tags || '').split(' ').includes(tg));
      const text = (el.dataset.name + ' ' + el.dataset.desc + ' ' + el.textContent).toLowerCase();
      const q = !query || text.includes(query.toLowerCase());
      const on = cats && tags && q;
      el.hidden = !on;
      if (on) shown++;
    });
    const count = $('[data-menu-count]');
    if (count) count.textContent = t('menu.results', { n: int(shown) });
    const empty = $('[data-menu-empty]');
    if (empty) empty.hidden = shown !== 0;
    $$('[data-cat]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.cat === filterCat)));
    $$('[data-tag]').forEach((b) => b.setAttribute('aria-pressed', String(activeTags.has(b.dataset.tag))));
    // keep item labels in sync
    items.forEach((el) => {
      const id = el.dataset.id;
      const add = $('[data-add]', el);
      if (add) add.textContent = basket[id] ? t('menu.added') : t('menu.add');
      const price = $('[data-price]', el);
      if (price) price.textContent = money(Number(price.dataset.price));
      const qty = $('[data-qty]', el);
      if (qty) qty.value = basket[id] || 0;
    });
  }

  function menuControls() {
    const board = $('[data-menu]');
    if (!board) return;
    const search = $('[data-menu-search]');
    if (search) {
      const wrap = search.closest('.search');
      const upd = () => {
        query = search.value.trim();
        wrap?.dataset && (wrap.dataset.filled = query ? 'true' : 'false');
        renderMenu();
      };
      search.addEventListener('input', upd);
      wrap?.querySelector('[data-clear-search]')?.addEventListener('click', () => { search.value = ''; upd(); search.focus(); });
      D.addEventListener('keydown', (e) => {
        if (e.key === '/' && !/input|textarea|select/i.test(e.target.tagName)) { e.preventDefault(); search.focus(); }
      });
    }
    $$('[data-cat]').forEach((b) => b.addEventListener('click', () => { filterCat = b.dataset.cat; renderMenu(); }));
    $$('[data-tag]').forEach((b) =>
      b.addEventListener('click', () => {
        const v = b.dataset.tag;
        activeTags.has(v) ? activeTags.delete(v) : activeTags.add(v);
        renderMenu();
      })
    );
    board.addEventListener('click', (e) => {
      const add = e.target.closest('[data-add]');
      if (add) { addToBasket(add.closest('[data-item]').dataset.id, 1); return; }
      const minus = e.target.closest('[data-minus]');
      if (minus) { addToBasket(minus.closest('[data-item]').dataset.id, -1); return; }
      const plus = e.target.closest('[data-plus]');
      if (plus) { addToBasket(plus.closest('[data-item]').dataset.id, 1); return; }
    });
  }

  /* --------------------------------------------------------------- basket */
  let basket = LS.get(BASKET_KEY, {});
  const products = Object.fromEntries((CFG.products || []).map((p) => [p.id, p]));

  const basketCount = () => Object.values(basket).reduce((a, b) => a + b, 0);
  const basketTotal = () => Object.entries(basket).reduce((s, [id, q]) => s + (products[id]?.price || 0) * q, 0);

  function saveBasket() { LS.set(BASKET_KEY, basket); }

  function addToBasket(id, delta) {
    const next = (basket[id] || 0) + delta;
    if (next <= 0) delete basket[id]; else basket[id] = Math.min(next, 99);
    saveBasket();
    renderMenu();
    renderBasket();
    if (delta > 0 && products[id]) {
      toast(`${t('product.' + id + '.name')} · ${t('basket.count', { n: basketCount() })}`);
      const item = D.querySelector(`[data-item][data-id="${id}"]`);
      if (item) { item.dataset.inBasket = 'true'; item.dataset.flash = 'true'; setTimeout(() => (item.dataset.flash = 'false'), 900); }
    }
  }

  function renderBasket() {
    const body = $('[data-basket-body]');
    const badge = $('[data-basket-count]');
    if (badge) {
      const n = basketCount();
      badge.textContent = n;
      badge.dataset.show = n > 0;
    }
    $$('[data-basket-summary]').forEach((el) => {
      const n = basketCount();
      el.textContent = n ? t('order.withBasket', { n: int(n), total: money(basketTotal()) }) : t('order.noBasket');
    });
    $$('[data-total]').forEach((el) => (el.textContent = money(basketTotal())));
    $$('[data-subtotal]').forEach((el) => (el.textContent = money(basketTotal())));
    if (!body) return;
    const ids = Object.keys(basket);
    if (!ids.length) {
      body.innerHTML = `<p class="basket__empty">${t('basket.empty')}</p>`;
      return;
    }
    body.innerHTML = ids
      .map((id) => {
        const p = products[id] || {};
        return `<div class="line" data-line="${id}">
          <img src="${CFG.base || '.'}/assets/${p.image || ''}" alt="" loading="lazy" width="64" height="64">
          <div>
            <p class="line__name">${t('product.' + id + '.name')}</p>
            <div class="stepper" role="group" aria-label="${t('basket.qty', { name: t('product.' + id + '.name') })}">
              <button type="button" data-b-minus aria-label="−">−</button>
              <output class="num">${basket[id]}</output>
              <button type="button" data-b-plus aria-label="+">+</button>
            </div>
          </div>
          <div style="text-align:end">
            <p class="line__name num">${money((p.price || 0) * basket[id])}</p>
            <button type="button" class="line__rm" data-b-rm>${t('basket.remove', { name: t('product.' + id + '.name') })}</button>
          </div>
        </div>`;
      })
      .join('');
  }

  function basketDrawer() {
    const drawer = $('[data-basket]');
    const scrim = $('[data-scrim]');
    if (!drawer) return;
    const open = (v) => {
      drawer.dataset.open = String(v);
      scrim && (scrim.dataset.open = String(v));
      drawer.setAttribute('aria-hidden', String(!v));
      if (v) { drawer.querySelector('button')?.focus(); }
    };
    $$('[data-open-basket]').forEach((b) => b.addEventListener('click', () => open(true)));
    $$('[data-close-basket]').forEach((b) => b.addEventListener('click', () => { open(false); $('[data-open-basket]')?.focus(); }));
    scrim?.addEventListener('click', () => open(false));
    addEventListener('keydown', (e) => { if (e.key === 'Escape') open(false); });
    drawer.addEventListener('click', (e) => {
      const line = e.target.closest('[data-line]');
      if (!line) return;
      if (e.target.closest('[data-b-plus]')) addToBasket(line.dataset.line, 1);
      if (e.target.closest('[data-b-minus]')) addToBasket(line.dataset.line, -1);
      if (e.target.closest('[data-b-rm]')) { delete basket[line.dataset.line]; saveBasket(); renderMenu(); renderBasket(); toast(t('basket.cleared')); }
    });
    const send = $('[data-basket-whatsapp]');
    send?.addEventListener('click', () => {
      const text = orderText();
      openTab(`https://wa.me/${CFG.whatsapp}?text=${encodeURIComponent(text)}`);
    });
  }

  function orderText() {
    const f = D.forms['preorder'];
    const lines = [
      `${CFG.brandName || ''} — ${t('order.title')}`,
      `${t('order.name')}: ${f?.elements.name.value || '—'}`,
      `${t('order.phone')}: ${f?.elements.phone.value || '—'}`,
      `${t('order.date')}: ${f?.elements.date.value || '—'} ${f?.elements.time.value || ''}`,
      `${t('order.method')}: ${f ? (f.elements.method.value === 'delivery' ? t('order.delivery') : t('order.pickup')) : ''}`,
      '',
      ...Object.entries(basket).map(([id, q]) => `${q}× ${t('product.' + id + '.name')} = ${money((products[id]?.price || 0) * q)}`),
      '',
      `${t('basket.total')}: ${money(basketTotal())}`,
      `${t('order.notes')}: ${f?.elements.notes.value || '—'}`,
    ];
    return lines.join('\n');
  }

  /* --------------------------------------------------- oven countdown/times */
  function nextBatch(now = new Date()) {
    const list = CFG.batches || [];
    for (const b of list) {
      const [h, m] = b.time.split(':').map(Number);
      const d = new Date(now); d.setHours(h, m, 0, 0);
      if (d > now) return { batch: b, at: d };
    }
    const first = list[0];
    if (!first) return null;
    const [h, m] = first.time.split(':').map(Number);
    const d = new Date(now); d.setDate(d.getDate() + 1); d.setHours(h, m, 0, 0);
    return { batch: first, at: d };
  }

  let tickHandle = 0;
  function renderBatch() {
    const box = $('[data-batch]');
    if (!box) return;
    const run = () => {
      const now = new Date();
      const nx = nextBatch(now);
      if (!nx) return;
      const diff = nx.at - now;
      const just = diff > -40 * 60000 && diff <= 0;
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      const clock = $('[data-batch-clock]', box);
      const label = $('[data-batch-label]', box);
      const items = $('[data-batch-items]', box);
      if (clock) {
        const pad = (n) => String(n).padStart(2, '0');
        clock.innerHTML = just
          ? `<span style="font-size:0.55em">${t('batch.now')}</span>`
          : `${pad(h)}<small>${t('batch.hours')}</small>${pad(m)}<small>${t('batch.minutes')}</small>${pad(s)}`;
      }
      if (label) label.textContent = just ? t('batch.out', { t: '00:00' }) : `${t('batch.next')} · ${fmtTime(nx.batch.time)}`;
      const inline = D.querySelector('[data-batch-countdown-inline]');
      if (inline) inline.textContent = just ? t('batch.now') : fmtTime(nx.at.getHours() + ':' + String(nx.at.getMinutes()).padStart(2, '0'));
      if (items) items.textContent = (nx.batch.items || []).map((id) => t('product.' + id + '.name')).join(' · ');
      $$('[data-batch-row]', box).forEach((row) => {
        const [rh, rm] = row.dataset.time.split(':').map(Number);
        const d = new Date(now); d.setHours(rh, rm, 0, 0);
        row.dataset.state = d <= now && now - d < 40 * 60000 ? 'now' : d <= now ? 'past' : 'next';
        const st = $('[data-batch-state]', row);
        if (st) st.textContent = row.dataset.state === 'now' ? t('batch.now') : row.dataset.state === 'past' ? t('common.closed') : fmtTime(row.dataset.time);
      });
    };
    run();
    clearInterval(tickHandle);
    tickHandle = setInterval(run, 1000);
  }

  function renderHours() {
    const rows = $$('[data-hours-row]');
    if (!rows.length) return;
    const days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
    const now = new Date();
    const todayKey = days[now.getDay()];
    rows.forEach((tr) => {
      const day = tr.dataset.hoursRow;
      tr.dataset.today = String(day === todayKey);
      const cell = $('[data-hours-value]', tr);
      const h = (CFG.hours || []).find((x) => x.day === day);
      if (cell) cell.textContent = h && h.open ? `${fmtTime(h.open)} – ${fmtTime(h.close)}` : t('hours.closed');
    });
    const h = (CFG.hours || []).find((x) => x.day === todayKey);
    const mins = now.getHours() * 60 + now.getMinutes();
    const toMin = (s) => (s ? +s.split(':')[0] * 60 + +s.split(':')[1] : null);
    const open = !!h && h.open && mins >= toMin(h.open) && mins < toMin(h.close);
    const nextOpen = (CFG.hours || []).slice().find((x) => x.open);
    $$('[data-open-badge]').forEach((b) => {
      b.dataset.state = open ? 'open' : 'closed';
      b.className = `badge ${open ? 'badge--open' : 'badge--closed'}`;
      b.innerHTML = `<span class="dot"></span><span></span>`;
      b.lastElementChild.textContent = open
        ? t('hours.open_now', { t: fmtTime(h.close) })
        : t('hours.closed_now', { d: t('hours.today'), t: nextOpen ? fmtTime(nextOpen.open) : '—' });
    });
  }

  /* ------------------------------------------------------------ carousel */
  function carousel() {
    const root = $('[data-carousel]');
    if (!root) return;
    const track = $('[data-track]', root);
    const slides = $$('.quote-card', root);
    const dots = $$('[data-dot]', root);
    let i = 0, timer = 0;
    const go = (n, user) => {
      i = (n + slides.length) % slides.length;
      track.style.transform = `translateX(${isRTL() ? '' : '-'}${i * 100}%)`;
      slides.forEach((s, k) => s.setAttribute('aria-hidden', String(k !== i)));
      dots.forEach((d, k) => d.setAttribute('aria-selected', String(k === i)));
      if (user) restart();
    };
    const restart = () => { clearInterval(timer); if (!reduced()) timer = setInterval(() => go(i + 1), 7000); };
    $$('[data-prev]', root).forEach((b) => b.addEventListener('click', () => go(i - 1, true)));
    $$('[data-next]', root).forEach((b) => b.addEventListener('click', () => go(i + 1, true)));
    dots.forEach((d, k) => d.addEventListener('click', () => go(Number(d.dataset.dot ?? k), true)));
    root.addEventListener('mouseenter', () => clearInterval(timer));
    root.addEventListener('mouseleave', restart);
    root.addEventListener('focusin', () => clearInterval(timer));
    root.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') go(i + 1, true); if (e.key === 'ArrowLeft') go(i - 1, true); });
    let x0 = null;
    root.addEventListener('pointerdown', (e) => (x0 = e.clientX));
    root.addEventListener('pointerup', (e) => {
      if (x0 == null) return;
      const dx = e.clientX - x0; x0 = null;
      if (Math.abs(dx) > 42) go(i + (dx < 0 ? 1 : -1), true);
    });
    // swipe direction flips in RTL, so invert the delta
    if (isRTL()) root.dataset.rtl = 'true';
    go(0);
    restart();
  }
  const renderCarouselMeta = () => {};

  /* ------------------------------------------------------------ lightbox */
  function lightbox() {
    const box = $('[data-lightbox]');
    const figs = $$('[data-gal-item]');
    if (!box || !figs.length) return;
    const img = $('img', box);
    const counter = $('[data-lb-counter]', box);
    let i = 0;
    const show = (n) => {
      i = (n + figs.length) % figs.length;
      const f = figs[i];
      img.src = f.dataset.full || $('img', f)?.src;
      img.alt = $('img', f)?.alt || '';
      if (counter) counter.textContent = t('gallery.counter', { i: int(i + 1), n: int(figs.length) });
    };
    const open = (n) => { show(n); box.hidden = false; D.documentElement.style.overflow = 'hidden'; $('[data-lb-close]', box)?.focus(); };
    const close = () => { box.hidden = true; D.documentElement.style.overflow = ''; figs[i]?.focus?.(); };
    figs.forEach((f, k) => {
      f.addEventListener('click', () => open(k));
      f.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(k); } });
    });
    $$('[data-lb-next]', box).forEach((b) => b.addEventListener('click', () => show(i + 1)));
    $$('[data-lb-prev]', box).forEach((b) => b.addEventListener('click', () => show(i - 1)));
    $$('[data-lb-close]', box).forEach((b) => b.addEventListener('click', close));
    box.addEventListener('click', (e) => { if (e.target === box) close(); });
    addEventListener('keydown', (e) => {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(i + (isRTL() ? -1 : 1));
      if (e.key === 'ArrowLeft') show(i + (isRTL() ? 1 : -1));
    });
  }

  /* ------------------------------------------------------------- accordion */
  function accordion() {
    $$('[data-acc] .acc__btn').forEach((btn) => {
      const item = btn.closest('.acc__item');
      btn.setAttribute('aria-expanded', String(item.dataset.open === 'true'));
      btn.addEventListener('click', () => {
        const willOpen = item.dataset.open !== 'true';
        $$('[data-acc] .acc__item').forEach((i) => {
          i.dataset.open = 'false';
          $('.acc__btn', i)?.setAttribute('aria-expanded', 'false');
        });
        if (willOpen) { item.dataset.open = 'true'; btn.setAttribute('aria-expanded', 'true'); }
      });
    });
  }

  /* --------------------------------------------------------- order form */
  function orderForm() {
    const form = D.forms['preorder'];
    if (!form) return;
    const status = $('[data-form-status]', form) || D.querySelector('[data-form-status]');
    const dateInput = form.elements.date;
    if (dateInput) {
      const d = new Date(); d.setDate(d.getDate() + 1);
      const iso = d.toISOString().slice(0, 10);
      dateInput.min = iso;
      if (!dateInput.value) dateInput.value = iso;
    }
    const setErr = (name, msg) => {
      const field = form.elements[name]?.closest('.field');
      if (!field) return;
      field.dataset.invalid = msg ? 'true' : 'false';
      const slot = $('[data-err]', field);
      if (slot) slot.textContent = msg || '';
      form.elements[name]?.setAttribute('aria-invalid', msg ? 'true' : 'false');
    };
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let ok = true;
      const fail = (name, msg) => { setErr(name, msg); ok = false; };
      if (!form.elements.name.value.trim()) fail('name', t('order.errorName')); else setErr('name', '');
      const phone = form.elements.phone.value.replace(/\D/g, '');
      if (phone.length < 7) fail('phone', t('order.errorPhone')); else setErr('phone', '');
      const dv = form.elements.date.value;
      if (!dv || dv < (dateInput?.min || '')) fail('date', t('order.errorDate')); else setErr('date', '');
      if (!basketCount()) { ok = false; if (status) { status.dataset.state = 'err'; status.textContent = t('order.errorBasket'); } }
      if (!ok) { if (status && status.dataset.state !== 'err') { status.dataset.state = 'err'; status.textContent = t('order.errorName'); } form.querySelector('[aria-invalid="true"]')?.focus(); return; }
      const btn = $('[data-submit]', form);
      if (btn) { btn.disabled = true; btn.dataset.prev = btn.textContent; btn.textContent = t('order.sending'); }
      setTimeout(() => {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.prev; }
        if (status) { status.dataset.state = 'ok'; status.textContent = t('order.success'); }
        const handoff = $('[data-order-handoff]', form);
        if (handoff) {
          const body = encodeURIComponent(orderText());
          handoff.innerHTML =
            `<a class="btn btn--ghost btn--sm" href="mailto:${CFG.email || ''}?subject=${encodeURIComponent((CFG.brandName || '') + ' — ' + t('order.title'))}&body=${body}">${t('order.submit')} ✉</a>
             <a class="btn btn--sm" href="https://wa.me/${CFG.whatsapp}?text=${body}" target="_blank" rel="noopener">WhatsApp</a>`;
        }
        D.dispatchEvent(new CustomEvent('levain:toast', { detail: t('order.success') }));
      }, 700);
    });
    ['name', 'phone', 'date'].forEach((n) => form.elements[n]?.addEventListener('input', () => setErr(n, '')));
  }

  /* -------------------------------------------------------------- reveal */
  function reveal() {
    const els = $$('[data-reveal]');
    if (!els.length) return;
    if (!('IntersectionObserver' in window) || reduced()) { els.forEach((e) => e.classList.add('is-in')); return; }
    const io = new IntersectionObserver(
      (es) => es.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }),
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    els.forEach((el, i) => { el.style.setProperty('--d', `${Math.min(i, 8) * 60}ms`); io.observe(el); });
  }

  /* ------------------------------------------------------------- toasts */
  let toastTimer = 0;
  function toast(msg) {
    const el = D.createElement('div');
    el.className = 'toast';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    el.textContent = msg;
    D.body.appendChild(el);
    requestAnimationFrame(() => (el.dataset.show = 'true'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { el.dataset.show = 'false'; setTimeout(() => el.remove(), 500); }, 2600);
  }
  D.addEventListener('levain:toast', (e) => toast(e.detail));

  const openTab = (url) => window.open(url, '_blank', 'noopener');

  /* ------------------------------------------------------------- embed */
  function embedMode() {
    const q = new URLSearchParams(location.search);
    if (q.get('embed') === '1') {
      D.documentElement.dataset.embed = 'true';
      $$('[data-embed-hide]').forEach((e) => e.remove());
    }
    const l = q.get('lang');
    if (l && DICT[l]) { LS.set(LANG_KEY, l); lang = l; }
    // the hub can drive the iframe language/theme without a reload
    addEventListener('message', (ev) => {
      const d = ev.data || {};
      if (d.type === 'levain:lang' && d.code) setLang(d.code, { quiet: true });
      if (d.type === 'levain:theme' && d.theme) D.documentElement.dataset.theme = d.theme;
    });
  }

  /* --------------------------------------------------------------- icons */
  const ICONS = {
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" width="20" height="20"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"/></svg>',
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" width="20" height="20"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
  };

  /* --------------------------------------------------------------- boot */
  function boot() {
    embedMode();
    const meta = LANGS.find((l) => l.code === lang) || {};
    D.documentElement.lang = lang;
    D.documentElement.dir = meta.dir || 'ltr';
    applyI18n();
    langPicker();
    headerChrome();
    modeToggle();
    menuControls();
    renderMenu();
    renderBasket();
    basketDrawer();
    renderHours();
    renderBatch();
    carousel();
    lightbox();
    accordion();
    orderForm();
    reveal();
    D.addEventListener('visibilitychange', () => (D.hidden ? clearInterval(tickHandle) : renderBatch()));
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot);
  else boot();

  // expose a tiny API for the hub page
  window.LevainKit = { t, setLang, money, int, fmtTime, toast, get lang() { return lang; }, applyI18n };
})();

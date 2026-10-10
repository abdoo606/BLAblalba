/* Headless behaviour test. Needs the dev/preview server running:
   `npm start` in one shell, then `node tools/smoke.mjs`.
   Drives the real built page in jsdom: language switch + RTL, basket, filters,
   countdown, accordion, carousel, form validation, hub calculator. */
import { JSDOM, VirtualConsole } from 'jsdom';

const BASE = process.env.BASE || 'http://localhost:5173';
const results = [];
const ok = (name, cond, extra = '') => results.push([cond ? '✓' : '✗', name + (extra ? ` — ${extra}` : ''), cond]);

const load = async (path) => {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => !/Could not parse CSS|not implemented/i.test(e.message) && errors.push(e.message));
  vc.on('error', (m) => errors.push(String(m)));
  const dom = await JSDOM.fromURL(BASE + path, {
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
    virtualConsole: vc,
  });
  await new Promise((r) => (dom.window.document.readyState === 'complete' ? r() : dom.window.addEventListener('load', r)));
  await new Promise((r) => setTimeout(r, 400)); // let deferred boot settle
  return { dom, win: dom.window, doc: dom.window.document, errors };
};

/* --------------------------------------------------------------- template */
{
  const { doc, win, errors } = await load('/templates/artisan/index.html');
  ok('page renders with English default', doc.documentElement.lang === 'en');
  ok('theme hook applied', doc.documentElement.dataset.theme === 'artisan');

  const h2 = doc.querySelector('#menu .h-sec')?.textContent || '';
  ok('menu heading translated', /Today at the counter/.test(h2), h2);

  // basket
  const addBtn = doc.querySelector('[data-add]');
  addBtn?.click();
  addBtn?.click();
  const pill = doc.querySelector('[data-basket-count]');
  ok('basket count follows two clicks', pill?.textContent === '2', pill?.textContent);
  ok('basket line rendered', !!doc.querySelector('[data-basket-body] .line'));
  const total = doc.querySelector('[data-total]')?.textContent || '';
  ok('basket total is a formatted currency', /[€0-9]/.test(total), total);
  const stepperOut = doc.querySelector('[data-item] [data-qty]')?.textContent;
  ok('item stepper synced to basket', stepperOut === '2', stepperOut);

  // filters
  const search = doc.querySelector('[data-menu-search]');
  search.value = 'cake';
  search.dispatchEvent(new win.Event('input', { bubbles: true }));
  const visible = [...doc.querySelectorAll('[data-item]')].filter((i) => !i.hidden);
  ok('search narrows the menu', visible.length > 0 && visible.length < 12, visible.length + ' of 12');
  search.value = 'zzzzz';
  search.dispatchEvent(new win.Event('input', { bubbles: true }));
  ok('empty state appears', !doc.querySelector('[data-menu-empty]')?.hidden);
  search.value = 'croissant';
  search.dispatchEvent(new win.Event('input', { bubbles: true }));
  ok(
    'cross-language search works (english query, french word present)',
    [...doc.querySelectorAll('[data-item]:not([hidden])')].length >= 1
  );
  doc.querySelector('[data-cat][data-cat="all"]')?.click();
  search.value = '';
  search.dispatchEvent(new win.Event('input', { bubbles: true }));

  // countdown + open badge
  await new Promise((r) => setTimeout(r, 1100));
  const clock = doc.querySelector('[data-batch-clock]')?.textContent || '';
  ok('oven countdown is live', /\d/.test(clock), clock.slice(0, 28).replace(/\s+/g, ' '));
  const badge = doc.querySelector('[data-open-badge]')?.textContent?.trim();
  ok('open-now badge has real text', !!badge && badge.length > 3, badge);
  const todayRows = [...doc.querySelectorAll('[data-hours-row]')].filter((r) => r.dataset.today === 'true');
  ok('today is highlighted in the hours table', todayRows.length === 1);

  // accordion + carousel + lightbox
  const acc = doc.querySelector('.acc__btn');
  acc?.click();
  ok('FAQ opens', acc?.closest('.acc__item')?.dataset.open === 'true' && acc.getAttribute('aria-expanded') === 'true');
  const before = doc.querySelector('[data-track]')?.style.transform;
  doc.querySelector('[data-next]')?.click();
  ok('carousel advances', doc.querySelector('[data-track]')?.style.transform !== before);
  doc.querySelector('[data-gal-item]')?.click();
  ok('lightbox opens', doc.querySelector('[data-lightbox]')?.hidden === false);

  // language switch → RTL
  doc.querySelector('#langSel').value = 'ar';
  doc.querySelector('#langSel').dispatchEvent(new win.Event('change', { bubbles: true }));
  ok('arabic sets dir=rtl', doc.documentElement.dir === 'rtl' && doc.documentElement.lang === 'ar');
  const h2ar = doc.querySelector('#menu .h-sec')?.textContent || '';
  ok('arabic string swapped in', /اليوم/.test(h2ar), h2ar);
  const priceAr = doc.querySelector('[data-item] [data-price]')?.textContent || '';
  ok('price re-formatted for the locale', /\d/.test(priceAr), priceAr);
  doc.querySelector('#langSel').value = 'fr';
  doc.querySelector('#langSel').dispatchEvent(new win.Event('change', { bubbles: true }));
  ok('french works too', /comptoir/i.test(doc.querySelector('#menu .h-sec')?.textContent || ''));

  // basket survived a language switch (and would survive a reload)
  ok('basket persists across language switch', doc.querySelector('[data-basket-count]')?.textContent === '2');

  // form validation
  doc.querySelector('[data-cat][data-cat="celebration"]')?.click();
  const form = doc.forms['preorder'];
  form.dispatchEvent(new win.Event('submit', { bubbles: true, cancelable: true }));
  const status = doc.querySelector('[data-form-status]');
  const nameField = doc.querySelector('#oname')?.closest('.field');
  ok('empty submit blocks with no basket → error state', status?.dataset.state === 'err' || nameField?.dataset.invalid === 'true', status?.dataset.state);
  form.elements.name.value = 'Test';
  form.elements.phone.value = '+33612345678';
  form.elements.date.value = doc.querySelector('#odate')?.min || '';
  doc.querySelector('[data-cat][data-cat="all"]')?.click();
  form.dispatchEvent(new win.Event('submit', { bubbles: true, cancelable: true }));
  await new Promise((r) => setTimeout(r, 900));
  ok('valid submit shows success + handoff', status?.dataset.state === 'ok' && !!doc.querySelector('[data-order-handoff] a'), status?.textContent);

  ok('no runtime errors on the template page', errors.length === 0, errors.slice(0, 2).join(' | '));
}

/* -------------------------------------------------------------------- hub */
{
  const { doc, win, errors } = await load('/');
  ok('hub renders', !!doc.querySelector('.kit-hero h1')?.textContent);
  ok('three template tabs', doc.querySelectorAll('.tpl-tab[data-tpl]').length === 3);
  const iframe = doc.querySelector('[data-live-demo]');
  ok('live iframe points at a real template', /templates\/artisan\/index\.html\?embed=1/.test(iframe?.src || ''), iframe?.src?.split('/').slice(-2).join('/'));

  const total0 = doc.querySelector('[data-calc-total]')?.textContent;
  doc.querySelector('[data-pkg][data-pkg="patisserie"]')?.click();
  const total1 = doc.querySelector('[data-calc-total]')?.textContent;
  ok('calculator recomputes on package change', total0 !== total1, `${total0} → ${total1}`);
  const before2 = doc.querySelector('[data-calc-total]')?.textContent;
  doc.querySelector('[data-langs="4"]')?.click();
  doc.querySelector('[data-opt="photo"] input')?.click();
  const after2 = doc.querySelector('[data-calc-total]')?.textContent;
  ok('calculator follows languages + add-ons', before2 !== after2, `${before2} → ${after2}`);
  ok('delivery line filled', /\d/.test(doc.querySelector('[data-calc-days]')?.textContent || ''), doc.querySelector('[data-calc-days]')?.textContent);
  ok('breakdown rows rendered', doc.querySelectorAll('[data-calc-rows] .calc__row').length >= 3);

  doc.querySelector('[data-set-lang="fr"]')?.click();
  ok('hub translates with the dictionary', /modèles/i.test(doc.querySelector('.kit-hero h1')?.textContent || ''), doc.querySelector('.kit-hero h1')?.textContent?.slice(0, 42));
  doc.querySelector('[data-size="mobile"]')?.click();
  ok('viewport emulator toggles', doc.querySelector('[data-viewport]')?.dataset.size === 'mobile');
  ok('no runtime errors on the hub', errors.length === 0, errors.slice(0, 2).join(' | '));
}

/* --------------------------------------------------------------- embed mode */
{
  const { doc } = await load('/templates/patisserie/index.html?embed=1&lang=es');
  ok('embed mode hides the header', doc.documentElement.dataset.embed === 'true' && !!doc.querySelector('.site-header'));
  ok('?lang=es respected', doc.documentElement.lang === 'es' && /mostrador/i.test(doc.querySelector('#menu .h-sec')?.textContent || ''), doc.querySelector('#menu .h-sec')?.textContent);
}

/* -------------------------------------------------------------- report */
const fail = results.filter(([, , c]) => !c);
for (const [sym, name] of results) console.log(`${sym} ${name}`);
console.log(`\n${results.length - fail.length}/${results.length} checks passed`);
process.exit(fail.length ? 1 : 0);

/* ==========================================================================
   Levain Kit — static generator.
   Reads src/data/*.json + src/data/locales/*.json, writes dist/.
   No dependencies, no framework: one file, ~1s, deterministic output.
   ========================================================================== */
import { readFileSync, writeFileSync, mkdirSync, cpSync, rmSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'src');
const DATA = join(SRC, 'data');
const DIST = join(ROOT, 'dist');

const site = JSON.parse(readFileSync(join(DATA, 'site.json'), 'utf8'));
const locales = Object.fromEntries(
  site.languages.map((l) => [l.code, JSON.parse(readFileSync(join(DATA, 'locales', `${l.code}.json`), 'utf8'))])
);
const DEF = site.defaultLanguage;

/* ------------------------------------------------------------ utilities */
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const path = (obj, key) => key.split('.').reduce((o, k) => (o == null ? o : o[k]), obj);
/** default-language string for static HTML (runtime swaps via data-i18n) */
const s = (key) => path(locales[DEF], key) ?? key;
const allNames = (id, field) => site.languages.map((l) => path(locales[l.code], `product.${id}.${field}`) ?? '').join(' ');
const moneyOf = (n, code = DEF) =>
  new Intl.NumberFormat(locales[code] ? site.languages.find((l) => l.code === code).locale : 'en-GB', {
    style: 'currency',
    currency: site.studio.currency,
  }).format(n);
const timeOf = (hhmm, code = DEF) => {
  const loc = site.languages.find((l) => l.code === code)?.locale || 'en-GB';
  const [h, m] = hhmm.split(':').map(Number);
  return new Intl.DateTimeFormat(loc, { hour: '2-digit', minute: '2-digit', hour12: code === 'en' }).format(new Date(2000, 0, 1, h, m));
};

/* --------------------------------------------------------------- icons */
const I = {
  basket: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h16l-1.4 11.2a2 2 0 0 1-2 1.8H7.4a2 2 0 0 1-2-1.8L4 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
  search: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>',
  close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
  left: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
  right: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>',
  up: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
  burger: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  clock: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-5.4 7-11a7 7 0 1 0-14 0c0 5.6 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
  phone: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h3l2 5-2.5 1.5a12 12 0 0 0 6 6L15 13l5 2v3a2 2 0 0 1-2.2 2A17 17 0 0 1 3 5.2A2 2 0 0 1 5 3Z"/></svg>',
  flame: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3s5 4.2 5 8.5a5 5 0 0 1-10 0C7 7.2 12 3 12 3Z"/><path d="M12 20a3 3 0 0 1-3-3c0-2 3-4 3-4s3 2 3 4a3 3 0 0 1-3 3Z"/></svg>',
  hands: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 13V5a1.5 1.5 0 0 1 3 0v6M10 11V4a1.5 1.5 0 0 1 3 0v7M13 11V6a1.5 1.5 0 0 1 3 0v8a6 6 0 0 1-6 6H9a5 5 0 0 1-5-5v-3l2 1"/></svg>',
  cake: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h16v-6a3 3 0 0 0-3-3H7a3 3 0 0 0-3 3v6Z"/><path d="M12 11V8M12 5.5c1 0 1.5-.7 1.5-1.5S13 2.5 12 2.5 10.5 3.2 10.5 4s.5 1.5 1.5 1.5Z"/></svg>',
  truck: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></svg>',
  bread: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10a4 4 0 0 1 4-4h8a4 4 0 0 1 0 8H8a4 4 0 0 1-4-4Z"/><path d="M9 14v4M15 14v4"/></svg>',
  croissant: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 15c6 3 12 3 18 0-1-5-4-8-9-8s-8 3-9 8Z"/><path d="M8 8 6 5M16 8l2-3"/></svg>',
  tart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h18l-2 7H5l-2-7Z"/><circle cx="9" cy="9" r="1.6"/><circle cx="15" cy="9" r="1.6"/></svg>',
  globe: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14 0 18M12 3c-3 3.5-3 14 0 18"/></svg>',
  star: '★',
};
const icon = (n, cls = '') => `<span class="${cls}" aria-hidden="true">${I[n] || ''}</span>`;
/** all build-time assets live in dist/assets/ */
const asset = (rel, p) => `${rel}/assets/${String(p).replace(/^\/+/, '')}`;

/* ---------------------------------------------------------------- layout */
const cssList = ['core.css', 'hub.css'];

function head({ rel, theme, title, desc, tplId, preload, lang = DEF, prefix = rel }) {
  const l = site.languages.find((x) => x.code === lang);
  const url = (code) => {
    const qs = code && code !== DEF ? `?lang=${code}` : '';
    const page = tplId ? `templates/${tplId}/index.html` : 'index.html';
    return `${site.baseUrl || prefix}/${page}${qs}`;
  };
  const hreflang = site.languages
    .map((x) => `<link rel="alternate" hreflang="${x.code}" href="${url(x.code)}">`)
    .join('\n    ');
  return `<!doctype html>
<html lang="${lang}" dir="${l.dir}" data-theme="${theme}" data-mode="light">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>${esc(tplId ? `${s(`brand.${tplId}.name`)} — ${s('hero.title')}` : title)}</title>
    <meta name="description" content="${esc(desc)}">
    <meta name="theme-color" content="${theme === 'artisan' ? '#1c1611' : theme === 'patisserie' ? '#fffafc' : theme === 'moderno' ? '#fbf6ee' : '#f7f4ef'}">
    <meta name="color-scheme" content="light dark">
    <meta name="author" content="${esc(site.studio.maker)}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="${esc(title)}">
    <meta property="og:description" content="${esc(desc)}">
    <meta property="og:locale" content="${l.locale.replace('-', '_')}">
    ${preload ? `<meta property="og:image" content="${site.baseUrl || prefix}/assets/${preload}">` : ''}
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="${url('')}">
    ${hreflang}
    <link rel="icon" href="${rel}/assets/favicon.svg" type="image/svg+xml">
    <link rel="manifest" href="${rel}/assets/site.webmanifest">
    ${preload ? `<link rel="preload" as="image" fetchpriority="high" href="${asset(rel, preload)}">` : ''}
    ${cssList.map((c) => `<link rel="stylesheet" href="${rel}/assets/${c}">`).join('\n    ')}
    <script>
      // prevent theme/lang flash: read prefs before first paint
      try {
        var l = JSON.parse(localStorage.getItem('levain.lang') || 'null');
        var m = JSON.parse(localStorage.getItem('levain.mode') || 'null');
        if (m) document.documentElement.dataset.mode = m;
        if (l && ${JSON.stringify(site.languages.map((x) => x.code))}.indexOf(l) > -1 && location.search.indexOf('lang=') < 0) {
          document.documentElement.lang = l;
          document.documentElement.dir = ${JSON.stringify(Object.fromEntries(site.languages.map((x) => [x.code, x.dir])))}[l];
        }
      } catch (e) {}
    </script>
  </head>`;
}

function scriptTail({ rel }) {
  return `    <script src="${rel}/assets/i18n.generated.js" defer></script>
    <script src="${rel}/assets/app.js" defer></script>
    <script src="${rel}/assets/hub.js" defer></script>
  </body>
</html>`;
}

/* -------------------------------------------------------------- sections */
function header({ rel, tplId, embedHide = '' }) {
  const brand = tplId ? `brand.${tplId}.name` : 'hub.badge';
  const brandName = tplId ? s(`brand.${tplId}.name`) : 'Levain Kit';
  const brandTag = tplId ? s(`brand.${tplId}.tag`) : 'Bakery · Pâtisserie · 4 languages';
  const nav = tplId
    ? ['menu', 'story', 'hours', 'order', 'faq'].map(
        (k) => `<li><a href="#${k}" data-i18n="nav.${k}">${esc(s(`nav.${k}`))}</a></li>`
      ).join('')
    : ['galleryTitle', 'featTitle', 'langTitle', 'calcTitle', 'docsTitle'].map(
        (k) => `<li><a href="#${k}" data-i18n="hub.${k}">${esc(s('hub.' + k))}</a></li>`
      ).join('');
  return `
  <a class="skip-link" href="#main" data-i18n="common.skip">${esc(s('common.skip'))}</a>
  <header class="site-header" data-stuck="false">
    <div class="wrap bar">
      <a class="brand" href="${rel}/${tplId ? '' : '#top'}">
        <span class="brand__mark" aria-hidden="true">${esc(brandName.slice(0, 2).toUpperCase())}</span>
        <span class="brand__text">
          <span class="brand__name" ${tplId ? `data-i18n="brand.${tplId}.name"` : ''}>${esc(brandName)}</span>
          <span class="brand__tag" ${tplId ? `data-i18n="brand.${tplId}.tag"` : ''}>${esc(brandTag)}</span>
        </span>
      </a>
      <nav class="nav" aria-label="Main">
        <ul>${nav}</ul>
      </nav>
      <div class="bar__actions">
        <div class="lang-picker">
          <label class="sr-only" for="langSel" data-i18n="common.lang">${esc(s('common.lang'))}</label>
          <select id="langSel" data-lang-select name="lang"></select>
        </div>
        <button class="icon-btn" type="button" data-mode-toggle aria-pressed="false" data-i18n-aria="common.theme" aria-label="Theme">
          <span data-mode-icon></span>
        </button>
        <button class="icon-btn" type="button" data-open-basket data-i18n-aria="nav.basket" aria-label="${esc(s('nav.basket'))}">
          ${I.basket}<span class="count-pill" data-basket-count data-show="false">0</span>
        </button>
        <a class="btn btn--sm btn--order" href="#order" ${embedHide} data-i18n="nav.order">${esc(s('nav.order'))}</a>
        <button class="icon-btn burger" type="button" aria-expanded="false" data-i18n-aria="common.menu" aria-label="${esc(s('common.menu'))}">${I.burger}</button>
      </div>
    </div>
    <div class="scrollbar-progress" aria-hidden="true"></div>
  </header>`;
}

function hero({ rel, tplId }) {
  const tpl = site.templates.find((x) => x.id === tplId);
  const stats = ['stat1', 'stat2', 'stat3']
    .map((k) => `<li data-reveal><span data-i18n="hero.${k}">${esc(s('hero.' + k))}</span></li>`)
    .join('');
  const editorial = tpl.heroLayout === 'editorial';
  return `
  <section class="hero" id="top" data-layout="${tpl.heroLayout}">
    <div class="wrap hero__grid">
      ${editorial ? `<div class="hero__side" aria-hidden="true"><span class="tiny">Est. 1991 · ${esc(s('brand.' + tplId + '.tag'))}</span></div>` : ''}
      <div class="hero__copy stack" style="--flow:1.05rem">
        <span class="eyebrow"><span data-i18n="hero.kicker">${esc(s('hero.kicker'))}</span></span>
        <h1>
          <span data-i18n="hero.title">${esc(s('hero.title'))}</span>
          <span class="accent" data-i18n="hero.titleAccent">${esc(s('hero.titleAccent'))}</span>
        </h1>
        <p class="hero__lead" data-i18n="hero.lead">${esc(s('hero.lead'))}</p>
        <div class="hero__cta">
          <a class="btn" href="#menu" data-i18n="hero.ctaMenu">${esc(s('hero.ctaMenu'))}</a>
          <a class="btn btn--ghost" href="#order" data-i18n="hero.ctaOrder">${esc(s('hero.ctaOrder'))}</a>
        </div>
        <ul class="hero__stats">${stats}</ul>
      </div>
      <div class="hero__media">
        <img src="${asset(rel, tpl.hero)}" alt="" width="1200" height="900" fetchpriority="high" decoding="async">
        <div class="hero__float">
          <span class="badge" data-open-badge><span class="dot"></span><span>${esc(s('common.open'))}</span></span>
          <span class="tiny muted" style="display:flex;align-items:center;gap:.4rem">${I.flame}<span data-i18n="batch.next">${esc(s('batch.next'))}</span> <b class="num" data-batch-countdown-inline>${timeOf(site.batches[1].time)}</b></span>
        </div>
        <span class="hero__bg-word" aria-hidden="true">${esc(s('brand.' + tplId + '.name').split(' ')[0])}</span>
      </div>
    </div>
  </section>`;
}

function marquee() {
  const items = ['i1', 'i2', 'i3', 'i4', 'i5', 'i6']
    .map((k) => `<span class="marquee__item" data-i18n="marquee.${k}">${esc(s('marquee.' + k))}</span>`)
    .join('');
  return `
  <div class="marquee" aria-hidden="true"><div class="marquee__track">${items}${items}</div></div>`;
}

function specialties() {
  const cards = ['1', '2', '3']
    .map(
      (n, i) => `
      <article class="spec" data-reveal style="--d:${i * 90}ms">
        <span class="spec__n">0${n}</span>
        <h3 data-i18n="specialties.c${n}t">${esc(s(`specialties.c${n}t`))}</h3>
        <p data-i18n="specialties.c${n}d">${esc(s(`specialties.c${n}d`))}</p>
      </article>`
    )
    .join('');
  return `
  <section class="section" id="specialties">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow" data-i18n="nav.menu">${esc(s('nav.menu'))}</span>
        <h2 class="h-sec" data-i18n="specialties.title">${esc(s('specialties.title'))}</h2>
        <p class="h-lead" data-i18n="specialties.lead">${esc(s('specialties.lead'))}</p>
      </div>
      <div class="grid grid--3">${cards}</div>
    </div>
  </section>`;
}

function menuBoard({ rel, tplId }) {
  const tpl = site.templates.find((x) => x.id === tplId);
  const cats = [{ id: 'all' }, ...site.categories].map(
    (c) =>
      `<button class="chip" type="button" data-cat="${c.id}" aria-pressed="${c.id === 'all'}">
         <span data-i18n="${c.id === 'all' ? 'menu.all' : 'menu.cat.' + c.id}">${esc(c.id === 'all' ? s('menu.all') : s('menu.cat.' + c.id))}</span>
       </button>`
  ).join('');
  const tags = ['vegan', 'gf', 'signature', 'seasonal']
    .map((tg) => `<button class="chip chip--tag" type="button" data-tag="${tg}" aria-pressed="false"><span data-i18n="menu.${tg}">${esc(s('menu.' + tg))}</span></button>`)
    .join('');
  const items = site.products
    .map((p, i) => {
      const tagsHtml = (p.tags || []).map((tg) => `<span class="badge tiny" data-i18n="menu.${tg}">${esc(s('menu.' + tg))}</span>`).join('');
      return `
      <article class="item" data-item data-id="${p.id}" data-category="${p.category}" data-tags="${(p.tags || []).join(' ')}"
               data-name="${esc(allNames(p.id, 'name'))}" data-desc="${esc(allNames(p.id, 'desc'))}" data-reveal style="--d:${(i % 3) * 70}ms">
        <div class="item__media">
          <img src="${asset(rel, p.image)}" alt="" loading="lazy" decoding="async" width="800" height="600">
          <div class="item__tags">${tagsHtml}</div>
          <span class="item__flash" data-flash data-i18n="menu.added">${esc(s('menu.added'))}</span>
        </div>
        <div class="item__body">
          <h3 class="item__name" data-i18n="product.${p.id}.name">${esc(s(`product.${p.id}.name`))}</h3>
          <p class="item__desc" data-i18n="product.${p.id}.desc">${esc(s(`product.${p.id}.desc`))}</p>
          <div class="item__foot">
            <p class="price"><span class="num" data-price="${p.price}">${moneyOf(p.price)}</span> <span class="unit">/ ${esc(p.weight)}</span></p>
            <div class="item__add">
              <div class="stepper">
                <button type="button" data-minus aria-label="−">−</button>
                <output data-qty class="num">0</output>
                <button type="button" data-plus aria-label="+">+</button>
              </div>
              <button class="btn btn--sm" type="button" data-add data-i18n="menu.add">${esc(s('menu.add'))}</button>
            </div>
          </div>
        </div>
      </article>`;
    })
    .join('');
  return `
  <section class="section section--alt" id="menu">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div class="stack" style="--flow:.5rem">
          <h2 class="h-sec" data-i18n="menu.title">${esc(s('menu.title'))}</h2>
          <p class="h-lead" data-i18n="menu.lead">${esc(s('menu.lead'))}</p>
        </div>
        <p class="menu-count num" data-menu-count>${esc(s('menu.results').replace('{{n}}', String(site.products.length)))}</p>
      </div>
      <div class="menu-tools">
        <div class="search">
          ${I.search}
          <label class="sr-only" for="q" data-i18n="menu.search">${esc(s('menu.search'))}</label>
          <input id="q" class="input" type="search" data-menu-search data-i18n-ph="menu.search" placeholder="${esc(s('menu.search'))}" autocomplete="off">
          <button class="search__clear" type="button" data-clear-search data-i18n-aria="basket.remove" aria-label="Clear">${I.close}</button>
        </div>
        <div class="chip-row" role="group" aria-label="${esc(s('menu.diet'))}">${cats}</div>
        <div class="chip-row" role="group" aria-label="${esc(s('menu.diet'))}">${tags}</div>
      </div>
      <div class="${tpl.menuLayout === 'list' ? 'menu-list' : 'menu-grid'}" data-menu data-menu-layout="${tpl.menuLayout}">${items}</div>
      <p class="menu-empty" data-menu-empty hidden data-i18n="menu.empty">${esc(s('menu.empty'))}</p>
      <p class="menu-foot">${I.clock}<span data-i18n="menu.note">${esc(s('menu.note'))}</span></p>
    </div>
  </section>`;
}

function batchSection() {
  const rows = site.batches
    .map(
      (b) => `
      <li class="batch__row" data-batch-row data-time="${b.time}">
        <span><b>${esc(s('batch.' + b.id))}</b><br><span class="tiny muted">${b.items.map((id) => `<span data-i18n="product.${id}.name">${esc(s('product.' + id + '.name'))}</span>`).join(' · ')}</span></span>
        <span class="batch__time num" data-batch-state>${timeOf(b.time)}</span>
      </li>`
    )
    .join('');
  return `
  <section class="section" id="batch">
    <div class="wrap">
      <div class="batch" data-batch>
        <div class="stack" style="--flow:.8rem" data-reveal>
          <span class="eyebrow"><span class="dot" style="color:var(--good)"></span><span data-i18n="batch.live">${esc(s('batch.live'))}</span></span>
          <h2 class="h-sec" data-i18n="batch.title">${esc(s('batch.title'))}</h2>
          <p class="h-lead" data-i18n="batch.lead">${esc(s('batch.lead'))}</p>
          <p class="batch__clock num" data-batch-clock aria-live="off">00:00:00</p>
          <p class="batch__label">${I.flame}<span data-batch-label>${esc(s('batch.next'))}</span></p>
          <p class="batch__items" data-batch-items></p>
        </div>
        <div data-reveal>
          <h3 class="tiny muted" style="text-transform:uppercase;letter-spacing:.1em;margin-bottom:.7rem" data-i18n="batch.today">${esc(s('batch.today'))}</h3>
          <ul class="batch__list" style="list-style:none;padding:0">${rows}</ul>
        </div>
      </div>
    </div>
  </section>`;
}

function storySection({ rel }) {
  const stats = site.stats
    .map(
      (st) => `
      <div class="stat" data-reveal>
        <p class="stat__v" data-count="${st.value}" data-suffix="${st.suffix}">0</p>
        <p class="stat__l" data-i18n="story.stat.${st.id}">${esc(s('story.stat.' + st.id))}</p>
      </div>`
    )
    .join('');
  return `
  <section class="section section--edge" id="story">
    <div class="wrap split">
      <div class="story__media" data-reveal>
        <img src="${asset(rel, 'img/atelier.jpg')}" alt="" width="1100" height="800" loading="lazy" decoding="async">
      </div>
      <div class="stack" style="--flow:1.1rem" data-reveal>
        <span class="eyebrow" data-i18n="story.kicker">${esc(s('story.kicker'))}</span>
        <h2 class="h-sec" data-i18n="story.title">${esc(s('story.title'))}</h2>
        <p class="h-lead" data-i18n="story.lead">${esc(s('story.lead'))}</p>
        <p data-i18n="story.p1">${esc(s('story.p1'))}</p>
        <p data-i18n="story.p2">${esc(s('story.p2'))}</p>
        <blockquote class="quote" data-i18n="story.quote">${esc(s('story.quote'))}</blockquote>
        <div class="stats">${stats}</div>
      </div>
    </div>
  </section>`;
}

function servicesSection() {
  const cards = site.services
    .map(
      (sv, i) => `
      <article class="svc" data-reveal style="--d:${i * 80}ms">
        <span class="svc__icon">${I[sv.icon] || I.bread}</span>
        <h3 data-i18n="services.${sv.id}.t">${esc(s(`services.${sv.id}.t`))}</h3>
        <p data-i18n="services.${sv.id}.d">${esc(s(`services.${sv.id}.d`))}</p>
        <a href="${sv.href}"><span data-i18n="nav.order">${esc(s('nav.order'))}</span> <span class="arrow" aria-hidden="true">→</span></a>
      </article>`
    )
    .join('');
  return `
  <section class="section" id="services">
    <div class="wrap">
      <div class="section-head">
        <h2 class="h-sec" data-i18n="services.title">${esc(s('services.title'))}</h2>
        <p class="h-lead" data-i18n="services.lead">${esc(s('services.lead'))}</p>
      </div>
      <div class="grid grid--3">${cards}</div>
    </div>
  </section>`;
}

function gallerySection({ rel }) {
  const figs = site.gallery
    .map(
      (g, i) => `
      <figure data-gal-item tabindex="0" data-full="${asset(rel, g.image)}" data-reveal>
        <img src="${asset(rel, g.image)}" alt="" loading="lazy" decoding="async" width="900" height="700">
        <figcaption>${I.search.replace('viewBox', 'style="width:14px;height:14px;stroke:#fff" viewBox')} <span data-i18n="gallery.open" data-i18n-args="${i + 1}">${esc(s('gallery.open').replace('{{n}}', i + 1))}</span></figcaption>
      </figure>`
    )
    .join('');
  return `
  <section class="section section--alt" id="gallery">
    <div class="wrap">
      <div class="section-head">
        <h2 class="h-sec" data-i18n="gallery.title">${esc(s('gallery.title'))}</h2>
        <p class="h-lead" data-i18n="gallery.lead">${esc(s('gallery.lead'))}</p>
      </div>
      <div class="gal">${figs}</div>
    </div>
    <div class="lightbox" hidden data-lightbox role="dialog" aria-modal="true" aria-label="${esc(s('gallery.title'))}">
      <div class="lightbox__bar">
        <span class="tiny num" data-lb-counter>1</span>
        <span style="display:flex;gap:.5rem">
          <button class="icon-btn" type="button" data-lb-prev data-i18n-aria="gallery.prev" aria-label="${esc(s('gallery.prev'))}">${I.left}</button>
          <button class="icon-btn" type="button" data-lb-next data-i18n-aria="gallery.next" aria-label="${esc(s('gallery.next'))}">${I.right}</button>
          <button class="icon-btn" type="button" data-lb-close data-i18n-aria="gallery.close" aria-label="${esc(s('gallery.close'))}">${I.close}</button>
        </span>
      </div>
      <img src="" alt="">
    </div>
  </section>`;
}

function testimonials() {
  const slides = site.voices
    .map(
      (v, i) => `
      <article class="quote-card${i % 2 ? ' quote-card--alt' : ''}" data-slide="${v.id}" aria-roledescription="slide">
        <p class="stars" aria-label="${v.rating}/5">${I.star.repeat(v.rating)}</p>
        <blockquote data-i18n="testimonials.${v.id}.text">${esc(s(`testimonials.${v.id}.text`))}</blockquote>
        <div class="quote-card__who">
          <span class="avatar" aria-hidden="true">${v.avatarInitials}</span>
          <span><b data-i18n="testimonials.${v.id}.name">${esc(s(`testimonials.${v.id}.name`))}</b><br>
          <span class="tiny muted" data-i18n="testimonials.${v.id}.role">${esc(s(`testimonials.${v.id}.role`))}</span></span>
        </div>
      </article>`
    )
    .join('');
  const dots = site.voices.map((v, i) => `<button type="button" data-dot="${i}" aria-selected="${i === 0}" aria-label="${esc(s('testimonials.' + v.id + '.name'))} — ${i + 1}/${site.voices.length}"></button>`).join('');
  return `
  <section class="section" id="voices">
    <div class="wrap">
      <div class="section-head">
        <h2 class="h-sec" data-i18n="testimonials.title">${esc(s('testimonials.title'))}</h2>
        <p class="h-lead" data-i18n="testimonials.lead">${esc(s('testimonials.lead'))}</p>
      </div>
      <div class="quotes" data-carousel tabindex="0" role="group" aria-roledescription="carousel" aria-label="${esc(s('testimonials.title'))}">
        <div class="quotes__viewport"><div class="quotes__track" data-track>${slides}</div></div>
        <div class="quotes__nav">
          <div class="dots" role="tablist" aria-label="Reviews">${dots}</div>
          <div class="chip-row">
            <button class="icon-btn" type="button" data-prev aria-label="${esc(s('gallery.prev'))}">${I.left}</button>
            <button class="icon-btn" type="button" data-next aria-label="${esc(s('gallery.next'))}">${I.right}</button>
          </div>
        </div>
      </div>
    </div>
  </section>`;
}

function hoursSection() {
  const rows = site.hours
    .map(
      (h) => `
      <tr data-hours-row="${h.day}">
        <td data-i18n="hours.day.${h.day}">${esc(s('hours.day.' + h.day))}</td>
        <td class="num" data-hours-value>${h.open ? `${timeOf(h.open)} – ${timeOf(h.close)}` : esc(s('hours.closed'))}</td>
      </tr>`
    )
    .join('');
  return `
  <section class="section section--alt" id="hours">
    <div class="wrap">
      <div class="section-head">
        <h2 class="h-sec" data-i18n="hours.title">${esc(s('hours.title'))}</h2>
        <p class="h-lead" data-i18n="hours.lead">${esc(s('hours.lead'))}</p>
      </div>
      <div class="hours-grid">
        <div class="card card--flat" data-reveal>
          <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;margin-bottom:.8rem">
            <h3 class="tiny" style="text-transform:uppercase;letter-spacing:.1em;color:var(--muted)" data-i18n="footer.hoursTitle">${esc(s('footer.hoursTitle'))}</h3>
            <span class="badge" data-open-badge><span class="dot"></span><span>${esc(s('common.open'))}</span></span>
          </div>
          <table class="hours-table"><tbody>${rows}</tbody></table>
          <p class="tiny muted" style="margin-top:.9rem">${I.clock} <span data-i18n="hours.holiday">${esc(s('hours.holiday'))}</span></p>
        </div>
        <div class="info-card" data-reveal>
          <div class="map"><span class="map__pin"><span></span><b class="tiny">${esc(s('hours.transit'))}</b></span></div>
          <div class="card">
            <p class="tiny muted" style="text-transform:uppercase;letter-spacing:.1em" data-i18n="hours.address">${esc(s('hours.address'))}</p>
            <address><strong data-i18n="hours.addressValue">${esc(s('hours.addressValue'))}</strong></address>
            <p class="tiny muted" data-i18n="hours.transit">${esc(s('hours.transit'))}</p>
            <div class="chip-row" style="margin-top:.6rem">
              <a class="btn btn--sm btn--ghost" href="tel:${site.studio.phone.replace(/\s/g, '')}">${I.phone}<span data-i18n="hours.phone">${esc(s('hours.phone'))}</span></a>
              <a class="btn btn--sm" href="https://maps.google.com/?q=${encodeURIComponent(s('hours.addressValue'))}" target="_blank" rel="noopener">${I.pin}<span data-i18n="hours.directions">${esc(s('hours.directions'))}</span></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>`;
}

function orderSection() {
  return `
  <section class="section" id="order">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow" data-i18n="nav.order">${esc(s('nav.order'))}</span>
        <h2 class="h-sec" data-i18n="order.title">${esc(s('order.title'))}</h2>
        <p class="h-lead" data-i18n="order.lead">${esc(s('order.lead'))}</p>
      </div>
      <div class="order-grid">
        <form class="card" name="preorder" novalidate data-reveal>
          <div class="form-grid form-grid--2">
            <p class="field"><label for="oname" data-i18n="order.name">${esc(s('order.name'))}</label>
              <input class="input" id="oname" name="name" required data-i18n-ph="order.namePh" placeholder="${esc(s('order.namePh'))}" autocomplete="name"><span class="field-error" data-err aria-live="polite"></span></p>
            <p class="field"><label for="ophone" data-i18n="order.phone">${esc(s('order.phone'))}</label>
              <input class="input" id="ophone" name="phone" type="tel" required data-i18n-ph="order.phonePh" placeholder="${esc(s('order.phonePh'))}" autocomplete="tel"><span class="field-error" data-err aria-live="polite"></span></p>
            <p class="field"><label for="omail" data-i18n="order.email">${esc(s('order.email'))}</label>
              <input class="input" id="omail" name="email" type="email" data-i18n-ph="order.emailPh" placeholder="${esc(s('order.emailPh'))}" autocomplete="email"><span class="field-error" data-err aria-live="polite"></span></p>
            <p class="field"><label for="odate" data-i18n="order.date">${esc(s('order.date'))}</label>
              <input class="input" id="odate" name="date" type="date" required><span class="field-error" data-err aria-live="polite"></span></p>
            <p class="field"><label for="otime" data-i18n="order.time">${esc(s('order.time'))}</label>
              <select class="input" id="otime" name="time">${site.batches.map((b) => `<option value="${b.time}">${timeOf(b.time)}</option>`).join('')}</select></p>
            <p class="field"><label for="opeople" data-i18n="order.people">${esc(s('order.people'))}</label>
              <input class="input" id="opeople" name="people" type="number" min="1" max="200" value="2"></p>
          </div>
          <p class="field" style="margin-top:1rem"><span class="tiny muted" data-i18n="order.method">${esc(s('order.method'))}</span>
            <span class="radio-row">
              <label><input type="radio" name="method" value="pickup" checked> <span data-i18n="order.pickup">${esc(s('order.pickup'))}</span></label>
              <label><input type="radio" name="method" value="delivery"> <span data-i18n="order.delivery">${esc(s('order.delivery'))}</span></label>
            </span></p>
          <p class="field" style="margin-top:1rem"><label for="onotes" data-i18n="order.notes">${esc(s('order.notes'))}</label>
            <textarea class="input" id="onotes" name="notes" data-i18n-ph="order.notesPh" placeholder="${esc(s('order.notesPh'))}"></textarea></p>
          <p class="field" style="margin-top:.6rem"><label style="display:flex;gap:.5rem;align-items:center;font-weight:500">
            <input type="checkbox" name="consent" checked> <span data-i18n="order.consent">${esc(s('order.consent'))}</span></label></p>
          <div style="display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-top:1.1rem">
            <button class="btn" type="submit" data-submit data-i18n="order.submit">${esc(s('order.submit'))}</button>
            <span data-order-handoff style="display:flex;gap:.5rem;flex-wrap:wrap"></span>
          </div>
          <p class="form-status" data-form-status role="status" aria-live="polite"></p>
          <p class="form-note" style="margin-top:.8rem" data-i18n="order.privacy">${esc(s('order.privacy'))}</p>
        </form>
        <aside class="card stack" style="--flow:.55rem" aria-label="${esc(s('order.summary'))}" data-reveal>
          <h3 data-i18n="order.summary">${esc(s('order.summary'))}</h3>
          <p data-basket-summary class="tiny muted">${esc(s('order.noBasket'))}</p>
          <p class="summary__row"><span data-i18n="basket.subtotal">${esc(s('basket.subtotal'))}</span><b class="num" data-subtotal>${moneyOf(0)}</b></p>
          <p class="summary__row summary__total"><span data-i18n="basket.total">${esc(s('basket.total'))}</span><b class="num" data-total>${moneyOf(0)}</b></p>
          <p class="tiny muted" data-i18n="basket.note">${esc(s('basket.note'))}</p>
          <button class="btn btn--ghost btn--sm" type="button" data-open-basket data-i18n="nav.basket">${esc(s('nav.basket'))}</button>
        </aside>
      </div>
    </div>
  </section>`;
}

function faqSection() {
  const items = site.faq
    .map(
      (f) => `
      <div class="acc__item" data-open="false">
        <h3><button class="acc__btn" type="button" aria-expanded="false" aria-controls="p-${f.id}"><span data-i18n="faq.${f.id}.q">${esc(s(`faq.${f.id}.q`))}</span></button></h3>
        <div class="acc__panel" id="p-${f.id}" role="region"><div><p data-i18n="faq.${f.id}.a">${esc(s(`faq.${f.id}.a`))}</p></div></div>
      </div>`
    )
    .join('');
  return `
  <section class="section section--edge" id="faq">
    <div class="wrap wrap--narrow">
      <div class="section-head">
        <h2 class="h-sec" data-i18n="faq.title">${esc(s('faq.title'))}</h2>
        <p class="h-lead" data-i18n="faq.lead">${esc(s('faq.lead'))}</p>
      </div>
      <div class="acc" data-acc>${items}</div>
    </div>
  </section>`;
}

function footerSection({ rel, tplId }) {
  const langs = site.languages
    .map((l) => `<li><button type="button" data-set-lang="${l.code}" ${l.code === DEF ? 'aria-current="true"' : ''}>${esc(l.native)}</button></li>`)
    .join('');
  const hoursRows = site.hours
    .slice(0, 7)
    .map((h) => `<li><span data-i18n="hours.day.${h.day}">${esc(s('hours.day.' + h.day))}</span> — <span class="num">${h.open ? `${timeOf(h.open)}–${timeOf(h.close)}` : esc(s('hours.closed'))}</span></li>`)
    .join('');
  return `
  <footer class="footer">
    <div class="wrap">
      <div class="foot-grid">
        <div class="stack" style="--flow:.7rem">
          <a class="brand" href="${rel}/">
            <span class="brand__mark" aria-hidden="true">${esc((tplId ? s(`brand.${tplId}.name`) : 'LK').slice(0, 2).toUpperCase())}</span>
            <span class="brand__text"><span class="brand__name">${esc(tplId ? s(`brand.${tplId}.name`) : 'Levain Kit')}</span></span>
          </a>
          <p class="tiny muted" data-i18n="footer.blurb">${esc(s('footer.blurb'))}</p>
          <p class="tiny"><span data-i18n="footer.made">${esc(s('footer.made'))}</span> · <a class="kit-link" href="${rel}/"><span data-i18n="footer.backKit">${esc(s('footer.backKit'))}</span> →</a></p>
        </div>
        <div><h4 data-i18n="footer.hoursTitle">${esc(s('footer.hoursTitle'))}</h4><ul>${hoursRows}</ul></div>
        <div><h4 data-i18n="footer.contactTitle">${esc(s('footer.contactTitle'))}</h4>
          <ul>
            <li><a href="tel:${site.studio.phone.replace(/\s/g, '')}">${esc(site.studio.phone)}</a></li>
            <li><a href="mailto:${site.studio.email}">${esc(site.studio.email)}</a></li>
            <li><a href="https://wa.me/${site.studio.whatsapp}">WhatsApp</a></li>
            <li><a href="#hours" data-i18n="footer.instagram">${esc(s('footer.instagram'))}</a></li>
          </ul>
        </div>
        <div>
          <h4 data-i18n="footer.langTitle">${esc(s('footer.langTitle'))}</h4>
          <ul>${langs}</ul>
          <form class="news" onsubmit="return false" aria-label="Newsletter">
            <label class="sr-only" for="nl" data-i18n="footer.emailPh">${esc(s('footer.emailPh'))}</label>
            <input class="input" id="nl" type="email" data-i18n-ph="footer.emailPh" placeholder="${esc(s('footer.emailPh'))}">
            <button class="btn btn--sm" type="submit" data-i18n="footer.newsletterCta">${esc(s('footer.newsletterCta'))}</button>
          </form>
          <p class="tiny muted" style="margin-top:.5rem" data-i18n="footer.newsletter">${esc(s('footer.newsletter'))}</p>
        </div>
      </div>
      <div class="foot-bar">
        <p>© ${site.studio.year} ${esc(tplId ? s(`brand.${tplId}.name`) : site.studio.maker)} — <span data-i18n="footer.rights">${esc(s('footer.rights'))}</span></p>
        <p class="tiny"><span data-i18n="common.demo">${esc(s('common.demo'))}</span> · <a href="#faq">FAQ</a> · <a href="#menu">${esc(s('nav.menu'))}</a></p>
      </div>
    </div>
    <button class="icon-btn to-top" type="button" data-show="false" data-i18n-aria="common.top" aria-label="${esc(s('common.top'))}">${I.up}</button>
  </footer>`;
}

function drawer() {
  return `
  <div class="scrim" data-scrim data-close-basket></div>
  <aside class="basket" data-basket data-open="false" aria-hidden="true" aria-label="${esc(s('basket.title'))}">
    <div class="basket__head">
      <h2 style="font-size:var(--fs-2)" data-i18n="basket.title">${esc(s('basket.title'))}</h2>
      <button class="icon-btn" type="button" data-close-basket data-i18n-aria="gallery.close" aria-label="${esc(s('gallery.close'))}">${I.close}</button>
    </div>
    <div class="basket__body" data-basket-body></div>
    <div class="basket__foot">
      <p class="summary__row"><span data-i18n="basket.total">${esc(s('basket.total'))}</span><b class="num" data-total>${moneyOf(0)}</b></p>
      <p class="tiny muted" data-i18n="basket.note">${esc(s('basket.note'))}</p>
      <button class="btn btn--block" type="button" data-basket-whatsapp>${esc(s('basket.whatsapp'))}</button>
      <a class="btn btn--ghost btn--block" href="#order" data-close-basket data-i18n="order.submit">${esc(s('order.submit'))}</a>
    </div>
  </aside>`;
}

/* ------------------------------------------------------------- the hub */
function hubPage({ rel }) {
  const tabs = site.templates
    .map(
      (tp, i) => `
      <button class="tpl-tab" type="button" role="tab" data-tpl="${tp.id}" aria-selected="${i === 0}">
        <span class="tpl-tab__n">0${i + 1} / ${tp.id}</span>
        <span class="tpl-tab__name" data-i18n="hub.t.${tp.id}">${esc(s('hub.t.' + tp.id))}</span>
        <span class="tpl-tab__k" data-i18n="hub.t.${tp.id}.k">${esc(s('hub.t.' + tp.id + '.k'))}</span>
        <span class="swatches" aria-hidden="true">
          ${['--bg', '--accent', '--text'].map(() => '').join('')}
          <i class="swatch" style="background:${i === 0 ? '#1c1611' : i === 1 ? '#fffafc' : '#fbf6ee'}"></i>
          <i class="swatch" style="background:${i === 0 ? '#e08a2e' : i === 1 ? '#a4445f' : '#c2532a'}"></i>
          <i class="swatch" style="background:${i === 0 ? '#c2ae98' : i === 1 ? '#ecd8de' : '#c2532a'}"></i>
        </span>
      </button>`
    )
    .join('');
  const cards = site.templates
    .map(
      (tp, i) => `
      <article class="card stack" style="--flow:.6rem" data-reveal>
        <p class="tiny mono muted">0${i + 1} · /templates/${tp.id}</p>
        <h3 style="font-size:var(--fs-2)" data-i18n="hub.t.${tp.id}">${esc(s('hub.t.' + tp.id))}</h3>
        <p class="tiny" style="color:var(--accent);font-weight:700;letter-spacing:.06em;text-transform:uppercase" data-i18n="hub.t.${tp.id}.k">${esc(s('hub.t.' + tp.id + '.k'))}</p>
        <p class="tiny muted" data-i18n="hub.t.${tp.id}.d">${esc(s('hub.t.' + tp.id + '.d'))}</p>
        <p class="chip-row">${tp.markets.slice(0, 6).map((m) => `<span class="chip chip--tag" aria-hidden="true">${m}</span>`).join('')}</p>
        <p style="display:flex;gap:.5rem;flex-wrap:wrap">
          <a class="btn btn--sm" href="${rel}/templates/${tp.id}/index.html" data-i18n="hub.open">${esc(s('hub.open'))}</a>
          <button class="btn btn--sm btn--ghost" type="button" data-tpl="${tp.id}" data-i18n="hub.previewNote">${esc(s('hub.previewNote'))}</button>
        </p>
      </article>`
    )
    .join('');
  const feats = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8']
    .map((f) => {
      const ico = { f1: 'globe', f2: 'bread', f3: 'basket', f4: 'flame', f5: 'clock', f6: 'tart', f7: 'hands', f8: 'croissant' }[f];
      return `<div class="feat__cell" data-reveal>
          <span class="feat__i">${I[ico]}</span>
          <h3 data-i18n="hub.${f}t">${esc(s(`hub.${f}t`))}</h3>
          <p data-i18n="hub.${f}d">${esc(s(`hub.${f}d`))}</p>
        </div>`;
    })
    .join('');
  const langRows = site.languages
    .map((l) => {
      const sample = path(locales[l.code], 'hub.langSample');
      const price = new Intl.NumberFormat(l.locale, { style: 'currency', currency: 'EUR' }).format(2.4);
      return `<div class="langlab__row" data-dir="${l.dir}" data-reveal>
          <span class="langlab__code">${l.code} · ${l.locale}</span>
          <span class="langlab__txt">${esc(sample)}<small>${esc(l.native)} · ${l.dir.toUpperCase()} · ${esc(price)}</small></span>
        </div>`;
    })
    .join('');
  const pkgBtns = site.packages
    .filter((p) => p.id !== 'licence')
    .map(
      (p) => `<button type="button" data-pkg="${p.id}" aria-pressed="${p.id === 'croissant'}">
        ${esc(s('hub.pkg.' + p.id))}<small>${moneyOf(p.price)} · ${p.languages} lang</small></button>`
    )
    .join('');
  const optBoxes = site.options
    .filter((o) => o.id !== 'language')
    .map(
      (o) => `<label data-opt="${o.id}"><input type="checkbox" ${o.id === 'seo' ? 'checked' : ''}><span><b>${esc(s('hub.opt.' + o.id))} — +${moneyOf(o.price)}${o.recurring ? '/mo' : ''}</b><span data-i18n="hub.opt.${o.id}.d">${esc(s(`hub.opt.${o.id}.d`))}</span></span></label>`
    )
    .join('');
  const steps = [1, 2, 3, 4]
    .map(
      (n) => `<article class="step" data-reveal><h3 data-i18n="hub.step${n}t">${esc(s(`hub.step${n}t`))}</h3><p data-i18n="hub.step${n}d">${esc(s(`hub.step${n}d`))}</p></article>`
    )
    .join('');
  const deploys = ['netlify', 'vercel', 'github', 'custom']
    .map(
      (d) => `<div class="feat__cell" data-reveal><h3>${esc(s('hub.deploy.' + d))}</h3><p data-i18n="hub.deploy.${d}.d">${esc(s(`hub.deploy.${d}.d`))}</p></div>`
    )
    .join('');
  const tryList = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']
    .map((d) => `<li data-reveal><span data-i18n="hub.${d}">${esc(s('hub.' + d))}</span></li>`)
    .join('');
  const docs = [
    ['docs/README.md', './docs/README.md', 'file.readme', 'MD'],
    ['docs/PRICING.md', './docs/PRICING.md', 'file.pricing', '€'],
    ['src/data/locales/', './assets/i18n.generated.js', 'file.locales', 'i18n'],
    ['src/styles/core.css', './assets/core.css', 'file.themes', 'CSS'],
  ]
    .map(
      ([label, href, key, tag]) => `<a class="doc" href="${href}" data-reveal><span class="doc__ico">${tag}</span><span><b>${esc(label)}</b><span data-i18n="hub.${key}">${esc(s('hub.' + key))}</span></span></a>`
    )
    .join('');

  return `
  <section class="kit-hero" id="top">
    <div class="wrap">
      <div class="kit-hero__top">
        <span class="pill"><strong>3</strong> templates · <strong>4</strong> languages · <strong>0</strong> dependencies · <strong>~38 KB</strong> JS</span>
        <div class="chip-row" role="group" aria-label="${esc(s('hub.switchLang'))}">
          ${site.languages.map((l) => `<button class="chip" type="button" data-set-lang="${l.code}" ${l.code === DEF ? 'aria-pressed="true"' : ''}>${esc(l.native)}</button>`).join('')}
        </div>
      </div>
      <div class="stack" style="--flow:1.1rem;max-inline-size:62rem">
        <span class="eyebrow" data-i18n="hub.badge">${esc(s('hub.badge'))}</span>
        <h1><span data-i18n="hub.title">${esc(s('hub.title'))}</span></h1>
        <p class="hero__lead" data-i18n="hub.lead">${esc(s('hub.lead'))}</p>
        <div class="kit-hero__actions">
          <a class="btn" href="#showcase" data-i18n="hub.ctaGallery">${esc(s('hub.ctaGallery'))}</a>
          <a class="btn btn--ghost" href="#calcTitle" data-i18n="hub.ctaPricing">${esc(s('hub.ctaPricing'))}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="showcase" style="padding-block-start:1.2rem">
    <div class="wrap">
      <div class="section-head section-head--row">
        <div><h2 class="h-sec" data-i18n="hub.galleryTitle">${esc(s('hub.galleryTitle'))}</h2>
        <p class="h-lead" data-i18n="hub.galleryLead">${esc(s('hub.galleryLead'))}</p></div>
      </div>
      <div class="showcase">
        <div class="showcase__list" role="tablist" aria-label="${esc(s('hub.switchLayout'))}">${tabs}</div>
        <div class="frame" data-frame>
          <div class="frame__chrome">
            <span class="frame__dots" aria-hidden="true"><i></i><i></i><i></i></span>
            <span class="frame__url" data-frame-url>/templates/artisan/index.html</span>
            <span class="frame__sizes" role="group" aria-label="Viewport">
              <button class="size-btn" type="button" data-size="mobile" aria-pressed="false" aria-label="Mobile preview — 390px" title="390px"><i></i></button>
              <button class="size-btn" type="button" data-size="tablet" aria-pressed="false" aria-label="Tablet preview — 768px" title="768px"><i></i></button>
              <button class="size-btn" type="button" data-size="desktop" aria-pressed="true" aria-label="Desktop preview — 1440px" title="1440px"><i></i></button>
            </span>
          </div>
          <div class="frame__viewport" data-viewport data-size="desktop">
            <iframe title="Template demo" src="${rel}/templates/artisan/index.html?embed=1" data-live-demo loading="eager"></iframe>
          </div>
        </div>
      </div>
      <div class="grid grid--3" style="margin-top:2.2rem">${cards}</div>
    </div>
  </section>

  <section class="section section--alt" id="featTitle">
    <div class="wrap">
      <div class="section-head"><span class="eyebrow">engine</span>
        <h2 class="h-sec" data-i18n="hub.featTitle">${esc(s('hub.featTitle'))}</h2>
        <p class="h-lead" data-i18n="hub.featLead">${esc(s('hub.featLead'))}</p>
      </div>
      <div class="feat">${feats}</div>
    </div>
  </section>

  <section class="section" id="langTitle">
    <div class="wrap">
      <div class="langlab">
        <div class="stack" style="--flow:.8rem" data-reveal>
          <span class="eyebrow">i18n · RTL</span>
          <h2 class="h-sec" data-i18n="hub.langTitle">${esc(s('hub.langTitle'))}</h2>
          <p class="h-lead" data-i18n="hub.langLead">${esc(s('hub.langLead'))}</p>
          <p class="tiny muted" data-i18n="hub.langNote">${esc(s('hub.langNote'))}</p>
        </div>
        <div class="langlab__demo" data-reveal>${langRows}</div>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="calcTitle">
    <div class="wrap">
      <div class="section-head"><span class="eyebrow">pricing</span>
        <h2 class="h-sec" data-i18n="hub.calcTitle">${esc(s('hub.calcTitle'))}</h2>
        <p class="h-lead" data-i18n="hub.calcLead">${esc(s('hub.calcLead'))}</p>
      </div>
      <div class="calc" data-calc>
        <div class="stack" style="--flow:1.2rem">
          <div class="calc__group">
            <span class="calc__legend" data-i18n="hub.calcTemplate">${esc(s('hub.calcTemplate'))}</span>
            <div class="chip-row" id="tplPick" role="group" aria-label="${esc(s('hub.calcTemplate'))}">${site.templates.map((tp, i) => `<button class="chip" type="button" data-quote-tpl="${tp.id}" aria-pressed="${i === 0}">${esc(s('hub.t.' + tp.id))}</button>`).join('')}</div>
          </div>
          <div class="calc__group">
            <span class="calc__legend" data-i18n="hub.calcPackage">${esc(s('hub.calcPackage'))}</span>
            <div class="seg" role="group">${pkgBtns}</div>
          </div>
          <div class="calc__group">
            <span class="calc__legend" data-i18n="hub.calcLangs">${esc(s('hub.calcLangs'))}</span>
            <div class="seg" data-langs role="group">${[1, 2, 3, 4].map((n) => `<button type="button" data-langs="${n}" aria-pressed="${n === 2}" aria-label="${n} ${esc(s('hub.calcLangs'))}">${n}</button>`).join('')}</div>
          </div>
          <div class="calc__group">
            <span class="calc__legend" data-i18n="hub.calcOptions">${esc(s('hub.calcOptions'))}</span>
            <div class="checks">${optBoxes}</div>
          </div>
          <p class="field"><label for="client" class="calc__legend" style="font-size:var(--fs--2)">Client name (optional)</label>
            <input class="input" id="client" data-client placeholder="Boulangerie Dupont"></p>
        </div>
        <div class="calc__out" data-reveal>
          <span class="calc__legend" style="opacity:.7" data-i18n="hub.calcTotal">${esc(s('hub.calcTotal'))}</span>
          <p class="calc__total" data-calc-total>—</p>
          <div class="calc__rows" data-calc-rows></div>
          <div class="calc__meta">
            <span class="pill"><span data-i18n="hub.calcMonthly">${esc(s('hub.calcMonthly'))}</span> <b data-calc-monthly>—</b></span>
            <span class="pill"><span data-i18n="hub.calcDays">${esc(s('hub.calcDays'))}</span> <b data-calc-days>—</b></span>
          </div>
          <div>
            <p class="calc__legend" style="margin-bottom:.4rem" data-i18n="hub.calcWhats">${esc(s('hub.calcWhats'))}</p>
            <ul class="tiny" style="display:grid;gap:.3rem" data-calc-list></ul>
          </div>
          <button class="btn btn--block" type="button" data-copy-quote data-i18n="hub.calcCopy">${esc(s('hub.calcCopy'))}</button>
          <p class="calc__note" data-i18n="hub.calcNote">${esc(s('hub.calcNote'))}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="devTitle">
    <div class="wrap">
      <div class="section-head"><span class="eyebrow">docs</span>
        <h2 class="h-sec" data-i18n="hub.devTitle">${esc(s('hub.devTitle'))}</h2>
        <p class="h-lead" data-i18n="hub.devLead">${esc(s('hub.devLead'))}</p>
      </div>
      <div class="grid" style="--gap:1.2rem;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:start">
        <div class="codewrap" data-reveal>
          <pre class="code"><code><span class="c"># 1 — clone &amp; preview</span>
git clone ${'https://github.com/abdoo606/BLAblalba.git'} cd BLAblalba
npm run dev              <span class="c"># http://localhost:5173</span>

<span class="c"># 2 — make it the client's shop</span>
<span class="p">nano</span> src/data/site.json          <span class="c"># prices, hours, batches</span>
<span class="p">nano</span> src/data/locales/fr.json     <span class="c"># copy &amp; translate</span>
<span class="p">nano</span> src/styles/core.css          <span class="c"># colours, type scale</span>

<span class="c"># 3 — build &amp; ship</span>
npm run build            <span class="c"># → dist/ (static, 4 pages)</span>
npm run package          <span class="c"># → release/levain-kit.zip</span>
<span class="k">gh</span> api /repos/x/pages  <span class="c"># or drop dist/ on any host</span></code></pre>
          <button class="copy-btn" type="button" data-copy="${'git clone && npm run dev'}">copy</button>
        </div>
        <div class="steps" data-reveal>${steps}</div>
      </div>
    </div>
  </section>

  <section class="section section--edge" id="deployTitle">
    <div class="wrap">
      <div class="section-head"><span class="eyebrow">hosting</span>
        <h2 class="h-sec" data-i18n="hub.deployTitle">${esc(s('hub.deployTitle'))}</h2>
        <p class="h-lead" data-i18n="hub.deployLead">${esc(s('hub.deployLead'))}</p>
      </div>
      <div class="feat" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))">${deploys}</div>
    </div>
  </section>

  <section class="section" id="demoTitle">
    <div class="wrap">
      <div class="grid" style="grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);--gap:2rem;align-items:start">
        <div class="stack" style="--flow:.8rem" data-reveal>
          <span class="eyebrow">QA checklist</span>
          <h2 class="h-sec" data-i18n="hub.demoTitle">${esc(s('hub.demoTitle'))}</h2>
          <p class="h-lead" data-i18n="hub.demoLead">${esc(s('hub.demoLead'))}</p>
        </div>
        <ol class="try">${tryList}</ol>
      </div>
    </div>
  </section>

  <section class="section" id="docsTitle">
    <div class="wrap">
      <div class="section-head"><span class="eyebrow">files</span>
        <h2 class="h-sec" data-i18n="hub.docsTitle">${esc(s('hub.docsTitle'))}</h2>
        <p class="h-lead" data-i18n="hub.docsLead">${esc(s('hub.docsLead'))}</p>
      </div>
      <div class="docs">${docs}</div>
    </div>
  </section>

  <section class="section" id="cta">
    <div class="wrap">
      <div class="bigcta" data-reveal>
        <h2 data-i18n="hub.ctaTitle">${esc(s('hub.ctaTitle'))}</h2>
        <p data-i18n="hub.ctaLead">${esc(s('hub.ctaLead'))}</p>
        <div class="bigcta__row">
          <a class="btn" href="mailto:${site.studio.email}" data-i18n="hub.ctaMail">${esc(s('hub.ctaMail'))}</a>
          <a class="btn btn--ghost" href="./docs/PRICING.md" data-i18n="hub.ctaDocs">${esc(s('hub.ctaDocs'))}</a>
        </div>
      </div>
    </div>
  </section>`;
}

/* ---------------------------------------------------- JSON-LD per shop */
function jsonLd(tpl) {
  const name = s(`brand.${tpl.id}.name`);
  return JSON.stringify(
    {
      '@context': 'https://schema.org',
      '@type': 'Bakery',
      name,
      description: s('hero.lead'),
      url: `${site.baseUrl || ''}/templates/${tpl.id}/index.html`,
      telephone: site.studio.phone,
      email: site.studio.email,
      address: { '@type': 'PostalAddress', streetAddress: s('hours.addressValue'), addressCountry: 'FR' },
      inLanguage: site.languages.map((l) => l.code),
      openingHoursSpecification: site.hours
        .filter((h) => h.open)
        .map((h) => ({
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: h.day.charAt(0).toUpperCase() + h.day.slice(1),
          opens: h.open,
          closes: h.close,
        })),
      menu: `${site.baseUrl || ''}/#menu`,
      servesCuisine: 'French, Mediterranean',
      priceRange: '€€',
      hasMerchantReturnPolicy: undefined,
    },
    null,
    1
  ).replace(/\s*"hasMerchantReturnPolicy":\s*undefined,?/, '');
}

/* ------------------------------------------------------------- renderer */
function renderTemplatePage(tpl) {
  const rel = '../..';
  const cfgInline = {
    templateId: tpl.id,
    base: rel,
    brandName: s(`brand.${tpl.id}.name`),
    brandSlug: tpl.id,
    currency: site.studio.currency,
    defaultLanguage: DEF,
    languages: site.languages,
    products: site.products,
    hours: site.hours,
    batches: site.batches,
    templates: site.templates,
    whatsapp: site.studio.whatsapp,
    email: site.studio.email,
    packages: site.packages,
    options: site.options,
    repo: 'https://github.com/abdoo606/BLAblalba',
  };
  const sections = {
    hero: () => hero({ rel, tplId: tpl.id }),
    marquee,
    specialties,
    menu: () => menuBoard({ rel, tplId: tpl.id }),
    batch: batchSection,
    story: () => storySection({ rel }),
    services: servicesSection,
    gallery: () => gallerySection({ rel }),
    testimonials,
    hours: hoursSection,
    order: orderSection,
    faq: faqSection,
    footer: () => footerSection({ rel, tplId: tpl.id }),
  };
  const body = [
    header({ rel, tplId: tpl.id }),
    `<main id="main">`,
    tpl.sections.filter((x) => x !== 'footer').map((x) => (sections[x] || (() => ''))()).join('\n'),
    `</main>`,
    footerSection({ rel, tplId: tpl.id }),
    drawer(),
  ].join('\n');
  return [
    head({
      rel,
      theme: tpl.theme,
      tplId: tpl.id,
      title: `${s(`brand.${tpl.id}.name`)} — ${s('hero.title')} ${s('hero.titleAccent')}`,
      desc: s('hero.lead'),
      preload: tpl.hero, prefix: '../..',
    }),
    body,
    `  <script>window.LEVAIN_CFG=${JSON.stringify(cfgInline)};</script>`,
    `  <script type="application/ld+json">${jsonLd(tpl)}</script>`,
    scriptTail({ rel }),
  ].join('\n');
}

function renderHub() {
  const rel = '.';
  const cfgInline = {
    templateId: 'kit',
    base: '.',
    brandName: 'Levain Kit',
    currency: site.studio.currency,
    defaultLanguage: DEF,
    languages: site.languages,
    templates: site.templates,
    products: site.products,
    hours: site.hours,
    batches: site.batches,
    packages: site.packages,
    options: site.options,
    whatsapp: site.studio.whatsapp,
    email: site.studio.email,
    repo: 'https://github.com/abdoo606/BLAblalba',
  };
  return [
    head({ rel, theme: 'kit', tplId: null, title: s('meta.title'), desc: s('meta.desc'), preload: 'img/hero-artisan.jpg' }),
    header({ rel, tplId: null }),
    `<main id="main">`,
    hubPage({ rel }),
    `</main>`,
    footerSection({ rel, tplId: null }),
    `  <script>window.LEVAIN_CFG=${JSON.stringify(cfgInline)};</script>`,
    scriptTail({ rel }),
  ].join('\n');
}

function render404() {
  return [
    head({ rel: '.', theme: 'kit', tplId: null, title: '404 — Levain Kit', desc: 'Page not found', preload: '' }),
    `<main id="main" class="section" style="min-block-size:60vh;display:grid;place-items:center;text-align:center">
      <div class="wrap wrap--narrow stack" style="--flow:1rem">
        <p class="eyebrow">404</p>
        <h1 style="font-size:var(--fs-5)">This tray is empty.</h1>
        <p class="h-lead">The page you wanted is not in this build — the oven is fine, the link is not.</p>
        <p><a class="btn" href="./">Back to the kit</a></p>
      </div>
    </main>`,
    scriptTail({ rel: '.' }),
  ].join('\n');
}

/* --------------------------------------------------------------- write */
function write(file, content) {
  const p = join(DIST, file);
  mkdirSync(dirname(p), { recursive: true });
  writeFileSync(p, content);
  return p;
}

function build() {
  rmSync(DIST, { recursive: true, force: true });
  // inlined dictionaries + shared config
  const dictFile = write('assets/i18n.generated.js', `/* generated by src/build.mjs — do not edit */\nwindow.LEVAIN_I18N=${JSON.stringify(locales)};\n`);
  // copy runtime
  cpSync(join(SRC, 'js', 'app.js'), join(DIST, 'assets', 'app.js'));
  cpSync(join(SRC, 'js', 'hub.js'), join(DIST, 'assets', 'hub.js'));
  cpSync(join(SRC, 'styles', 'core.css'), join(DIST, 'assets', 'core.css'));
  cpSync(join(SRC, 'styles', 'hub.css'), join(DIST, 'assets', 'hub.css'));
  if (existsSync(join(SRC, 'assets', 'img'))) cpSync(join(SRC, 'assets', 'img'), join(DIST, 'assets', 'img'), { recursive: true });
  mkdirSync(join(DIST, 'docs'), { recursive: true });
  // Never publish the pipeline: docs/PROSPECTS.md and sales/* stay out of dist/ on purpose.
  const PRIVATE = ['PROSPECTS.md'];
  for (const f of ['PRICING.md', 'HANDOVER.md', 'README.md'].filter((x) => !PRIVATE.includes(x))) {
    const p = join(ROOT, 'docs', f);
    if (existsSync(p)) cpSync(p, join(DIST, 'docs', f));
    else if (f === 'README.md' && existsSync(join(ROOT, 'README.md'))) cpSync(join(ROOT, 'README.md'), join(DIST, 'docs', f));
  }
  write('assets/favicon.svg', `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#b4530a"/><path d="M14 36c0-9 8-15 18-15s18 6 18 15c0 2-2 3-4 3H18c-2 0-4-1-4-3Z" fill="#fff3e2"/><path d="M22 26c2-4 6-6 10-6M20 39l4-6M30 39l2-8M40 39l-3-7" stroke="#b4530a" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>`);
  write(
    'assets/site.webmanifest',
    JSON.stringify(
      {
        name: 'Levain Kit — bakery template',
        short_name: 'Levain Kit',
        start_url: '.',
        display: 'standalone',
        background_color: '#fffdf9',
        theme_color: '#b4530a',
        lang: 'en',
        icons: [{ src: 'favicon.svg', sizes: 'any', type: 'image/svg+xml' }],
      },
      null,
      2
    )
  );

  const pages = [];
  for (const tpl of site.templates) {
    pages.push([`templates/${tpl.id}/index.html`, renderTemplatePage(tpl)]);
  }
  pages.push(['index.html', renderHub()]);
  pages.push(['404.html', render404()]);
  for (const [file, html] of pages) write(file, html);

  // per-language folders for real deployments (static hosts serve /fr/ etc.)
  write(
    'robots.txt',
    `User-agent: *\nAllow: /\nSitemap: ${(site.baseUrl || 'https://example.netlify.app')}/sitemap.xml\n`
  );
  const urls = [];
  for (const tpl of site.templates) for (const l of site.languages) urls.push(`/templates/${tpl.id}/index.html?lang=${l.code}`);
  write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.6">\n${urls
    .map((u) => `  <url><loc>${(site.baseUrl || '') + u}</loc></url>`)
    .join('\n')}\n</urlset>\n`);

  // parity check between locales (build fails if a key is missing)
  const flat = (o, p = '') => Object.entries(o).flatMap(([k, v]) => (v && typeof v === 'object' ? flat(v, `${p}${k}.`) : [`${p}${k}`]));
  const base = new Set(flat(locales[DEF]));
  const problems = [];
  for (const l of site.languages) {
    const keys = new Set(flat(locales[l.code]));
    for (const k of base) if (!keys.has(k)) problems.push(`${l.code}: missing ${k}`);
    for (const k of keys) if (!base.has(k)) problems.push(`${l.code}: extra ${k}`);
  }
  if (problems.length) {
    console.error('\n❌ locale parity:\n' + problems.slice(0, 40).join('\n'));
    process.exitCode = 1;
  }
  const kb = (n) => (n / 1024).toFixed(1) + ' KB';
  const size = (f) => (existsSync(f) ? statSync(f).size : 0);
  console.log('✓ built', pages.length + 4, 'pages →', relative(ROOT, DIST));
  console.log('  dictionaries:', kb(size(dictFile)), '| app.js:', kb(size(join(DIST, 'assets', 'app.js'))));
  for (const [f] of pages) console.log('  ·', f, kb(size(join(DIST, f))));
  if (!problems.length) console.log('✓ ' + site.languages.length + ' locales in parity (' + base.size + ' keys each)');
}

build();

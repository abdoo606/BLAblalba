import csv, json

p = 'sales/prospects-2026.csv'
rows = list(csv.DictReader(open(p, newline='')))
fields = list(rows[0].keys())

NEW = [
 ("Toad Bakery", "London (Camberwell + Deptford)", "GB", "artisan", "croissant", "2", "seo + multi-location", 2010, "A — hot",
  "Good Food Guide 2026 Britain's Best Bakeries; Time Out reports the Saturday queue; OPENED A SECOND SHOP IN DEPTFORD IN 2026",
  "Unaudited. Camberwell bakery with a second site since 2026 — check whether one page serves both and whether either shows today's bakes",
  "londonyaar.com — 15 best bakeries in London to visit in 2026", "2026-08-16"),
 ("Layla Bakery", "London (Ladbroke Grove)", "GB", "patisserie", "croissant", "2", "seo", 1830, "A — hot",
  "Named the Good Food Guide's best bakery in London for 2026 — a moment the whole street will search for",
  "Unaudited. Award press vs what their own site says is the gap",
  "londonyaar.com — 15 best bakeries in London to visit in 2026", "2026-08-16"),
 ("Chatsworth Bakehouse", "London (Crystal Palace)", "GB", "moderno", "croissant", "2", "preorder + multi-location", 2090, "A — hot",
  "Destination bakery people cross London for; Good Food Guide 2026 list; sandwiches and pastries sell out daily",
  "Unaudited. Sold-out handling and a queue-busting pre-order are the two things to check",
  "londonyaar.com — 15 best bakeries in London to visit in 2026", "2026-08-16"),
 ("Suba Bakery", "London (Walthamstow)", "GB", "artisan", "baguette", "2", "seo + photo", 1450, "B — upgrade",
  "NEW ENTRY in Britain's 50 Best Bakeries 2026; one-owner shop (Pa Modou, from Gambia by way of Hackney) with African- and Asian-inflected bakes",
  "Unaudited. Micro-bakery, probably Instagram-run — sole trader, so a visit or a DM beats a cold email",
  "thegoodfoodguide.co.uk — Britain's 50 Best Bakeries 2026", "2026-06-08"),
 ("Wild Hearth Bakery", "Comrie, Perthshire", "GB", "artisan", "baguette", "1", "preorder", 1210, "B — upgrade",
  "NEW ENTRY in Britain's 50 Best Bakeries 2026; one baker (John Castley), mill-to-oven range from sourdough bomboloni to German schrotbrot",
  "Unaudited. Hamlet bakery — a paper order book is the norm; sell the order book, not a “website”",
  "thegoodfoodguide.co.uk — Britain's 50 Best Bakeries 2026", "2026-06-08"),
 ("Little Sourdough Kitchen", "London (Fulham)", "GB", "artisan", "baguette", "1", "preorder", 1210, "B — upgrade",
  "Recommended in the FT's current London bread and pastry guide — neighbourhood favourite with no way to reserve",
  "Unaudited. Single-focus shop: menu + hours + a notify-me line is the whole job",
  "londonyaar.com citing the FT", "2026-08-16"),
 ("The Bakery House", "Bryn Mawr / Paoli, PA", "US", "moderno", "croissant", "2", "multi-location + preorder", 2090, "A — hot",
  "37 years old and just OPENED A SECOND STOREFRONT (Paoli Village Shoppes, announced 25 Sep 2026); Philadelphia Magazine “Best Pie” 2024; custom cakes, croissants, chicken salad",
  "Unaudited. Two locations plus custom-cake enquiries is exactly the shape this kit serves",
  "patch.com — award-winning bakery opens new shop in Paoli", "2026-09-25"),
]

WAVE = {'US': 1, 'GB': 1, 'CA': 1, 'FR': 2, 'ES': 2, 'GR': 2, 'RE': 3}
VATS = {1: 'wave 1 - no VAT anywhere', 2: 'wave 2 - reverse charge + their VAT number'}

log = list(csv.DictReader(open('sales/OUTREACH-LOG.csv', newline='')))
lf = list(log[0].keys())
for r in log:
    if r['id'] in ('1', '6'):
        r['status'] = 'sent'
        r['channel'] = 'email'
        r['first_touch_date'] = '2026-10-11T09:12Z'
        r['next_action'] = 'follow-up day 5 if silent, once more at day 14, then stop'
        r['notes'] = ('SENT 2026-10-11 from abdulrhmant948@gmail.com with user approval. Personalised, verified facts '
                      'only, source + opt-out in the footer, price read from the Drive sheet. Reply check: npm run progress')

NEXT = max(int(r['id']) for r in rows)
for (b, city, c, tpl, pkg, langs, addons, price, prio, sig, note, src, sdate) in NEW:
    NEXT += 1
    r = {k: '' for k in fields}
    r.update(dict(id=str(NEXT), business=b, city=city, country=c, segment='independent / neighbourhood',
                  growth_signal_why_now=sig, web_presence_note=note, recommended_template=tpl, package=pkg,
                  languages=langs, addons=addons, quote_eur=str(price), quote_usd=str(round(price * 1.09)),
                  care_eur_per_month='45', first_year_value_eur=str(price + 540), discount_pct='0', priority=prio,
                  contact_channel='to find: site footer / Instagram bio / Google Business listing',
                  verification='NOT YET VERIFIED — press-list only (2026-10-11)',
                  verification_2026_10_10='NOT YET VERIFIED 2026-10-11 — new from press lists; open their site, Instagram and Google listing before any message',
                  site_found='', contact_verified='', audit_note=note,
                  pitch_angle='Award / expansion moment vs what their own page can do with it',
                  source=src, source_date=sdate,
                  tax_wave=('1 - send freely (no VAT anywhere)' if WAVE[c] == 1 else '2 - reverse charge + VAT number'),
                  vat_note=VATS[WAVE[c]]))
    rows.append(r)
    log.append(dict({k: '' for k in lf}, **dict(id=str(NEXT), business=b, status='to-verify', channel='unknown',
                 next_action='4-min check (site, Google Business, IG bio) then a personalised draft',
                 notes='Added 2026-10-11 from current award/expansion coverage. NOT verified.', quoted_eur=str(price),
                 source_of_address=src + ' ' + sdate, suppression_list='no')))

with open(p, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
json.dump(rows, open('sales/prospects-2026.json', 'w'), ensure_ascii=False, indent=1)
with open('sales/OUTREACH-LOG.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=lf); w.writeheader(); w.writerows(log)
print('leads:', len(rows), '| log rows:', len(log), '| new ids:', [r['id'] for r in rows[-7:]])

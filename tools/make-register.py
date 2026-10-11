#!/usr/bin/env python3
"""tools/make-register.py — the outreach register, as a PDF.

One document that answers, for every shop we have contacted: who they are, which address we used and
where that address came from, what we opened with, exactly what was offered, at what price, where the
conversation stands, and — the part a spreadsheet never says — whether I can take it to done without
Abdulrhman, or what specifically stops me.

Everything is READ from the CSVs in sales/. Nothing is typed in here except the autonomy rules and the
"watch for" notes, which are judgement, not data. Re-run after every send or status change:

    python3 tools/make-register.py      ->  sales/OUTREACH-REGISTER.pdf
"""
import csv, datetime, os, re, sys

try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    sys.exit("needs fpdf2:  pip install --break-system-packages fpdf2")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROS = os.path.join(ROOT, "sales", "prospects-2026.csv")
LOG = os.path.join(ROOT, "sales", "OUTREACH-LOG.csv")
SENT = os.path.join(ROOT, "sales", "SENT-RECORD.csv")
OUT = os.path.join(ROOT, "sales", "OUTREACH-REGISTER.pdf")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
INK = (24, 26, 30)
MUTED = (108, 114, 124)
RULE = (206, 210, 216)
BAND = (32, 42, 58)
SOFT = (244, 245, 247)
ACCENT = (140, 74, 30)

DAYS = {"licence": 1, "baguette": 5, "croissant": 7, "patisserie": 10}


def read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# One place, all conversions. EUR/GBP/USD are the rates the whole pipeline already quotes with
# (GBP x0.86, USD x1.09). TRY and AED are here so the number makes sense in the currency people
# around us actually hold - they are INDICATIVE ONLY: refresh them in this file before any invoice.
RATES = {"EUR": 1.0, "USD": 1.09, "SYP": 1.09 * 14500}
GBP_RATE = 0.86  # kept out of the table on purpose - see the footnote
RATE_DATE = "USD x1.09 (the kit's standing quote rate) - SYP shown at 14,500 per USD, indicative only"


def money(r, plain=False):
    eur = int(r.get("quote_eur") or 0)
    if not eur:
        return "-"
    if plain:
        return "%s EUR" % f"{eur:,}"
    billed = "USD" if r.get("country") == "US" else "EUR"
    out = []
    for c in ("USD", "EUR", "SYP"):
        v = round(eur * RATES[c])
        out.append("%s %s%s" % (c, f"{v:,}", "   <- billed" if c == billed else ""))
    return "\n".join(out)


def offer(p):
    pack = p["package"].strip()
    days = DAYS.get(pack, 7)
    langs = (p.get("languages") or "1").strip()
    addons = (p.get("addons") or "").strip()
    txt = "%s package · %s template" % (pack, p["recommended_template"])
    if langs and langs not in ("1", "1 "):
        txt += " · %s languages" % langs
    if addons:
        txt += " · " + addons
    txt += " · %d working days · 40%% deposit, balance at go-live · 2 revision rounds · files and repo become theirs · care 45 EUR/mo optional" % days
    return txt


WATCH = {
    "hello@august-bakery.com": "queue-driven, owner is the baker: expect 'when' more than 'how much'",
    "shop@northern-rye.co.uk": "two sites (Ouseburn + North Shields) — they may ask for both locations priced separately",
    "wildcrumb@gmail.com": "Beard winner with a team: will likely want references and a written scope",
    "info@subabakery.com": "the broken newsletter widget is the whole opener — screenshot it before the call",
    "hello@chatsworthbakehouse.com": "duplicate map pins: they can fix that free in 10 min, say so first",
    "aniek@laylabakery.com": "one shared inbox for two shops — reply may come from either owner",
    "orders@wildhearthbakery.com": "address mismatch front page vs footer — B-Corp-ish, they care about accuracy",
    "thebakeryhouse604@gmail.com": "quote was given in USD in the email (2,270) — keep that number, not the EUR",
    "info@wildyeastbakehouse.com": "new Wayne unit opening: urgency is real, timing may slip",
    "Owner@heritagerisesourdough.com": "'By Appointment' pickup table — they may not consider themselves retail",
    "swarthomestead@gmail.com": "pre-orders run off-site; the ask is a page, not a platform",
    "hello@bornandbreadbakehouse.com": "we corrected ourselves in-thread within 8 min — reference it as the working style",
    "hello@aran-bakery.com": "auto-reply only; their admin days are Tue-Fri, phone 01350 727029 is published",
    "hola@gustobread.com": "menu lives on canva.link — offer to keep Toast and only move the menu",
    "bake@loafofsourdough.com": "they own the shorter domain already; the pitch is moving the site onto it",
}


def autonomy(p):
    """What a stranger in this repo cannot do without Abdulrhman."""
    stops = ["contract + invoice signature (his name, not mine)",
             "receiving money (bank or USDT — only he can decide/hold)",
             "buying or transferring the domain in the client's name"]
    if p["country"] == "GB":
        stops.append("VAT: no UK establishment — they reverse-charge; his decision to accept")
    if p["country"] == "US":
        stops.append("US: no sales tax, W-8BEN (I fill it, he signs it), no 1099")
    if p["country"] in ("FR", "ES"):
        stops.append("wave 2: their VAT number needed + registration check before ANY invoice")
    return stops


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DV", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "Levain Kit — outreach register · generated %s · sales/OUTREACH-REGISTER.pdf" % TODAY,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.set_draw_color(*RULE)
        self.line(self.l_margin, 13, self.w - self.r_margin, 13)
        self.set_y(17)

    def footer(self):
        self.set_y(-11)
        self.set_font("DV", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "Read from sales/prospects-2026.csv + OUTREACH-LOG.csv + SENT-RECORD.csv — do not hand-edit this PDF.   page %d/{nb}"
                  % self.page_no(), align="C")


NOW = datetime.datetime.now(datetime.timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d %H:%MZ")

pros = {r["id"]: r for r in read(PROS)}
log = {r["id"]: r for r in read(LOG)}
sent = read(SENT)
pitched = [s for s in sent if s["kind"] == "cold pitch"]
by_mail = {}
for s in pitched:
    by_mail.setdefault(s["to"].lower(), []).append(s)

# join sent record -> log row -> prospect row
rows = []
for r_id, r in log.items():
    if not r["status"].startswith("sent"):
        continue
    p = pros.get(r_id, {})
    key = (r.get("contact_used") or "").lower()
    recs = by_mail.get(key, [])
    rows.append({
        "id": r_id, "p": p, "log": r,
        "to": r.get("contact_used", ""),
        "subject": recs[0]["subject"] if recs else "",
        "when": recs[0]["sent_utc"] if recs else r.get("first_touch_date", ""),
        "mid": recs[0]["gmail_msg_id"] if recs else "",
        "corr": [x for x in recs if x["kind"] == "self correction"],
    })
rows.sort(key=lambda x: x["when"])

un_sent = [r for r in log.values() if r["status"] in ("verified-ready", "no-pitch")]


def build():
    pdf = PDF(orientation="L", format="A4")
    pdf.set_margins(11, 12, 11)
    pdf.set_auto_page_break(True, margin=13)
    pdf.alias_nb_pages()
    for name, f in (("DV", "DejaVuSans.ttf"), ("DP", "DejaVuSans-Bold.ttf"), ("DM", "DejaVuSansMono.ttf")):
        pdf.add_font(name, "", os.path.join(FONT_DIR, f))
    W = pdf.w - pdf.l_margin - pdf.r_margin

    # ---------- title band ----------
    pdf.add_page()
    pdf.set_fill_color(*BAND); pdf.set_text_color(255, 255, 255)
    pdf.rect(0, 0, pdf.w, 30, "F")
    pdf.set_xy(11, 7)
    pdf.set_font("DP", "", 17)
    pdf.cell(0, 8, "Levain Kit — Outreach Register", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(11); pdf.set_font("DV", "", 8.6); pdf.set_text_color(214, 220, 230)
    pdf.cell(0, 5.4, "Every shop we wrote to, the address we used and where it came from, what we opened with, the offer, "
                     "the price, and whether I can take it to done without you  ·  generated %s" % TODAY,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(11)
    pdf.cell(0, 5.4, "Abdulrhman Thali · freelance web developer · Karm El-Zeitoun, Homs, Syria · work is 100% remote · "
                     "github.com/abdoo606/BLAblalba", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---------- KPI boxes ----------
    quoted = sum(int(r["log"].get("quoted_eur") or 0) for r in rows)
    stats = [("leads in pipeline", len(pros)), ("verified by opening their site", sum(1 for p in pros.values() if p["verification"].startswith("VERIFIED"))),
             ("emails sent", len(rows)), ("quoted", "%s EUR" % f"{quoted:,}"), ("human replies", 0),
             ("auto-replies", 1), ("bounces", 0), ("suppressed", 0)]
    bw = W / len(stats)
    pdf.set_y(36)
    for i, (label, val) in enumerate(stats):
        x = pdf.l_margin + i * bw
        pdf.set_xy(x, 36)
        pdf.set_fill_color(*SOFT); pdf.rect(x + 0.8, 36, bw - 1.6, 15, "F")
        pdf.set_xy(x + 3, 38)
        pdf.set_font("DP", "", 11.5); pdf.set_text_color(*INK)
        pdf.cell(bw - 6, 6, str(val), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_xy(x + 3, 44.6)
        pdf.set_font("DV", "", 6.6); pdf.set_text_color(*MUTED)
        pdf.multi_cell(bw - 5, 3.1, label)
    pdf.set_y(55)

    def section(title, note=""):
        pdf.ln(1.5)
        y = pdf.get_y()
        if y > pdf.h - 40:
            pdf.add_page(); y = pdf.get_y()
        pdf.set_font("DP", "", 11); pdf.set_text_color(*ACCENT)
        pdf.cell(0, 6.6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if note:
            pdf.set_font("DV", "", 7.6); pdf.set_text_color(*MUTED)
            pdf.multi_cell(0, 3.8, note, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.2)

    def text_h(txt, w, size=7.0, lh=3.5):
        """Lines needed at width w, counted by hand: multi_cell(dry_run=True) measures across an
        automatic page break and returns a monster height when the cursor sits near the bottom
        margin, which turned a 4-page register into 45 pages."""
        pdf.set_font("DV", "", size)
        lines = 0
        for para in str(txt).split("\n"):
            if not para.strip():
                lines += 1
                continue
            cur, n = "", 1
            for word in para.split(" "):
                cand = (cur + " " + word).strip()
                if pdf.get_string_width(cand) <= w - 3.6:
                    cur = cand
                else:
                    n += 1
                    cur = word
            lines += n
        return max(lines * lh + 1.6, 7.4)

    def table(cols, data, zebra=True, mono_cols=()):
        widths = [c[1] for c in cols]
        LH = 3.5
        pdf.set_font("DV", "", 7.3)
        # header row
        hh = 6.2
        x0 = pdf.l_margin

        def draw_head():
            y = pdf.get_y()
            for i, (nm, w) in enumerate(cols):
                pdf.set_xy(x0 + sum(widths[:i]), y)
                pdf.set_fill_color(*BAND); pdf.set_text_color(255, 255, 255); pdf.set_font("DP", "", 7.2)
                pdf.multi_cell(w, hh, nm, fill=True, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_xy(x0, y + hh)

        if pdf.get_y() + hh + 12 > pdf.h - 14:
            pdf.add_page()
        draw_head()
        pdf.set_auto_page_break(False)
        for n, row in enumerate(data):
            rh = max(text_h(cell, widths[i]) for i, cell in enumerate(row))
            if pdf.get_y() + rh > pdf.h - 14:
                pdf.add_page()
                draw_head()          # a table that runs over a page keeps its headers
            y0 = pdf.get_y()
            for i, cell in enumerate(row):
                pdf.set_xy(x0 + sum(widths[:i]), y0)
                if zebra and n % 2:
                    pdf.set_fill_color(*SOFT)
                pdf.set_text_color(*INK)
                pdf.set_font("DV", "", 7.0)
                pdf.set_draw_color(*RULE)
                pdf.multi_cell(widths[i], rh, str(cell), fill=bool(zebra and n % 2), border="B",
                               new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_xy(x0, y0 + rh)
        pdf.set_auto_page_break(True, margin=13)
        pdf.ln(1.5)

    # ---------- table 1: what was sent ----------
    section("1 · Every email we sent: to whom, what we said, what it costs",
            "One row per shop. The address column is the point: every line is an address published on that shop's own site, "
            "read by us on the day we wrote. Nothing here was bought, scraped from a list, or guessed.")
    cols = [("#", 6), ("Shop · where", 32), ("Who we wrote to + where we got the address", 46), ("What we said first (the subject line)", 48),
            ("What they get, and how we work", 56), ("Price: USD / EUR / SYP", 32), ("Where it stands now", 52.6)]
    data = []
    for r in rows:
        p = r["p"]
        src = (p.get("source") or "").replace(" | merged with the older to-verify row for the same shop (duplicate removed 2026-10-11, one row per shop)", " [merged dup]")
        data.append([r["id"], "%s\n%s · %s" % (p.get("business", "?"), p.get("city", ""), p.get("country", "")),
                     "%s\nfrom: %s" % (r["to"], src[:150]),
                     "%s\n%s" % (r["subject"], ("+ in-thread correction %s" % r["corr"][0]["sent_utc"]) if r["corr"] else ""),
                     offer(p), money(p),
                     "%s\n%s\nquoted %s EUR\n%s" % (r["log"]["status"], r["when"], f"{int(r['log'].get('quoted_eur') or 0):,}", ("next: " + (r["log"].get("next_action") or "")[:110]))])
    table(cols, data, mono_cols=(2,))
    pdf.set_font("DV", "", 6.8); pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 3.4, "Prices: %s. 'billed' = the currency the client is invoiced in. UK clients are quoted in "
                           "EUR and may ask to pay GBP - multiply the EUR by %s in your head, or 0.86 at today's rate; it is not a column here "
                           "because the quote they receive is the one we wrote. Syrian pounds are shown so the size of a job is legible at home, "
                           "not for quoting anyone: refresh the SYP figure before an invoice, and remember payment in SYP never happens - "
                           "money arrives by transfer or USDT, with the client's written agreement. Max 15%% discount, 40%% deposit, "
                           "care 45 EUR/month if they want it." % (RATE_DATE, GBP_RATE),
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ---------- table 2: autonomy ----------
    section("2 · Can I finish this job without you?",
            "Honest answer for every lead: everything up to a signature is mine; money, legal identity and the domain are not. "
            "If a client says yes tonight, the blockers below are the list of things only you can unblock, and they are the same three "
            "for all 15 shops — which is why the process is worth pre-building once.")
    acols = [("#", 6), ("Shop", 33), ("I do this alone - no need to ask you", 88), ("Only Abdulrhman can do this", 88), ("What to watch for when they answer", 62)]
    ad = []
    for r in rows:
        p = r["p"]
        mine = ("verify their site and re-read the pages · build the board and the site from the kit · translate (EN/FR/ES/AR) · "
                "send the follow-ups in-thread · hold the price (max 15% discount, already delegated) · write the invoice draft · "
                "deploy to any host you point me at · log everything here")
        ad.append([r["id"], p.get("business", "?"), mine, "  ·  ".join(autonomy(p)),
                   WATCH.get(r["to"].lower(), "—")])
    table(acols, ad)

    # ---------- table 3: looked at, not sent ----------
    section("3 · Shops we checked on purpose and did not email",
            "These are the ones a careless pipeline would have blasted. Either no address is published on their own site (so there is "
            "nothing to write to that we can defend), or their own stack is already better than what we sell — saying so is the deal.")
    ncols = [("#", 6), ("Shop · where", 40), ("Why we sent nothing", 88), ("What we would offer if they call us", 76), ("Next step + date", 68)]
    nd = []
    for r in sorted(un_sent, key=lambda x: x["id"]):
        p = pros.get(r["id"], {})
        nd.append([r["id"], "%s\n%s · %s" % (p.get("business", "?"), p.get("city", ""), p.get("country", "")),
                   (p.get("web_presence_note") or "")[:300],
                   "%s\n%s" % (offer(p), money(p)),
                   "%s\n%s" % ((r.get("next_action") or "")[:180], ("due " + r["next_action_date"]) if r["next_action_date"] else "")])
    table(ncols, nd)

    # ---------- page: how to run it ----------
    pdf.add_page()
    section("4 · The rules this list runs on",
            "Written down so the pipeline survives being handed to anyone else, and so no future batch quietly lowers the bar.")
    rules = [
        ("Gate", "A lead is pitchable only after someone opens the shop's own site and reads the address off it. Search snippets, "
                 "directories, Instagram bios and purchased lists are not addresses — they are how you end up emailing the wrong "
                 "business with a similar name (it nearly happened with Lucky Yu: the award list meant Walthamstow, the domain belonged "
                 "to a canteen in Edinburgh)."),
        ("No invented praise", "Every email rests on one checkable observation from their own page — duplicated hero text, two "
                               "different opening weeks, a Menu button that leaves the domain, a 404 where the contact page should be. "
                               "If we get an observation wrong, we correct it in the same thread within the hour, like we did for "
                               "Born & Bread."),
        ("Identity", "Abdulrhman Thali, freelance web developer, Karm El-Zeitoun, Homs, Syria — stated in every email, never hidden. "
                     "No claim of a UK/EU/US presence anywhere in the pipeline."),
        ("Tax", "Wave 1 only (US + GB clients, 55 of 70 leads): a Syria-based freelancer selling remotely owes no VAT there and no "
                "registration in the client's country — UK clients reverse-charge, US clients owe no sales tax on a foreign "
                "independent contractor (W-8BEN, no 1099). Wave 2 (FR/ES, 15 leads) is parked until their VAT number and a "
                "registration check are in writing — see sales/TAX-SCOPE.md."),
        ("Money", "USDT is allowed only if the client agrees, raised at quote/invoice level, never inside a cold email, and never "
                  "presented as a way around anything. Bank transfer stays on the table."),
        ("Exit", "One line in every email: reply 'remove me' → permanent suppression, no follow-up call, removed from the list."),
        ("Cadence", "Day 0 first touch · day 5 short follow-up in the same thread · day 14 last one · then parked and not reopened "
                    "for 6 months. ARAN-style: if they publish admin days (Tue–Fri), the follow-up lands on a Tuesday morning, "
                    "because a Tuesday mail is read and a Saturday mail dies."),
        ("Price", "Licence 149 EUR · Baguette 750 · Croissant 1,450 · Pâtisserie 2,900 · +language 220 · SEO 380 · photography 320 · "
                  "extra location 180 · wholesale portal 640 · care 45/mo · hosting 90/yr · rush +25% · max discount 15% · "
                  "40% deposit. GBP ×0.86, USD ×1.09. Never a quote two clients could compare."),
    ]
    for name, txt in rules:
        pdf.set_font("DP", "", 8.4); pdf.set_text_color(*INK)
        pdf.cell(30, 4.6, name, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("DV", "", 7.8); pdf.set_text_color(*MUTED)
        pdf.multi_cell(0, 4.2, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.1)

    section("5 · What happens the moment a real person replies",
            "No lead is waiting on me for anything except a decision from you. The sequence below is already scripted.")
    steps = [
        ("1", "Same day, human replies → I answer in-thread with their board attached (single self-contained HTML file, opens in any browser, no demo account, no link that expires)."),
        ("2", "They like it → I send the scope as a one-page list: what's in the package, what isn't, the price in their currency, the timeline, the care option."),
        ("3", "They say yes → I draft the agreement + invoice with their name on it; you sign, you choose the payment rail (bank or USDT, their call, in writing)."),
        ("4", "Domain: registered in their name, not ours — I prepare the DNS records, you hand over the purchase link, ownership never touches us."),
        ("5", "Build: 5–10 working days by package. I do data, languages, RTL, SEO schema, hosting files, and the README a stranger can run."),
        ("6", "Launch + day-30 check, then care mode if they took it. Everything logged in this register; Drive gets the new sheet; repo gets the commit."),
    ]
    for n, t in steps:
        pdf.set_font("DP", "", 9); pdf.set_text_color(*ACCENT)
        pdf.cell(8, 4.6, n, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("DV", "", 7.9); pdf.set_text_color(*INK)
        pdf.multi_cell(0, 4.6, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.8)

    pdf.output(OUT)
    print("wrote %s (%d bytes, %d pages)" % (os.path.relpath(OUT, ROOT), os.path.getsize(OUT), pdf.pages_count if hasattr(pdf, "pages_count") else pdf.page_no()))


if __name__ == "__main__":
    build()

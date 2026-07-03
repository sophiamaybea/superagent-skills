#!/usr/bin/env python3
"""build_page.py — turn harvested pain quotes into a "Keep The Cut" landing page.

Reddit blocks direct datacenter requests (403), so the AGENT harvests quotes via
its web_search/read_web_page tools and writes them to a quotes JSON file, then
runs this to render the page. This keeps generation deterministic + honest
(every quote carries its real source URL).

quotes JSON shape:
{ "niche":"salons", "town":"Golders Green", "villain":"Fresha",
  "cta":"https://wa.me/447847321961",
  "quotes":[ {"quote":"...", "subreddit":"UberEATS", "ups":320, "url":"https://reddit.com/..."} ] }
"""
import sys, os, json, html, re

NICHES = {
    "salons":      {"villains":["Fresha","Treatwell"],             "hook":"Ditch the 20%",        "cut":"20% on every new client"},
    "barbers":     {"villains":["Booksy","Fresha"],                "hook":"Ditch the fees",       "cut":"30% on the first appointment"},
    "restaurants": {"villains":["Deliveroo","Uber Eats","Just Eat"],"hook":"Keep the 30%",         "cut":"up to 38% per order"},
    "takeaways":   {"villains":["Just Eat","Uber Eats"],           "hook":"Keep the 30%",         "cut":"per-order commission"},
    "trades":      {"villains":["Checkatrade","MyBuilder"],        "hook":"Stop paying per lead", "cut":"pay-per-lead fees"},
    "clinics":     {"villains":["the marketplace"],                "hook":"Own your front door",  "cut":"lost private-patient revenue"},
}

def esc(s): return html.escape(s or "")

def build(cfg, niche, town, villain, quotes, cta):
    v0 = villain or cfg["villains"][0]
    hook, cut = cfg["hook"], cfg["cut"]
    singular = niche[:-1] if niche.endswith("s") else niche
    headline = f"{hook}: a {singular} website in {town} that {v0} can't touch"
    q5 = quotes[:5]
    md = f"""# {headline}

## The problem
{v0} takes {cut}. Worse — your only online presence is a {v0} profile that lists
your competitors one tap away, and AI search barely knows you exist. You're
paying to rent your own customers.

## What real owners actually say
""" + ("\n".join(f'> “{q["quote"]}” — r/{q.get("subreddit","reddit")} ({q.get("ups",0)}↑) {q.get("url","")}' for q in q5) or "> (add quotes)") + f"""

## Keep the calendar. Own the front door.
A fast, mobile-first {niche} site for {town} that ranks for your services, feeds
Google + AI search, and takes bookings commission-free — so a Google click
becomes a booked slot without {v0} taking {cut}.

## {hook}
I'm a London-based designer. Free 2-minute mockup of your {town} booking page,
no obligation.

CTA → {cta}

_Keep The Cut · by Studio Bea Sophia_
"""
    proof = "\n".join(
        f'  <blockquote>“{esc(q["quote"])}”<cite>r/{esc(q.get("subreddit","reddit"))} · {q.get("ups",0)}↑</cite></blockquote>'
        for q in q5) or "  <p>(add quotes)</p>"
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(headline)} | Keep The Cut</title>
<meta name="description" content="{esc(hook)} — a commission-free {esc(niche)} booking website in {esc(town)}. Stop paying {esc(cut)} to {esc(v0)}.">
<style>
body{{font-family:Georgia,serif;max-width:740px;margin:0 auto;padding:2.5rem 1.4rem;color:#111;line-height:1.55}}
h1{{font-size:2rem;line-height:1.15}} h2{{margin-top:2.2rem;color:#5b6ef5}}
blockquote{{border-left:3px solid #f07d1a;margin:1rem 0;padding:.4rem 1rem;background:#faf7f2;font-style:italic}}
cite{{display:block;font-size:.8rem;color:#666;font-style:normal;margin-top:.3rem}}
.cta{{display:inline-block;margin-top:1.6rem;background:#f07d1a;color:#fff;padding:.9rem 1.6rem;border-radius:8px;text-decoration:none;font-family:sans-serif;font-weight:bold}}
.hook{{font-family:sans-serif;font-weight:bold;color:#f07d1a}}
</style></head><body>
<p class="hook">{esc(hook)}</p>
<h1>{esc(headline)}</h1>
<h2>The problem</h2>
<p>{esc(v0)} takes <strong>{esc(cut)}</strong>. Worse — your only online presence is a
{esc(v0)} profile that lists your competitors one tap away, and AI search barely
knows you exist. You're paying to rent your own customers.</p>
<h2>What real owners actually say</h2>
{proof}
<h2>Keep the calendar. Own the front door.</h2>
<p>A fast, mobile-first {esc(niche)} site for {esc(town)} that ranks for your services,
feeds Google + AI search, and takes bookings commission-free.</p>
<a class="cta" href="{esc(cta)}">Send me a free mockup →</a>
<p style="margin-top:2.5rem;font-family:sans-serif;font-size:.8rem;color:#999">Keep The Cut · by Studio Bea Sophia</p>
</body></html>"""
    return md, page

def main():
    if len(sys.argv) < 2:
        print("usage: build_page.py <quotes.json> [out_dir]"); sys.exit(1)
    data = json.load(open(sys.argv[1]))
    out = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/keepthecut_{data.get('niche','x')}"
    niche = data.get("niche","salons").lower()
    cfg = NICHES.get(niche, NICHES["salons"])
    town = data.get("town","your town")
    villain = data.get("villain")
    cta = data.get("cta","https://wa.me/447847321961")
    quotes = data.get("quotes", [])
    os.makedirs(out, exist_ok=True)
    md, page = build(cfg, niche, town, villain, quotes, cta)
    open(f"{out}/page.md","w").write(md)
    open(f"{out}/page.html","w").write(page)
    print(f"✓ {len(quotes)} quotes → landing page")
    print(f"✓ {out}/page.md")
    print(f"✓ {out}/page.html")

if __name__ == "__main__":
    main()

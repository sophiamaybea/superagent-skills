#!/usr/bin/env python3
"""pain-scraper — mine Reddit for marketplace pain, emit Keep The Cut landing pages.

Free: uses Reddit's public .json search endpoints (no API key). Polite UA + delay.
"""
import sys, os, json, re, time, html, urllib.request, urllib.parse

NICHES = {
    "salons":      {"villains": ["Fresha", "Treatwell"],            "hook": "Ditch the 20%",       "cut": "20% on every new client",
                    "subs": ["Esthetics","BehindTheChair","smallbusinessuk","eyelashextensions","hairstylist"],
                    "terms": ["fresha commission","fresha fees","fresha expensive","treatwell commission","salon booking fees"]},
    "barbers":     {"villains": ["Booksy", "Fresha"],               "hook": "Ditch the fees",      "cut": "booking fees + commission",
                    "subs": ["Barber","smallbusinessuk","smallbusiness"],
                    "terms": ["booksy fees","booksy commission","barber booking software expensive"]},
    "restaurants": {"villains": ["Deliveroo","Uber Eats","Just Eat"],"hook": "Keep the 30%",       "cut": "up to 30% per order",
                    "subs": ["restaurateur","smallbusinessuk","KitchenConfidential","smallbusiness"],
                    "terms": ["deliveroo commission","just eat fees","uber eats 30%","delivery app commission restaurant"]},
    "takeaways":   {"villains": ["Just Eat","Uber Eats"],           "hook": "Keep the 30%",        "cut": "per-order commission",
                    "subs": ["smallbusinessuk","takeaway","smallbusiness"],
                    "terms": ["just eat commission takeaway","uber eats fees takeaway"]},
    "trades":      {"villains": ["Checkatrade","MyBuilder"],        "hook": "Stop paying per lead","cut": "pay-per-lead fees",
                    "subs": ["smallbusinessuk","Tradesmen","plumbing","electricians"],
                    "terms": ["checkatrade fees","mybuilder leads expensive","pay per lead trades"]},
}

# High-signal pain phrases — a quote scores higher if it contains these.
PAIN = ["commission","20%","30%","fees","fee","held","payout","held payout","deceptively expensive",
        "greedy","expensive","buried","can't cancel","cant cancel","rip off","ripoff","scam","charged",
        "hidden","per staff","per member","hostage","own customers","lock","subscription"]

UA = "Mozilla/5.0 (compatible; StudioBeaSophia-research/1.0; +https://studiobeasophia.com)"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def clean(t):
    t = html.unescape(t or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def score_text(t):
    tl = t.lower()
    return sum(2 if p in tl else 0 for p in PAIN)

def harvest(niche):
    cfg = NICHES[niche]
    seen, quotes = set(), []
    # 1) global search per term  2) subreddit-scoped search
    urls = []
    for term in cfg["terms"]:
        q = urllib.parse.quote(term)
        urls.append(f"https://www.reddit.com/search.json?q={q}&sort=relevance&limit=25&t=year")
        for sub in cfg["subs"][:3]:
            urls.append(f"https://www.reddit.com/r/{sub}/search.json?q={q}&restrict_sr=1&sort=top&limit=15&t=all")
    for u in urls:
        try:
            data = fetch(u)
        except Exception as e:
            sys.stderr.write(f"  skip {u[:60]}: {e}\n"); time.sleep(1); continue
        for c in data.get("data", {}).get("children", []):
            d = c.get("data", {})
            pid = d.get("id")
            if pid in seen: continue
            seen.add(pid)
            title = clean(d.get("title"))
            body  = clean(d.get("selftext"))[:600]
            text  = (title + " — " + body).strip(" —")
            sc = score_text(text) + min(d.get("ups", 0) // 20, 6)
            if score_text(text) >= 4 and len(text) > 25:
                quotes.append({
                    "quote": text[:400],
                    "score": sc,
                    "ups": d.get("ups", 0),
                    "subreddit": d.get("subreddit"),
                    "url": "https://reddit.com" + d.get("permalink", ""),
                })
        time.sleep(0.8)  # polite
    quotes.sort(key=lambda x: -x["score"])
    # dedupe near-identical
    out, sigs = [], set()
    for qz in quotes:
        sig = qz["quote"][:60].lower()
        if sig in sigs: continue
        sigs.add(sig); out.append(qz)
    return out[:12]

def esc(s): return html.escape(s or "")

def build_page(niche, town, cfg, quotes, cta):
    villains = " / ".join(cfg["villains"])
    hook = cfg["hook"]; cut = cfg["cut"]
    v0 = cfg["villains"][0]
    headline = f"{hook}: a {niche[:-1] if niche.endswith('s') else niche} website in {town} that {v0} can't touch"
    proof = "\n".join(
        f'  <blockquote>“{esc(q["quote"])}” <cite>r/{esc(q["subreddit"])} · {q["ups"]}↑</cite></blockquote>'
        for q in quotes[:5]) or "  <p>(run again — no quotes harvested this pass)</p>"
    md = f"""# {headline}

## The problem
{v0} takes {cut}. Worse — your only online presence is a {v0} profile that lists
your competitors one tap away, and AI search barely knows you exist. You're
paying to rent your own customers.

## What real owners say (from Reddit, {town} & beyond)
""" + "\n".join(f'> “{q["quote"]}” — r/{q["subreddit"]} ({q["ups"]}↑) {q["url"]}' for q in quotes[:5]) + f"""

## Keep The Cut
Keep the calendar if you like it. Own the front door.
A fast, mobile-first {niche} site for {town} that ranks for your treatments in
your town, feeds Google + AI search, and takes bookings commission-free — so a
Google click becomes a booked slot without {v0} taking {cut}.

## {hook}
I'm a London-based designer. I'll send you a free 2-minute mockup of your
{town} booking page — no obligation.

CTA: {cta}
"""
    page_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(headline)} | Keep The Cut</title>
<meta name="description" content="{esc(hook)} — a commission-free {niche} booking website in {town}. Stop paying {esc(cut)} to {esc(v0)}.">
<style>
body{{font-family:Georgia,serif;max-width:740px;margin:0 auto;padding:2.5rem 1.4rem;color:#111;line-height:1.55}}
h1{{font-size:2rem;line-height:1.15;color:#111}} h2{{margin-top:2.2rem;color:#5b6ef5}}
blockquote{{border-left:3px solid #f07d1a;margin:1rem 0;padding:.4rem 1rem;background:#faf7f2;font-style:italic}}
cite{{display:block;font-size:.8rem;color:#666;font-style:normal;margin-top:.3rem}}
.cta{{display:inline-block;margin-top:1.6rem;background:#f07d1a;color:#fff;padding:.9rem 1.6rem;border-radius:8px;text-decoration:none;font-family:sans-serif;font-weight:bold}}
.hook{{font-family:sans-serif;font-weight:bold;color:#f07d1a;letter-spacing:.02em}}
</style></head><body>
<p class="hook">{esc(hook)}</p>
<h1>{esc(headline)}</h1>
<h2>The problem</h2>
<p>{esc(v0)} takes <strong>{esc(cut)}</strong>. Worse — your only online presence is a
{esc(v0)} profile that lists your competitors one tap away, and AI search barely knows
you exist. You're paying to rent your own customers.</p>
<h2>What real owners say</h2>
{proof}
<h2>Keep the calendar. Own the front door.</h2>
<p>A fast, mobile-first {esc(niche)} site for {esc(town)} that ranks for your treatments,
feeds Google + AI search, and takes bookings commission-free.</p>
<a class="cta" href="{esc(cta)}">Send me a free mockup →</a>
<p style="margin-top:2.5rem;font-family:sans-serif;font-size:.8rem;color:#999">Keep The Cut · by Studio Bea Sophia</p>
</body></html>"""
    return md, page_html

def main():
    args = sys.argv[1:]
    if not args:
        print("usage: run.py <niche> \"<town>\" [--villain X] [--out DIR] [--max N] [--cta URL]"); sys.exit(1)
    niche = args[0].lower()
    if niche not in NICHES:
        print(f"unknown niche '{niche}'. options: {', '.join(NICHES)}"); sys.exit(1)
    town = "your town"; out = f"/tmp/pain_{niche}"; cta = "https://wa.me/447847321961"
    rest = args[1:]
    pos = [a for a in rest if not a.startswith("--")]
    if pos: town = pos[0]
    def opt(name, default):
        if name in rest:
            i = rest.index(name)
            return rest[i+1] if i+1 < len(rest) else default
        return default
    out = opt("--out", out); cta = opt("--cta", cta)
    cfg = dict(NICHES[niche])
    vil = opt("--villain", None)
    if vil: cfg["villains"] = [vil.title()] + [v for v in cfg["villains"] if v.lower()!=vil.lower()]

    os.makedirs(out, exist_ok=True)
    sys.stderr.write(f"[pain-scraper] niche={niche} town={town} villains={cfg['villains']}\n")
    quotes = harvest(niche)
    sys.stderr.write(f"[pain-scraper] harvested {len(quotes)} high-signal pain quotes\n")
    json.dump({"niche": niche, "town": town, "villains": cfg["villains"], "quotes": quotes},
              open(f"{out}/pain.json","w"), indent=2)
    md, page_html = build_page(niche, town, cfg, quotes, cta)
    open(f"{out}/page.md","w").write(md)
    open(f"{out}/page.html","w").write(page_html)
    print(f"\n✓ {len(quotes)} pain quotes → {out}/pain.json")
    print(f"✓ landing page → {out}/page.md  +  {out}/page.html")
    print(f"\n--- top 3 quotes ---")
    for q in quotes[:3]:
        print(f"  [{q['ups']}↑ r/{q['subreddit']}] {q['quote'][:120]}")

if __name__ == "__main__":
    main()

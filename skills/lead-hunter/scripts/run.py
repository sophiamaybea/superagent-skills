#!/usr/bin/env python3
"""
lead-hunter — the full Studio Bea Sophia lead pipeline in ONE command.

Pipeline:
  1. SEARCH   Google Maps for a niche + location (GmapsScraper.io, 2 credits/search)
  2. DEDUPE   drop duplicates + obvious chains + very-low-rated strugglers
  3. DIAGNOSE each business's website for free: dead / no-site / third-party-only /
              template (Wix/Squarespace/GoDaddy) / has-booking
  4. SCORE    0-100 composite using the four pillars, with a rating boost for
              busy-but-invisible businesses (high stars + weak web = strong lead)
  5. ENRICH   for real sites with no API email, crawl the site for a contact email (free)
  6. EMIT     write a leads.json the agent can push straight into the CRM,
              plus a scannable stdout table

This does NOT write to the CRM itself (the agent does that via create_entity_records
so records go through row-level security). It produces clean, scored, de-duped,
email-enriched lead objects ready to insert.

Usage:
  python3 run.py "hair salon in Golders Green London" [more "queries"...] \
      --out /tmp/run --min-score 62 --max-crawl 20

Env: GMAPS_SCRAPER_API_KEY
"""
import os, sys, re, csv, json, time, argparse, urllib.request, urllib.parse, ssl

API = "https://gmapsscraper.io/api/v1"
UA = "Mozilla/5.0 (compatible; StudioBeaSophia-LeadBot/1.0)"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]{2,64}@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,24}\b")
JUNK = ("example.com","sentry.io","wix.com","wixpress.com","godaddy.com","squarespace.com",
        "wixstatic","parastorage","cloudflare","gstatic","schema.org","w3.org",".png",".jpg",
        ".jpeg",".gif",".webp",".svg",".js",".css",".min",".max",".now",".push",".length",
        ".prototype",".hash",".href",".reload",".register",".substring",".vst",".uag","@2x",
        "@a.","@er.","@or.","@e.","yourdomain","email@","name@","user@","migr@","templ@",
        "separ@","anim@","regener@","loc@","navig@","d@a","st@","m@h","ud@","formd@","transl@",
        "public@","hbspt","targetedcontent")
CONTACT_PATHS = ["contact","contact-us","contactus","about","about-us","get-in-touch","book","booking"]
THIRD_PARTY = ("treatwell","booksy","facebook","instagram","alleatapp","eathome","justeat",
               "deliveroo","fresha","ubereats")
CHAINS = ("caffe nero","caffè nero","starbucks","costa","greggs","pret","mcdonald","kfc",
          "subway","domino","nando","pizza express","wagamama","gail","leon")


def _post(path, body):
    req = urllib.request.Request(f"{API}{path}", data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json",
                 "Authorization":f"Bearer {os.environ.get('GMAPS_SCRAPER_API_KEY','')}"}, method="POST")
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.load(r)


def _get(path, raw=False):
    req = urllib.request.Request(f"{API}{path}",
        headers={"Authorization":f"Bearer {os.environ.get('GMAPS_SCRAPER_API_KEY','')}"})
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        d = r.read()
    return d if raw else json.loads(d)


def credits_left():
    try: return _get("/credits").get("credits","?")
    except Exception: return "?"


def search(keywords):
    job = _post("/scrape", {"keywords":[keywords],"lang":"en","email":True})
    jid = job.get("id")
    if not jid: raise RuntimeError(f"no job id: {job}")
    for _ in range(40):
        time.sleep(6)
        if _get(f"/jobs/{jid}").get("status") == "complete": break
    rows = list(csv.DictReader(_get(f"/jobs/{jid}/download", raw=True).decode("utf-8","ignore").splitlines()))
    return rows


def clean_emails(text):
    out = []
    for m in EMAIL_RE.findall(text or ""):
        m = m.strip().lower().rstrip(".")
        if any(j in m for j in JUNK): continue
        if m not in out: out.append(m)
    return out


def deobf(text):
    t = re.sub(r'\s*[\[\(\{]\s*(?:at|AT)\s*[\]\)\}]\s*', '@', text)
    t = re.sub(r'\s*[\[\(\{]\s*(?:dot|DOT)\s*[\]\)\}]\s*', '.', t)
    return t


def fetch(url, timeout=8):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":UA})
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.read(200000).decode("utf-8","ignore")
    except Exception:
        return ""


def is_third_party(url):
    return any(tp in (url or "").lower() for tp in THIRD_PARTY)


def crawl_email(website):
    if not website: return []
    if not website.startswith("http"): website = "http://" + website
    p = urllib.parse.urlparse(website); base = f"{p.scheme}://{p.netloc}"
    home = fetch(base); seen = []; deadline = time.time() + 18
    links = re.findall(r'href=["\']([^"\']+)["\']', home, re.I)
    disc = [l if l.startswith("http") else base + l for l in links
            if any(k in l.lower() for k in ("contact","about","get-in-touch"))][:4]
    for url in [base] + [f"{base}/{p}" for p in CONTACT_PATHS] + disc:
        if time.time() > deadline: break
        html = home if url == base else fetch(url)
        if not html: continue
        mailtos = re.findall(r'mailto:([^"\'>\s?]+)', html, re.I)
        for e in clean_emails(" ".join(mailtos) + " " + deobf(html)):
            if e not in seen: seen.append(e)
        if seen: break
    return seen


def diagnose(url):
    if not url: return ("no website at all — invisible online", "no-site")
    if is_third_party(url):
        tp = next(t for t in THIRD_PARTY if t in url.lower())
        return (f"{tp} only, no owned site", "third-party")
    html = fetch(url)
    if not html: return ("website is dead/won't load", "dead")
    h = html.lower()
    # parked / coming-soon / for-sale domains — mid-transition, very receptive
    parked_markers = ("coming soon","under construction","site coming soon","launching soon",
                      "domain is for sale","buy this domain","parked free","this domain is parked",
                      "godaddy.com/domainsearch","future home of","website coming soon")
    if any(m in h for m in parked_markers) or len(html) < 1200:
        return ("site is a 'coming soon'/parked placeholder — no real site yet", "parked")
    plat = ""
    if "wix.com" in h or "wixstatic" in h: plat = "Wix"
    elif "squarespace" in h: plat = "Squarespace"
    elif "wordpress" in h or "wp-content" in h: plat = "WordPress"
    elif "godaddy" in h or "website builder" in h: plat = "GoDaddy-builder"
    insecure = url.lower().startswith("http://")  # no HTTPS — browsers warn, Google penalises
    booking = any(b in h for b in ("book now","book online","booking","appointment","reserve","fresha","booksy","treatwell"))
    thin = len(html) < 6000
    if thin:
        tag = f"{plat or 'thin'} near-empty page, no booking"
        return (tag + (" (no HTTPS)" if insecure else ""), "thin")
    if insecure:
        return (f"{plat or 'site'} loads over insecure http, no HTTPS", "insecure")
    if not booking: return (f"{plat or 'site'}, no online booking", "no-booking")
    return (f"{plat or 'custom'}, has booking", "has-booking")


def score(kind, rating):
    base = {"dead":88,"parked":86,"no-site":78,"third-party":74,"thin":72,"insecure":70,"no-booking":68,"has-booking":52}.get(kind,50)
    if base >= 68:
        if rating >= 4.8: base += 6
        elif rating >= 4.5: base += 3
    return min(base, 98)


ANGLE = {
 "dead":"Paying for a domain that doesn't load — every click is a lost customer.",
 "no-site":"You show up on Maps but have no site — customers can't find hours, prices or book.",
 "third-party":"Renting your presence on a third-party page — no owned home, paying commission.",
 "thin":"Site loads but it's near-empty with no way to book — enquiries leak to voicemail.",
 "no-booking":"Site loads but there's no way to book — enquiries leak to voicemail.",
 "parked":"The site is just a 'coming soon' placeholder — visitors assume you've closed down.",
 "insecure":"Site loads over insecure http — browsers flag it 'Not secure' and Google ranks it lower.",
 "has-booking":"Already has booking — only worth a design refresh.",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="+", help="one or more 'niche in location' queries")
    ap.add_argument("--out", default="/tmp/lead-hunter")
    ap.add_argument("--min-score", type=int, default=62)
    ap.add_argument("--max-crawl", type=int, default=20)
    ap.add_argument("--source", default="")
    a = ap.parse_args()
    if not os.environ.get("GMAPS_SCRAPER_API_KEY"): sys.exit("✗ GMAPS_SCRAPER_API_KEY not set")
    os.makedirs(a.out, exist_ok=True)
    src = a.source or f"lead-hunter {time.strftime('%Y-%m-%d')}"

    print(f"Credits before run: {credits_left()}  |  {len(a.queries)} search(es) = {len(a.queries)*2} credits")
    raw = {}
    for q in a.queries:
        print(f"→ {q!r}")
        try:
            for r in search(q):
                t = (r.get("title") or "").strip()
                if t and t not in raw: raw[t] = r
        except Exception as e:
            print(f"  ✗ search failed: {e}")
    print(f"  {len(raw)} unique businesses")

    leads = []; crawled = 0
    for t, r in raw.items():
        low = t.lower()
        if any(c in low for c in CHAINS): continue
        if "vape" in low: continue
        rating = float(r.get("review_rating") or 0)
        rev = int(r.get("review_count") or 0)
        if rating and rating < 3.0: continue  # struggling business, poor client fit
        web = (r.get("website") or "").strip()
        pain, kind = diagnose(web)
        s = score(kind, rating)
        if s < a.min_score: continue
        email = clean_emails(r.get("emails") or r.get("email") or "")
        if not email and kind in ("thin","no-booking","has-booking","dead") and web \
                and not is_third_party(web) and crawled < a.max_crawl:
            crawled += 1
            email = crawl_email(web)
        leads.append({
            "business_name": t,
            "website_url": web,
            "location": "", "borough": "",
            "business_type": r.get("category",""),
            "contact_phone": r.get("phone",""),
            "contact_email": email[0] if email else "",
            "pain_signals": pain,
            "why_good_fit": f"{rating}star" + (f", {rev} reviews" if rev else "") + f" — {kind}",
            "score": s,
            "priority": "A" if s >= 78 else ("B" if s >= 65 else "C"),
            "status": "new",
            "outreach_angle": ANGLE.get(kind,""),
            "source_run": src,
        })
    leads.sort(key=lambda x: -x["score"])
    json.dump(leads, open(os.path.join(a.out,"leads.json"),"w"), indent=1)

    with_email = sum(1 for l in leads if l["contact_email"])
    print(f"\n{'='*66}")
    print(f"{len(leads)} qualified leads | {with_email} with email ({crawled} crawled) | credits left: {credits_left()}")
    print(f"leads.json → {os.path.join(a.out,'leads.json')}")
    print(f"{'='*66}")
    for l in leads:
        print(f"  {l['score']:>2} {l['priority']}  {l['business_name'][:30]:<31} "
              f"{(l['contact_email'] or l['contact_phone'] or '—')[:28]:<28} {l['pain_signals'][:30]}")


if __name__ == "__main__":
    main()

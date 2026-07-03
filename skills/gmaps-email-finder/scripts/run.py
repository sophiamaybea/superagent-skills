#!/usr/bin/env python3
"""
gmaps-email-finder — search Google Maps for local businesses AND find their emails.

Two-stage email discovery:
  1. GmapsScraper.io API returns whatever emails it already knows (email:true).
  2. For any business with a website but NO email, crawl the site's own pages
     (home + likely contact/about pages) and extract emails for FREE — no API credits.

Usage:
  python3 run.py "keywords..." [--out DIR] [--no-crawl] [--max-crawl N]

Examples:
  python3 run.py "hair salon in Golders Green London"
  python3 run.py "independent cafe in Hendon London" --out /tmp/hendon
  python3 run.py "barber in West Hampstead London" --max-crawl 15

Env:
  GMAPS_SCRAPER_API_KEY  (required for the search stage; crawl stage is free)

Output:
  <out>/results.csv   full rows incl. an added `found_email` column
  prints a scannable summary to stdout
"""
import os, sys, re, csv, json, time, argparse, urllib.request, urllib.parse, ssl

API = "https://gmapsscraper.io/api/v1"
UA = "Mozilla/5.0 (compatible; StudioBeaSophia-LeadBot/1.0)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]{2,64}@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,24}\b")
# junk emails we never want (image filenames, placeholders, tracking)
JUNK = ("example.com", "sentry.io", "wix.com", "wixpress.com", "godaddy.com",
        "squarespace.com", "wixstatic", "parastorage", "cloudflare", "gstatic",
        "schema.org", "w3.org", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
        ".js", ".css", ".min", ".max", ".now", ".push", ".length", ".prototype",
        ".hash", ".href", ".reload", ".register", ".substring", ".vst", ".uag",
        "@2x", "@a.", "@er.", "@or.", "@e.", "yourdomain", "email@", "name@", "user@",
        "migr@", "templ@", "separ@", "anim@", "regener@", "loc@", "navig@", "d@a",
        "st@", "m@h", "ud@", "formd@", "transl@", "public@", "hbspt", "targetedcontent")
# pages likely to hold a contact email
CONTACT_PATHS = ["", "contact", "contact-us", "contactus", "about", "about-us",
                 "get-in-touch", "book", "booking", "appointments"]


def api_post(path, body):
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {os.environ.get('GMAPS_SCRAPER_API_KEY','')}"},
        method="POST")
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.load(r)


def api_get(path, raw=False):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={"Authorization": f"Bearer {os.environ.get('GMAPS_SCRAPER_API_KEY','')}"})
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        data = r.read()
    return data if raw else json.loads(data)


def credits_left():
    try:
        return api_get("/credits").get("credits", "?")
    except Exception:
        return "?"


def run_search(keywords):
    print(f"→ Searching Google Maps: {keywords!r}  (costs 2 credits)")
    job = api_post("/scrape", {"keywords": [keywords], "lang": "en", "email": True})
    jid = job.get("id")
    if not jid:
        sys.exit(f"✗ No job id returned: {job}")
    print(f"  job {jid} created — {job.get('credits_remaining','?')} credits left. Polling…")
    for _ in range(40):
        time.sleep(6)
        st = api_get(f"/jobs/{jid}").get("status")
        if st == "complete":
            break
        print(f"  status={st}…")
    csv_bytes = api_get(f"/jobs/{jid}/download", raw=True)
    rows = list(csv.DictReader(csv_bytes.decode("utf-8", "ignore").splitlines()))
    print(f"  ✓ {len(rows)} businesses returned")
    return rows


def clean_emails(text):
    out = []
    for m in EMAIL_RE.findall(text or ""):
        m = m.strip().lower().rstrip(".")
        if any(j in m for j in JUNK):
            continue
        if m not in out:
            out.append(m)
    return out



def deobfuscate(text):
    """Catch 'info [at] domain [dot] com' style obfuscation."""
    t = text
    # ONLY bracketed obfuscation: "info [at] x [dot] com" / "(at)" / "{at}"
    t = re.sub(r'\s*[\[\(\{]\s*(?:at|AT)\s*[\]\)\}]\s*', '@', t)
    t = re.sub(r'\s*[\[\(\{]\s*(?:dot|DOT)\s*[\]\)\}]\s*', '.', t)
    return t


def discover_contact_links(html, base):
    """Find real contact/about links on the page instead of guessing paths."""
    links = re.findall(r'href=["\']([^"\']+)["\']', html, re.I)
    good = []
    for h in links:
        low = h.lower()
        if any(k in low for k in ("contact", "about", "get-in-touch", "reach")):
            if h.startswith("http"):
                good.append(h)
            elif h.startswith("/"):
                good.append(base + h)
    # dedupe, cap
    out = []
    for g in good:
        if g not in out:
            out.append(g)
    return out[:4]


def fetch(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.read(200000).decode("utf-8", "ignore")
    except Exception:
        return ""


def crawl_site_for_email(website):
    """Visit the site's home + likely contact pages, return first good email(s)."""
    if not website:
        return []
    website = website.strip()
    if not website.startswith("http"):
        website = "http://" + website
    p = urllib.parse.urlparse(website)
    base = f"{p.scheme}://{p.netloc}"
    seen = []
    deadline = time.time() + 20  # hard 20s budget per site
    home = fetch(base, timeout=8)
    # build the list of pages to check: home, guessed paths, AND real discovered links
    to_check = [base] + [f"{base}/{p}" for p in CONTACT_PATHS if p]
    to_check += discover_contact_links(home, base)
    checked = set()
    for url in to_check:
        if time.time() > deadline:
            break
        if url in checked:
            continue
        checked.add(url)
        html = home if url == base else fetch(url, timeout=8)
        if not html:
            continue
        mailtos = re.findall(r'mailto:([^"\'>\s?]+)', html, re.I)
        blob = " ".join(mailtos) + " " + deobfuscate(html)
        for e in clean_emails(blob):
            if e not in seen:
                seen.append(e)
        if seen:
            break
    return seen


def is_third_party(url):
    low = (url or "").lower()
    return any(tp in low for tp in
               ("treatwell", "booksy", "facebook", "instagram", "alleatapp",
                "eathome", "justeat", "deliveroo", "fresha", ".booksy.com"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords")
    ap.add_argument("--out", default="/tmp/gmaps-email-finder")
    ap.add_argument("--no-crawl", action="store_true",
                    help="skip the free website-crawl stage")
    ap.add_argument("--max-crawl", type=int, default=25,
                    help="max sites to crawl for emails")
    a = ap.parse_args()

    if not os.environ.get("GMAPS_SCRAPER_API_KEY"):
        sys.exit("✗ GMAPS_SCRAPER_API_KEY not set.")

    os.makedirs(a.out, exist_ok=True)
    rows = run_search(a.keywords)

    crawled = 0
    for r in rows:
        api_email = (r.get("emails") or r.get("email") or "").strip()
        found = clean_emails(api_email)
        r["_source"] = "api" if found else ""
        website = (r.get("website") or "").strip()
        if not found and not a.no_crawl and website and not is_third_party(website) \
                and crawled < a.max_crawl:
            crawled += 1
            site_emails = crawl_site_for_email(website)
            if site_emails:
                found = site_emails
                r["_source"] = "crawl"
        r["found_email"] = found[0] if found else ""
        r["all_emails"] = "; ".join(found)

    # write csv
    out_csv = os.path.join(a.out, "results.csv")
    if rows:
        cols = list(rows[0].keys())
        with open(out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

    with_email = [r for r in rows if r.get("found_email")]
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(rows)} businesses | {len(with_email)} with email "
          f"({crawled} sites crawled free) | credits left: {credits_left()}")
    print(f"CSV: {out_csv}")
    print(f"{'='*60}")
    for r in sorted(rows, key=lambda x: (0 if x.get('found_email') else 1)):
        name = (r.get("title") or "")[:30]
        rating = (r.get("review_rating") or "")[:3]
        em = r.get("found_email") or "—"
        src = r.get("_source") or ""
        web = "web" if r.get("website") and not is_third_party(r.get("website")) else "no-site"
        tag = f"[{src}]" if src else ""
        print(f"  {name:<31} {rating}⭐ {web:<8} {em} {tag}")


if __name__ == "__main__":
    main()

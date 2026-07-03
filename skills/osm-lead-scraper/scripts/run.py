#!/usr/bin/env python3
"""
osm-lead-scraper — FREE local-business lead scraper. No API key, no credits.

Pulls businesses from OpenStreetMap's Overpass API (open data, free, legal),
then enriches each with a website + email by a light free web lookup + the
site crawler. Feeds the same lead-hunter pipeline (diagnose → score → CRM-ready).

Why: replaces the paid GmapsScraper.io dependency (credit limits + 403s).
Trade-off: OSM has no star ratings / review counts, and website/phone coverage
is patchy — so we backfill websites via a free DuckDuckGo HTML lookup and then
crawl for emails.

Usage:
  python3 run.py --area "Golders Green London" \
      --shops hairdresser,beauty,nails --amenities cafe,restaurant \
      --out /tmp/osm --max 60 --enrich 25 --source "OSM NW11 sweep"

Or with an explicit bounding box (south,west,north,east):
  python3 run.py --bbox 51.570,-0.205,51.590,-0.185 --shops hairdresser

Output: <out>/leads.json — CRM-ready objects (same shape as lead-hunter).
"""
import sys, os, re, json, time, argparse, urllib.request, urllib.parse, ssl

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; StudioBeaSophia-LeadBot/1.0; +https://studiobeasophia.com)"
OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]
NOMINATIM = "https://nominatim.openstreetmap.org/search"

# reuse the proven diagnose/score/crawl from lead-hunter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lead-hunter", "scripts"))
try:
    import run as lh  # diagnose, score, crawl_email, clean_emails, ANGLE, CHAINS, is_third_party
except Exception:
    lh = None

CHAINS = ("caffe nero","caffè nero","starbucks","costa","greggs","pret","mcdonald","kfc",
          "subway","domino","nando","pizza express","wagamama","gail","leon","sally beauty",
          "superdrug","boots")


def http(url, data=None, timeout=40, ctype=None):
    headers = {"User-Agent": UA, "Accept": "*/*"}
    if ctype: headers["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read().decode("utf-8", "ignore")


def geocode(area):
    """area name -> bounding box (south,west,north,east) via free Nominatim."""
    url = f"{NOMINATIM}?" + urllib.parse.urlencode({"q": area, "format": "json", "limit": 1})
    time.sleep(1)  # Nominatim politeness
    res = json.loads(http(url, timeout=20))
    if not res: raise RuntimeError(f"couldn't geocode {area!r}")
    bb = res[0]["boundingbox"]  # [south, north, west, east]
    return float(bb[0]), float(bb[2]), float(bb[1]), float(bb[3])


def overpass(bbox, shops, amenities):
    s, w, n, e = bbox
    parts = []
    if shops:
        parts.append(f'node["shop"~"{"|".join(shops)}"]({s},{w},{n},{e});')
        parts.append(f'way["shop"~"{"|".join(shops)}"]({s},{w},{n},{e});')
    if amenities:
        parts.append(f'node["amenity"~"{"|".join(amenities)}"]({s},{w},{n},{e});')
        parts.append(f'way["amenity"~"{"|".join(amenities)}"]({s},{w},{n},{e});')
    q = f"[out:json][timeout:40];({''.join(parts)});out center tags 200;"
    data = urllib.parse.urlencode({"data": q}).encode()
    last = None
    for mirror in OVERPASS_MIRRORS:
        try:
            raw = http(mirror, data=data, timeout=60,
                       ctype="application/x-www-form-urlencoded")
            return json.loads(raw).get("elements", [])
        except Exception as e:
            last = e; time.sleep(2); continue
    raise RuntimeError(f"all Overpass mirrors failed: {last}")


def ddg_website(name, area):
    """Free website lookup via DuckDuckGo HTML (no key). Returns best-guess URL or ''."""
    try:
        url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": f"{name} {area}"})
        html = http(url, timeout=12)
        # DDG wraps results in uddg= redirect params
        m = re.findall(r'uddg=([^&"]+)', html)
        for enc in m[:5]:
            u = urllib.parse.unquote(enc)
            low = u.lower()
            if any(b in low for b in ("duckduckgo","facebook","instagram","tripadvisor",
                                       "yelp","google.","yell.com","wikipedia","booking.com")):
                continue
            if u.startswith("http"):
                return u
    except Exception:
        pass
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", default="")
    ap.add_argument("--bbox", default="", help="south,west,north,east")
    ap.add_argument("--shops", default="hairdresser,beauty")
    ap.add_argument("--amenities", default="")
    ap.add_argument("--out", default="/tmp/osm")
    ap.add_argument("--max", type=int, default=60)
    ap.add_argument("--enrich", type=int, default=25, help="max websites to look up + crawl")
    ap.add_argument("--min-score", type=int, default=62)
    ap.add_argument("--source", default="")
    a = ap.parse_args()

    if a.bbox:
        bbox = tuple(float(x) for x in a.bbox.split(","))
        area_name = a.area or "custom bbox"
    elif a.area:
        print(f"Geocoding {a.area!r}...")
        bbox = geocode(a.area); area_name = a.area
    else:
        sys.exit("need --area or --bbox")
    print(f"bbox: {bbox}")

    shops = [s for s in a.shops.split(",") if s]
    ams = [s for s in a.amenities.split(",") if s]
    els = overpass(bbox, shops, ams)
    print(f"{len(els)} raw OSM elements")

    # dedupe by name, drop chains + unnamed
    seen = {}
    for el in els:
        t = el.get("tags", {})
        name = (t.get("name") or "").strip()
        if not name: continue
        low = name.lower()
        if any(c in low for c in CHAINS): continue
        if name in seen: continue
        seen[name] = t
    print(f"{len(seen)} named, non-chain businesses")

    os.makedirs(a.out, exist_ok=True)
    src = a.source or f"OSM {area_name} {time.strftime('%Y-%m-%d')}"
    leads = []; enriched = 0
    for name, t in list(seen.items())[:a.max]:
        web = t.get("website") or t.get("contact:website") or ""
        phone = t.get("phone") or t.get("contact:phone") or ""
        email = t.get("email") or t.get("contact:email") or ""
        cat = t.get("shop") or t.get("amenity") or ""
        # free enrichment: find a website if OSM has none
        if not web and enriched < a.enrich:
            enriched += 1
            web = ddg_website(name, area_name)
            time.sleep(1.5)  # be polite
        # diagnose + score using lead-hunter logic
        if lh:
            pain, kind = lh.diagnose(web)
            score = lh.score(kind, 0)  # OSM has no rating -> no boost
            angle = lh.ANGLE.get(kind, "")
        else:
            pain, kind, score, angle = ("unknown","generic",60,"")
        if score < a.min_score: continue
        # crawl for email if we have a real site and no email yet
        if not email and web and lh and not lh.is_third_party(web) \
                and kind in ("thin","no-booking","has-booking","dead"):
            got = lh.crawl_email(web)
            email = got[0] if got else ""
        leads.append({
            "business_name": name, "website_url": web, "location": area_name, "borough": "",
            "business_type": cat, "contact_phone": phone, "contact_email": email,
            "pain_signals": pain, "why_good_fit": f"{kind} (OSM, no rating)",
            "score": score, "priority": "A" if score>=78 else ("B" if score>=65 else "C"),
            "status": "new", "outreach_angle": angle, "source_run": src,
        })
    leads.sort(key=lambda x: -x["score"])
    json.dump(leads, open(os.path.join(a.out, "leads.json"), "w"), indent=1)

    with_contact = sum(1 for l in leads if l["contact_email"] or l["contact_phone"])
    print(f"\n{'='*64}")
    print(f"{len(leads)} leads (score ≥{a.min_score}) | {with_contact} with a contact | FREE, 0 credits")
    print(f"→ {os.path.join(a.out,'leads.json')}\n{'='*64}")
    for l in leads[:30]:
        c = l["contact_email"] or l["contact_phone"] or "—"
        print(f"  {int(l['score']):>2} {l['priority']} {l['business_name'][:26]:<27} {c[:26]:<27} {l['pain_signals'][:26]}")


if __name__ == "__main__":
    main()

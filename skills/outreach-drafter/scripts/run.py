#!/usr/bin/env python3
"""
outreach-drafter — turn CRM leads into OPSA cold emails per the Studio Bea Sophia
playbook, and VALIDATE every draft against the hard rules.

Reads a leads.json (from lead-hunter, or a CRM export) and produces, per lead:
  - drafted_email_subject   (1-4 words, lowercase, <45 chars)
  - drafted_email_body      (OPSA: Observation→Problem→Solution→Ask, 50-75 words, one CTA, P.S.)
  - _validation             list of any rule violations (empty = clean)

It builds the draft from templates keyed on the lead's pain "kind" (dead, no-site,
third-party, thin, no-booking) so the Observation + Problem are specific and true.
The agent should still eyeball each draft — this gets 90% there, on-rule.

Usage:
  python3 run.py leads.json [--out drafts.json] [--only-with-email] [--kind dead,no-site]

Never sends. Drafting + validation only.
"""
import sys, json, re, argparse

SIGN = "Studio Bea Sophia"
BANNED = ["hope this finds you well","came across your profile","really impressed",
          "leverage","synergies","best-in-class","just bumping","free","guarantee",
          "urgent","act now","limited time"," ai ","a.i."]

# Per-kind Observation + Problem + Solution + Ask. First name inserted where possible.
def first_word(name):
    w = re.sub(r"[^A-Za-z0-9& ].*$","",name).strip().split(" ")[0]
    # soften SHOUTY brand names (COCOLAS -> Cocolas) so drafts don't read as ALL CAPS
    if w.isupper() and len(w) > 2:
        w = w.capitalize()
    return w

def subject_for(kind, name):
    return {
        "dead":       "your website",
        "no-site":    "your google listing",
        "third-party":"owning your bookings",
        "thin":       "your booking page",
        "no-booking": "your booking page",
    }.get(kind, "quick idea")

def body_for(lead):
    kind = _kind(lead)
    name = lead.get("business_name","your shop")
    short = first_word(name)
    O = {
      "dead": f"It looks like the website linked from {short}'s Google listing isn't loading right now.",
      "no-site": f"It seems like {short} shows up on Google Maps but there's no website attached yet.",
      "third-party": f"It looks like {short}'s bookings run entirely through a third-party page rather than your own site.",
      "thin": f"It looks like {short}'s site is up, but it's close to a placeholder with no way to book.",
      "no-booking": f"It looks like {short}'s site is lovely, but there's no way to book online from it.",
    }.get(kind, f"It looks like {short}'s site could be doing more for you.")
    P = {
      "dead": "So anyone who clicks through hits a dead page — and most won't call, they'll just pick the next salon.",
      "no-site": "So people find you, then can't see hours, prices, or book — and quietly go elsewhere.",
      "third-party": "So you pay commission on every booking and don't own the customer relationship or show up well on Google.",
      "thin": "So an interested customer lands, finds nothing to act on, and the enquiry leaks to voicemail.",
      "no-booking": "So enquiries come in by phone at the worst moments, and after-hours interest just evaporates.",
    }.get(kind, "So you're likely leaving bookings on the table.")
    S = "I build small, fast booking pages for local places like yours that turn a Google click into a booked slot."
    A = "Want me to send a 2-minute mockup of what yours could look like?"
    PS = "P.S. — if the site's already handled, no worries; happy to point you to something useful instead."
    return f"Hi {short},\n\n{O} {P}\n\n{S}\n\n{A}\n\n— {SIGN}\n\n{PS}"

def _kind(lead):
    p = (lead.get("pain_signals") or "").lower()
    if "dead" in p or "won't load" in p: return "dead"
    if "no website" in p or "no owned site" not in p and "invisible" in p: return "no-site"
    if "only" in p or "third" in p: return "third-party"
    if "near-empty" in p or "thin" in p: return "thin"
    if "no booking" in p or "no online booking" in p: return "no-booking"
    return "generic"

def word_count(body):
    # count words in the body excluding the signature line and greeting nicety
    txt = re.sub(r"—\s*Studio Bea Sophia","",body)
    txt = re.sub(r"P\.S\..*$","",txt, flags=re.S)  # P.S. excluded from core count
    txt = re.sub(r"^Hi [^\n,]+,","",txt)
    return len(re.findall(r"\b[\w'&-]+\b", txt))

def validate(subject, body):
    issues = []
    wc = word_count(body)
    if wc > 80: issues.append(f"body {wc}w > 80 (hard cap)")
    elif wc < 45: issues.append(f"body {wc}w < 45 (too thin)")
    low = body.lower()
    for b in BANNED:
        if b.strip() and b in low: issues.append(f"banned phrase: {b.strip()!r}")
    # never open with "I"
    firstline = [l for l in body.splitlines() if l.strip() and not l.startswith("Hi ")]
    if firstline and re.match(r"\s*I['’ ]", firstline[0]): issues.append("opens with 'I'")
    if SIGN not in body: issues.append("missing signature")
    ctas = body.count("?")
    if ctas != 1: issues.append(f"{ctas} question marks (want exactly 1 CTA)")
    if "!" in body: issues.append("contains '!'")
    body_no_greeting = re.sub(r"^Hi [^\n]+", "", body)
    # allow known brand-name caps; flag only shouty words in the pitch
    caps = [w for w in re.findall(r"\b[A-Z]{4,}\b", body_no_greeting) if w not in ("STOP",)]
    if caps: issues.append(f"ALL CAPS word: {caps[0]}")
    if len(subject) > 45: issues.append(f"subject {len(subject)} chars > 45")
    if subject != subject.lower(): issues.append("subject not lowercase")
    if len(subject.split()) > 4: issues.append("subject > 4 words")
    return issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("leads")
    ap.add_argument("--out", default="")
    ap.add_argument("--only-with-email", action="store_true")
    ap.add_argument("--kind", default="")
    a = ap.parse_args()
    leads = json.load(open(a.leads))
    kinds = set(a.kind.split(",")) if a.kind else None
    out = []
    for L in leads:
        if a.only_with_email and not L.get("contact_email"): continue
        if kinds and _kind(L) not in kinds: continue
        subj = subject_for(_kind(L), L.get("business_name",""))
        body = body_for(L)
        L2 = dict(L)
        L2["drafted_email_subject"] = subj
        L2["drafted_email_body"] = body
        L2["_validation"] = validate(subj, body)
        out.append(L2)
    dst = a.out or a.leads.replace(".json","") + "_drafts.json"
    json.dump(out, open(dst,"w"), indent=1)
    clean = sum(1 for x in out if not x["_validation"])
    print(f"{len(out)} drafts | {clean} clean, {len(out)-clean} with issues")
    print(f"→ {dst}\n")
    for x in out[:12]:
        wc = word_count(x["drafted_email_body"])
        flag = "✓" if not x["_validation"] else "⚠ " + "; ".join(x["_validation"])
        print(f"  [{x.get('score','?')}] {x['business_name'][:26]:<27} subj:{x['drafted_email_subject']:<20} {wc}w  {flag}")

if __name__ == "__main__":
    main()

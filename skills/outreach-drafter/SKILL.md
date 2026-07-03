---
name: outreach-drafter
description: Turn CRM leads into OPSA cold emails per the Studio Bea Sophia playbook and validate every draft against the hard rules (50-75 words, one CTA, no banned phrases, no "I" opener, signed, P.S.). Reads a leads.json and writes per-lead drafted_email_subject + drafted_email_body ready to review and send. Use to draft first-touch outreach for a batch of leads.
version: 1.0.0
metadata:
  requires:
    bins:
      - python3
  emoji: "✍️"
---

# Outreach Drafter

Drafts + validates OPSA cold emails. Never sends. Encodes the cold-email playbook
(.agents/rules/cold-email-playbook.md) as behaviour.

## Run

```bash
python3 .agents/skills/outreach-drafter/scripts/run.py /tmp/lead-hunter/leads.json \
  --out /tmp/drafts.json --only-with-email --kind dead,no-site
```

Args:
- positional: a `leads.json` (from lead-hunter, or a CRM export)
- `--out FILE`          output (default `<leads>_drafts.json`)
- `--only-with-email`   skip leads with no email
- `--kind a,b`          only draft these pain kinds (dead, no-site, third-party, thin, no-booking)

## Output

Each lead gains:
- `drafted_email_subject` — 1-4 words, lowercase, <45 chars
- `drafted_email_body`    — OPSA body, 50-75 words, one CTA, signed, P.S.
- `_validation`           — list of rule violations (empty = clean)

## OPSA templates by pain kind

Observation + Problem are specific per kind so the email is TRUE, not generic:
- **dead** — site linked from Google won't load → clicks hit a dead page
- **no-site** — on Maps but no website → can't see hours/prices/book
- **third-party** — bookings via Treatwell/Booksy → commission + no owned customer
- **thin** — placeholder site, nothing to act on → enquiry leaks to voicemail
- **no-booking** — nice site, no online booking → after-hours interest evaporates

CTA is value-first ("Want me to send a 2-minute mockup?"). Signed "Studio Bea Sophia".

## Validation (hard rules enforced)

Flags: >80 or <45 words, banned phrases, opening with "I", missing signature,
≠1 CTA, "!", ALL-CAPS words, subject >45 chars / not lowercase / >4 words.
All-caps brand names (e.g. COCOLAS) are auto-softened in the draft.

## Workflow

1. `lead-hunter` → leads.json
2. `outreach-drafter` → drafts.json (review the ⚠ ones)
3. agent writes drafts back to the `Lead` records, then sends via Gmail on approval,
   logging to OutreachLog and scheduling the 7-step follow-up.

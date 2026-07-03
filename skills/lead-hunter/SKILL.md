---
name: lead-hunter
description: The full Studio Bea Sophia lead pipeline in ONE command — search Google Maps for a niche + location, dedupe/drop chains, diagnose every website (dead/no-site/third-party/template/booking), score 0-100 via the four pillars, enrich missing emails by crawling sites for free, and emit CRM-ready lead objects. Use to run a whole discovery sweep of a high street or niche in one call.
version: 1.0.0
metadata:
  requires:
    env:
      - GMAPS_SCRAPER_API_KEY
    bins:
      - python3
  emoji: "🎯"
---

# Lead Hunter

One command = a full discovery run. Replaces the old 6-step manual process
(search → dedupe → diagnose → score → enrich → format).

## Run

```bash
python3 .agents/skills/lead-hunter/scripts/run.py \
  "hair salon in Golders Green London" \
  "independent cafe in Golders Green London" \
  --source "NW11 sweep 2026-07-03" --min-score 62 --max-crawl 20
```

Args:
- positional: one or more `"niche in location"` queries (each = 2 credits)
- `--out DIR`        output dir (default `/tmp/lead-hunter`)
- `--min-score N`    drop leads below this (default 62 — skips already-good sites)
- `--max-crawl N`    cap free email crawls (default 20)
- `--source STR`     value written to each lead's `source_run`

## What it produces

`<out>/leads.json` — an array of CRM-ready objects with fields matching the
`Lead` entity: business_name, website_url, location, borough, business_type,
contact_phone, contact_email, pain_signals, why_good_fit, score, priority,
status, outreach_angle, source_run.

Plus a scannable stdout table (score, priority, name, contact, pain).

## Then insert into the CRM

The skill does NOT write to the DB (so records go through row-level security).
The agent reads `leads.json` and calls `create_entity_records("Lead", [...])`.
Set `location`/`borough` before insert (the skill leaves them blank — the agent
knows the area from the query).

## Scoring

Base by website state: dead 88, no-site 78, third-party 74, thin 72,
no-booking 68, has-booking 52. Rating boost (+6 if ≥4.8⭐, +3 if ≥4.5⭐) for
strong-but-invisible businesses. Priority: A ≥78, B ≥65, C else.

## Filters

Drops chains (Nero, Costa, Greggs…), vape shops, and businesses rated <3.0⭐
(struggling = poor client fit).

## Credits

2 per search. Check: `GET /api/v1/credits` → `{"credits":N}` (N/2 = searches).
Email crawling is always free.

---
name: osm-lead-scraper
description: FREE local-business lead scraper — no API key, no credits. Pulls businesses from OpenStreetMap's Overpass API (open data), backfills websites via a free DuckDuckGo lookup, then diagnoses/scores/enriches emails using the lead-hunter pipeline. Use as the default discovery tool; falls back to paid GMaps only when ratings/phones are essential.
version: 1.0.0
metadata:
  requires:
    bins:
      - python3
  emoji: "🗺️"
---

# OSM Lead Scraper (free)

Replaces the paid GmapsScraper.io dependency for discovery. Uses only free,
open, legal sources: OpenStreetMap Overpass (businesses) + Nominatim (geocoding)
+ DuckDuckGo HTML (website lookup) + the site crawler (emails).

## Run

```bash
python3 .agents/skills/osm-lead-scraper/scripts/run.py \
  --area "Golders Green London" \
  --shops hairdresser,beauty,nails --amenities cafe,restaurant \
  --out /tmp/osm --max 60 --enrich 25 --source "OSM NW11 sweep"
```

Or with an explicit bounding box (south,west,north,east):
```bash
python3 run.py --bbox 51.570,-0.205,51.590,-0.185 --shops hairdresser
```

Args:
- `--area STR`     place name (geocoded to a bbox via Nominatim)
- `--bbox S,W,N,E` explicit bounding box (skips geocoding)
- `--shops`        OSM shop tags, comma-sep (hairdresser,beauty,nails,tattoo,florist,bakery…)
- `--amenities`    OSM amenity tags (cafe,restaurant,bar,pub,dentist…)
- `--max N`        cap leads processed (default 60)
- `--enrich N`     max free website lookups + crawls (default 25; each ~1.5s, be polite)
- `--min-score N`  drop below (default 62)
- `--source STR`   source_run tag

## Output

`<out>/leads.json` — same CRM-ready shape as lead-hunter. Agent inserts via
`create_entity_records("Lead", …)`.

## Strengths vs the paid API

- FREE + unlimited (no credits, no 403s).
- Broader coverage: often 3× more businesses per area (OSM lists small/no-website shops).
- Finds no-website leads Google hides — perfect for "you're invisible online" outreach.

## Limitations (be honest with the lead data)

- No star ratings / review counts (OSM has none) → scoring skips the rating boost.
- Phone coverage is patchy (many OSM entries have no `phone` tag).
- Website coverage patchy → backfilled via DuckDuckGo best-guess (verify before use).

## When to still use the paid GMaps skill

When you specifically need ⭐ ratings, review counts, or reliable phone numbers
(e.g. to prioritise busy-but-invisible shops, or for phone/WhatsApp outreach).
Otherwise default to this free scraper.

## Common OSM tags

shop: hairdresser, beauty, nails, tattoo, massage, florist, bakery, butcher,
      greengrocer, optician, jewelry, bicycle, car_repair, dry_cleaning
amenity: cafe, restaurant, bar, pub, fast_food, dentist, veterinary, cinema

---
name: pain-scraper
description: Niche-aware pain-point harvester + "Keep The Cut" SEO landing-page generator. Turns real marketplace-owner complaints (Fresha/Treatwell for salons, Booksy for barbers, Deliveroo/UberEats/JustEat for restaurants & takeaways, Checkatrade/MyBuilder for trades) into ready-to-publish commission-free-booking landing pages per niche + town. Use when Bea wants fresh pain evidence or wants to spin up a "Keep The Cut" page for a new niche/area.
---

# pain-scraper — the "Keep The Cut" content engine

Turns real marketplace-owner anger into publishable SEO landing pages.
One build, every niche — just swap the villain.

Service brand: **Keep The Cut by Studio Bea Sophia**.
Per-niche hooks: salons "Ditch the 20%", restaurants "Keep the 30%",
barbers "Ditch the fees", trades "Stop paying per lead".

## IMPORTANT — how harvesting works
Reddit blocks direct datacenter/sandbox requests (HTTP 403). So the AGENT
harvests quotes with its own `web_search` + `read_web_page` tools (which CAN
read Reddit), then feeds them to the deterministic page builder. This keeps it
honest: every quote carries its real source URL.

## Two-step flow
1. HARVEST (agent, via web_search): run 2–3 searches like
   `"<villain> commission <niche> reddit"`, `"<villain> fees killing <niche>"`,
   pull the strongest real quotes (the angry, specific, number-carrying ones),
   and write them to a quotes JSON:
   ```json
   { "niche":"restaurants", "town":"Camden", "villain":"Deliveroo",
     "cta":"https://wa.me/447847321961",
     "quotes":[ {"quote":"...", "subreddit":"UberEATS", "ups":320,
                 "url":"https://reddit.com/..."} ] }
   ```
2. GENERATE:
   ```
   python3 scripts/build_page.py <quotes.json> [out_dir]
   ```
   → `<out>/page.md` and `<out>/page.html` (styled, publishable).

## Niche map
| niche       | villain(s)                     | hook            | the cut |
|-------------|--------------------------------|-----------------|---------|
| salons      | Fresha, Treatwell              | Ditch the 20%   | 20% new client |
| barbers     | Booksy, Fresha                 | Ditch the fees  | 30% first appt |
| restaurants | Deliveroo, UberEats, JustEat   | Keep the 30%    | up to 38%/order |
| takeaways   | JustEat, UberEats              | Keep the 30%    | per-order |
| trades      | Checkatrade, MyBuilder         | Stop paying per lead | lead fees |
| clinics     | (WhatsApp-triage angle)        | Own your front door | private-patient revenue |

## Rules
- HONEST: only real scraped quotes, each with its source URL. Never fabricate.
- Page copy follows "Keep the calendar, own the front door — stop paying to rent
  your own customers."
- To launch a niche: harvest fresh quotes → build page → publish per town.
  Clone across towns for compounding local SEO (the passive-income engine).

## Note on the old run.py
`scripts/run.py` still contains the direct-Reddit scraper — kept for reference,
but it 403s from the sandbox. Use the web_search → build_page.py flow instead.

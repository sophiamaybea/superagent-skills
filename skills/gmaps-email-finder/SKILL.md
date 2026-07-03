---
name: gmaps-email-finder
description: Find local businesses on Google Maps AND get their email addresses. Runs a GmapsScraper.io search, then for any lead with a website but no email, crawls the business's own site (contact/about pages) to extract emails for free — no extra API credits. Use when building a local lead list that needs contact emails for outreach.
version: 1.0.0
metadata:
  requires:
    env:
      - GMAPS_SCRAPER_API_KEY
    bins:
      - python3
  emoji: "📧"
---

# GMaps Email Finder

Built in-house for Studio Bea Sophia. Solves the gap where the GMaps scraper
returns businesses with phones but no emails.

## What it does

1. **Search stage (2 credits):** POST to `gmapsscraper.io/api/v1/scrape` with
   `email:true`, poll `/jobs/{id}` until complete, download the CSV.
2. **Free crawl stage (0 credits):** for every business that has a real website
   but no email from the API, fetch the site's home + likely contact pages
   (`/contact`, `/about`, `/book`, etc.), pull emails from `mailto:` links and
   page text, filter out junk (image filenames, wix/godaddy placeholders).

Third-party-only "sites" (Treatwell, Booksy, Facebook, Instagram, JustEat…) are
skipped for crawling — there's no owned inbox to find.

## Usage

```bash
python3 .agents/skills/gmaps-email-finder/scripts/run.py "hair salon in Golders Green London"
python3 .agents/skills/gmaps-email-finder/scripts/run.py "cafe in Hendon London" --out /tmp/hendon
python3 .agents/skills/gmaps-email-finder/scripts/run.py "barber in West Hampstead London" --max-crawl 15 --no-crawl
```

Flags:
- `--out DIR`     where to write `results.csv` (default `/tmp/gmaps-email-finder`)
- `--no-crawl`    skip the free website crawl (API emails only)
- `--max-crawl N` cap how many sites to crawl (default 25)

## Output

- `<out>/results.csv` — all scraper columns plus `found_email`, `all_emails`,
  `_source` (`api` or `crawl`).
- A scannable stdout summary: name, rating, has-site, email, source tag.

## Credits

Each search = 2 credits. Check remaining: `GET /api/v1/credits`. The crawl stage
is always free. Free signup = 10 credits (5 searches).

## Notes / gotchas

- Correct API flow (the older gmaps skills had a stale endpoint):
  CREATE `POST /api/v1/scrape` → POLL `GET /api/v1/jobs/{id}` → DOWNLOAD
  `GET /api/v1/jobs/{id}/download`.
- Auth header: `Authorization: Bearer $GMAPS_SCRAPER_API_KEY`.
- Businesses with NO website at all can't be email-found here — use phone/walk-in
  (fine for local outreach).

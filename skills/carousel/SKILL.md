# carousel

Generate crisp, on-brand Instagram carousel PNGs (1080×1350, 2× retina) from a
plain JSON content file — NO Canva, NO AI image tools (which mangle text).

Each slide is real HTML/CSS rendered to PNG via headless Chromium, so text is
pixel-perfect and the whole deck re-renders in seconds when the words change.

## When to use
When Bea wants an Instagram carousel / post image with text on it. You write
the words as JSON; the skill renders the images.

## How to run
```
run_skill carousel '<path-to-content.json> [output-dir]'
```
- `content.json` — the deck (see format below). Defaults to `deck.json`.
- `output-dir` — where PNGs are written. Defaults to `carousel-out/`.

Output: `slide-01.png`, `slide-02.png`, … plus a copy of the deck used.
After rendering, use `send_image` (messaging) or `upload_file` to share them.

## content.json format
```json
{
  "brand": "STUDIO BEA SOPHIA",
  "slides": [
    { "layout": "cover",  "eyebrow": "A THREAD",
      "title": "Vibe coding\nis quiet spam." },
    { "layout": "list",   "eyebrow": "THE MODEL", "title": "How the pitch works.",
      "items": ["Find a small business", "Paste name into an AI builder",
                "AI spits out a site", "Cold-pitch it for £1,000"],
      "kicker": "Here's every problem with it." },
    { "layout": "statement", "eyebrow": "THE FIX",
      "title": "Sell the outcome,\nnot the template." },
    { "layout": "quote", "quote": "Text stays crisp because it's real HTML.",
      "attribution": "— the whole point" }
  ]
}
```
Layouts: `cover` (big centered title), `list` (eyebrow + title + arrow items +
optional kicker), `statement` (eyebrow + large left title), `quote` (centered
quote + attribution). Use `\n` for line breaks. Page numbers + brand mark +
orange footer rule are added automatically. Omit the page number on slide 1 by
setting `"pageno": false`.

## Brand system (locked)
Fonts Fraunces (serif headlines) + IBM Plex Mono (body). Colours: periwinkle
#5b6ef5 eyebrows, orange #f07d1a accent, ink #111. Edit `base.css` to tweak.

## Signature end-card (auto)
Every deck automatically gets a final **signature** slide: the red cherub logo
centered on the brand ground with the @studiobeasophia handle + orange rule.
It stays clean/red even when `photocopy:true` (photocopy-exempt by default).

- Opt out for a whole deck: add `"signature": false` at the top level.
- Add it manually / control placement: include `{ "layout": "signature", "handle": "@studiobeasophia" }`.
- Force it to halftone too: `{ "layout": "signature", "photocopy": true }`.

The cherub asset lives at `assets/cherub.png` (transparent PNG).

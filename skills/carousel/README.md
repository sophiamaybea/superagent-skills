# Carousel Image Generator

Renders on-brand Instagram carousel slides (1080x1350, 2x retina) from HTML/CSS
instead of an AI image tool — so text is always crisp and exactly correct.

## Why HTML, not AI images
AI image generators mangle text. These slides are real HTML rendered to PNG via
headless Chromium, so copy is pixel-perfect and the template is reusable.

## Brand system (base.css)
- Fonts: Fraunces (serif headlines) + IBM Plex Mono (body/labels)
- Colours: periwinkle #5b6ef5 (eyebrows), orange #f07d1a (accent), ink #111
- STUDIO BEA SOPHIA mark top-left, orange footer rule + page number

## Usage
1. Edit or add slide files (s1.html, s2.html, ...) using base.css classes.
2. List the slides to render in slides.json, e.g. ["s1","s2","s8"].
3. Run: `node render.mjs` (needs playwright-core + a chromium headless shell,
   plus system libs: libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2
   libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2
   libgbm1 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0).
4. PNGs are written next to the HTML (s1.png, ...).

## Sample decks
- "Vibe coding side hustle is spam" — 9-slide critique carousel.

# Studio Bea Sophia — MASTER BUILD PROMPT
# Landing + Constellation node-map + Dashboard/Customer-view (one connected site)

Build a complete, awwwards-worthy website for STUDIO BEA SOPHIA — a boutique web
design studio for small independent businesses. ONE cohesive site with three
connected parts: (A) a LANDING page, (B) an interactive CONSTELLATION node-map of
what the studio builds, and (C) a live mock DASHBOARD + split CUSTOMER-VIEW for
each industry. NOT a template — a crafted digital world that proves, by existing,
that this studio builds things worth being chosen for.

## GLOBAL FEEL
Editorial, warm, boutique — a beautifully printed magazine that moves. Slow,
intentional motion; everything eases. Tactile: elements respond to hover, drag,
tap. Fast: lazy-load, respect prefers-reduced-motion, mobile-first (most traffic
is phone-from-Instagram).

## DESIGN SYSTEM (shared across all parts — they MUST feel like one site)
Fonts: Fraunces (display/headings, italics for character) + Inter (body/UI).
Palette: paper cream #faf6f0, deep ink #2b2420, terracotta #c8613f (single
accent), soft red tint #f7e4de for "pain/right now", soft green tint #e4efe1 for
"fixed/with this build". Thin 1px lines, small geometric glyphs, generous
negative space, low-opacity paper-grain texture overlay. Rounded but refined.

## SHARED NAV (sticky, on every view)
Logo "Studio Bea Sophia" left. Links: Home, The Map, What I'd build, Contact.
Consistent everywhere so nothing feels orphaned.

## PART A — LANDING
- Hero: full-viewport, Fraunces headline "Websites that get small businesses
  chosen." Sub: "I don't sell design — I build the piece of your business that
  makes life easier and gets you picked." Primary button "Explore the map →"
  (scrolls/links to the constellation). Subtle cursor-parallax ink-bloom
  illustrations in the background.
- Four pillars strip: Revenue · Credibility · Visibility · Urgency — each a
  short line, revealing with fade+rise on scroll.
- A short "how I think" teaser that leads into the constellation.

## PART B — THE CONSTELLATION (node-map)
A warm near-empty canvas. Centre: a small terracotta bloom/asterisk mark =
"Studio Bea Sophia", subtitle "Websites that get small businesses chosen"; it
gently breathes. On load, thin ink lines draw outward like constellation threads
to labelled nodes, each ending in a small glyph (circle, square, triangle,
hexagon) with an optional numbered badge (1/2/3). Solid lines = things built;
dashed lines = philosophy/ideas.
Nodes:
1. The Seasonal Drop (florists)  2. The Job Tracker (upholsterers)
3. The Auto-Waitlist (class studios)  4. Sell Direct (Etsy makers)
5. Quote in 2 Taps (framers)  6. The Client Gallery (photographers)
7. "Never sell design, sell utility" (dashed)
8. Revenue · Credibility · Visibility · Urgency (dashed)
9. Founding Clients (offer node)
Interaction: whole map gently drifts/breathes; hovering a node highlights it and
its line in terracotta and dims the rest; drag to pan, pinch/scroll to zoom; on
mobile drag to explore, tap a node to open its dashboard. Keyboard-navigable,
focus states.

## PART C — DASHBOARD + CUSTOMER VIEW (opens from a node)
Clicking a node transitions into a mock control-panel for THAT business — their
future running smoothly, today. Numbers gently count up; tools are live and
interactive, NOT screenshots. Each opens with an atmosphere line in italic
Fraunces. Inside each dashboard, a toggle/split shows the SAME moment from the
CUSTOMER's phone, proving it improves customer experience too.

- FLORIST — Seasonal Drop.  Atmosphere: "Feels like opening the flower shed at
  7am, buckets still cool."  Owner: "This week's drop" grid of stems with live
  "3 left / sold out" tags that update when you tap Add; "Takings this week £340"
  counting up; "Pickups today: 2, 4-6pm at the barn gate"; "Deposits secured £90".
  Customer: "Your peonies are reserved 🌸 pickup Sat 10-12, see you at the barn".
- POTTERY/CLASS — Auto-Waitlist.  Atmosphere: "Feels like a full room with the
  wheel already spinning."  Owner: "Tonight's class 8/8 full, 3 on waitlist"; a
  "cancel a seat" control that visibly auto-offers it to the next person;
  "Revenue recovered this month £240". Customer: warm text "A spot just opened in
  Tuesday's class — grab it?" with one-tap booking + instant confirm.
- UPHOLSTERER — Job Tracker.  Owner: commissions list animating Fabric ordered →
  In workshop → Ready when advanced; "Status-chase texts this week: 0". Customer:
  a private status page "Your chair — in the workshop, ready to collect Fri".
- ETSY MAKER — Sell Direct.  Owner: fee calculator — type monthly sales, watch
  "kept vs lost to Etsy" count in real time. Customer: a clean branded checkout.
- FRAMER — Quote in 2 Taps.  Owner: pick size + finish, instant estimate appears.
  Customer: uploads a photo, gets an instant ballpark, feels looked-after.
- PHOTOGRAPHER — Client Gallery.  Owner: gallery with print-order sales ticking
  up. Customer: a beautiful lightbox gallery with one-tap "order print".
Each dashboard shows an ILLUSTRATIVE value figure, clearly labelled as an
industry average, not a promise.

## MOTION
Scroll-triggered fade+rise reveals; subtle smooth/momentum scroll (e.g. Lenis);
cursor parallax / magnetic buttons; constellation lines draw on load; every
prototype truly responds — no fake screenshots; micro-interactions everywhere
(counters, tag flips, card tilts). MUST respect prefers-reduced-motion and be
beautiful and usable on mobile.

## CLOSING / CONTACT (end of scroll)
Calm line: "An interactive experience of connections, for small businesses who
deserve to be chosen." Founding-client offer: "3 founding client spots, from
£450, in exchange for a testimonial once it's live." Primary CTA: a green
WhatsApp button linking to https://wa.me/447847321961 with a pre-filled message
that includes the industry/node explored (e.g. "Hi Bea, I saw your showcase — I
run a florist and I'd love a founding-client mockup"). Secondary: an email-
capture field ("Drop your email for a free mockup sketch") that stores
submissions. Email fallback: studiobeasophia@gmail.com.

## TECH
SVG or canvas for the constellation + lines (radial/force layout or hand-placed
coordinates for control); light framework or plain HTML/CSS/JS. Optional: GSAP +
ScrollTrigger for animation, Lenis for smooth scroll. Keep LCP fast, lazy-load
images, defer non-critical JS. Accessible: real focus states, alt text,
keyboard-operable nodes and prototypes.

## HONESTY (non-negotiable)
All figures are illustrative industry averages, clearly labelled — never
guaranteed results or real client data. A small persistent note states this.

## GOAL
A visitor lands on a striking homepage, is pulled into a living map of how I
think, clicks their own industry, watches their business run smoothly, toggles
to see their customers delighted — then messages on WhatsApp thinking "if the
showcase is this good, imagine what she'd build for me."

# Studio Bea Sophia — Awwwards-Worthy Interactive Experience Brief
# (Node Map → Dashboard → Customer View)

Build an immersive, awwwards-worthy interactive experience for Studio Bea
Sophia, a boutique web design studio for small independent businesses. It has
THREE connected layers a visitor moves through: (1) an interactive NODE-MAP of
what the studio builds, (2) a live mock DASHBOARD of the visitor's own business
running smoothly, and (3) a split CUSTOMER-VIEW showing what that same tool
feels like for their customers. NOT a template — a crafted digital world that
proves, by existing, that this studio builds things worth being chosen for.

## FEEL
Editorial, warm, boutique — a beautifully printed magazine that moves. Slow,
intentional motion; everything eases. Tactile: elements respond to hover, drag,
tap. Fast: lazy-load, respect prefers-reduced-motion, mobile-first (most
traffic is phone-from-Instagram).

## DESIGN SYSTEM
Fonts: Fraunces (display/headings, use italics for character) + Inter (body/UI).
Palette: paper cream #faf6f0, deep ink #2b2420, terracotta #c8613f (single
accent), soft red tint #f7e4de for "pain/right now", soft green tint #e4efe1
for "fixed/with this build". Thin 1px lines, small geometric glyphs, generous
negative space, low-opacity paper-grain texture overlay. Rounded but refined.

## LAYER 1 — THE NODE MAP (entry)
A warm near-empty canvas. In the centre, a small terracotta bloom/asterisk mark:
"Studio Bea Sophia", subtitle "Websites that get small businesses chosen". The
mark gently breathes. On load, thin ink lines draw outward like constellation
threads to labelled nodes, each ending in a small glyph (circle, square,
triangle, hexagon) with an optional numbered badge (1/2/3). Solid lines = things
built; dashed lines = philosophy/ideas.
Nodes:
1. The Seasonal Drop (florists) 2. The Job Tracker (upholsterers)
3. The Auto-Waitlist (class studios) 4. Sell Direct (Etsy makers)
5. Quote in 2 Taps (framers) 6. The Client Gallery (photographers)
7. "Never sell design, sell utility" (dashed) 8. Revenue · Credibility ·
Visibility · Urgency (dashed) 9. Founding Clients (offer node).
Interaction: whole map gently drifts/breathes; hovering a node highlights it +
its line in terracotta and dims the rest; drag to pan, pinch/scroll to zoom;
on mobile drag to explore, tap a node to open. Keyboard-navigable, focus states.

## LAYER 2 — THE DASHBOARD (opens when a node/industry is chosen)
Clicking a node transitions into a mock control-panel for THAT business — their
future running smoothly, today. Numbers gently count up; tools are live and
interactive, not screenshots. Include an atmosphere line in italic Fraunces at
the top of each. Examples:
- Florist (Seasonal Drop): "This week's drop" grid of stems with live
  "3 left / sold out" tags that update when you tap Add; "Takings this week
  £340" counting up; "Pickups today: 2, 4-6pm at the barn gate"; "Deposits
  secured £90 — no more no-shows". Atmosphere: "Feels like opening the flower
  shed at 7am, buckets still cool."
- Pottery/class (Auto-Waitlist): "Tonight's class 8/8 full, 3 on waitlist";
  a "cancel a seat" control that visibly auto-offers it to the next person;
  "Revenue recovered this month £240". Atmosphere: "Feels like a full room with
  the wheel already spinning."
- Upholsterer (Job Tracker): commissions list animating Fabric ordered → In
  workshop → Ready when advanced; "Status-chase texts this week: 0".
- Etsy maker (Sell Direct): fee calculator — type monthly sales, watch "kept
  vs lost to Etsy" count in real time.
- Framer (Quote in 2 Taps): pick size + finish, instant estimate appears.
- Photographer (Client Gallery): mini gallery lightbox with an "order print"
  action.
Each dashboard shows an ILLUSTRATIVE value figure, clearly labelled as an
industry average, not a promise.

## LAYER 3 — THE CUSTOMER VIEW (split screen inside each dashboard)
A toggle or side-by-side split showing the SAME moment from the customer's
phone — proving the tool improves customer experience, not just the owner's.
Examples (owner side | customer side):
- Class: "Seat freed → auto-offered, £30 recovered" | a warm text "A spot just
  opened in Tuesday's class — grab it?" with one-tap booking + instant confirm;
  customer feels looked-after.
- Florist: "Deposit taken, pickup logged" | "Your peonies are reserved 🌸
  pickup Sat 10-12, see you at the barn" — customer feels like a regular.
- Upholsterer: "Zero chase texts" | a private status page: "Your chair — in the
  workshop, ready to collect Fri" — customer feels informed, never ignored.
Same event, two happy endings: owner sees efficiency, customer feels cared for.

## MOTION
Scroll-triggered fade+rise reveals; subtle smooth/momentum scroll (e.g. Lenis);
cursor parallax / magnetic buttons on the map; every prototype truly responds —
no fake screenshots; micro-interactions everywhere (counters, tag flips, card
tilts). MUST respect prefers-reduced-motion and be beautiful and usable on mobile.

## CLOSING SECTION (scroll past the map)
Calm line: "An interactive experience of connections, for small businesses who
deserve to be chosen." Then the founding-client offer: "3 founding client
spots, from £450, in exchange for a testimonial once it's live." Primary CTA:
a green WhatsApp button linking to https://wa.me/447847321961 with a pre-filled
message that includes the industry/node the visitor explored (e.g. "Hi Bea, I
saw your showcase — I run a florist and I'd love a founding-client mockup").
Secondary: an email-capture field ("Drop your email for a free mockup sketch")
that stores submissions so non-ready visitors still convert. Email fallback:
studiobeasophia@gmail.com.

## TECH
SVG or canvas for the map + connecting lines (radial/force layout or hand-placed
coordinates for control); light framework or plain HTML/CSS/JS. Optional: GSAP +
ScrollTrigger for animation, Lenis for smooth scroll. Keep LCP fast, lazy-load
images, defer non-critical JS. Accessible: real focus states, alt text,
keyboard-operable nodes and prototypes.

## HONESTY (non-negotiable)
All figures are illustrative industry averages, clearly labelled — never
guaranteed results or real client data. A small persistent note states this.

## GOAL
A visitor lands, watches the map bloom, explores it, clicks their industry,
sees their own business running smoothly, toggles to see their customers
delighted — then messages on WhatsApp thinking "if the showcase is this good,
imagine what she'd build for me."

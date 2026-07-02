---
name: sales-digital-products
description: "Sells digital products — ebooks, templates, courses, downloads, software, presets, printables. Covers pricing strategy, product-market fit, delivery, upsells, launch playbooks, and platform selection. Use when you have a digital product idea but don't know how to price or sell it, sales are flat and you need a better launch strategy, you're unsure which platform fits your product type, or delivery and upsell flow isn't converting. Do NOT use for membership/subscription sites (use /sales-membership), checkout page optimization (use /sales-checkout), or platform-specific setup (use /sales-kit, /sales-groove, etc.)."
argument-hint: "[describe your digital product question or goal]"
license: MIT
version: 1.0.0
tags: [sales, digital-products, ebooks, courses, ecommerce]
---
# Digital Product Sales

Help the user sell digital products — ebooks, templates, courses, downloads, software, presets, and printables. Covers product-market fit, pricing strategy, delivery, upsells, launch playbooks, and platform selection. This skill is tool-agnostic but includes platform-specific guidance.

## Step 1 — Gather context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user:

1. **What type of digital product?**
   - A) Ebook / guide / PDF
   - B) Templates / swipe files / spreadsheets
   - C) Online course / video training
   - D) Software / SaaS / plugins
   - E) Design assets (presets, fonts, icons, mockups)
   - F) Audio (music, sound effects, podcasts)
   - G) Printables / planners
   - H) Community access / paid group
   - I) Not sure yet — need help deciding

2. **Where are you in the process?**
   - A) Idea stage — haven't built anything yet
   - B) Product is built — need to sell it
   - C) Already selling — want to optimize or scale
   - D) Want to add digital products to an existing business

3. **Do you have an existing audience?**
   - A) Yes — newsletter, social, or community (approximate size?)
   - B) No — starting from scratch
   - C) Small audience (<1,000) but growing

## Step 2 — Strategy and approach

### Product-market fit for digital products

**Validation before building**:
1. **Pre-sell**: Offer the product at a discount before it exists. If 10+ people pay, build it.
2. **Waitlist**: Landing page with email capture. 100+ signups = strong signal.
3. **Free version**: Give away a mini version (checklist from the ebook, 1 lesson from the course). Track engagement.
4. **Audience polling**: Ask your list "Would you pay $X for Y?" — but weigh actions over words.

**High-demand digital product categories**:
- "Done for you" templates (save time) — highest conversion
- Skill-building courses (increase earning power) — highest price point
- Creative assets (presets, fonts, mockups) — volume play
- Knowledge products (ebooks, guides) — lower price, higher volume
- Tools/software (calculators, apps) — recurring revenue potential

## Step 3 — Platform-specific guidance

**Read `references/platform-guide.md`** for detailed pricing strategy, launch playbook, delivery methods, upsell frameworks, platform comparisons, and revenue benchmarks.

### In MailerLite
MailerLite supports selling digital products directly within its platform:
- **Digital product sales**: Sell ebooks, downloads, and digital files. Buyers receive a download link in a confirmation email.
- **Stripe required**: All payments go through Stripe — no PayPal or other payment processors.
- **Plan limits**: 1 digital product on Free, 3 on Growing Business ($10/mo), unlimited on Advanced ($20/mo).
- **Paid newsletters**: Separate from digital products — recurring subscription payments via Stripe for gated content.
- **Landing pages**: Use MailerLite's built-in landing page builder for product sales pages (10 on Free, unlimited on paid).
- **Automation integration**: Trigger post-purchase email sequences automatically based on product purchase events.
- **Limitations**: No order bumps, no upsell/downsell flows, no cart/checkout page customization. For complex digital product sales with bundles and upsells, use Gumroad, Lemon Squeezy, or Kit Commerce and connect to MailerLite for email follow-up.
- **Best for**: Solopreneurs and creators already using MailerLite who want to sell 1-3 simple digital products (ebooks, templates) without adding another platform.

### In Gumroad
Gumroad is the simplest platform for selling digital products — zero monthly fees, upload and price in minutes:
- **Pricing**: 10% + $0.50 per sale (no monthly fee). Discover marketplace sales cost 30%. No volume discounts.
- **Product types**: Digital downloads, courses, memberships, software (with license keys), bundles, physical products.
- **Pay-what-you-want**: Set a minimum (including $0) and let buyers choose their price. Good for building an audience.
- **Gumroad Discover**: Built-in marketplace for organic traffic — but requires at least one sale before your product appears. Don't rely on it as your only traffic source.
- **Tax handling**: Full Merchant of Record since Jan 2025 — Gumroad handles all VAT/GST/sales tax globally.
- **PayPal removed**: Since Oct 2024, buyers can only pay via credit/debit card. This may reduce conversions for audiences that prefer PayPal.
- **Fee impact on low-priced products**: A $5 product loses ~20% to Gumroad fees (before payment processing). Bundle products or price at $25+ to reduce the effective rate.
- **Email broadcasts**: Basic — good for product announcements, but no automation or sequences. Use a dedicated ESP for marketing campaigns.
- **Best for**: First-time creators, side projects, quick product launches, software license key distribution. Move to Payhip or Lemon Squeezy when revenue exceeds ~$3K/month and fees become painful.
- For platform-specific setup, use `/sales-gumroad`.

### In Sellfy
Sellfy is a creator storefront for digital products, print-on-demand merch, physical goods, and subscriptions:
- **Pricing model is unusual — sales-volume caps, not per-sale fees**: 0% Sellfy transaction fee on all tiers (processor ~2.9%+30¢ still applies), but each tier caps **annual revenue** — Starter ~$10k ($22/mo annual), Business ~$50k ($59/mo), Premium ~$200k ($119/mo). Crossing the cap forces an upgrade, so model expected *annual* revenue, not just feature needs. Premium's ~$200k ceiling can be a hard wall for scaling sellers.
- **Digital protection built in**: PDF stamping + download limits, auto-delivery via unique links — good for ebooks/files you don't want freely shared.
- **Print-on-demand**: native POD (t-shirts, mugs, etc.) via 11 fulfillment centers — handy if you want merch alongside downloads without a separate Printful/Printify setup.
- **Feature gates**: product upselling, cart abandonment, and affiliate marketing are **Business+**, not on Starter.
- **Not a Merchant of Record**: you own VAT/GST/sales tax. Limited design (~10 themes), no blog, weak SEO. Payments are Stripe/PayPal only.
- **Automation**: no public REST API — only outbound webhooks + a Zapier API token. Fine for event-driven CRM sync, not for programmatic catalog management.
- **Best for**: creators who want a quick all-in-one store (downloads + merch + subscriptions) with file protection. Compare with Payhip (all features on free tier, EU/UK VAT handled) and Gumroad (full MoR tax). For setup, use `/sales-sellfy`.

### In Printful (print-on-demand merch)
Printful adds a **physical merch channel** alongside your digital products — print-on-demand apparel, accessories, and all-over print with no inventory:
- **Fulfillment model**: you upload designs, Printful prints and ships on demand. It owns its fulfillment (more consistent quality + in-house branding/embroidery) vs Printify, which brokers a provider network. No upfront inventory cost.
- **How it connects**: plug it into a store (Shopify/WooCommerce/Etsy/Wix/Squarespace) so orders auto-fulfill, or run **headless via its REST API** (create orders, generate mockups, quote shipping). Always order by `catalog_variant_id`, not product id.
- **Pricing**: Free $0 (509 products, unlimited stores). Growth $24.99/mo — **free above $12K/yr sales** — for up to 33% off product pricing + 9% off branding. Add-ons cost per item (inside label $0.99, outside label $2.49, premium image $1, embroidery digitization $2.95–$6.50). Your margin = retail − (base + fulfillment + shipping).
- **Shipping caveat**: US/EU orders ~5 days, worldwide can be 10–14 — if 30%+ of buyers are international, weigh **Gelato** (local print network) instead.
- **Automation**: v2 REST API (Bearer token, 120 req/60s leaky bucket) + 19 signed webhook events; community MCP server for Claude/Cursor. For setup/integration, use `/sales-printful`.

### In CustomCat (budget US print-on-demand)
CustomCat is the **margin-first POD alternative** — lowest base prices and fastest US production, with branding and reach traded away:
- **Fulfillment model**: in-house production in Detroit (1–3 business-day turnaround — the fastest of the big three), so you carry no inventory. Decoration via DIGISOFT™ (DTG/DTF), embroidery, and dye sublimation across 200+ products.
- **The two big trade-offs vs Printful**: **no private-label branding** (products keep the manufacturer's tags — no custom neck labels or packing slips) and **US-only fulfillment** (international shipping runs 1–4 weeks). Pick CustomCat for cheap domestic merch; pick Printful for branded unboxing, or **Gelato** for fast international.
- **How it connects**: store connectors for **Shopify/Etsy/WooCommerce/BigCommerce** (fewer than Printful's 20+), CSV upload, or **headless via the REST API** (`customcat-beta.mylocker.net/api/v1/`).
- **Pricing**: **Lite $0** (full catalog at standard wholesale), **Pro $30/mo or $300/yr (≈$25/mo, 60-day trial)** for **20–40% off** the catalog, **Enterprise** custom (30–50% off + custom API). Pro only pays off once its discount on your monthly volume beats $30. Back print adds $5/line item. Not a Merchant of Record (you own tax).
- **Automation**: REST API with **read-only + read-write keys** (a read-only key on a write call = `403`), `order_id` as the idempotency key, and **6 unsigned webhook topics** (verify the echoed read-only key + keep a `/order/status` polling backup). For setup/integration, use `/sales-customcat`.

### In SendOwl
SendOwl is the **delivery-security-first** option — built to sell and *securely deliver* downloads, not to be a storefront:
- **Delivery protection is the differentiator**: per-product download limits + link expiry, **PDF stamping** (embeds the buyer's identity to deter sharing), and **license keys** for software. The most common reason to pick SendOwl over Gumroad/Payhip is "customers keep sharing my link."
- **Pricing (best-effort, 2026)**: subscription model, **no free tier**, **no per-transaction fee** — Launch $39/mo, Grow $87, Scale $159, Business $299+. Plans cap **orders/year and sales/year** (Launch ~$10k, Grow ~$36k, Scale ~$100k); crossing a cap forces an upgrade. **All features on every plan** (API, subscriptions, stamping, license keys, upsells, affiliates). Reviewers report **abrupt, large price increases** — keep a migration path ready.
- **Hosts links, not files**: historically ~250-file cap; host large media externally (S3/Bunny/Cloudflare) and deliver the link through SendOwl. Not a Merchant of Record (you own VAT/GST).
- **Automation**: full **REST API** (Basic Auth; orders on `/api/v1_3/`, everything else `/api/v1/`, ~1 req/sec) + **HMAC-signed webhooks** (`X-SENDOWL-HMAC-SHA256`, 14 order/subscription events, 10 retries). Strong for syncing sales into a CRM/warehouse.
- **Best for**: creators selling downloads/software/ebooks/audio/video who prioritize file protection over storefront design. For setup/integration, use `/sales-sendowl`.

*You no longer need the platform guide details — focus on the user's specific situation.*

## Step 4 — Actionable guidance

## Gotchas

1. **Don't build before validating** — pre-sell or waitlist first. 50% of digital products never sell because the creator assumed demand. Even a simple "buy now, get it in 2 weeks" test is better than 3 months of silent building.

2. **Platform fees vary wildly** — Gumroad free tier takes 10%, Lemon Squeezy takes 5%, Kit takes 0.6%, WooCommerce takes 0%. At $10K+ in annual sales, the difference is hundreds to thousands of dollars. Model your fees before committing.

3. **Courses need ongoing maintenance** — a $497 course creates support expectations. Budget time for Q&A, community management, and content updates. Ebooks and templates are lower-maintenance products to start with.

4. **Price anchoring works both ways** — if you launch at $19, it's very hard to raise to $99 later with the same audience. Launch at a higher price and discount strategically rather than starting low.

5. **Tax compliance is real** — selling digital products internationally triggers VAT/GST obligations in the EU, UK, Australia, etc. Use a merchant of record (Lemon Squeezy, Paddle) or handle it yourself. Don't ignore this.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Before recommending a specific platform skill

This skill covers a strategy domain across many platforms. **Before pointing the user to any specific platform skill** (any `/sales-{platform}` listed in `## Related skills`, e.g., `/sales-mailshake`, `/sales-klaviyo`, `/sales-apollo`), read that platform skill's actual `SKILL.md` first. The 1-line description in `## Related skills` is enough to *identify* a candidate — it's not enough to *commit* to it or to write a prompt that invokes it well.

**How to read it:**
- If `~/.claude/skills/{skill-name}/SKILL.md` exists locally, `Read` it.
- For `sales-*` skills, `WebFetch` directly from this repo: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/{skill-name}/SKILL.md` — e.g., for `sales-mailshake`: `https://raw.githubusercontent.com/sales-skills/sales/main/skills/sales-mailshake/SKILL.md`.
- For non-`sales-*` skills (third-party), look up `{org}/{repo}` in `~/.claude/skills/sales-do/references/skill-sources.md` if installed and fetch the same `skills/{skill-name}/SKILL.md` path under that repo.

**After reading,** ground your recommendation in something concrete from the SKILL.md (its scope, a sub-flow, its `argument-hint` shape, or a "Do NOT use for..." negative trigger). Align any generated invocation with the platform skill's `argument-hint`. If the platform skill turns out not to fit the user's situation, swap to another or handle the question here directly rather than recommending a poor fit.

## Related skills

- `/sales-checkout` — Checkout page optimization (upsells, order bumps, payment plans, cart abandonment)
- `/sales-membership` — Membership sites and online courses (recurring access, content dripping)
- `/sales-newsletter` — Newsletter monetization (paid subscriptions, sponsorships)
- `/sales-audience-growth` — Growing your audience (lead magnets, referrals, cross-promotion)
- `/sales-email-marketing` — Email marketing (launch sequences, nurture campaigns)
- `/sales-funnel` — Sales funnel strategy (landing pages, conversion paths)
- `/sales-mailerlite` — MailerLite platform help (digital product sales, paid newsletters)
- `/sales-kit` — Kit platform help (Kit Commerce setup)
- `/sales-groove` — Groove.cm platform help (GrooveSell, GroovePages)
- `/sales-beehiiv` — Beehiiv platform help (digital products, paid subscriptions, newsletter monetization)
- `/sales-podia` — Podia platform help (courses, downloads, memberships, coaching, email)
- `/sales-payhip` — Payhip platform help (digital downloads, courses, memberships, coaching, store builder, API)
- `/sales-gumroad` — Gumroad platform help (digital products, license keys, Discover marketplace, API, webhooks)
- `/sales-lemonsqueezy` — Lemon Squeezy platform help (payments, subscriptions, license keys, tax compliance as merchant of record)
- `/sales-sellfy` — Sellfy platform help (creator storefront: digital products, print-on-demand merch, subscriptions; 0% fee with annual sales-volume caps; PDF stamping; webhooks + Zapier, no REST API; not a MoR)
- `/sales-printful` — Printful platform help (print-on-demand merch fulfillment; REST API v2 + signed webhooks, mockup generator, store connectors; Free vs Growth plan; SKU/sync-variant and failed-order troubleshooting)
- `/sales-customcat` — CustomCat platform help (budget US print-on-demand; lowest base prices + 1–3 day production, no private-label branding, US-only; REST API with read/write keys + 6 unsigned webhook topics; Lite vs Pro plan)
- `/sales-sendowl` — SendOwl platform help (delivery-security-first: download-limit/expiry links, PDF stamping, license keys, subscriptions, drip; REST API + HMAC-signed webhooks; subscription pricing with annual order/sales caps, no free tier)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: First digital product
**User says**: "I want to create and sell my first ebook about freelance copywriting"
**Skill does**: Recommends validation via pre-sale to newsletter, suggests $29 pricing with bundle option ($49 with template swipe file), compares Kit Commerce vs Gumroad for delivery, provides launch email sequence
**Result**: User has a validated product idea, pricing strategy, platform choice, and 7-day launch plan

### Example 2: Platform selection
**User says**: "I'm selling a Notion template pack — should I use Gumroad or Lemon Squeezy?"
**Skill does**: Compares fees (Gumroad 10% free tier vs Lemon Squeezy 5%), tax handling (LS is merchant of record), checkout experience, and discovery features. Recommends Lemon Squeezy for international sales, Gumroad for discovery.
**Result**: User makes an informed platform choice based on their priorities

### Example 3: Course launch
**User says**: "I have a 3,000-subscriber list and want to launch a $297 course on data analytics"
**Skill does**: Designs a 4-week launch sequence (tease → waitlist → early-bird → open → close), recommends payment plan option ($3 × $107), suggests Kit Commerce or Podia, provides revenue projection (3K × 2% = 60 sales = $17,820)
**Result**: User has a complete launch plan with email sequence, pricing, and revenue targets

## Troubleshooting

### Low conversion on product page
**Symptom**: Traffic to product page but <1% conversion
**Cause**: Weak value proposition, no social proof, price not justified, too many options
**Solution**: Add testimonials (even from beta testers). Show the transformation ("before → after"). Add a money-back guarantee. Remove distracting navigation. Test a lower entry price with an upsell.

### High refund rate (>10%)
**Symptom**: Sales coming in but refund requests exceed 10%
**Cause**: Product doesn't match the sales page promise, or product quality is low
**Solution**: Survey refund requesters (what did they expect?). Align sales copy with actual product content. Add a "getting started" email immediately after purchase. Consider a lower price point if expectations are too high.

### Can't get first 10 sales
**Symptom**: Product is live but not selling
**Cause**: No audience, no launch event, or selling to wrong people
**Solution**: Don't rely on organic discovery. Email your list with a dedicated launch sequence (not just a mention). Offer founding member pricing (50% off first 20 buyers). Ask 5 people personally to buy and give feedback. If you have no audience, use `/sales-audience-growth` first.

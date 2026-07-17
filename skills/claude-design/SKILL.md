---
name: claude-design
description: >-
  Connect to Claude Design and turn a Claude-generated design into a live,
  editable Base44 app. Use this whenever Bea has created a design in Claude
  (the in-chat design / artifact feature) and wants to publish it, ship it,
  build on it, or hand it to a client — i.e. any time she says "import my
  Claude design", "connect this design to Base44", "make my design into a
  real site/app", or shares a Claude Design export URL.
---

# Claude Design → Base44

This skill bridges a design Bea creates inside **Claude Design** (Claude's
in-chat visual design feature) into **Base44**, where it becomes a real,
editable, deployable web app. This is the core Studio Bea Sophia loop:
design illustrated layouts in Claude, then turn them into live sites for
independent businesses.

## How the connection works

Claude Design exports a finished design as a **self-contained HTML bundle**
(all images, fonts, and styles inlined) hosted at a **public HTTPS URL**.
Base44 fetches that URL server-side and starts building an editable app from
it, returning a Base44 Editor URL immediately so Bea can watch it build.

```
Claude Design  ──export──►  public HTML URL  ──import──►  Base44 editable app
```

The bridge tool is `mcp__Base44__import-claude-design-from-url`.

## When to use this skill

- Bea has a design in Claude and wants it as a real website/app.
- Bea pastes a Claude Design export/share URL.
- Bea says "connect my design", "import to Base44", "make this live".

If Bea instead wants to build an app **from a text description** (no existing
design), use `mcp__Base44__create_base44_app` instead — that path skips the
design import.

## Steps

1. **Get the design URL.**
   - If Bea pasted a public HTTPS URL to the design export, use it directly.
   - If she hasn't, ask her to export/share the design from Claude Design and
     paste the link. The export URL is only valid for **~1 hour**, so import
     promptly.

2. **Import into Base44.** Call `mcp__Base44__import-claude-design-from-url`:
   - `url`: the public HTTPS design URL (required).
   - `title`: a clear name for the app (e.g. the client/project name).

3. **Send Bea the Editor URL immediately.** The tool returns a Base44 Editor
   URL right away. Surface that link to Bea first thing so she can watch the
   build progress — don't wait for the build to finish.

4. **Confirm and next steps.** Let Bea know the app is building in Base44 and
   that all further editing happens in the Base44 Editor (not this chat).
   Offer to list her apps (`mcp__Base44__list_user_apps`) if she wants to
   find it again later.

## Guardrails

- The import URL must be **publicly fetchable over HTTPS** — Base44 fetches it
  server-side. Local files or login-gated links won't work.
- Export URLs expire (~1 hour). If the import fails on a stale link, ask Bea
  to re-export and retry.
- Don't rewrite or "improve" the design before importing — import the export
  as-is; refinements happen in the Base44 Editor afterward.

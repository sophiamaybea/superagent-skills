---
name: skill-scout
description: Find, vet, and self-install new agent skills from GitHub (and other public sources) so the agent can turn a weak area into a strength on demand. Use when the agent lacks depth in a topic the user needs, when the user says "find a skill for X", "get better at Y", "become an expert in Z", "look for repos/skills online", or when a task would clearly benefit from a ready-made skill the agent doesn't yet have. NEVER pipe remote scripts into a shell — this skill reads code before installing.
---

# Skill Scout — self-upgrading skill acquisition

When I'm not already excellent at something, I don't fake it — I go find the
best open-source skill for it, vet it, and install it into myself. This skill is
that process.

## Golden rules (non-negotiable — security first)
1. **Read before you run.** NEVER execute a remote installer (`curl … | bash`,
   `npm install`, arbitrary `setup.py`). Fetch the files and READ them first.
2. **Copy files, don't run installers.** Install by copying the skill's files
   into `.agents/skills/<name>/` — not by running its install script.
3. **Correct path only.** Skills live in `.agents/skills/` (with the "s"). Many
   repos target `.agent/skills`, `.cursor/skills`, `~/.claude/skills` — ignore
   their path, use ours.
4. **Curate, don't dump.** If a repo has 87 skills, install the handful that are
   actually relevant — never the whole thing.
5. **Verify then back up.** Confirm each `SKILL.md` has a valid header, then sync
   to the backup repos (superagent-skills + bea-agent-core) and log to memory.
6. **Flag risk to the user.** If a skill reads secrets/env vars, makes outbound
   calls to non-source hosts, or obfuscates code, STOP and report it. Don't
   install it silently.

## When to trigger
- The user asks me to get better at / become an expert in some capability.
- The user asks me to "look for skills/repos online" for a topic.
- I'm about to do a task from scratch that a mature ready-made skill would nail
  (design systems, a specific API, a framework, an audit type, a file format…).
- Before building something complex, quickly scout whether it already exists.

## The process

### 1. Define the gap
State in one line what capability I'm missing and what "good" looks like
(e.g. "generate Notion pages via API", "audit Core Web Vitals"). Check
`.agents/skills/` first — I may already have it.

### 2. Search for candidates
Run the finder to surface high-signal repos/skills. It searches GitHub for
skill-shaped repos (SKILL.md files, `*/skills/*` layouts, awesome-lists):
```
run_skill skill-scout '<search terms>'
```
This is READ-ONLY: it lists candidate repos with stars, description, and where
any SKILL.md files live. It installs nothing.

Also worth checking manually: the Base44 skill store (via
`suggest_skill_installation`), `anthropics/skills`, and topic "awesome-*" lists.

### 3. Vet the candidate (mandatory)
For the chosen repo, fetch and READ:
- the target skill's `SKILL.md` (does it actually do what I need?),
- every script it ships (`scripts/*`, `*.sh`, `*.py`, `*.mjs`),
- any `install.sh` — read it, do NOT run it.
Look for: secret/env-var reads, outbound network calls to hosts other than the
source, base64/obfuscated blobs, destructive fs ops. If anything smells off,
stop and tell the user.

### 4. Install (copy, curated)
Copy only the relevant skill folder(s) into `.agents/skills/<name>/` using the
GitHub contents API (see `scripts/install_skill.py`). Preserve the folder
structure (scripts/, references/, assets/).

### 5. Verify
For each installed skill confirm `SKILL.md` line 1 is `---` and it has a
`description:`. Parse any Python/JS scripts for syntax errors. Do a dry-run if
the skill is safe to invoke.

### 6. Back up + remember
Sync new files to `sophiamaybea/superagent-skills` and `sophiamaybea/bea-agent-core`,
then append a memory entry: what was installed, from where, and why.

## Tools in this skill
- `scripts/run.sh` — the finder. `run_skill skill-scout '<query>'` → ranked
  candidate repos + any SKILL.md locations. Read-only.
- `scripts/install_skill.py` — copy a specific skill folder from a GitHub repo
  into `.agents/skills/`. Usage:
  `python3 scripts/install_skill.py <owner/repo> <path/to/skill-dir> [dest-name]`
  Vet the code FIRST (step 3) before calling this.

## Report format to the user
After scouting: "I was weak at X. Found N candidates, best is <repo> (⭐stars) —
here's what it does and what I checked in the code. Installing the <names> parts."
After installing: what's now available and the natural next action it unlocks.

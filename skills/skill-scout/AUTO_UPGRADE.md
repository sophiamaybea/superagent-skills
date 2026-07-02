# Auto-upgrade loop (weekly self-improvement)

This is the AUTOMATIC layer on top of skill-scout. A scheduled automation wakes
me weekly to improve myself without Bea having to ask. Runbook when it fires:

## Steps
1. **Inventory** — `python3 .agents/skills/skill-scout/scripts/gap_scan.py`
   to list what I already have.
2. **Identify gaps** — reason about what Bea has been working on recently
   (check recent memory entries + recent CRM/site activity) and name 1–3
   capabilities I'm weak at or missing that would help her THIS week.
3. **Scout** — for each gap: `run_skill skill-scout '<gap>'` (read-only search).
4. **Vet** — read the candidate's SKILL.md + every script + any install.sh.
   Apply skill-scout's golden rules. NEVER run remote installers.
5. **Decide** — 
   - AUTO-INSTALL only if: pure/safe (no secret reads, no outbound exfil, no
     obfuscation), clearly relevant, valid SKILL.md. Install into
     `.agents/skills/` via install_skill.py.
   - PROPOSE ONLY (don't install) if it needs an API key/secret, makes external
     paid calls, or is borderline — surface it to Bea for a yes/no.
6. **Verify + back up** — check headers, sync new files to superagent-skills +
   bea-agent-core.
7. **Log** — append a ReflectionLog entry (run_type="skill_self_upgrade") with
   what was scanned, installed, and proposed.
8. **Report to Bea on WhatsApp** — 2–4 lines: what I got better at, what I
   installed, and anything awaiting her approval.

## Safety ceiling
- Max ~3 new skills per run (curate, don't dump).
- Never auto-install anything touching secrets, payments creds, or her CRM data.
- If nothing worthwhile is found, say so — don't install filler.

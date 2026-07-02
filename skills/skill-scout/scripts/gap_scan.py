#!/usr/bin/env python3
"""skill-scout gap-scan — READ-ONLY self-audit.
Lists my currently installed skills so I (the agent) can reason about gaps
against what Bea has been working on, then decide what to scout. Prints a
compact inventory; installs nothing.
"""
import os, glob

BASE = os.path.join(os.getcwd(), ".agents", "skills")

def first_desc(skill_md):
    try:
        lines = open(skill_md, encoding="utf-8").read().splitlines()
    except Exception:
        return ""
    for i, l in enumerate(lines):
        if l.strip().startswith("description:"):
            d = l.split("description:", 1)[1].strip()
            return (d if d not in (">", "|") else (lines[i+1].strip() if i+1 < len(lines) else ""))[:90]
    return ""

skills = []
for sk in sorted(glob.glob(os.path.join(BASE, "*"))):
    md = os.path.join(sk, "SKILL.md")
    flat = sk if os.path.isfile(sk) and sk.endswith((".sh", ".py", ".mjs")) else None
    if os.path.isfile(md):
        skills.append((os.path.basename(sk), first_desc(md)))
    elif flat:
        skills.append((os.path.basename(sk), "(flat script skill)"))

print(f"INSTALLED SKILLS ({len(skills)}):")
for name, desc in skills:
    print(f"  • {name} — {desc}")
print("\nGap-scan complete. Reason about what capability Bea needs next that")
print("ISN'T covered above, then run the finder: run_skill skill-scout '<gap>'")

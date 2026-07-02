#!/usr/bin/env bash
# skill-scout finder — READ-ONLY. Searches GitHub for skill-shaped repos/files.
# Usage: run_skill skill-scout '<search terms>'
set -euo pipefail

QUERY="${*:-}"
if [ -z "$QUERY" ]; then
  echo "Usage: run_skill skill-scout '<what capability do you need>'"
  exit 1
fi

AUTH=()
if [ -n "${GITHUB_ACCESS_TOKEN:-}" ]; then
  AUTH=(-H "Authorization: Bearer ${GITHUB_ACCESS_TOKEN}")
fi

echo "🔎 Scouting skills for: $QUERY"
echo "======================================================"

python3 - "$QUERY" <<'PYEOF'
import json, os, sys, urllib.parse, urllib.request

query = sys.argv[1]
token = os.environ.get("GITHUB_ACCESS_TOKEN", "")

def gh(url):
    hdr = {"Accept": "application/vnd.github+json", "User-Agent": "skill-scout"}
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=hdr)
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r), None
    except Exception as e:
        return None, str(e)

def search_repos(q, label):
    url = "https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + "&sort=stars&order=desc&per_page=6"
    data, err = gh(url)
    print(f"\n## {label}")
    if err or not data:
        print(f"  (search failed: {err})")
        return
    items = data.get("items", [])
    if not items:
        print("  (no results)")
        return
    for it in items:
        print(f"  ⭐ {it['stargazers_count']:>6}  {it['full_name']}")
        desc = (it.get('description') or '').strip()
        if desc:
            print(f"          {desc[:100]}")

# 1) repos that look like skill collections
search_repos(f"{query} skill", "Repos matching your topic + 'skill'")
# 2) awesome-lists (curated directories)
search_repos(f"awesome {query}", "Curated 'awesome' lists")
# 3) code search for SKILL.md files mentioning the topic (needs auth)
if token:
    url = "https://api.github.com/search/code?q=" + urllib.parse.quote(f"{query} filename:SKILL.md") + "&per_page=6"
    data, err = gh(url)
    print("\n## SKILL.md files mentioning your topic")
    if err or not data:
        print(f"  (code search unavailable: {err})")
    else:
        items = data.get("items", [])
        if not items:
            print("  (none found)")
        for it in items:
            repo = it["repository"]["full_name"]
            print(f"  📄 {repo} :: {it['path']}")
else:
    print("\n## SKILL.md code search\n  (skipped — needs GitHub auth)")

print("\n======================================================")
print("Next: pick a repo, then VET it (read SKILL.md + all scripts;")
print("read any install.sh, never run it). Then install with:")
print("  python3 .agents/skills/skill-scout/scripts/install_skill.py <owner/repo> <path/to/skill> [dest-name]")
PYEOF
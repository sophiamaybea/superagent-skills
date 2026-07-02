#!/usr/bin/env python3
"""skill-scout installer — copy ONE skill folder from a GitHub repo into
.agents/skills/. Does NOT run any remote scripts; it only downloads files.

VET THE CODE FIRST (read SKILL.md + all scripts + any install.sh) before running.

Usage:
  python3 install_skill.py <owner/repo> <path/to/skill-dir> [dest-name] [--ref BRANCH]
Example:
  python3 install_skill.py anthropics/skills skills/skill-creator
"""
import base64, json, os, sys, urllib.request

def gh(url):
    token = os.environ.get("GITHUB_ACCESS_TOKEN", "")
    hdr = {"Accept": "application/vnd.github+json", "User-Agent": "skill-scout"}
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=hdr)) as r:
        return json.load(r)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ref = None
    if "--ref" in sys.argv:
        ref = sys.argv[sys.argv.index("--ref") + 1]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    repo, skill_path = args[0], args[1].rstrip("/")
    dest_name = args[2] if len(args) > 2 else os.path.basename(skill_path)
    dest_base = os.path.join(os.getcwd(), ".agents", "skills")
    dest = os.path.join(dest_base, dest_name)

    if os.path.exists(dest):
        print(f"⚠️  {dest} already exists — files will be overwritten/merged.")

    refq = f"?ref={ref}" if ref else ""
    count = [0]

    def walk(path, out):
        os.makedirs(out, exist_ok=True)
        listing = gh(f"https://api.github.com/repos/{repo}/contents/{path}{refq}")
        if isinstance(listing, dict):  # single file
            listing = [listing]
        for f in listing:
            if f["type"] == "dir":
                walk(f["path"], os.path.join(out, f["name"]))
            elif f["type"] == "file":
                blob = gh(f["url"])
                data = base64.b64decode(blob["content"])
                with open(os.path.join(out, f["name"]), "wb") as fh:
                    fh.write(data)
                count[0] += 1
                print("  ↓", os.path.relpath(os.path.join(out, f["name"]), dest))

    print(f"Installing {repo}:{skill_path} -> {dest}")
    walk(skill_path, dest)

    # verify SKILL.md header
    sk = os.path.join(dest, "SKILL.md")
    ok = os.path.isfile(sk) and open(sk, encoding="utf-8").readline().strip() == "---"
    print(f"\n{count[0]} files installed. SKILL.md header: {'valid ✓' if ok else '⚠️ MISSING/INVALID'}")
    if not ok:
        print("  → check the skill has a proper '---\\nname:\\ndescription:\\n---' header.")

if __name__ == "__main__":
    main()

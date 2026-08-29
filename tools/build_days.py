#!/usr/bin/env python3
"""
Builds data/days.json - the wall of days.

The mods' git history was squashed flat when the repos were tidied up, so
GitHub has no day-by-day record left. The honest record that does survive is
on Elduin's Mac: every source file in every mod still carries the day it was
last written. This walks the mod folders, buckets those days, and writes out
which mods were being worked on each day.

Only file paths and modification times are read - never file contents.

Run on Elduin's Mac (it can't run in CI - the working copies only exist here):

    python3 tools/build_days.py [~/GitHub]

Then commit data/days.json. Days not in the file are drawn grey on the site.
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS_DIR = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "GitHub"

# What counts as "working on the mod": the mod's own source and assets, and the
# few top-level files that get edited by hand. Deliberately NOT the Gradle
# wrapper or anything copied in from a template - those carry the date somebody
# else made them, months before Elduin touched the mod, and would put phantom
# blocks on the wall.
KEEP = {".java", ".json", ".png", ".toml", ".md", ".mcmeta", ".mcfunction",
        ".accesswidener", ".ogg", ".properties"}
IGNORE = {"build", ".git", ".gradle", "gradle", "run", "libs", "node_modules",
          "dist", ".idea", "logs", "saves"}

# how many files a day has to touch to earn a darker block
LEVELS = ((40, 3), (12, 2), (1, 1))


def main():
    try:
        known = {m["repo"] for m in json.loads((ROOT / "data/mods.json").read_text())["mods"]}
    except FileNotFoundError:
        sys.exit("run tools/build_mods.py first - data/mods.json is missing")

    if not MODS_DIR.is_dir():
        sys.exit(f"{MODS_DIR} is not a folder - pass the folder the mods live in")

    counts, worked = {}, {}
    for repo in sorted(p for p in MODS_DIR.iterdir() if p.is_dir()):
        name = repo.name
        for path in repo.rglob("*"):
            if not path.is_file() or path.suffix not in KEEP:
                continue
            parts = path.relative_to(repo).parts
            if IGNORE & set(parts):
                continue
            if "src" not in parts:      # mod content only, nothing from a template
                continue
            day = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
            counts[day] = counts.get(day, 0) + 1
            if name in known:
                worked.setdefault(day, set()).add(name)

    days = {}
    for day in sorted(counts):
        n = counts[day]
        days[day] = {"v": next((lvl for floor, lvl in LEVELS if n >= floor), 0),
                     "n": n,
                     "mods": sorted(worked.get(day, ()))}

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "first": min(days) if days else None,
        "last": max(days) if days else None,
        "days": days,
    }
    (ROOT / "data/days.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"wrote data/days.json - {len(days)} days of building, "
          f"{out['first']} to {out['last']}")


if __name__ == "__main__":
    sys.exit(main())

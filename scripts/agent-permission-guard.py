#!/usr/bin/env python3
"""
TR-SEC-010 -- Agent tool permission allowlist guard (least agency).

"Make dangerous changes loud, not impossible": this script hard-codes the
reviewed baseline of approved permission grants for a settings file, co-located
in this same file rather than a separate config file. Widening the allowlist
requires editing REVIEWED_BASELINE here too, so the widening diff and the
settings-file diff land in the same pull request and the same code review --
instead of a silent allowlist edit nobody re-reviews.

Two independent checks:
  1. FORBIDDEN -- wildcard write/install/exec/network grants are never
     accepted, no matter what REVIEWED_BASELINE says (a barrier, not friction;
     see templates/threat-model.md's Impossible vs. Tedious section).
  2. UNREVIEWED -- any grant present in the settings file but absent from
     REVIEWED_BASELINE fails until a human adds it here.

Honest limit: this catches accidental or casual allowlist drift in a diff a
human is expected to read. It does not stop a determined author from editing
this script and the settings file in the same PR -- branch protection and
human review of settings/workflow diffs remain the real backstop. This is a
friction control against casual drift, not a barrier against a determined
attacker with repo write access.

Usage:
    python3 scripts/agent-permission-guard.py --settings PATH [--settings PATH ...]

Exit code 0 if clean, 1 if any forbidden or unreviewed grant is found, 2 on a
usage error (missing file, invalid JSON, no permissions.allow key).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Reviewed, currently-approved grants keyed by the --settings path exactly as
# invoked. Widening this requires a human to add the new grant here, in the
# same PR as the settings-file change that introduces it. This default
# baseline covers only this repo's own example fixture below -- copy this
# script into your own repo and curate REVIEWED_BASELINE against your own
# settings file(s); it is not a universal allowlist.
REVIEWED_BASELINE: dict[str, frozenset[str]] = {
    "examples/agent-permission-guard/settings.example.json": frozenset({
        "Bash(git status:*)",
        "Bash(pytest:*)",
    }),
}

# Never accepted regardless of REVIEWED_BASELINE -- a barrier, not friction.
_DANGEROUS_VERBS = (
    "pip install", "npm install", "bash -c", "python -c", "python3 -c",
    "git push", "curl", "cat >", "rm -rf", "sudo",
)
FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("wildcard_dangerous_verb", re.compile(
        r"(?:" + "|".join(re.escape(v) for v in _DANGEROUS_VERBS) + r").*\*"
    )),
    ("unrestricted_home_read", re.compile(r"Read\(//?\*\*\)")),
]


def load_allow_list(path: Path) -> list[str]:
    if not path.is_file():
        print(f"ERROR: settings file not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: {path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    allow = data.get("permissions", {}).get("allow")
    if allow is None:
        print(f"ERROR: {path} has no permissions.allow list", file=sys.stderr)
        sys.exit(2)
    return list(allow)


def check_file(path: Path, baseline_key: str) -> list[str]:
    violations: list[str] = []
    baseline = REVIEWED_BASELINE.get(baseline_key, frozenset())
    for grant in load_allow_list(path):
        forbidden_hit = False
        for name, pattern in FORBIDDEN_PATTERNS:
            if pattern.search(grant):
                violations.append(
                    f"FORBIDDEN [{name}] {baseline_key}: {grant!r} -- wildcard "
                    "write/install/exec/network grants are never allowed"
                )
                forbidden_hit = True
        if not forbidden_hit and grant not in baseline:
            violations.append(
                f"UNREVIEWED {baseline_key}: {grant!r} -- not in REVIEWED_BASELINE; "
                "add it to scripts/agent-permission-guard.py in this PR if intentional"
            )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--settings", action="append", required=True, dest="settings_paths",
        help="Path to a settings.json/settings.local.json file; repeatable",
    )
    args = parser.parse_args()

    all_violations: list[str] = []
    for raw_path in args.settings_paths:
        all_violations.extend(check_file(Path(raw_path), raw_path))

    if all_violations:
        for v in all_violations:
            print(v)
        return 1
    print("OK -- no forbidden or unreviewed agent permission grants.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

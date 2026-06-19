#!/usr/bin/env python3
"""
TR-PUB-002 / TR-PUB-003 — Validate a public standards repo checkout.

Checks:
  1. Required public docs exist (README, LICENSE, ATTRIBUTIONS, etc.)
  2. Generic public-repo hygiene: env/runtime artifact paths and secret-like content
  3. Python scripts compile

Usage:
    python3 scripts/public-export-check.py [REPO_ROOT]

Exit code 0 if clean, 1 if any check fails.
Default REPO_ROOT: current directory.

This script is intended to be published with the public repo. Maintainers may run
additional release checks outside this repository before publishing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_DOCS = [
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "ATTRIBUTIONS.md",
    "CONTRIBUTING.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "SECURITY.md",
]

FORBIDDEN_PATH_PARTS = {
    ".env", "data", "logs", ".venv", "venv", ".pages_repo",
}

SKIP_PATH_PARTS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache"}

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("aws_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github_token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("openai_key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9\-]{20,}")),
    ("generic_api_key", re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{16,}")),
]

def resolve_repo_root(arg: str | None) -> Path:
    if arg is None:
        return Path.cwd()
    p = Path(arg)
    return p if p.is_absolute() else Path.cwd() / p


def check_required_docs(repo_root: Path) -> list[str]:
    issues = []
    for name in REQUIRED_DOCS:
        if not (repo_root / name).is_file():
            issues.append(f"MISSING required doc: {name}")
    return issues


def check_forbidden_paths(repo_root: Path) -> list[str]:
    issues = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if set(path.parts) & SKIP_PATH_PARTS:
            continue
        parts = set(path.parts)
        hit = parts & FORBIDDEN_PATH_PARTS
        if hit:
            issues.append(f"FORBIDDEN path segment {hit}: {path.relative_to(repo_root)}")
        if path.name.startswith(".env"):
            issues.append(f"FORBIDDEN env file: {path.relative_to(repo_root)}")
    return issues


def check_secret_patterns(repo_root: Path) -> list[str]:
    issues = []
    skip_suffixes = {".png", ".jpg", ".gif", ".pyc", ".woff", ".ico"}
    for path in repo_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in skip_suffixes:
            continue
        if set(path.parts) & SKIP_PATH_PARTS:
            continue
        rel = path.relative_to(repo_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                issues.append(f"SECRET pattern {name}: {rel}")
    return issues


def check_python_compile(repo_root: Path) -> list[str]:
    issues = []
    scripts_dir = repo_root / "scripts"
    if not scripts_dir.is_dir():
        return issues
    for path in scripts_dir.glob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as e:
            issues.append(f"SYNTAX {path.relative_to(repo_root)}: {e}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=None,
        help="Public repository root (default: current directory)",
    )
    args = parser.parse_args()
    repo_root = resolve_repo_root(args.repo_root).resolve()

    if not repo_root.is_dir():
        print(f"ERROR: public repository root not found: {repo_root}", file=sys.stderr)
        return 1

    print(f"Checking public repo: {repo_root}")
    all_issues: list[str] = []
    all_issues.extend(check_required_docs(repo_root))
    all_issues.extend(check_forbidden_paths(repo_root))
    all_issues.extend(check_secret_patterns(repo_root))
    all_issues.extend(check_python_compile(repo_root))

    if all_issues:
        print(f"\nFAILED — {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            print(f"  {issue}")
        print("\nSee TR-PUB-002 / TR-PUB-003.")
        return 1

    print("OK — public repo self-check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

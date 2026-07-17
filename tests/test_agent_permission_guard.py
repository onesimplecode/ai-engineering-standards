"""Pins the CLI contract of scripts/agent-permission-guard.py (TR-SEC-010, v0.5
roadmap "make dangerous changes loud, not impossible" guard).

Contract under test: exit 0 on a settings file whose grants are all present in
REVIEWED_BASELINE and none match a forbidden pattern; exit 1 when a forbidden
wildcard grant or an unreviewed grant is found; exit 2 on a usage error
(missing file, invalid JSON, no permissions.allow key).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "scripts" / "agent-permission-guard.py"

# Matches the REVIEWED_BASELINE key hard-coded in the guard for this fixture.
BASELINE_KEY = "examples/agent-permission-guard/settings.example.json"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GUARD), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def write_settings(path: Path, grants: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"permissions": {"allow": grants}}), encoding="utf-8")


def test_shipped_fixture_fails_with_forbidden_and_unreviewed_grants() -> None:
    result = run("--settings", BASELINE_KEY)
    assert result.returncode == 1
    assert "FORBIDDEN" in result.stdout
    assert "'Bash(pip install:*)'" in result.stdout
    assert "UNREVIEWED" in result.stdout
    assert "'Bash(ruff check:*)'" in result.stdout


def test_clean_baseline_only_grants_pass(tmp_path: Path) -> None:
    settings = tmp_path / BASELINE_KEY
    write_settings(settings, ["Bash(git status:*)", "Bash(pytest:*)"])
    result = subprocess.run(
        [sys.executable, str(GUARD), "--settings", BASELINE_KEY],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert "OK" in result.stdout


def test_forbidden_wildcard_grant_fails_even_if_added_to_baseline(tmp_path: Path) -> None:
    settings = tmp_path / BASELINE_KEY
    write_settings(settings, ["Bash(git status:*)", "Bash(pytest:*)", "Bash(curl:*)"])
    result = subprocess.run(
        [sys.executable, str(GUARD), "--settings", BASELINE_KEY],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 1
    assert "FORBIDDEN" in result.stdout
    assert "'Bash(curl:*)'" in result.stdout


def test_unreviewed_grant_not_matching_baseline_key_fails(tmp_path: Path) -> None:
    other_path = "some/other/settings.json"
    settings = tmp_path / other_path
    write_settings(settings, ["Bash(git status:*)"])
    result = subprocess.run(
        [sys.executable, str(GUARD), "--settings", other_path],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 1
    assert "UNREVIEWED" in result.stdout


def test_missing_file_exits_2() -> None:
    result = run("--settings", "does/not/exist.json")
    assert result.returncode == 2
    assert "not found" in result.stderr


def test_invalid_json_exits_2(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text("{not valid json", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(GUARD), "--settings", "settings.json"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 2
    assert "not valid JSON" in result.stderr


def test_missing_permissions_allow_key_exits_2(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({"permissions": {}}), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(GUARD), "--settings", "settings.json"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert result.returncode == 2
    assert "no permissions.allow list" in result.stderr

"""Pins the behavior config-drift-demo.yml and downstream users depend on.

No test previously existed for check-config-consistency.py. These pin the CLI
contract described in its own docstring: exit 0 clean, exit 1 on retired
strings/drift, exit 2 on a usage error (bad --root, unknown --app, zero apps
discovered) — and that DRIFT locations aren't duplicated by overlapping
SCAN_GLOBS patterns matching the same file.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check-config-consistency.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_default_root_has_no_top_level_apps() -> None:
    # This repo intentionally has no top-level app directories (see
    # .github/workflows/config-drift-demo.yml) — pins that discover_apps() stays
    # non-recursive, so it can never reach examples/worked-example/sample-app/
    # two levels down.
    result = run()
    assert result.returncode == 2
    assert "No apps discovered" in result.stderr


def test_worked_example_fixture_is_detected() -> None:
    result = run("--root", "examples/worked-example", "--app", "sample-app")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "DRIFT" in result.stdout
    assert "local-gemma-model" in result.stdout
    # One location per file, not duplicated by overlapping SCAN_GLOBS patterns
    # matching the same "search_config.yaml.example" file twice.
    assert result.stdout.count("search_config.yaml.example:5") == 1


def test_unknown_app_name_exits_two_with_known_list() -> None:
    result = run("--root", "examples/worked-example", "--app", "does-not-exist")
    assert result.returncode == 2
    assert "Unknown app(s): does-not-exist" in result.stderr
    assert "sample-app" in result.stderr


def test_nonexistent_root_exits_two_not_a_crash() -> None:
    result = run("--root", "./this-directory-does-not-exist")
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "does not exist" in result.stderr

"""Public repo CI tests — run from public-standards/ root when published standalone."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "public-export-check.py"


def test_public_repo_root_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECK), "."],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr

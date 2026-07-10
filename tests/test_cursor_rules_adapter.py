"""Pins the CLI contract of scripts/cursor-rules-adapter.py (v0.4 roadmap item 1).

Contract under test: exit 0 on successful generation or a clean --check,
exit 1 when --check finds drift (changed, missing, or stale .mdc files),
exit 2 on a usage error (missing registry, unparseable registry). Output is
deterministic: one .mdc file per included registry section, Cursor MDC
frontmatter (description / alwaysApply per https://cursor.com/docs/context/rules),
"Public Release" sections and non-active requirements excluded.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADAPTER = ROOT / "scripts" / "cursor-rules-adapter.py"

FIXTURE_REGISTRY = """\
# Comment header, ignored by the parser.
requirements:

  - id: TR-SEC-001
    title: No hardcoded secrets
    status: active
    section: "Secrets Management"
    text: >
      All secrets must be stored in a vault. Never hardcoded in configuration files,
      source code, comments, or test fixtures.

  - id: TR-SEC-003
    title: PII routed to local LLM only
    status: active
    section: "Agents"
    text: >
      For privacy-focused use cases, local LLMs must be used.

  - id: TR-TEST-001
    title: TDD required for core logic
    status: active
    section: "Testing"
    text: >
      Tests are written before or alongside core logic.

  - id: TR-TEST-999
    title: Retired testing requirement
    status: retired
    section: "Testing"
    text: >
      Must not appear in generated rules.

  - id: TR-PUB-001
    title: Curated public release scope
    status: active
    section: "Public Release"
    text: >
      Repo-release operations, not coding rules; excluded from the export.
"""


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ADAPTER), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def write_fixture(tmp_path: Path) -> Path:
    registry = tmp_path / "tr-registry.yaml"
    registry.write_text(FIXTURE_REGISTRY, encoding="utf-8")
    return registry


def generate(tmp_path: Path) -> Path:
    registry = write_fixture(tmp_path)
    out = tmp_path / "rules"
    result = run("--registry", str(registry), "--out", str(out))
    assert result.returncode == 0, result.stderr
    return out


# --- generation ---------------------------------------------------------


def test_generates_one_mdc_per_included_section(tmp_path: Path) -> None:
    out = generate(tmp_path)
    names = sorted(p.name for p in out.glob("*.mdc"))
    assert names == ["agents.mdc", "secrets-management.mdc", "testing.mdc"]


def test_public_release_section_is_excluded(tmp_path: Path) -> None:
    out = generate(tmp_path)
    assert not (out / "public-release.mdc").exists()
    all_text = "".join(p.read_text(encoding="utf-8") for p in out.glob("*.mdc"))
    assert "TR-PUB-001" not in all_text


def test_non_active_requirements_are_excluded(tmp_path: Path) -> None:
    out = generate(tmp_path)
    testing = (out / "testing.mdc").read_text(encoding="utf-8")
    assert "TR-TEST-999" not in testing
    assert "Retired testing requirement" not in testing


def test_safety_sections_get_always_apply_true(tmp_path: Path) -> None:
    out = generate(tmp_path)
    secrets = (out / "secrets-management.mdc").read_text(encoding="utf-8")
    agents = (out / "agents.mdc").read_text(encoding="utf-8")
    testing = (out / "testing.mdc").read_text(encoding="utf-8")
    assert "alwaysApply: true" in secrets
    # PII routing (TR-SEC-003) is safety-critical; its "Agents" section is always on.
    assert "alwaysApply: true" in agents
    assert "alwaysApply: false" in testing


def test_frontmatter_and_body_shape(tmp_path: Path) -> None:
    out = generate(tmp_path)
    secrets = (out / "secrets-management.mdc").read_text(encoding="utf-8")
    # MDC frontmatter delimiters, description naming the section and TR IDs.
    assert secrets.startswith("---\n")
    assert "description:" in secrets
    assert "Secrets Management" in secrets
    assert "TR-SEC-001" in secrets
    # Requirement rendered as heading + folded text joined to one paragraph.
    assert "## TR-SEC-001 — No hardcoded secrets" in secrets
    assert (
        "All secrets must be stored in a vault. Never hardcoded in "
        "configuration files, source code, comments, or test fixtures." in secrets
    )
    # Generated-file provenance marker so hand-edits are discouraged.
    assert "cursor-rules-adapter.py" in secrets


def test_output_is_deterministic(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    out1 = generate(tmp_path / "a")
    out2 = generate(tmp_path / "b")
    files1 = {p.name: p.read_bytes() for p in out1.glob("*.mdc")}
    files2 = {p.name: p.read_bytes() for p in out2.glob("*.mdc")}
    assert files1 == files2


# --- --check mode -------------------------------------------------------


def test_check_passes_on_fresh_output(tmp_path: Path) -> None:
    registry = write_fixture(tmp_path)
    out = tmp_path / "rules"
    assert run("--registry", str(registry), "--out", str(out)).returncode == 0
    result = run("--registry", str(registry), "--out", str(out), "--check")
    assert result.returncode == 0, result.stderr


def test_check_fails_on_tampered_file(tmp_path: Path) -> None:
    registry = write_fixture(tmp_path)
    out = tmp_path / "rules"
    run("--registry", str(registry), "--out", str(out))
    target = out / "testing.mdc"
    target.write_text(target.read_text(encoding="utf-8") + "\nhand edit\n", encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(out), "--check")
    assert result.returncode == 1
    assert "testing.mdc" in result.stdout + result.stderr


def test_check_fails_on_missing_file(tmp_path: Path) -> None:
    registry = write_fixture(tmp_path)
    out = tmp_path / "rules"
    run("--registry", str(registry), "--out", str(out))
    (out / "secrets-management.mdc").unlink()
    result = run("--registry", str(registry), "--out", str(out), "--check")
    assert result.returncode == 1


def test_check_fails_on_stale_extra_file(tmp_path: Path) -> None:
    registry = write_fixture(tmp_path)
    out = tmp_path / "rules"
    run("--registry", str(registry), "--out", str(out))
    (out / "stale-section.mdc").write_text("---\n---\nleftover\n", encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(out), "--check")
    assert result.returncode == 1
    assert "stale-section.mdc" in result.stdout + result.stderr


# --- usage errors -------------------------------------------------------


def test_missing_registry_exits_2(tmp_path: Path) -> None:
    result = run("--registry", str(tmp_path / "nope.yaml"), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2


def test_unparseable_registry_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    registry.write_text(
        "requirements:\n  - id: TR-X-001\n    nested:\n      mapping: unsupported\n",
        encoding="utf-8",
    )
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2
    assert "line" in (result.stdout + result.stderr).lower()


def test_missing_required_field_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    registry.write_text(
        "requirements:\n  - id: TR-X-001\n    title: No status or section or text\n",
        encoding="utf-8",
    )
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2


def bad_registry_item(**overrides: str) -> str:
    """A single well-formed item with per-field overrides, for failure-mode tests."""
    fields = {
        "id": "TR-X-001",
        "title": "Some requirement",
        "status": "active",
        "section": '"Testing"',
        "text": ">\n      Some text.",
    }
    fields.update(overrides)
    lines = ["requirements:", ""]
    lines.append(f"  - id: {fields['id']}")
    for key in ("title", "status", "section", "text"):
        lines.append(f"    {key}: {fields[key]}")
    return "\n".join(lines) + "\n"


def test_inline_comment_in_value_exits_2(tmp_path: Path) -> None:
    # `status: active  # note` must not silently parse as status "active  # note"
    # (which would exclude the requirement from the export with exit 0).
    registry = tmp_path / "bad.yaml"
    registry.write_text(bad_registry_item(status="active  # temporarily"), encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2
    assert "comment" in (result.stdout + result.stderr).lower()


def test_unknown_status_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    registry.write_text(bad_registry_item(status="activeish"), encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2
    assert "status" in (result.stdout + result.stderr).lower()


def test_duplicate_field_key_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    registry.write_text(
        bad_registry_item() + "    title: Second title wins silently otherwise\n",
        encoding="utf-8",
    )
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2


def test_duplicate_requirement_id_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    item = bad_registry_item()
    second = bad_registry_item().replace("requirements:\n\n", "")
    registry.write_text(item + second, encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2
    assert "TR-X-001" in result.stdout + result.stderr


def test_empty_folded_text_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    registry.write_text(bad_registry_item(text=">"), encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2


def test_section_filename_collision_exits_2(tmp_path: Path) -> None:
    # "Testing One" and "Testing-One" both kebab to testing-one.mdc; the first
    # section's requirements must not silently vanish.
    registry = tmp_path / "bad.yaml"
    first = bad_registry_item(section='"Testing One"')
    second = bad_registry_item(section='"Testing-One"').replace(
        "requirements:\n\n", ""
    ).replace("TR-X-001", "TR-X-002")
    registry.write_text(first + second, encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2
    assert "testing-one" in (result.stdout + result.stderr).lower()


def test_registry_with_no_exportable_requirements_exits_2(tmp_path: Path) -> None:
    registry = tmp_path / "bad.yaml"
    registry.write_text(bad_registry_item(section='"Public Release"'), encoding="utf-8")
    result = run("--registry", str(registry), "--out", str(tmp_path / "rules"))
    assert result.returncode == 2


# --- repo integration ---------------------------------------------------


def test_committed_example_rules_match_real_registry() -> None:
    """The pregenerated examples/cursor-rules output must not drift from the registry."""
    result = run(
        "--registry", str(ROOT / "registry" / "tr-registry.yaml"),
        "--out", str(ROOT / "examples" / "cursor-rules" / ".cursor" / "rules"),
        "--check",
    )
    assert result.returncode == 0, result.stdout + result.stderr

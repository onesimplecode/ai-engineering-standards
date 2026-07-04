# Changelog

All notable changes to the public standards repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.3.0] - 2026-07-04

### Added

- `examples/engine-interface/` — reference implementation of the TR-AGT-003 loop-contract
  pattern (SearXNG-inspired multi-source polling engine interface), plus a Loop Contracts
  pointer in `AGENTS.md` and a `requirements-implementation-map.md` row update. This was
  published directly to the public repo (commit `c20c72d`) without a corresponding private-repo
  change; pulled back into the private source here so the next `publish-public-standards.yml`
  run (which mirrors private → public via `rsync --delete`) does not silently delete it.
- `AGENTS.md` — new "MCP Tool Annotations (TR-AGT-003, field 5)" section: the
  `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint` convention for MCP-exposed
  nodes, ported from the private operating conventions (v0.3 roadmap item 1).
  `registry/tr-registry.yaml`'s `TR-AGT-003` entry extended to reference field 5.
- `examples/worked-example/` — the TR-AGT-004 trace now runs to completion: step 5 shows real
  `check-config-consistency.py` output (previously only described hypothetically) and a new
  step 6, `.github/workflows/config-drift-demo.yml`, is a CI job whose success condition is
  that the example's planted `local-gemma-model` drift is still detected — the "TR-ID → ADR →
  maturity row → script output → CI gate" full path the v0.3 roadmap asked for. Corrected the
  maturity-checklist's Annex A mapping in the process: the CI-gate evidence now lives on a new
  A.10 row (third-party/supplier relationships, matching the template's own mapping for
  `check-config-consistency.py`) instead of conflated into A.9 (human oversight); the now-closed
  `LUMIA-DEBT` tag was removed from `sample-app/CLAUDE.md`.
- `scripts/check-config-consistency.py` — new `--root PATH` flag (default: the script's own
  repo root), so it can scan any app monorepo, not just the one it lives in (P2). `README.md`'s
  usage example updated to show `--root /path/to/your/repo --app YourApp`.
- `registry/tr-registry.yaml` — `TR-PUB-006`: agent persona drift check between the private
  operating-persona tree and its public-standards rewrite. Compares last-changed time for each
  pair and fails on drift, forcing a human reconciliation decision instead of silent staleness.
- `.gitignore` — `__pycache__/`, `*.pyc`, `.pytest_cache/` (P3); nothing previously kept these
  out of a future `git add -A` in the public repo. Added to `docs/public-export-manifest.yaml`'s
  `generated:` list.

### Fixed

- `scripts/check-config-consistency.py` — an unknown `--app` name or a nonexistent `--root`
  previously printed a false "OK" (or crashed) instead of failing; now exits 2 with an
  explicit "Unknown app(s): ... . Known: ..." message (P1, P2).
- `ATTRIBUTIONS.md` — added the `detect-secrets` (Yelp, Apache-2.0) entry that should have
  shipped alongside v0.2.0's secret-scanning CI step but was missed.
- `ATTRIBUTIONS.md` — added a SearXNG (AGPL-3.0) entry for `examples/engine-interface/`'s
  cited pattern source, found during v0.3 release-readiness review; verified no code was
  copied (SearXNG's actual `searx/engines/demo_online.py` uses an unrelated module-level
  plugin API) before writing the entry.

### Changed

- `templates/completion-checklist.md` strengthened to match the private template's rigor:
  file:line evidence citation per acceptance criterion, an explicit anti-mock-masking clause
  on test completeness, and a "Reviewer scope complete" item (docs/ADRs, not just code, must
  be in a reviewer's stated scope). The public copy's own "Post-write verification" item is
  kept (P4) — nothing here required staying private.
- `.github/workflows/release-check.yml` — `actions/checkout`/`actions/setup-python` bumped to
  Node.js 24-compatible versions, clearing the Node 20 deprecation warning.

## [0.2.0] - 2026-06-26

### Added

- Secret-scanning step (`detect-secrets>=1.4,<2`) in `release-check` CI workflow; `^templates/`
  and `^examples/` path patterns excluded to avoid false positives on placeholder content (TR-PUB-002)
- `docs/releasing.md` — maintainer release process: export from source, local CI checks,
  CHANGELOG/ROADMAP updates, tagging, and version numbering convention
- `examples/worked-example/docs/decisions/ADR-002-example.md` — synthetic ADR illustrating
  the adoption of EARS syntax for testable requirements
- `examples/worked-example/docs/decisions/ADR-003-example.md` — synthetic ADR illustrating
  the four-field loop contract decision (TR-AGT-003)

## [0.1.0] - 2026-06-19

### Added

- Initial public standards toolkit: README, MIT `LICENSE`, `ATTRIBUTIONS.md`
- Curated `registry/tr-registry.yaml` (governance, agents, security, public-release TR-PUB-*)
- Public `AGENTS.md` with tool-neutral AI agent conventions
- Public agent role specs under `agents/`
- `docs/ai-engineering-operating-model.md`
- `docs/requirements-implementation-map.md`
- Templates: ADR, AI impact assessment, maturity checklist, governance review, LLM regression benchmark, LLM eval, completion checklist
- Scripts: `check-config-consistency.py`, `debt-report.py`, `public-export-check.py`
- Synthetic worked example under `examples/worked-example/`
- `CONTRIBUTING.md`, `SECURITY.md`, issue/PR templates, `release-check` CI workflow
- Roadmap and changelog for intentional release cadence

[Unreleased]: https://github.com/onesimplecode/ai-engineering-standards/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/onesimplecode/ai-engineering-standards/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/onesimplecode/ai-engineering-standards/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/onesimplecode/ai-engineering-standards/releases/tag/v0.1.0

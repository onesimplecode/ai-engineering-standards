# Changelog

All notable changes to the public standards repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

No unreleased changes.

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

[Unreleased]: https://github.com/onesimplecode/ai-engineering-standards/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/onesimplecode/ai-engineering-standards/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/onesimplecode/ai-engineering-standards/releases/tag/v0.1.0

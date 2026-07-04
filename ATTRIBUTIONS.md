# Attributions and Third-Party Influences

LumiaForge AI Engineering Standards documents ideas and patterns learned from other
projects and standards. **No third-party code or substantial third-party prose is
included unless explicitly noted below.** Shipped templates, scripts, registry entries,
and examples are maintainer-authored unless a file header states otherwise.

## Open-source projects (ideas and selective adoption)

| Source | License | How used |
|--------|---------|----------|
| [Yelp/detect-secrets](https://github.com/Yelp/detect-secrets) | Apache-2.0 | Runtime CI dependency used in `release-check` workflow to scan the staging tree for accidental secrets before publish. Installed via pip; no code copied into this repository. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | Process baseline evaluation; ADR lifecycle, CI quality-gate concepts, reviewer procedure patterns. Not a code fork. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT | Debt-tag convention, config consistency checking concept; adapted as `LUMIA-DEBT:` / `POC-EXCEPTION:` and `check-config-consistency.py`. |
| [MODSetter/SurfSense](https://github.com/MODSetter/SurfSense) | Apache-2.0 | Comparative analysis only; selective pattern adoption (RRF, automations) documented in private app ADRs — not shipped as SurfSense code. |
| Karpathy LLM Wiki (public write-ups) | N/A (ideas) | Three-layer vault structure, file-based session state, ingest queue patterns — described and reimplemented independently. |
| [SearXNG](https://github.com/searxng/searxng) | AGPL-3.0 | Comparative pattern reference only for `examples/engine-interface/` (TR-AGT-003 loop contract demo). No code copied — verified directly against `searx/engines/demo_online.py`, which uses a module-level `setup()`/`init()`/`request()`/`response()` plugin API, structurally unrelated to this example's synthetic ABC-based `source_name`/`fetch()`/`default_timeout` pattern. The per-engine declared-timeout *idea* is the only thing carried over. |
| AGENTS.md ecosystem | Open standard | Complementary positioning; this repo focuses on governance/traceability, not replacing AGENTS.md. |
| [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) | (see upstream) | Comparative positioning only; this repo focuses on design-time and repo-time standards, not runtime agent governance. |
| Dify and similar RAG/agent platforms | (varies by project) | Comparative positioning only; no code, docs, or implementation copied. |

## Standards (document shapes, not certification)

| Source | How used |
|--------|----------|
| ISO/IEC 42001:2023 | Maturity checklist and impact assessment **templates** inspired by Annex A control objectives. No claim of ISO certification. |
| [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) | Changelog structure and headings only. |

## Maintainer-authored content

Templates, TR registry entries, scripts, worked examples, and ADRs in this repository are
authored by the LumiaForge maintainer unless a file header states otherwise. The MIT
license text in `LICENSE` is the standard MIT License text with project-specific
copyright attribution.

## Adding third-party content

Before merging third-party code or substantial prose:

1. Confirm license compatibility with MIT.
2. Add a row to this file: source URL, license, copied vs adapted, affected paths.
3. Complete the maintainer legal/open-source review before publishing.

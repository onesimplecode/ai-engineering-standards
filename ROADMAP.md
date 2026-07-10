# Roadmap

Releases are **curated and periodic**, not continuous dumps of unrelated work.
See `CHANGELOG.md` for shipped versions.

## v0.1 — Public standards baseline

- [x] Curated TR registry subset
- [x] Governance templates (ADR, impact assessment, maturity checklist, governance review)
- [x] Reference scripts: config consistency, debt report, public export check
- [x] Synthetic worked example
- [x] Contribution, security, and issue boundaries
- [x] Public `AGENTS.md`, role specs, operating model, and requirements map
- [x] Public LLM eval and completion/self-critique templates
- [x] Unit tests for `public-export-check.py` in CI

## v0.2 — Release hardening

- [x] Add a generic secret-scanning step to the `release-check` CI workflow
- [x] Document the maintainer release process
- [x] Public-safe process ADR examples explaining the governance decisions

## v0.3 — Enforced workflow example

- [x] Export MCP tool annotation conventions (TR-AGT-003 field 5) to public `AGENTS.md`
- [x] Worked example shows full path: TR-ID → ADR → maturity row → script output → CI gate
- [x] Sample GitHub Actions job that fails on config drift

## v0.4 — Cross-tool adapters (current)

- [x] Cursor rules adapter generated from TR registry subset
- [x] Document integration with `agent-skills` (complement, not compete)

## v0.5 — CI-enforced security guardrails

- [ ] "Make dangerous changes loud, not impossible" guard pattern: a script that
      hard-codes the reviewed baseline (permissions allowlist, required
      ignore-rules, forbidden lifecycle scripts) and fails CI on any drift,
      forcing the widening diff and the allowlist update into the same PR
      (worked example: `MadsLorentzen/ai-job-search`'s `tools/security_guards.py`
      + `.github/workflows/ci.yml`)
- [ ] Document as a public governance pattern: co-locate the guard with its own
      allowlist (not a separate config file), state the honest limit inline
      (a PR can edit the workflow itself — this catches accidents/casual
      attempts, not a determined author; branch protection + human review of
      workflow/settings diffs remain the real backstop)

## Non-goals

- Shipping application source code
- Runtime agent governance (see Microsoft Agent Governance Toolkit for that layer)
- Competing with full RAG/agent platforms (SurfSense, Dify, etc.)

## Cadence

- Target: **monthly** or **milestone** releases when standards change materially
- Minimum: **quarterly** sync if no changes (changelog notes "maintenance — no content delta")

## Seeded issues

On first GitHub publish, create issues from `.github/labels.md` with label `roadmap`.

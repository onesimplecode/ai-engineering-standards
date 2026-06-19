# LumiaForge AI Engineering Standards

An auditable **engineering operating model** for agent-assisted software work — not another
prompt library or RAG platform.

## Problem

AI coding agents default to the shortest path: skip tests, leak context across trust boundaries,
drift config and docs, and loop without budgets. Senior engineers prevent these failures with
standards, reviews, and deterministic checks. This repository packages that discipline for
public reuse.

## What this is

| Included | Not included |
|----------|----------------|
| Machine-readable requirement registry (`registry/tr-registry.yaml`) | Production runtime or hosted services |
| Portable agent conventions (`AGENTS.md`, `agents/`) | Tool-specific private agent sessions |
| Governance and eval templates (ADR, impact assessment, maturity checklist, LLM eval, completion checklist) | Full application frameworks |
| Reference scripts (config drift, debt tags, release validation) | Full `agent-skills` replacement |
| Synthetic worked example | Personal data |

## Quick start

```bash
# Validate a staging tree (or this repo root)
python3 scripts/public-export-check.py .

# Scan for config/model-string drift (point at your app monorepo)
python3 scripts/check-config-consistency.py --app YourApp

# Report deferred-work tags
python3 scripts/debt-report.py --path /path/to/your/repo
```

## Enforced workflow (v0.1)

See [`examples/worked-example/`](examples/worked-example/) for a synthetic trace:

**TR-AGT-004** → ADR → maturity checklist row → `LUMIA-DEBT:` tag → `check-config-consistency.py`

## Public Evidence Map

- [`AGENTS.md`](AGENTS.md) — tool-neutral agent rules for data routing, loop contracts,
  trigger classification, external-content trust boundaries, and deterministic checks.
- [`agents/`](agents/) — reusable role specs for developer, reviewer, private researcher,
  and public researcher agents.
- [`docs/ai-engineering-operating-model.md`](docs/ai-engineering-operating-model.md) —
  the overall model: requirements, roles, artifacts, checks.
- [`docs/requirements-implementation-map.md`](docs/requirements-implementation-map.md) —
  where each public requirement is implemented and how strongly it is enforced.
- [`templates/llm-eval.md`](templates/llm-eval.md) and
  [`templates/completion-checklist.md`](templates/completion-checklist.md) —
  eval and self-critique patterns that make agent output reviewable.

## Positioning

- **Complements** [AGENTS.md](https://agents.md), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), and runtime governance tools.
- **Differentiator:** design-time traceability — requirement IDs, PII routing rules, loop contracts,
  trigger classification, and scriptable drift detection.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Releases follow [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md).

## License

MIT — see [LICENSE](LICENSE). Third-party influences: [ATTRIBUTIONS.md](ATTRIBUTIONS.md).

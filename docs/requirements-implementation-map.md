# Requirements Implementation Map

This map shows how the public LumiaForge standards turn requirements into
concrete artifacts. It is intentionally limited to public, reusable evidence.

| Requirement area | Public implementation | Enforcement level | Evidence |
|---|---|---|---|
| Stable requirement IDs | Machine-readable registry | Documented + reusable | `registry/tr-registry.yaml` |
| Agent role boundaries | Tool-neutral role specs | Documented | `AGENTS.md`, `agents/*.md` |
| Private/public data routing | Role split and routing rule | Documented + reviewable | `AGENTS.md`, `agents/private-researcher.md`, `agents/public-researcher.md` |
| Loop contracts | Required four-field node contract + reference implementation | Documented + Example | `AGENTS.md`, `registry/tr-registry.yaml`, `examples/engine-interface/` |
| Trigger classification | ADR-triggered trigger type | Documented + example | `examples/worked-example/`, `templates/adr.md` |
| External content trust boundary | Retrieved content treated as data | Documented | `AGENTS.md`, `registry/tr-registry.yaml` |
| LLM eval convention | Co-located golden eval files guarded by `LLM_EVAL=true` | Template | `templates/llm-eval.md`, `AGENTS.md` |
| Post-write verification | Persistent side effects require observable verification | Template + documented | `templates/completion-checklist.md`, `AGENTS.md` |
| Provider prompt portability | Provider-specific system prompt variants isolated from business logic | Documented | `AGENTS.md` |
| Completion self-critique | Acceptance coverage, tests, symbol verification, data flow, and verification | Template | `templates/completion-checklist.md` |
| ADR discipline | Standard decision template | Template | `templates/adr.md` |
| AI impact assessment | Affected parties, data, harms, mitigations | Template | `templates/ai-impact-assessment.md` |
| Maturity tracking | Per-app checklist pattern | Template | `templates/maturity-checklist.md` |
| Governance review cadence | Review cycle template | Template | `templates/governance-review.md` |
| Model/config drift | Deterministic scanner | Script | `scripts/check-config-consistency.py` |
| Deferred work visibility | Structured debt tags | Script | `scripts/debt-report.py` |
| Public release hygiene | Required docs, secret-like strings, artifact paths | Script + CI | `scripts/public-export-check.py`, `.github/workflows/release-check.yml` |
| Public support boundary | Contribution and issue policy | Documented | `CONTRIBUTING.md`, `SECURITY.md`, `.github/` |
| License/attribution boundary | License and influence disclosure | Documented | `LICENSE`, `ATTRIBUTIONS.md` |

## Status Categories

- **Documented** — human/agent instructions exist.
- **Template** — reusable artifact shape exists.
- **Script** — deterministic check exists.
- **CI** — check runs automatically in the public repo.

## Gaps By Design

This public repo does not include application source code, live production
metrics, or full deployment evidence. It shows the engineering operating
model and the checks that make it reusable.

## Recommended Review Path

1. Read `AGENTS.md` to understand the agent rules.
2. Read `registry/tr-registry.yaml` to see the stable requirement IDs.
3. Open `examples/worked-example/` to see one requirement flow through an ADR,
   maturity checklist, and drift-check example.
4. Run `python3 scripts/public-export-check.py .`.

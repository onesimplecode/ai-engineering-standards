# Maturity Checklist: Sample App (Synthetic)

**Last updated:** 2026-07-04
**Current tier:** POC
**Operationalizes:** TR-GOV-004

| # | Objective | Mechanism | Applicable | Status | Evidence |
|---|-----------|-----------|------------|--------|----------|
| A.5 | AI impact assessment | templates/ai-impact-assessment.md | Yes | N/A | No user-facing AI output in this example |
| A.9 | Human oversight | Tiered Autonomy | Yes | Partial | ADR-001 documents user-initiated trigger classification (TR-AGT-004) |
| A.10 | Third-party / supplier relationships | `scripts/check-config-consistency.py` (TR-GOV-001) | Yes | Met | `.github/workflows/config-drift-demo.yml` runs the script against this example on every change and fails if the planted `local-gemma-model` drift is ever not detected |

## Open items

None currently open for this example.

# AI Impact Assessment: [Short Title]
Date: YYYY-MM-DD
Related ADR: ADR-NNNN

**Operationalizes:** TR-GOV-005 (ISO/IEC 42001 clause 6.1.4 / Annex A.5).

Attach this to any ADR that introduces or materially changes an AI system's
behavior toward people: new data collected, a new automated output or decision
surfaced to a user, or new externally-sourced content ingested. If none of those
apply, skip this assessment and say so in the ADR.

## Scope

What AI system, feature, or pipeline change is being assessed?

## Affected Parties

Who could be affected by this system or change? Consider:
- The Builder (operator)
- End users / customers of the app
- Third parties whose data appears in inputs (e.g. names in scraped job listings)
- Data subjects whose information is stored, retrieved, or transmitted

## Data Involved

- **What data does this touch?** (inputs, outputs, stored state)
- **PII classification:** [None | Possible | Confirmed]
- **Routing:** Local-only (TR-SEC-003) / Cloud-approved (cite ADR exception) — confirm this matches actual implementation, not just intent
- **Retention:** how long is this data kept, and where (TR retention defaults: logs 7 days, reports 1 year, backups 7 days unless overridden)

## Potential Harms

List plausible negative outcomes — even unlikely ones. Include both direct
(wrong output causes user harm) and indirect (data exposure, cost runaway,
availability).

| Harm | Affected party | Severity (Low/Med/High) | Likelihood (Low/Med/High) |
|---|---|---|---|
| | | | |

## Mitigations

For each harm above, what control reduces severity or likelihood — and which
TR-ID or design pattern implements it (e.g. TR-SEC-005 sanitization, output
validation/clamping, TR-AGT-003 resource budget, rate limiting)?

| Harm | Mitigation | TR-ID / pattern | Status |
|---|---|---|---|
| | | | |

## Human Oversight

- **Tiered Autonomy level** for this system's actions: [1 / 2 / 3]
- **Review gate before this output reaches a person or takes an external action:** [describe, or "none — justify why that's acceptable"]

## Residual Risk & Decision

- [ ] **Accept** — residual risk is acceptable at the current tier; no further action.
- [ ] **Mitigate further before merge** — list blocking items.
- [ ] **Escalate** — requires a decision beyond this ADR's scope.

## Review Trigger

When should this assessment be revisited? (e.g. before tier graduation, if the
data sources change, if the model is swapped per TR-TEST-004, or at the next
governance review per TR-GOV-006)

# LLM Regression Benchmark: [old-model] → [new-model]

Operationalizes **TR-TEST-004**. Run this before completing any switch or upgrade
of the LLM used for an application's runtime (classification, scoring, synthesis,
embeddings, etc.). Save the completed report to
`docs/experiments/YYYY-MM-DD-llm-switch-<old>-to-<new>.md` in the affected app.

This is deliberately lightweight — a fixed task set run against both models, not a
general-purpose benchmark harness. Scope it to the app's actual LLM call sites.

## Context

- **App / module:** [e.g. sample-app deep scorer]
- **Old model:** [provider/model-id]
- **New model:** [provider/model-id]
- **Reason for switch:** [cost, capability, deprecation, availability]
- **Config constant(s) affected:** [e.g. `DEFAULT_DEEP_MODEL` in `config.py`]

## Standard task set

List 5-10 representative inputs that exercise the call site's actual prompt and
output schema — drawn from real (or realistic synthetic) data, not toy examples.
Each task needs a way to judge correctness (exact match, schema validity, or a
human/LLM-judge rubric).

| # | Input summary | Expected output / rubric |
|---|---|---|
| 1 | | |
| 2 | | |
| ... | | |

## Results

| # | Old model output | New model output | Correct? (old / new) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

## Metrics

| Metric | Old model | New model | Delta |
|---|---|---|---|
| p50 latency | | | |
| p95 latency | | | |
| Cost per call (estimated, from provider pricing or local cost log) | | | |
| Cost for full task set | | | |
| Tasks correct / total | | | |
| Output schema validation failures | | | |

## Decision

- [ ] Proceed with switch — new model meets or exceeds old model on correctness, and cost/latency deltas are acceptable.
- [ ] Roll back — record why below.
- [ ] Investigate further — record open questions below.

**Notes:**

## Follow-up

- [ ] Update the config constant at its single source-of-truth location (no copy-paste — see AGENTS.md).
- [ ] Run `scripts/check-config-consistency.py` to confirm no stale references to the old model string remain.
- [ ] If this changes a documented default, file an ADR per TR-ADR-001.

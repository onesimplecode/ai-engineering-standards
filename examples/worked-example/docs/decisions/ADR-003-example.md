# ADR-003: Require Four-Field Loop Contract Before Agent Node Implementation (Synthetic Example)
Date: 2026-06-17
Status: Accepted

## Context

During early agent development, pipeline nodes were implemented without documenting their
expected inputs, outputs, exit conditions, or resource budgets. This led to three classes
of failure:

1. **Infinite loops** — the node's LLM output diverged from the expected format; with no
   declared exit condition, retry logic ran until hitting an external timeout.
2. **Runaway token spend** — retry-heavy nodes had no declared budget, so cost accumulated
   silently across long sessions.
3. **Silent integration breakage** — a node's output schema changed without a contract
   update; downstream nodes broke in ways that only surfaced at runtime.

TR-AGT-003 was created to prevent this class of failure at design time.

## Decision

Every agent pipeline node must declare four fields **before implementation begins**:

1. **Input schema** — the state or data the node expects to receive
2. **Output schema** — the state or data the node produces
3. **Exit condition** — the observable, deterministically verifiable result that signals
   the node is done (must be checkable without trusting the LLM's own return value)
4. **Resource budget** — maximum iteration count, token budget, or wall-clock timeout

A node missing any field is considered incomplete design and must not be merged.

Nodes exposed as MCP tools additionally declare the four MCP tool annotation hints
(`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`). These are advisory
hints to MCP clients — they do not enforce behavior at the protocol level.

## Consequences

**Positive:**
- Exit conditions are written before code, forcing authors to think about failure modes
  before optimistic-path implementation.
- Budget exhaustion tests can be derived directly from the declared resource budget field —
  no guesswork about what "too many retries" means.
- Contract diffs in PRs expose intent changes, not just implementation changes. A reviewer
  can spot "this node's output schema changed" without tracing through implementation.

**Negative:**
- Adds ~15 minutes of upfront design per node.
- Lightweight single-step nodes (no retry, no pipeline) still formally require all four
  fields — the overhead can feel disproportionate for trivial nodes.

## Alternatives Considered

- **Document contracts after implementation** — rejected; post-hoc documentation
  rationalizes existing behavior instead of designing it. The runaway-retry failure that
  prompted this ADR was caught after the fact.
- **Schema validation only (no budget/exit fields)** — rejected; schema contracts alone
  would not have caught the runaway-retry failure. Exit conditions and budgets are the
  fields that prevent unbounded execution.
- **Informal conventions only** — rejected; conventions without a required structure are
  inconsistently applied and cannot be checked by tooling or reviewers.

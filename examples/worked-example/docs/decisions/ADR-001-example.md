# ADR-001: Classify Sample Agent Trigger Type (Synthetic Example)
Date: 2026-06-17
Status: Accepted

## Context

The sample-app command handler invokes an LLM on each `!example` message.
TR-AGT-004 requires trigger classification before implementation.

## Decision

Classify the `!example` handler as **user-initiated**. It runs only when a user sends
an explicit command; it is not scheduled and not event-driven from file changes.

## Consequences

**Positive:** Trigger is documented; reviewers can verify no background side effects.

**Negative:** Future scheduled digest feature will need a separate ADR for scheduled trigger.

## Alternatives Considered

- **Event-driven** — rejected; no file or message bus trigger without user command.
- **Scheduled** — rejected; no cron/task loop in v0.1.

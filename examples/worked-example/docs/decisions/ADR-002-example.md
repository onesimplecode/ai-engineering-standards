# ADR-002: Use EARS Syntax for Active Requirements (Synthetic Example)
Date: 2026-06-17
Status: Accepted

## Context

The project needed a consistent format for writing requirements that can be:
- Verified against a falsifiable claim (not just intent)
- Understood by AI coding agents without interpretation
- Unambiguous about trigger, behavior, and observable outcome

Early drafts used plain imperative prose: "The system should validate URLs before fetching."
This created recurring ambiguity — "should" implies optional; the trigger condition was
implicit; there was no distinction between a testable system behavior and general guidance.

Reviewed alternatives included Gherkin (Given/When/Then) and plain prose requirements.

## Decision

Require EARS syntax (Easy Approach to Requirements Syntax) for all active requirements.
Standard form:

> When `<trigger>`, the system shall `<observable behavior>`.

New TR-IDs must use this format. Existing TR-IDs in `registry/tr-registry.yaml` use
plain imperative prose and are grandfathered; they will be updated opportunistically
as requirements are revised.

Restricted vocabulary:
- **shall** — required behavior (testable)
- **should** / **will** / **must** — banned in active requirements (ambiguous obligation)

Rationale and architectural intent belong in ADRs, not in requirements text.

## Consequences

**Positive:**
- Each requirement has an explicit trigger and a falsifiable claim — a test can be written
  from the requirement text alone.
- AI agents parse trigger→behavior pairs directly without interpreting prose intent.
- Reviewers can identify missing triggers ("when does this apply?") as a structural gap,
  not just a style issue.

**Negative:**
- Authors must think through the trigger condition before writing — slightly more upfront
  effort than prose.
- Rationale (the "why") still needs a separate narrative in an ADR or decision log;
  EARS text alone does not capture motivation.

## Alternatives Considered

- **Plain prose** — rejected; too ambiguous for automated tooling and AI agent consumption.
  "Should" and "will" do not have consistent obligation semantics across authors.
- **Gherkin / BDD** ("Given/When/Then") — rejected; adds feature-file scaffolding and
  product-owner framing that does not fit a standards toolkit aimed at engineering teams.
  EARS is lighter and language-agnostic.
- **Structured natural language (RFC 2119 keywords only)** — rejected; MUST/SHOULD/MAY
  keywords help but still leave trigger conditions implicit. EARS makes the trigger
  structure explicit.

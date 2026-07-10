# Integrating with agent-skills

This repository **complements** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
(and skill collections like it) — it does not compete with them. The two operate
at different layers, and they compose.

## The layer split

| | agent-skills | ai-engineering-standards (this repo) |
|---|---|---|
| Unit | A skill: a task-level playbook ("how to do X well") | A requirement: a stable, ID'd constraint ("what must always hold") |
| Scope | Per-task, invoked when the task matches | Cross-cutting, applies to every task |
| Enforcement | Instruction-following by the agent | Deterministic scripts and CI gates where possible (`scripts/`), documented conventions elsewhere |
| Evolution | New skills for new tasks | IDs are permanent; text evolves under changelog discipline |

A skill tells an agent how to do a code review or write a commit message.
A standard says no hardcoded secrets (TR-SEC-001), PII routes to local models
only (TR-SEC-003), every agent node declares a loop contract (TR-AGT-003) —
regardless of which skill is running.

## Integration patterns

**1. Cite TR IDs inside skills.** When a skill's instructions touch a governed
area, reference the requirement ID instead of restating (and eventually
forking) the rule. A testing skill that says "follow TR-TEST-001" inherits
registry updates for free, and reviewers can trace which constraint applied.

**2. Generate editor/agent context from the registry.** The registry is
machine-readable precisely so tool-specific context can be derived rather than
hand-maintained. `scripts/cursor-rules-adapter.py` is the working example: it
exports the coding-relevant registry subset as Cursor `.mdc` rules
(pregenerated copy in `examples/cursor-rules/`), with CI failing on drift.
The same pattern applies to any tool that consumes context files — skills
handle the task layer, generated rules pin the constraint layer underneath.

**3. Gate skill output with the governance artifacts.** Whatever skill
produced a change, the same checks apply: the completion self-critique
(`templates/completion-checklist.md`), the reviewer role spec
(`agents/reviewer.md`), and the deterministic scanners
(`check-config-consistency.py`, `debt-report.py`) in CI. Skills raise the
ceiling of what an agent does well; the gates hold the floor.

## Boundary (by design)

Per `CONTRIBUTING.md`, this repo does not accept task playbooks or skill
collections — contribute those to a skills repository. What belongs here is
the constraint layer: registry entries, templates, deterministic checks, and
adapters that export them into other tools' formats.

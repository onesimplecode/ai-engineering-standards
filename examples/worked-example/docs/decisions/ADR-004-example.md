# ADR-004: Adopt an ATT&CK-Informed Security Baseline for the Toolchain (Synthetic Example)
Date: 2026-07-12
Status: Accepted

## Context

A routine security review of this sample app's development toolchain — not its
production code — checked local credential files, CI workflow permissions, and
the coding agent's tool allowlist against the MITRE ATT&CK technique catalog
(https://attack.mitre.org/). Application-level controls were already solid (no
hardcoded secrets, PII routed to a local LLM), but three toolchain gaps had no
tracked requirement:

1. The local `.env` file was mode 664 (group/world-readable) — ATT&CK
   T1552.001 — and no secret scan ran before commit.
2. The CI workflow declared no `permissions:` block (default token scope) and
   pinned third-party actions to a mutable version tag rather than a commit
   SHA — ATT&CK T1195.
3. The coding agent's tool-permission allowlist contained a wildcard grant
   (`bash -c *`) left over from early prototyping. A prompt-injected agent
   session could run arbitrary shell commands with no confirmation prompt —
   ATT&CK T1059 — bypassing the project's own tiered-autonomy confirmation
   rule for anything destructive.

The common thread: security requirements covered the application but not the
pipeline and agent tooling that build it.

## Decision

Add three requirements, extending the security registry:

- **Local credential files are permission-restricted and secret-scanned** —
  mode 600 for secret-bearing files; a secret-scan gate before commit while
  secrets live in files rather than a vault.
- **CI pipelines run least-privilege and fully pinned** — explicit
  least-privilege `permissions:` block per workflow; actions pinned to full
  commit SHAs with the human-readable version in a trailing comment.
- **Agent tool permission grants are a security boundary** — no wildcard
  write/install/exec/network grants in agent allowlists; grant the specific
  command instead. This is the *least-agency* principle (OWASP's extension of
  least privilege to agentic tools): restrict not just what an identity can
  access, but what each tool can do, how often, and where.

Adopt a lightweight threat-model step at design time (`templates/threat-model.md`):
required for any change introducing a new listener, credential, agent tool
grant, or external content source; optional otherwise. Every listed mitigation
is classified as a **barrier** (removes the capability) or **friction**
(raises cost only), with the real backstop named for friction-class controls —
the "impossible vs. tedious" test. Agentic attackers have unlimited patience
and near-zero per-attempt cost, so a friction-only control should never be
presented as though it stops them.

## Consequences

**Positive:**
- The three gaps become tracked, testable requirements with attack-technique
  citations instead of one-off fixes that can silently regress.
- Threat modeling happens at the cheapest point (design), in the vocabulary
  (ADRs, requirement IDs) already in use — no new process layer.

**Negative:**
- SHA-pinned actions no longer auto-update within a major version; bumping a
  dependency becomes a deliberate, reviewed act.
- Tighter agent allowlists mean more confirmation prompts during development;
  accepted for install/write/network operations, since that friction is the
  point — narrow, specific read-only commands can still be pre-approved.

## Alternatives Considered

- **Fix the three findings without adding requirements.** Rejected: the same
  drift (a new workflow missing a permissions block, a new wildcard grant)
  would silently recur with nothing to catch it at the next review.
- **A single omnibus "security hardening" requirement.** Rejected: the three
  concerns are audited by different mechanisms (file mode, workflow lint,
  allowlist review) and fail independently; one ID would make exceptions and
  waivers imprecise.
- **Adopt a full external framework (e.g. NIST SSDF) instead of targeted
  requirements.** Rejected as heavyweight for this project's size; most of
  its controls would duplicate what the existing registry already encodes.
  Reconsider if the project takes on external contributors, where
  framework-attestation has signaling value.

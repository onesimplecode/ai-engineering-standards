# Completion Checklist

Complete this before marking any non-trivial implementation done. Attach the
filled checklist to the change summary or pull request description.

## Checklist

- [ ] **Acceptance criteria coverage** — every acceptance criterion has a
  specific implementation or documentation artifact.

- [ ] **Test completeness** — acceptance criteria, edge cases, and error paths
  have tests or a documented reason why testing is deferred.

- [ ] **Pattern adherence** — new code or process follows an existing local
  pattern, or an ADR explains why a new pattern is needed.

- [ ] **First-party symbol verification** — internal functions, classes, config
  keys, paths, and commands were verified before use.

- [ ] **Data flow trace** — input schema, transformation, output schema, and
  trust boundary are understood at each hand-off.

- [ ] **Post-write verification** — persistent writes or external side effects
  have an observable verification step, not only a successful return value.

## Evidence

| Item | Evidence |
|---|---|
| Acceptance criteria coverage | |
| Test completeness | |
| Pattern adherence | |
| First-party symbols | |
| Data flow trace | |
| Post-write verification | |

## Gap Log

If any item has a gap, describe it, the fix applied, and how it was re-verified.

| Gap found | Fix applied | Re-verified |
|---|---|---|
| | | |

## Summary

<!-- What changed and why? Link related issue if any. -->

## Change type

- [ ] Documentation only
- [ ] Template / registry update
- [ ] Script / enforcement
- [ ] Worked example
- [ ] Other (describe)

## Checks run

- [ ] `python3 scripts/public-export-check.py .` (or staging path)
- [ ] `python3 -m py_compile scripts/*.py`
- [ ] `python3 scripts/check-config-consistency.py --root examples/worked-example --app sample-app`
      (if `examples/worked-example` touched — the bare no-args form always exits 2 in this
      repo, since it has no top-level app directories to discover; see
      `.github/workflows/config-drift-demo.yml`)

## Attribution

- [ ] No third-party code or substantial prose copied
- [ ] Third-party content included — `ATTRIBUTIONS.md` updated (source URL + license)

## Scope confirmation

- [ ] This PR stays within standards-toolkit scope (no private app code, secrets, or PII)

## THINGS I DIDN'T TOUCH (intentionally)

<!-- List areas deliberately left unchanged -->

## POTENTIAL CONCERNS

<!-- Anything reviewers should scrutinize -->

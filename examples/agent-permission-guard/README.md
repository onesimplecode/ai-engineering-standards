# Worked Example: Agent Permission Guard (TR-SEC-010)

`settings.example.json` is a synthetic agent tool-permission file with two
planted problems for `scripts/agent-permission-guard.py` to catch:

| Grant | Why it's flagged |
|---|---|
| `Bash(git status:*)` | Clean — matches `REVIEWED_BASELINE` for this fixture |
| `Bash(pytest:*)` | Clean — matches `REVIEWED_BASELINE` for this fixture |
| `Bash(pip install:*)` | **FORBIDDEN** — wildcard package install; never accepted regardless of baseline (a barrier, not friction) |
| `Bash(ruff check:*)` | **UNREVIEWED** — not dangerous, but absent from the reviewed baseline; a human must add it to the script in the same PR if intentional |

Run from the public repo root:

```bash
python3 scripts/agent-permission-guard.py --settings examples/agent-permission-guard/settings.example.json
```

Expected output (exit code 1 — this fixture is *supposed* to fail):

```
FORBIDDEN [wildcard_dangerous_verb] examples/agent-permission-guard/settings.example.json: 'Bash(pip install:*)' -- wildcard write/install/exec/network grants are never allowed
UNREVIEWED examples/agent-permission-guard/settings.example.json: 'Bash(ruff check:*)' -- not in REVIEWED_BASELINE; add it to scripts/agent-permission-guard.py in this PR if intentional
```

`.github/workflows/agent-permission-guard-demo.yml` runs this exact command in
CI on every change to this fixture or the script — the job's *success*
condition is that the drift is still caught, the same pattern as
`config-drift-demo.yml`.

**Honest limit** (see `templates/threat-model.md`'s Impossible vs. Tedious
section): this is a friction control against casual, undiscussed allowlist
widening — it forces the diff into a reviewed PR. It is not a barrier against
a determined author who edits the settings file *and* `REVIEWED_BASELINE` in
the same commit; branch protection and human review of that diff are the real
backstop.

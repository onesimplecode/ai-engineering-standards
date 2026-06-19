# Worked Example: TR-AGT-004 End-to-End (Synthetic)

This directory shows how one requirement flows through LumiaForge governance
artifacts. **All content is fictional** — no private data or real application code.

## Trace

| Step | Artifact | Evidence |
|------|----------|----------|
| 1 | `registry-snippet.yaml` | TR-AGT-004 defined as active |
| 2 | `docs/decisions/ADR-001-example.md` | Trigger type classified: user-initiated |
| 3 | `docs/maturity-checklist.md` | A.9 human oversight row = Partial |
| 4 | `sample-app/CLAUDE.md` | Documents trigger + debt tag |
| 5 | `check-config-consistency.py` | Would catch model-string drift in real app |

## Run (from public repo root)

```bash
python3 scripts/public-export-check.py .
python3 scripts/debt-report.py --path examples/worked-example
```

## Deliberate drift example

`sample-app/CLAUDE.md` references `gemma4:31b` while `config/search_config.yaml.example`
uses `gemma4:26b`. In a real app at repo root, `check-config-consistency.py` would
report **DRIFT** for the `local-gemma-model` family.

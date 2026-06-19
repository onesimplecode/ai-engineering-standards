# Sample App — CLAUDE.md (Synthetic)

**Tier:** POC  
**Trigger classification (TR-AGT-004):** user-initiated — `!example` command only.

## Runtime

- Default local model: `gemma4:31b` via Ollama
- Config template: `config/search_config.yaml.example`

## Known debt

LUMIA-DEBT: wire check-config-consistency.py into CI (TR-GOV-001)

## Privacy (TR-SEC-003)

This sample app processes no PII. Production apps must route PII through local inference only.

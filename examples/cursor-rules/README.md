# Cursor Rules Export (generated)

Pregenerated [Cursor project rules](https://cursor.com/docs/context/rules) derived
from [`registry/tr-registry.yaml`](../../registry/tr-registry.yaml) by
[`scripts/cursor-rules-adapter.py`](../../scripts/cursor-rules-adapter.py) —
one `.mdc` file per exported registry section.

**Do not edit these files by hand.** The registry is the single source of truth;
CI runs the adapter in `--check` mode and fails on any drift between this
directory and the registry (same discipline as `check-config-consistency.py`).

## Use in your own repo

```bash
# Write rules into your project's .cursor/rules/
python3 scripts/cursor-rules-adapter.py --out /path/to/your/repo/.cursor/rules

# Later, verify they haven't drifted from the registry
python3 scripts/cursor-rules-adapter.py --out /path/to/your/repo/.cursor/rules --check
```

## Export rules

- Only `status: active` requirements are exported.
- "Public Release" requirements (`TR-PUB-*`) govern this repository's release
  process, not coding, and are excluded.
- Safety-critical sections (Secrets Management, Data Privacy, Prompt Injection,
  and Agents — which carries the PII-to-local-LLM routing rule) are emitted with
  `alwaysApply: true`; all other sections attach via their `description` so they
  only load when relevant.

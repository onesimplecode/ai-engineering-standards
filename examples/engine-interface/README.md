# Loop Contract Reference: Engine Interface Pattern

**Requirement:** TR-AGT-003 (Agentic node loop contracts)  
**Pattern source:** [SearXNG](https://github.com/searxng/searxng) — `searx/engines/demo_online.py`

---

## What this shows

TR-AGT-003 requires every multi-step agent pipeline node to declare four fields before implementation:

1. **Input schema** — what data the node receives
2. **Output schema** — what data the node produces
3. **Exit condition** — observable evidence that the node is done
4. **Resource budget** — max timeout, iteration count, or token budget

The **SearXNG engine interface** is a concrete, public implementation of this pattern applied to a multi-source polling pipeline. Each engine (search source) declares all four fields as part of its module-level contract rather than burying them in implementation detail.

---

## The pattern

```python
from abc import ABC, abstractmethod


class SourceEngine(ABC):
    """Loop contract for a single polling pipeline node.

    TR-AGT-003 fields:
      INPUT  : fetch(roles, days_back) — caller provides search parameters
      OUTPUT : list[Result] — normalized result objects (same shape from every engine)
      EXIT   : fetch() always returns ([] on failure — NEVER raises)
      BUDGET : default_timeout (int, seconds) — per-engine HTTP resource ceiling
    """
    default_timeout: int = 15     # BUDGET — override at class level for slow sources
    categories: list[str] = []    # Engine metadata — for routing and observability

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Stable identifier for this source. Stored in Result.source."""

    @abstractmethod
    def fetch(self, roles: list[str], days_back: int) -> list:
        """Fetch and return normalized results. NEVER raises — return [] on any error."""
        ...
```

The runner reads `default_timeout` from each engine to apply a per-engine deadline — not a global constant. This makes the resource budget **declared at the source**, not scattered through the orchestrator.

---

## Why this is TR-AGT-003 in practice

| TR-AGT-003 field | Engine interface expression |
|---|---|
| Input schema | `fetch(roles, days_back)` signature — runner passes search parameters |
| Output schema | `list[Result]` — same normalized shape from every engine |
| Exit condition | `fetch()` always returns (`[]` = source miss or failure, non-empty = results found) |
| Resource budget | `default_timeout: int` class attribute — per-engine HTTP ceiling |

The critical insight: when the resource budget is a **declared attribute on the node** rather than a hardcoded constant in the orchestrator, it becomes part of the node's contract. A new source with different latency characteristics (e.g., a Playwright scraper vs. a fast REST API) overrides one attribute rather than patching the orchestrator.

---

## Contrast: node without a loop contract

```python
# Anti-pattern: loop contract is implicit

def fetch_from_source(query: str) -> list:
    # timeout? hardcoded in here somewhere
    # result shape? varies per source
    # exit condition? unclear — might raise, might return None
    resp = requests.get(f"https://source.example.com/search?q={query}", timeout=15)
    return resp.json()["results"]  # KeyError on failure, not []
```

Problems:
- Resource budget (timeout) is invisible to the orchestrator
- Output schema is "whatever the source returns" — no normalization contract
- Exit condition is undefined — raises on failure instead of returning `[]`

---

## Applying this in a new project

When designing a multi-source polling pipeline (job boards, news feeds, search APIs, data sources):

1. Define a base class / protocol with `default_timeout`, `source_name`, and a `fetch()` method
2. `fetch()` must NEVER raise — catch all exceptions, log, return `[]`
3. Make `default_timeout` a **class attribute** (per-source) not a constructor param (per-instance) — timeout is a property of the source type, not a specific instantiation
4. Normalize output to a shared dataclass before returning — the orchestrator should never need to branch on which source returned the result

See `job_source_engine.py` in this directory for a minimal Python implementation.

---

## Trace to standards artifacts

| Artifact | Location |
|---|---|
| TR-AGT-003 definition | `registry/tr-registry.yaml` |
| Loop contract rule | `AGENTS.md` — "Loop Contracts (TR-AGT-003)" |
| ADR template | `templates/adr.md` |
| Completion checklist | `templates/completion-checklist.md` — row 4: resource budget declared |

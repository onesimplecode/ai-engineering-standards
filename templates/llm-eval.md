# LLM Eval Template

**Operationalizes:** TR-TEST-005 (LLM eval files co-located with agent modules).

Place completed eval files in `<app>/tests/evals/test_<agent>_eval.py`.
Run via:

```bash
LLM_EVAL=true LLM_EVAL_TRIALS=3 pytest tests/evals/ -v
```

Evals are intentionally separate from the default unit test suite. They are
slower, may cost money, and often require provider credentials.

---

## File Structure

```python
"""LLM eval: [Agent Name] - [what this eval measures].

Operationalizes TR-TEST-005.
Run with:
    LLM_EVAL=true LLM_EVAL_TRIALS=3 pytest tests/evals/test_<agent>_eval.py -v
"""

from __future__ import annotations

import os

import pytest


pytestmark = pytest.mark.skipif(
    os.environ.get("LLM_EVAL", "").lower() != "true",
    reason="LLM evals require LLM_EVAL=true and the relevant provider credentials",
)


GOLDEN: list[dict] = [
    {
        "input": {
            # Fill in the agent's input fields.
            # Retrieval example: {"query": "...", "top_k": 5}
            # Synthesis example: {"query": "...", "chunks": [...], "intent": "ask"}
            # Classification example: {"text": "..."}
        },
        "expected": "...",
        "description": "one-sentence description of what this case tests",
    },
]


def score(output: str, expected: str) -> float:
    """Return a score in [0, 1]. Replace with task-appropriate scoring."""
    return 1.0 if expected in output else 0.0


def run_task(case_input: dict) -> str:
    """Call the agent under test and return a string representation of output."""
    # Import here to defer startup side effects until the eval actually runs.
    # from src.<module> import <agent_function>
    # result = <agent_function>(**case_input)
    # return str(result)
    raise NotImplementedError("Replace with actual agent call")


@pytest.mark.parametrize("case", GOLDEN, ids=[c["description"] for c in GOLDEN])
def test_eval(case: dict) -> None:
    trials = int(os.environ.get("LLM_EVAL_TRIALS", "1"))
    scores = []
    last_output = ""
    for _ in range(trials):
        last_output = run_task(case["input"])
        scores.append(score(last_output, case["expected"]))

    avg = sum(scores) / len(scores)
    print(f"\n  expected : {case['expected']!r}")
    print(f"  actual   : {last_output!r}")
    print(f"  score    : {avg:.2f} over {trials} trial(s)")
    assert avg >= 0.8, f"Eval failed: avg score {avg:.2f} < 0.8"
```

---

## Scoring Patterns

| Task type | Scoring approach | Example |
|---|---|---|
| Structured extraction | Exact match | Classification returns `"management"` and expected is `"management"` |
| Citation presence | Substring or regex | Expected source title appears in the answer |
| Retrieval recall | Set membership | Correct document title appears in top-k results |
| Format correctness | Parser or schema validation | YAML frontmatter parses successfully |
| Generation quality | Rubric or judge | Separate judge model scores faithfulness against evidence |

## Conventions

- Prefer structural scoring whenever possible.
- Use LLM-as-Judge only when structural scoring cannot measure the behavior.
- Mock external dependencies except the LLM behavior being evaluated.
- Record meaningful eval results in `docs/experiments/`.
- Re-run evals when switching runtime models or prompt variants.

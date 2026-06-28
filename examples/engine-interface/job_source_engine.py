"""Minimal reference implementation of the engine-interface loop contract pattern.

Demonstrates TR-AGT-003 (loop contracts) applied to a multi-source polling
pipeline, inspired by the SearXNG engine interface (searx/engines/demo_online.py).

All content is synthetic — no real job boards are queried.
"""
from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Output schema (shared across all engines)
# ---------------------------------------------------------------------------

@dataclass
class JobResult:
    """Normalized job result — same shape regardless of which engine produced it.

    TR-AGT-003 OUTPUT: every engine must return list[JobResult], never a
    source-specific dict. Normalization happens inside the engine, not in the
    orchestrator.
    """
    id: str
    title: str
    company: str
    url: str
    description: str
    source: str
    fetched_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    @classmethod
    def make_id(cls, title: str, company: str) -> str:
        norm = (title + company).lower().replace(" ", "")
        return hashlib.sha256(norm.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Base engine (loop contract declaration)
# ---------------------------------------------------------------------------

class JobSourceEngine(ABC):
    """Base class for a single-source polling pipeline node.

    TR-AGT-003 loop contract fields:

    INPUT  : fetch(roles, days_back) — caller provides search parameters
    OUTPUT : list[JobResult]  — normalized, never raises
    EXIT   : fetch() returns (empty list = no results or failure)
    BUDGET : default_timeout (int, seconds) — per-engine HTTP ceiling;
             override at the class level for slow or fast sources
    """

    default_timeout: int = 15
    """Per-engine HTTP timeout in seconds (TR-AGT-003 BUDGET).

    Override at class level — this is a property of the source type, not
    of a specific instance. A Playwright-based scraper might use 30 s;
    a cached local API might use 5 s.
    """

    categories: list[str] = []
    """Engine metadata — used by the orchestrator for routing and logging."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Stable identifier for this source. Stored in JobResult.source."""

    @abstractmethod
    def fetch(self, roles: list[str], days_back: int) -> list[JobResult]:
        """Fetch job listings and return normalized results.

        TR-AGT-003 EXIT CONDITION: this method must always return — it must
        NEVER raise. On any failure (network error, parse error, rate limit),
        log a warning to stderr and return [].
        """


# ---------------------------------------------------------------------------
# Example engines (synthetic implementations)
# ---------------------------------------------------------------------------

class SyntheticAtsEngine(JobSourceEngine):
    """Example: fast REST API engine (default timeout is fine)."""

    categories = ["ats", "company_direct"]

    def __init__(self, company_name: str, slug: str) -> None:
        self._company = company_name
        self._slug = slug

    @property
    def source_name(self) -> str:
        return f"ats:{self._slug}"

    def fetch(self, roles: list[str], days_back: int) -> list[JobResult]:
        import sys
        try:
            # Synthetic: in a real engine, call the ATS API here
            # resp = requests.get(f"https://api.example.com/{self._slug}/jobs",
            #                     timeout=self.default_timeout)
            synthetic_jobs = [
                {"title": f"Engineering Manager", "url": f"https://{self._slug}.example.com/em"},
            ]
            return [
                JobResult(
                    id=JobResult.make_id(j["title"], self._company),
                    title=j["title"],
                    company=self._company,
                    url=j["url"],
                    description="",
                    source=self.source_name,
                )
                for j in synthetic_jobs
            ]
        except Exception as exc:
            print(f"WARNING: {self.source_name} fetch failed: {exc}", file=sys.stderr)
            return []


class SyntheticSlowScraperEngine(JobSourceEngine):
    """Example: slow scraper engine — overrides timeout at the class level."""

    default_timeout: int = 45  # Playwright rendering takes longer than REST calls
    categories = ["scraper"]

    def __init__(self, url: str) -> None:
        self._url = url

    @property
    def source_name(self) -> str:
        return "slow_scraper"

    def fetch(self, roles: list[str], days_back: int) -> list[JobResult]:
        import sys
        try:
            # Synthetic: in a real engine, call crawl4ai or Playwright here
            return []
        except Exception as exc:
            print(f"WARNING: {self.source_name} fetch failed: {exc}", file=sys.stderr)
            return []


# ---------------------------------------------------------------------------
# Minimal orchestrator (reads default_timeout from each engine)
# ---------------------------------------------------------------------------

class EngineRegistry:
    """Minimal multi-source orchestrator.

    Calls each engine's fetch(), catches any exceptions (defense-in-depth on
    top of the never-raises contract), and deduplicates by result.id.
    """

    def __init__(self, engines: list[JobSourceEngine]) -> None:
        self._engines = engines

    def fetch_all(self, roles: list[str], days_back: int) -> list[JobResult]:
        import sys
        seen: dict[str, JobResult] = {}
        for engine in self._engines:
            # The orchestrator CAN read engine.default_timeout for logging/enforcement
            # without needing to know anything about the engine's internals.
            try:
                results = engine.fetch(roles, days_back)
            except Exception as exc:
                print(
                    f"WARNING: {engine.source_name!r} raised despite never-raises "
                    f"contract: {exc}",
                    file=sys.stderr,
                )
                results = []
            for result in results:
                if result.id not in seen:
                    seen[result.id] = result
        return list(seen.values())


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    registry = EngineRegistry([
        SyntheticAtsEngine("Acme Corp", "acme"),
        SyntheticAtsEngine("Globex Corp", "globex"),
        SyntheticSlowScraperEngine("https://careers.example.com"),
    ])
    jobs = registry.fetch_all(roles=["Engineering Manager"], days_back=7)
    for job in jobs:
        print(f"[{job.source}] {job.company}: {job.title}")
    print(f"\n{len(jobs)} unique listings from {len(registry._engines)} engines")
    print(f"Timeouts: {[e.default_timeout for e in registry._engines]} s per engine")

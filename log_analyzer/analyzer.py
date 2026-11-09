"""Core log parsing and summary operations."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Iterable

SEVERITIES = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
_LEVEL_PATTERN = re.compile(
    r"\b(DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL)\b",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class LogSummary:
    """Immutable counts collected while processing a log source."""

    total_lines: int
    severity_counts: dict[str, int]
    unclassified: int

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable representation of this summary."""
        return asdict(self)


def _severity_for(line: str) -> str | None:
    """Return the first recognised severity token in a line."""
    match = _LEVEL_PATTERN.search(line)
    if match is None:
        return None
    level = match.group(1).upper()
    return "WARNING" if level == "WARN" else level


def analyze_lines(lines: Iterable[str]) -> LogSummary:
    """Count severity levels in an iterable of log lines."""
    counts = Counter({level: 0 for level in SEVERITIES})
    total = 0
    unclassified = 0

    for line in lines:
        total += 1
        severity = _severity_for(line)
        if severity is None:
            unclassified += 1
        else:
            counts[severity] += 1

    return LogSummary(
        total_lines=total,
        severity_counts=dict(counts),
        unclassified=unclassified,
    )


def analyze_file(path: str | Path) -> LogSummary:
    """Analyse a UTF-8 text log file.

    File and decoding errors propagate so callers can choose their own
    recovery and reporting policy.
    """
    with Path(path).open("r", encoding="utf-8") as log_file:
        return analyze_lines(log_file)

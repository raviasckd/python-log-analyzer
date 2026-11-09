"""Command-line interface for the log analyzer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from log_analyzer.analyzer import SEVERITIES, analyze_file


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log-analyzer",
        description="Summarise severity levels in a text log file.",
    )
    parser.add_argument("log_file", type=Path, help="Path to a UTF-8 log file")
    parser.add_argument("--json", dest="json_path", type=Path,
                        help="Write the summary as JSON to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit status."""
    args = _build_parser().parse_args(argv)

    try:
        summary = analyze_file(args.log_file)
    except (OSError, UnicodeError) as exc:
        print(f"log-analyzer: {exc}", file=sys.stderr)
        return 2

    if args.json_path is not None:
        try:
            args.json_path.write_text(
                json.dumps(summary.to_dict(), indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"log-analyzer: cannot write report: {exc}", file=sys.stderr)
            return 2

    print(f"File: {args.log_file}")
    print(f"Total lines: {summary.total_lines}")
    for level in SEVERITIES:
        print(f"{level:8} {summary.severity_counts[level]}")
    print(f"Unclassified: {summary.unclassified}")
    if args.json_path is not None:
        print(f"JSON report: {args.json_path}")
    return 0

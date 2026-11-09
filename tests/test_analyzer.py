"""Tests for the log analysis functions."""

from pathlib import Path
import tempfile
import unittest

from log_analyzer.analyzer import analyze_file, analyze_lines


class AnalyzeLinesTests(unittest.TestCase):
    def test_counts_supported_levels(self) -> None:
        result = analyze_lines([
            "DEBUG cache miss", "INFO started", "WARN retrying",
            "WARNING queue filling", "ERROR failed", "CRITICAL stopped",
        ])
        self.assertEqual(result.total_lines, 6)
        self.assertEqual(result.severity_counts, {
            "DEBUG": 1, "INFO": 1, "WARNING": 2, "ERROR": 1, "CRITICAL": 1,
        })
        self.assertEqual(result.unclassified, 0)

    def test_unclassified_lines_are_counted(self) -> None:
        result = analyze_lines(["startup complete", "INFO ready", ""])
        self.assertEqual(result.total_lines, 3)
        self.assertEqual(result.unclassified, 2)

    def test_matching_is_case_insensitive(self) -> None:
        result = analyze_lines(["error: connection refused"])
        self.assertEqual(result.severity_counts["ERROR"], 1)

    def test_empty_input_returns_zero_counts(self) -> None:
        result = analyze_lines([])
        self.assertEqual(result.total_lines, 0)
        self.assertEqual(result.unclassified, 0)
        self.assertTrue(all(count == 0 for count in result.severity_counts.values()))

    def test_severity_must_be_a_complete_token(self) -> None:
        result = analyze_lines(["INFORMATION message", "ERROR_CODE value"])
        self.assertEqual(result.unclassified, 2)


class AnalyzeFileTests(unittest.TestCase):
    def test_reads_utf8_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "app.log"
            path.write_text("INFO café\nERROR failed\n", encoding="utf-8")
            result = analyze_file(path)
        self.assertEqual(result.total_lines, 2)
        self.assertEqual(result.severity_counts["INFO"], 1)
        self.assertEqual(result.severity_counts["ERROR"], 1)


if __name__ == "__main__":
    unittest.main()

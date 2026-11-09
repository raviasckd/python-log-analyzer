# Python Log Analyzer

A dependency-free Python CLI for summarising application log files. It recognises common severity levels, reports unclassified lines, and can write a JSON summary.

## Requirements
- Python 3.10+
- No runtime dependencies

## Quick start
```bash
git clone https://github.com/raviasckd/python-log-analyzer.git
cd python-log-analyzer
python -m log_analyzer examples/sample.log
python -m log_analyzer examples/sample.log --json report.json
```

Run tests:
```bash
python -m unittest discover -s tests -v
```

## Supported levels
DEBUG, INFO, WARN/WARNING, ERROR and CRITICAL. Matching is case-insensitive and uses complete tokens. Lines without a recognised level are counted as unclassified.

## JSON report
The report includes the input path, total line count, severity counts and unclassified line count.

## Layout
```text
log_analyzer/
  __init__.py
  __main__.py
  analyzer.py
  cli.py
tests/
.github/workflows/tests.yml
```

## Scope
This is a local, line-oriented text log summariser, not a centralised logging platform. It currently reads UTF-8 files into the analysis flow and does not infer application-specific meanings or parse structured JSON log schemas.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports should include a small reproducible input.

## License
MIT. See [LICENSE](LICENSE).

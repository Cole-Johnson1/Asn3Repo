# Course Schedule Checker

This small command-line project checks a student's course schedule for overlapping class times.  It reads a JSON file, reports any conflicts, and returns a non-zero exit code when the schedule is invalid or has conflicts.

## Requirements

- Python 3.10 or newer
- Install development tools with `python -m pip install -e ".[test]"`

## Run

```powershell
python -m course_schedule_checker data/sample_schedule.json
```

## Test and coverage

```powershell
python -m pytest --cov=course_schedule_checker --cov-report=xml:coverage.xml
```

The initial baseline deliberately has areas to investigate during the static-analysis exercise.  The first report should be based on the actual baseline scan and test results, then improvements should be made in later commits.

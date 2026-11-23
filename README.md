# Course Schedule Checker

This small command-line project checks a student's course schedule for overlapping class times.  It reads a JSON file, reports any conflicts, and returns a non-zero exit code when the schedule is invalid or has conflicts.

## Requirements

- Python 3.10 or newer
- Install development tools with `python -m pip install -e ".[test]"`

## Run from the folder that contains your schedule

```powershell
course-schedule-checker data/sample_schedule.json
```

Give the command a JSON file inside the current folder or one of its subfolders.  If your schedule is elsewhere, change to its containing folder first.  The command returns 0 for a valid schedule without overlaps, 1 for overlaps, and 2 for a usage or input error.  Meetings must end later on the same day.

## Test and coverage

```powershell
python -m pytest --cov --cov-report=term-missing --cov-report=xml:coverage.xml
```

"""Command-line interface for checking course schedules."""

import json
import sys
from datetime import datetime
from pathlib import Path


def _to_minutes(value):
    """Convert an HH:MM string to minutes after midnight."""
    parsed = datetime.strptime(value, "%H:%M")
    return parsed.hour * 60 + parsed.minute


def load_courses(file_path):
    """Read a schedule JSON file inside the current working directory."""
    schedule_root = Path.cwd().resolve()
    schedule_path = (schedule_root / file_path).resolve()
    if not schedule_path.is_relative_to(schedule_root):
        raise ValueError("The schedule must be inside the current working folder.")
    if schedule_path.suffix.lower() != ".json":
        raise ValueError("The schedule must be a JSON file.")

    with schedule_path.open("r", encoding="utf-8") as schedule_file:
        courses = json.load(schedule_file)

    if not isinstance(courses, list):
        raise ValueError("The schedule must contain a JSON list of meetings.")
    for meeting in courses:
        if not isinstance(meeting, dict) or not all(
            isinstance(meeting.get(field), str)
            for field in ("course", "day", "start", "end")
        ):
            raise ValueError("Each meeting needs course, day, start and end strings.")
        if _to_minutes(meeting["start"]) >= _to_minutes(meeting["end"]):
            raise ValueError("A meeting's end time must be after its start time.")
    return courses


def find_conflicts(courses):
    """Return pairs of course codes whose meetings overlap on the same day."""
    conflicts = []
    for first_index in range(len(courses)):
        for second_index in range(first_index + 1, len(courses)):
            first = courses[first_index]
            second = courses[second_index]
            if first["day"].lower() == second["day"].lower():
                first_start = _to_minutes(first["start"])
                first_end = _to_minutes(first["end"])
                second_start = _to_minutes(second["start"])
                second_end = _to_minutes(second["end"])
                if first_start < second_end and second_start < first_end:
                    conflicts.append((first["course"], second["course"]))
    return conflicts


def main():
    """Run the schedule checker from the command line."""
    if len(sys.argv) != 2:
        print("Usage: course-schedule-checker <schedule.json>", file=sys.stderr)
        return 2

    try:
        courses = load_courses(sys.argv[1])
    except (OSError, ValueError) as error:
        print(f"Unable to load schedule: {error}", file=sys.stderr)
        return 2

    conflicts = find_conflicts(courses)
    if conflicts:
        for first_course, second_course in conflicts:
            print(f"Conflict: {first_course} overlaps {second_course}")
        return 1

    print(f"No conflicts found across {len(courses)} course meetings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

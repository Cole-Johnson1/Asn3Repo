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
    """Read course meetings from a JSON file."""
    try:
        with Path(file_path).open("r", encoding="utf-8") as schedule_file:
            return json.load(schedule_file)
    except Exception as error:
        print("Unable to load schedule:", error)
        return []


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
        print("Usage: course-schedule-checker <schedule.json>")
        return 2

    courses = load_courses(sys.argv[1])
    conflicts = find_conflicts(courses)
    if conflicts:
        for first_course, second_course in conflicts:
            print(f"Conflict: {first_course} overlaps {second_course}")
        return 1

    print(f"No conflicts found across {len(courses)} course meetings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Tests for the schedule-checking command-line functions."""

import json

from course_schedule_checker.cli import find_conflicts, load_courses


def test_find_conflicts_detects_overlapping_meetings():
    courses = [
        {"course": "A", "day": "Monday", "start": "09:00", "end": "10:30"},
        {"course": "B", "day": "monday", "start": "10:00", "end": "11:00"},
    ]

    assert find_conflicts(courses) == [("A", "B")]


def test_find_conflicts_ignores_different_days_and_adjacent_meetings():
    courses = [
        {"course": "A", "day": "Monday", "start": "09:00", "end": "10:00"},
        {"course": "B", "day": "Monday", "start": "10:00", "end": "11:00"},
        {"course": "C", "day": "Tuesday", "start": "09:30", "end": "10:30"},
    ]

    assert find_conflicts(courses) == []


def test_load_courses_reads_json(tmp_path):
    schedule = [{"course": "A", "day": "Monday", "start": "09:00", "end": "10:00"}]
    schedule_path = tmp_path / "schedule.json"
    schedule_path.write_text(json.dumps(schedule), encoding="utf-8")

    assert load_courses(schedule_path) == schedule

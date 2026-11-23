"""Tests for the schedule-checking command-line functions."""

import json
import sys

import pytest

from course_schedule_checker.cli import find_conflicts, load_courses, main


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


def test_load_courses_reads_json_in_nested_folder(tmp_path, monkeypatch):
    schedule = [{"course": "A", "day": "Monday", "start": "09:00", "end": "10:00"}]
    monkeypatch.chdir(tmp_path)
    folder = tmp_path / "schedules"
    folder.mkdir()
    schedule_path = folder / "schedule.json"
    schedule_path.write_text(json.dumps(schedule), encoding="utf-8")

    assert load_courses("schedules/schedule.json") == schedule


def test_load_courses_rejects_schedule_outside_working_folder(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.chdir(workspace)
    schedule_path = tmp_path / "schedule.json"
    schedule_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="inside the current working folder"):
        load_courses(schedule_path)


@pytest.mark.parametrize(
    ("file_name", "contents", "message"),
    [
        ("missing.json", None, "Unable to load schedule"),
        ("schedule.json", "[", "Unable to load schedule"),
        ("schedule.json", "{}", "JSON list of meetings"),
        ("schedule.json", '[{"course": "A"}]', "needs course, day, start and end"),
        (
            "schedule.json",
            '[{"course": "A", "day": "Monday", "start": "10:00", "end": "09:00"}]',
            "end time must be after",
        ),
        ("schedule.txt", "[]", "must be a JSON file"),
    ],
)
def test_main_rejects_invalid_schedule(file_name, contents, message, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["course-schedule-checker", file_name])
    if contents is not None:
        (tmp_path / file_name).write_text(contents, encoding="utf-8")

    assert main() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert message in captured.err


def test_main_reports_usage_without_a_path(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["course-schedule-checker"])

    assert main() == 2
    assert "Usage:" in capsys.readouterr().err


def test_main_reports_a_valid_schedule_without_conflicts(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["course-schedule-checker", "schedule.json"])
    (tmp_path / "schedule.json").write_text("[]", encoding="utf-8")

    assert main() == 0
    assert "No conflicts found" in capsys.readouterr().out


def test_main_reports_conflicts(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["course-schedule-checker", "schedule.json"])
    meetings = [
        {"course": "A", "day": "Monday", "start": "09:00", "end": "10:30"},
        {"course": "B", "day": "Monday", "start": "10:00", "end": "11:00"},
    ]
    (tmp_path / "schedule.json").write_text(json.dumps(meetings), encoding="utf-8")

    assert main() == 1
    assert "Conflict: A overlaps B" in capsys.readouterr().out

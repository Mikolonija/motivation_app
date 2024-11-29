from pytest import MonkeyPatch
from utils.helpers import (
    get_non_empty_input,
    get_task_category_name,
    get_task_status_name,
    msg_output,
)


def test_non_empty_input() -> None:
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr("builtins.input", lambda _: "Valid input")
    result: str = get_non_empty_input("Enter something: ", "Error: Answer cannot be empty")
    assert result == "Valid input"


def test_msg_output(capsys):
    message = "Test message"
    msg_output(message)
    captured = capsys.readouterr()
    assert captured.out == (
        "--------------------------------------------------------------------------------------------------------------------------------\n"
        "Test message\n"
        "--------------------------------------------------------------------------------------------------------------------------------\n"
    )


def test_get_task_category_name():
    assert get_task_category_name("1") == "Everyday Essentials"
    assert get_task_category_name("2") == "Growth & Learning"
    assert get_task_category_name("3") == "Health & Fitness"
    assert get_task_category_name("unknown_type") == "Unknown Category"


def test_get_task_status_name():
    assert get_task_status_name("1") == "In Progress"
    assert get_task_status_name("2") == "Completed"
    assert get_task_status_name("3") == "Expired"
    assert get_task_status_name("unknown_status") == "Unknown Status"

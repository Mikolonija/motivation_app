from enum import Enum


MENU_OPTION = Enum(
    "MENU_OPTION",
    [
        ("MANAGE_TASKS", "1"),
        ("VIEW_ALL_TASKS", "2"),
        ("VIEW_TODO_TASKS", "3"),
        ("MANAGE_PROFILE", "4"),
        ("VIEW_PROFILE", "5"),
        ("VIEW_ITEMS", "6"),
        ("BUY_ITEMS", "7"),
        ("SUBMIT_FEEDBACK", "8"),
        ("EXIT", "9"),
    ],
)

MENU_ACTION = Enum(
    "MENU_ACTION",
    [
        ("BACK", "1"),
    ],
)

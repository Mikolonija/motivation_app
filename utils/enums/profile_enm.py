from enum import Enum


ACTION_TYPE = Enum(
    "ACTION_TYPE",
    [
        ("UPDATE_FIRST_NAME", "1"),
        ("UPDATE_LAST_NAME", "2"),
        ("UPDATE_PHYSICAL", "3"),
        ("UPDATE_SMART", "4"),
        ("UPDATE_LIFESTYLE", "5"),
        ("ADD_COINS", "6"),
        ("UPDATE_COINS", "7"),
        ("ADD_ITEM", "8"),
    ],
)

FIELD = Enum(
    "FIELD",
    [
        ("FIRST_NAME", "FIRST_NAME"),
        ("LAST_NAME", "LAST_NAME"),
        ("PHYSICAL", "PHYSICAL"),
        ("SMART", "SMART"),
        ("LIFESTYLE", "LIFESTYLE"),
        ("COINS", "COINS"),
        ("ITEMS", "ITEMS"),
    ],
)
MODE_TYPE = Enum(
    "MODE_TYPE",
    [
        ("ADD", "1"),
        ("EDIT", "2"),
    ],
)
POINTS = Enum(
    "POINTS",
    [
        ("COINS", 20),
        ("PHYSICAL", 10),
        ("LIFESTYLE", 10),
        ("SMART", 10),
    ],
)

POINTS_BY_DIFUCALYTI = Enum(
    "POINTS_BY_DIFUCALYTI",
    [
        ("EASY", 5),
        ("MEDIUM", 10),
        ("HARD", 15),
    ],
)

from enum import Enum


MODE_TYPE = Enum(
    "MODE_TYPE",
    [
        ("ADD", "1"),
        ("MARK_AS_COMPLETED", "2"),
        ("UPDATE_DESCRIPTION", "3"),
        ("REMOVE", "4"),
    ],
)

CATEGORY_TYPE = Enum(
    "CATEGORY_TYPE",
    [
        ("EVERYDAY_ESSENTIALS", "1"),
        ("GROWTH_LEARNING", "2"),
        ("HEALTH_FITNESS", "3"),
    ],
)

FIELD = Enum(
    "FIELD",
    [
        ("ID", "ID"),
        ("DESCRIPTION", "DESCRIPTION"),
        ("DEADLINE", "DEADLINE"),
        ("STATUS", "STATUS"),
        ("CATEGORY", "CATEGORY"),
        ("DIFFICULTY", "DIFFICULTY"),
    ],
)

DIFFICULTY = Enum(
    "DIFFICULTY",
    [
        ("EASY", "1"),
        ("MEDIUM", "2"),
        ("HARD", "3"),
    ],
)


STATUS = Enum(
    "STATUS",
    [
        ("IN_PROGRESS", "1"),
        ("COMPLETED", "2"),
        ("EXPIRED", "3"),
    ],
)

VIEW_TYPE = Enum(
    "VIEW_TYPE",
    [
        ("ALL", "1"),
        ("TODO", "2"),
    ],
)

ACTION_TYPE = Enum(
    "ACTION_TYPE",
    [
        ("UPDATE_DESCRIPTION", "1"),
        ("UPDATE_STATUS", "2"),
        ("REMOVE_TASK", "3"),
    ],
)

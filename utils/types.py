from typing import TypedDict


class Task(TypedDict):
    ID: int
    DESCRIPTION: str
    DEADLINE: str
    STATUS: str
    CATEGORY: str


class Profile(TypedDict):
    FIRST_NAME: str
    LAST_NAME: str
    PHYSICAL: int
    SMART: int
    LIFESTYLE: int
    COINS: int
    ITEMS: list[str]


class Items(TypedDict):
    ID: int
    ITEM: str
    NAME: str
    COINS: int

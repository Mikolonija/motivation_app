from prompt_toolkit import prompt
from utils.enums import profile_enm, task_enm
from utils.types import Profile, Task


def get_non_empty_input_with_default(prompt_text: str, default: str, error_message: str) -> str:
    user_input = prompt(prompt_text, default=default).strip()
    while not user_input:
        msg_output(error_message)
        user_input = prompt(prompt_text, default=default).strip()
    return " ".join(user_input.split())


def input_with_default(prompt_text: str, default: str) -> str:
    user_input = prompt(prompt_text, default=default).strip()
    return " ".join(user_input.split())


def msg_output(msg: str) -> None:
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print(f"{msg}")
    print("--------------------------------------------------------------------------------------------------------------------------------")


def get_non_empty_input(prompt: str, error_message: str) -> str:
    user_input: str = input(prompt).strip()
    while not user_input:
        msg_output(error_message)
        user_input: str = input(prompt).strip()
    return " ".join(user_input.split())


def get_task_difficulty_name(type: str) -> str:
    difficulty_map = {
        task_enm.DIFFICULTY.EASY.value: "Easy",
        task_enm.DIFFICULTY.MEDIUM.value: "Medium",
        task_enm.DIFFICULTY.HARD.value: "Hard",
    }
    return difficulty_map.get(type, "Unknown Difficulty")


def get_task_category_name(type: str) -> str:
    category_map = {
        task_enm.CATEGORY_TYPE.EVERYDAY_ESSENTIALS.value: "Everyday Essentials",
        task_enm.CATEGORY_TYPE.GROWTH_LEARNING.value: "Growth & Learning",
        task_enm.CATEGORY_TYPE.HEALTH_FITNESS.value: "Health & Fitness",
    }
    return category_map.get(type, "Unknown Category")


def get_task_status_name(type: str) -> str:
    status_map = {
        task_enm.STATUS.IN_PROGRESS.value: "In Progress",
        task_enm.STATUS.COMPLETED.value: "Completed",
        task_enm.STATUS.EXPIRED.value: "Expired",
    }
    return status_map.get(type, "Unknown Status")


def get_points_by_task_difucalyti(task: Task) -> int:
    match task[task_enm.FIELD.DIFFICULTY.value]:
        case task_enm.DIFFICULTY.EASY.value:
            return profile_enm.POINTS_BY_DIFUCALYTI.EASY.value
        case task_enm.DIFFICULTY.MEDIUM.value:
            return profile_enm.POINTS_BY_DIFUCALYTI.MEDIUM.value
        case task_enm.DIFFICULTY.HARD.value:
            return profile_enm.POINTS_BY_DIFUCALYTI.HARD.value


def count_points_and_coins(task: Task, points_by_difucalyti: int) -> list[int] | None:
    coins = points_by_difucalyti + profile_enm.POINTS.COINS.value
    match task[task_enm.FIELD.CATEGORY.value]:
        case task_enm.CATEGORY_TYPE.EVERYDAY_ESSENTIALS.value:
            points = points_by_difucalyti + profile_enm.POINTS.LIFESTYLE.value
            return [points, coins]
        case task_enm.CATEGORY_TYPE.GROWTH_LEARNING.value:
            points = points_by_difucalyti + profile_enm.POINTS.SMART.value
            return [points, coins]
        case task_enm.CATEGORY_TYPE.HEALTH_FITNESS.value:
            points = points_by_difucalyti + profile_enm.POINTS.PHYSICAL.value
            return [points, coins]

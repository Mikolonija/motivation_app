from prompt_toolkit import prompt
from utils.enums import profile_enm, task_enm
from utils.types import Profile


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


def get_task_category_name(type: str):
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


def build_profile(first_name: str, last_name: str, physical: int = 100, smart: int = 100, lifestyle: int = 100, coins: int = 0, items: list = []):
    new_profile: Profile = {
        profile_enm.FIELD.FIRST_NAME.value: first_name,
        profile_enm.FIELD.LAST_NAME.value: last_name,
        profile_enm.FIELD.PHYSICAL.value: physical,
        profile_enm.FIELD.SMART.value: smart,
        profile_enm.FIELD.LIFESTYLE.value: lifestyle,
        profile_enm.FIELD.COINS.value: coins,
        profile_enm.FIELD.ITEMS.value: items,
    }
    return [new_profile]

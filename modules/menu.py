import os, sys
from modules.profile_managment.manage_profile import manage_profile
from modules.profile_managment.view_profile import profile_viewing
from modules.items_managment.buy_item import buy_item
from modules.items_managment.view_items import items_viewing
from modules.task_management.manage_tasks import manage_tasks
from modules.submit_feedback import submit_feedback
from modules.task_management.view_tasks import tasks_viewing
from utils import descriptions
from utils.enums import menu_enm, task_enm
from utils.helpers import get_non_empty_input, msg_output


def menu_selection(selection: str) -> None:
    match selection:
        case menu_enm.MENU_OPTION.MANAGE_TASKS.value:
            os.system("cls")
            manage_tasks()
        case menu_enm.MENU_OPTION.VIEW_ALL_TASKS.value:
            os.system("cls")
            tasks_viewing(task_enm.VIEW_TYPE.ALL.value)
        case menu_enm.MENU_OPTION.VIEW_TODO_TASKS.value:
            os.system("cls")
            tasks_viewing(task_enm.VIEW_TYPE.TODO.value)
        case menu_enm.MENU_OPTION.MANAGE_PROFILE.value:
            os.system("cls")
            manage_profile()
        case menu_enm.MENU_OPTION.VIEW_PROFILE.value:
            os.system("cls")
            profile_viewing()
        case menu_enm.MENU_OPTION.VIEW_ITEMS.value:
            os.system("cls")
            items_viewing()
        case menu_enm.MENU_OPTION.BUY_ITEMS.value:
            os.system("cls")
            buy_item()
        case menu_enm.MENU_OPTION.SUBMIT_FEEDBACK.value:
            os.system("cls")
            submit_feedback()
        case menu_enm.MENU_OPTION.EXIT.value:
            sys.exit()
        case _:
            os.system("cls")
            msg_output(f"Error: Please enter a number between 1 and {len(descriptions.menu_descriptions)} try again.")


def print_menu_options() -> None:
    print("\nPlease select an option:")
    for key, description in descriptions.menu_descriptions.items():
        print(f"{key}: {description}")


def menu() -> None:
    while True:
        try:
            print_menu_options()
            selection: str = get_non_empty_input(f"Select (1-{len(descriptions.menu_descriptions)}): ", "Error: select option cannot be empty")
            menu_selection(selection)
        except EOFError:
            os.system("cls")
        except KeyboardInterrupt:
            os.system("cls")
        except ValueError:
            msg_output(f"Error: Please enter a number between 1 and {len(descriptions.menu_descriptions)} try again.")

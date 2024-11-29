import os
from modules.file_operations.task_file_handler import TaskFileHandler
from utils.enums import menu_enm, task_enm
from utils.helpers import get_non_empty_input, get_task_category_name, get_task_status_name, msg_output
from utils.types import Task


class RemoveTask:
    def __init__(self, task_id: str, task_file_handler=TaskFileHandler()) -> None:
        self.task_id: str = task_id
        self.task_file_handler = task_file_handler
        self.all_tasks: list[Task] | list = self.task_file_handler.get_all_tasks()

    @classmethod
    def get_id(cls):
        while True:
            print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
            print(f"Attention: To go back to task mode selection, type '{menu_enm.MENU_ACTION.BACK.name.lower()}'.")
            try:
                txt: str = get_non_empty_input(
                    f"\nEnter the ID of the tasks you want remove or write {menu_enm.MENU_ACTION.BACK.name.lower()}: ", "Error:ID cannot be empty"
                )
                if txt.lower() == menu_enm.MENU_ACTION.BACK.name.lower():
                    os.system("cls")
                    break
                else:
                    task_id: int = int(txt)
                    return cls(task_id)
            except ValueError:
                os.system("cls")
                msg_output(f"Error: ID must be a number")

    def modify_task(self) -> None:
        task: Task | None = self.get_current_task_by_id()
        task_exist: bool = self.does_task_exist(task)
        if task_exist:
            self.print_task_info(task)
            self.remove(task)
        remove_task()

    def get_current_task_by_id(self) -> Task | None:
        for task in self.all_tasks:
            if int(task[task_enm.FIELD.ID.value]) == self.task_id:
                return task
        return None

    def does_task_exist(self, task: Task | None) -> bool:
        if task is None:
            os.system("cls")
            msg_output(f"Error: Task with ID {self.task_id} not found.")
            return False
        else:
            return True

    def print_task_info(self, task: Task) -> None:
        print(f"\nDESCRIPTION: {task[task_enm.FIELD.DESCRIPTION.value]}")
        print(f"DEADLINE: {task[task_enm.FIELD.DEADLINE.value]}")
        print(f"STATUS: {get_task_status_name(task[task_enm.FIELD.STATUS.value])}")
        print(f"CATEGORY: {get_task_category_name(task[task_enm.FIELD.CATEGORY.value])}")

    def remove(self, task: Task) -> None:
        confirm: str = get_non_empty_input(f"\nDo you want to remove task? (yes/no): ", "Error: Text cannot be empty")
        if confirm.lower() == "yes":
            os.system("cls")
            self.task_file_handler.update_task_in_file(task, task_enm.ACTION_TYPE.REMOVE_TASK.value)
        else:
            os.system("cls")
            msg_output("No changes were made.")


def remove_task() -> None:
    task_action = RemoveTask.get_id()
    if task_action:
        task_action.modify_task()
    return None

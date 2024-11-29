import os
from modules.file_operations.task_file_handler import TaskFileHandler
from modules.task_management.add_task import add_task
from modules.task_management.remove_task import remove_task
from modules.task_management.update_task import update_task
from utils import descriptions
from utils.enums import task_enm
from utils.helpers import get_non_empty_input, msg_output


class ManageTasks:
    def __init__(self, current_task_mode: str, task_file_handler=TaskFileHandler()) -> None:
        self.current_task_mode: str = current_task_mode
        self.task_file_handler = task_file_handler

    @classmethod
    def get_mode(cls):
        print_task_mode_type_choices()
        while True:
            choice: str = get_non_empty_input(f"\nEnter task mode type: ", "Error: task mode type cannot be empty ")
            if choice not in [
                task_enm.MODE_TYPE.ADD.value,
                task_enm.MODE_TYPE.MARK_AS_COMPLETED.value,
                task_enm.MODE_TYPE.UPDATE_DESCRIPTION.value,
                task_enm.MODE_TYPE.REMOVE.value,
            ]:
                msg_output(
                    f"Error: Please enter {task_enm.MODE_TYPE.ADD.value} to create a task, {task_enm.MODE_TYPE.MARK_AS_COMPLETED.value} to mark task as completed, {task_enm.MODE_TYPE.UPDATE_DESCRIPTION.value} to update the task description, and {task_enm.MODE_TYPE.REMOVE.value} to delete a task. Try again."
                )
                continue
            return cls(choice)

    def run_mode(self):
        if self.current_task_mode == task_enm.MODE_TYPE.ADD.value:
            os.system("cls")
            add_task()
        elif self.current_task_mode == task_enm.MODE_TYPE.MARK_AS_COMPLETED.value:
            os.system("cls")
            update_task(task_enm.MODE_TYPE.MARK_AS_COMPLETED.value)
        elif self.current_task_mode == task_enm.MODE_TYPE.UPDATE_DESCRIPTION.value:
            os.system("cls")
            update_task(task_enm.MODE_TYPE.UPDATE_DESCRIPTION.value)
        else:
            os.system("cls")
            remove_task()
        manage_tasks()


def print_task_mode_type_choices() -> None:
    print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
    print("Select the task mode type:")
    for key, value in descriptions.task_mode_type_descriptions.items():
        print(f"{key}: {value}")


def manage_tasks() -> None:
    manage_task = ManageTasks.get_mode()
    if manage_task:
        manage_task.run_mode()
    return None

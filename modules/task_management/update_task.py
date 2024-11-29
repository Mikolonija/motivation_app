import os
from modules.file_operations.profile_file_handler import ProfileFileHandler
from modules.file_operations.task_file_handler import TaskFileHandler
from utils.enums import menu_enm, task_enm
from utils.helpers import get_non_empty_input, get_task_category_name, get_task_status_name, input_with_default, msg_output
from utils.types import Task


class UpdateTask:
    def __init__(
        self,
        task_mode_type: str,
        task_id: str,
        task_file_handler=TaskFileHandler(),
        profile_file_handler=ProfileFileHandler(),
    ) -> None:
        self.task_mode_type: str = task_mode_type
        self.task_id: str = task_id
        self.task_file_handler = task_file_handler
        self.profile_file_handler = profile_file_handler
        self.tasks = (
            self.task_file_handler.get_not_completed_tasks()
            if self.task_mode_type == task_enm.MODE_TYPE.MARK_AS_COMPLETED.value
            else self.task_file_handler.get_all_tasks()
        )

    @classmethod
    def get_id(cls, task_mode_type: str):
        while True:
            print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
            print(f"Attention: To go back to task mode selection, type '{menu_enm.MENU_ACTION.BACK.name.lower()}'.")
            try:
                txt: str = get_non_empty_input(
                    f"\nEnter the ID of the tasks you want update or write {menu_enm.MENU_ACTION.BACK.name.lower()}: ",
                    "Error:ID cannot be empty",
                )
                if txt.lower() == menu_enm.MENU_ACTION.BACK.name.lower():
                    os.system("cls")
                    break
                else:
                    task_id: int = int(txt)
                    return cls(task_mode_type, task_id)
            except ValueError:
                os.system("cls")
                msg_output(f"Error: ID must be a number")

    def modify_task(self) -> None:
        task: Task | None = self.get_current_task_by_id()
        task_exist: bool = self.does_task_exist(task)
        if task_exist:
            self.update_field(task)
        update_task(self.task_mode_type)

    def update_field(self, task):
        if self.task_mode_type == task_enm.MODE_TYPE.UPDATE_DESCRIPTION.value:
            self.print_task_info(task)
            new_description = self.handle_new_description(task)
            self.update_task_field(task, task_enm.FIELD.DESCRIPTION.value, new_description, "Do you want to update task description?")
        else:
            self.print_task_info(task)
            self.update_task_field(
                task, task_enm.FIELD.STATUS.value, task_enm.STATUS.COMPLETED.value, "Do you want to change task status to completed?"
            )

    def get_current_task_by_id(self) -> Task | None:
        for task in self.tasks:
            if int(task[task_enm.FIELD.ID.value]) == int(self.task_id):
                return task
        return None

    def does_task_exist(self, task: Task | None) -> bool:
        if task is None:
            os.system("cls")
            if self.task_mode_type == task_enm.MODE_TYPE.MARK_AS_COMPLETED.value:
                msg_output(f"Error: Task with ID {self.task_id} not found or has already been completed.")
            else:
                msg_output(f"Error: Task with ID {self.task_id} not found.")
            return False
        else:
            return True

    def print_task_info(self, task: Task) -> None:
        print(f"\nDESCRIPTION: {task[task_enm.FIELD.DESCRIPTION.value]}")
        print(f"DEADLINE: {task[task_enm.FIELD.DEADLINE.value]}")
        print(f"STATUS: {get_task_status_name(task[task_enm.FIELD.STATUS.value])}")
        print(f"CATEGORY: {get_task_category_name(task[task_enm.FIELD.CATEGORY.value])}")

    def handle_new_description(self, task: Task) -> str:
        current_description: str = task[task_enm.FIELD.DESCRIPTION.value]
        new_description: str = input_with_default(f"\nEdit description: ", current_description)
        if new_description == "" or new_description == current_description.strip():
            os.system("cls")
            msg_output("No changes were made. The value you entered is either identical to the previous one or empty.")
            return update_task(self.task_mode_type)
        return new_description

    def update_task_field(self, task: Task, field: str, new_value: str, action_message: str) -> None:
        task[field] = new_value
        confirm: str = get_non_empty_input(f"\n{action_message} (yes/no): ", "Error: Text cannot be empty")
        if confirm.lower() == "yes" and self.task_mode_type == task_enm.MODE_TYPE.MARK_AS_COMPLETED.value:
            os.system("cls")
            self.task_file_handler.update_task_in_file(task, task_enm.ACTION_TYPE.UPDATE_STATUS.value)
            self.profile_file_handler.update_profile_level_and_coins(task)
        elif confirm.lower() == "yes" and self.task_mode_type == task_enm.MODE_TYPE.UPDATE_DESCRIPTION.value:
            os.system("cls")
            self.task_file_handler.update_task_in_file(task, task_enm.ACTION_TYPE.UPDATE_DESCRIPTION.value)
        else:
            os.system("cls")
            msg_output("No changes were made.")


def update_task(task_mode_type: str) -> None:
    task_action = UpdateTask.get_id(task_mode_type)
    if task_action:
        task_action.modify_task()
    return None

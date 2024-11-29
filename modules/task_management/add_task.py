import os
from modules.file_operations.task_file_handler import TaskFileHandler
from utils import config, descriptions
from utils.enums import task_enm, menu_enm
from utils.helpers import get_non_empty_input, msg_output
from utils.types import Task
from datetime import datetime, timedelta


class AddTask:
    def __init__(self, task_category: str, task_file_handler=TaskFileHandler()) -> None:
        self.task_category: str = task_category
        self.task_file_handler = task_file_handler
        self.id: int = self.task_file_handler.get_id()
        self.tasks: list[Task] | list = self.task_file_handler.get_tasks()

    @classmethod
    def get_choices(cls):
        print_task_type_category_choices()
        while True:
            choice: str = get_non_empty_input(
                f"\nEnter a task category (1-{len(task_enm.CATEGORY_TYPE)}) to create a task, or write {menu_enm.MENU_ACTION.BACK.name.lower()}: ",
                "Error: task category type cannot be empty ",
            )
            if choice.lower() == menu_enm.MENU_ACTION.BACK.name.lower():
                os.system("cls")
                break
            if choice not in [
                task_enm.CATEGORY_TYPE.EVERYDAY_ESSENTIALS.value,
                task_enm.CATEGORY_TYPE.GROWTH_LEARNING.value,
                task_enm.CATEGORY_TYPE.HEALTH_FITNESS.value,
            ]:
                msg_output(
                    f"Error: Please enter a valid choice. Use {task_enm.CATEGORY_TYPE.EVERYDAY_ESSENTIALS.value} to create an EVERYDAY_ESSENTIALS task, {task_enm.CATEGORY_TYPE.GROWTH_LEARNING.value} to create a GROWTH_LEARNING task, {task_enm.CATEGORY_TYPE.HEALTH_FITNESS.value} to create a HEALTH_FITNESS task, or {menu_enm.MENU_ACTION.BACK.value} to return to task mode selection. Please try again."
                )
                continue
            return cls(choice)

    def add_task(self) -> None:
        task_description: str = get_non_empty_input(
            f"Enter the {task_enm.CATEGORY_TYPE(self.task_category).name} task description: ", "Error: Task description cannot be empty"
        )
        task_deadline: str = self.create_task_deadline()
        self.create_task(task_description, task_deadline)
        add_task()

    def create_task_deadline(self) -> str:
        while True:
            task_deadline: str = get_non_empty_input(
                f"Enter the {task_enm.CATEGORY_TYPE(self.task_category).name} task deadline (YYYY-MM-DD): ",
                "Error: Task deadline cannot be empty",
            )
            try:
                yesterday = datetime.now() - timedelta(days=1)
                deadline_date: datetime = datetime.strptime(task_deadline, "%Y-%m-%d")
                if deadline_date < yesterday:
                    msg_output(f"Error: The deadline must be {datetime.now().strftime('%Y-%m-%d')} or a later date. Please enter a valid date.")
                else:
                    return task_deadline
            except ValueError:
                msg_output("Error: Invalid date format. Please enter the date in YYYY-MM-DD format.")

    def create_task(self, task_description: str, task_deadline: str) -> None:
        new_task: Task = self.build_task(task_description, task_deadline)
        self.add_task_to_file(new_task)
        self.print_success_message()

    def build_task(self, task_description: str, task_deadline: str) -> Task:
        new_task: Task = {
            task_enm.FIELD.ID.value: self.id,
            task_enm.FIELD.DESCRIPTION.value: task_description,
            task_enm.FIELD.DEADLINE.value: task_deadline,
            task_enm.FIELD.STATUS.value: task_enm.STATUS.IN_PROGRESS.value,
            task_enm.FIELD.CATEGORY.value: self.task_category,
        }
        return new_task

    def add_task_to_file(self, new_task: Task) -> None:
        self.tasks.append(new_task)
        self.task_file_handler.save_in_file(self.tasks)

    def print_success_message(self) -> None:
        os.system("cls")
        print(f"Your task has been saved to {config.FILE_TASKS_PATH}.")
        msg_output(f"{task_enm.CATEGORY_TYPE(self.task_category).name} task added successfully.")


def print_task_type_category_choices() -> None:
    print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
    print(f"Attention: To go back to task mode selection, type '{menu_enm.MENU_ACTION.BACK.name.lower()}'.")
    print(f"\nSelect a task category(1-{len(task_enm.CATEGORY_TYPE)}) to create a task:")
    for key, value in descriptions.task_category_type_descriptions.items():
        print(f"{key}: {value}")


def add_task() -> None:
    task_creation = AddTask.get_choices()
    if task_creation:
        task_creation.add_task()
    return None

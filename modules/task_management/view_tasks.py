import os
from modules.file_operations.task_file_handler import TaskFileHandler
from utils import config
from utils.enums import task_enm
from utils.helpers import get_task_category_name, get_task_difficulty_name, get_task_status_name, msg_output
from utils.types import Task
from tabulate import tabulate


class TaskView:
    def __init__(self, view_type: str, task_file_handler=TaskFileHandler()) -> None:
        self.view_type: str = view_type
        self.task_file_handler = task_file_handler
        self.todo_tasks: list[Task] | list = self.task_file_handler.get_not_completed_tasks()
        self.all_tasks: list[Task] | list = self.task_file_handler.get_all_tasks()

    def __str__(self) -> str:
        if not os.path.exists(config.FILE_TASKS_PATH):
            return f"Error: Cannot view tasks because the {config.FILE_TASKS_PATH} file does not exist."
        elif self.view_type == task_enm.VIEW_TYPE.ALL.value:
            view = self.view_all_tasks()
            return view
        else:
            view = self.view_todo_tasks()
            return view

    def view_all_tasks(self) -> str:
        if len(self.all_tasks) <= 0:
            return f"Error: Cannot view all tasks because from {config.FILE_TASKS_PATH} file the tasks does not exist."
        else:
            self.convert_types(self.all_tasks)
            return tabulate(self.all_tasks, headers="keys", tablefmt="grid")

    def view_todo_tasks(self) -> str:
        if len(self.todo_tasks) <= 0:
            return f"Error: Cannot view todo tasks because tasks with status {task_enm.STATUS.EXPIRED.name} and {task_enm.STATUS.IN_PROGRESS.name} does not exist from {config.FILE_TASKS_PATH} file."
        else:
            self.convert_types(self.todo_tasks)
            return tabulate(self.todo_tasks, headers="keys", tablefmt="grid")

    def convert_types(self, tasks) -> None:
        for task in tasks:
            task[task_enm.FIELD.STATUS.value] = get_task_status_name(task.get(task_enm.FIELD.STATUS.value))
            task[task_enm.FIELD.CATEGORY.value] = get_task_category_name(task.get(task_enm.FIELD.CATEGORY.value))
            task[task_enm.FIELD.DIFFICULTY.value] = get_task_difficulty_name(task.get(task_enm.FIELD.DIFFICULTY.value))


def tasks_viewing(view_type: int) -> None:
    tasks_view = TaskView(view_type)
    if tasks_view:
        msg_output(tasks_view)
    return None

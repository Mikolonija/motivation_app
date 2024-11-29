import csv, os
from datetime import datetime, timedelta
from utils import config
from utils.enums import task_enm
from utils.helpers import msg_output
from utils.types import Task


class TaskFileHandler:
    def save_in_file(self, tasks: list[Task]) -> None:
        fieldnames: list = self.get_fieldnames()
        os.makedirs(os.path.dirname(config.FILE_TASKS_PATH), exist_ok=True)
        with open(config.FILE_TASKS_PATH, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in tasks:
                writer.writerow(task)

    def get_tasks(self) -> list[Task] | list:
        if os.path.exists(config.FILE_TASKS_PATH):
            with open(config.FILE_TASKS_PATH, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                tasks = [row for row in reader]
                return tasks
        else:
            return []

    def check_expired_status(self) -> list[Task] | list:
        tasks: list[Task] | list = self.get_tasks()
        updated_tasks = self.update_status_expired(tasks)
        self.save_in_file(updated_tasks)
        return updated_tasks

    def get_not_completed_tasks(self) -> list:
        tasks: list[Task] | list = self.check_expired_status()
        tasks_not_completed: list[Task] = list(filter(lambda t: t[task_enm.FIELD.STATUS.value] != task_enm.STATUS.COMPLETED.value, tasks))
        return sorted(tasks_not_completed, key=lambda task: datetime.strptime(task[task_enm.FIELD.DEADLINE.value], "%Y-%m-%d"))

    def get_all_tasks(self) -> list:
        tasks: list[Task] | list = self.check_expired_status()
        return tasks

    def get_id(self) -> int:
        tasks: list[Task] | list = self.get_tasks()
        if tasks:
            return max(int(task[task_enm.FIELD.ID.value]) for task in tasks) + 1
        return 1

    def get_fieldnames(self) -> list:
        return [field.value for field in task_enm.FIELD]

    def update_status_expired(self, tasks) -> Task:
        yesterday = datetime.now() - timedelta(days=1)
        for task in tasks:
            deadline = datetime.strptime(task["DEADLINE"], "%Y-%m-%d")
            if yesterday > deadline and task[task_enm.FIELD.STATUS.value] != task_enm.STATUS.COMPLETED.value:
                task[task_enm.FIELD.STATUS.value] = task_enm.STATUS.EXPIRED.value
        return tasks

    def update_task_in_file(self, updated_task: Task, action_type: str) -> bool:
        all_tasks: list[Task] | list = self.get_tasks()
        for i, task in enumerate(all_tasks):
            if task[task_enm.FIELD.ID.value] == updated_task[task_enm.FIELD.ID.value]:
                self.update_field(updated_task, all_tasks, i, action_type)
                self.save_in_file(all_tasks)
                return True
        msg_output("Error: Failed to update the task field. Please try again.")
        return False

    def update_field(self, updated_task: Task, all_tasks: list[Task], i: int, action_type: str) -> None:
        match action_type:
            case task_enm.ACTION_TYPE.REMOVE_TASK.value:
                del all_tasks[i]
                msg_output("Task successfully removed.")
                for task in range(i, len(all_tasks)):
                    all_tasks[task][task_enm.FIELD.ID.value] = str(task + 1)
            case task_enm.ACTION_TYPE.UPDATE_STATUS.value:
                all_tasks[i] = updated_task
                msg_output(
                    f"Task ID {updated_task[task_enm.FIELD.ID.value]} {task_enm.FIELD.STATUS.name} updated successfully to {task_enm.STATUS.COMPLETED.name}."
                )
            case task_enm.ACTION_TYPE.UPDATE_DESCRIPTION.value:
                all_tasks[i] = updated_task
                msg_output(f"Task ID {updated_task[task_enm.FIELD.ID.value]} {task_enm.FIELD.DESCRIPTION.name} updated successfully.")

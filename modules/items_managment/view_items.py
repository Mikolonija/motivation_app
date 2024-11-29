import os
from modules.file_operations.items_file_handler import ItemsFileHandler
from utils import config
from utils.helpers import msg_output
from tabulate import tabulate
from utils.types import Items


class ItemsView:
    def __init__(self, items_file_handler=ItemsFileHandler()) -> None:
        self.items_file_handler = items_file_handler
        self.items: list[Items] = self.items_file_handler.get_items()

    def __str__(self):
        if not os.path.exists(config.FILE_ITEMS_PATH):
            return f"Error: Cannot view items because the {config.FILE_ITEMS_PATH} file does not exist."
        elif len(self.items) <= 0:
            return f"Error: Items does not exist from file {config.FILE_ITEMS_PATH}."
        else:
            return tabulate(self.items, headers="keys", tablefmt="grid")


def items_viewing():
    items_view = ItemsView()
    if items_view:
        msg_output(items_view)
    return None

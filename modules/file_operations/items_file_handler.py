import csv, os
from utils import config


class ItemsFileHandler:
    def get_items(self) -> list[dict]:
        if os.path.exists(config.FILE_ITEMS_PATH):
            with open(config.FILE_ITEMS_PATH, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                item = [row for row in reader]
                return item
        else:
            return []

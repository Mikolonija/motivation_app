import os
from modules.file_operations.items_file_handler import ItemsFileHandler
from modules.file_operations.profile_file_handler import ProfileFileHandler
from utils.enums import item_enm, profile_enm
from utils.helpers import get_non_empty_input, msg_output
from utils.types import Items, Profile, Task


class BuyItem:
    def __init__(self, item_id: int, profile_file_handler=ProfileFileHandler(), items_file_handler=ItemsFileHandler()) -> None:
        self.item_id: int = item_id
        self.profile_file_handler = profile_file_handler
        self.items_file_handler = items_file_handler
        self.items: list[Items] = self.items_file_handler.get_items()
        self.profile: list[Profile] = self.profile_file_handler.get_profile_info()

    @classmethod
    def get_id(cls):
        print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
        while True:
            try:
                id: str = get_non_empty_input(f"Enter the ID of the item you want to buy: ", "Error: Cannot be empty")
                item_id = int(id)
                return cls(item_id)
            except ValueError:
                msg_output(f"Error: ID must be a number")

    def buy(self) -> None:
        item: Items | None = self.get_current_item_by_id()
        can_buy: bool = self.does_can_buy(item)
        if can_buy:
            self.print_item(item)
            self.update_field(item)
        buy_item()

    def get_current_item_by_id(self) -> Items | None:
        for item in self.items:
            if int(item[item_enm.FIELD.ID.value]) == int(self.item_id):
                return item
        return None

    def does_can_buy(self, item: Task | None) -> bool:
        if item is None:
            os.system("cls")
            msg_output(f"Error: Item with ID {self.item_id} not found.")
            return False
        elif not self.profile:
            os.system("cls")
            msg_output(f"Error: You cannot buy the item because you don't have a profile.")
            return False
        elif int(item[item_enm.FIELD.COINS.value]) > int(self.profile[0][profile_enm.FIELD.COINS.value]):
            os.system("cls")
            self.print_item(item)
            msg_output(
                f"Error: You doesn't have coins to buy {item[item_enm.FIELD.NAME.value]} you need {int(item[item_enm.FIELD.COINS.value]) - int(self.profile[0][profile_enm.FIELD.COINS.value])} coins."
            )
            return False
        else:
            return True

    def print_item(self, item: Items) -> None:
        print(f"\nID: {item[item_enm.FIELD.ID.value]}")
        print(f"ITEM: {item[item_enm.FIELD.ITEM.value]}")
        print(f"NAME: {item[item_enm.FIELD.NAME.value]}")
        print(f"COINS: {item[item_enm.FIELD.COINS.value]}")
        msg_output(f"You have {self.profile[0][profile_enm.FIELD.COINS.value]} coins")

    def update_field(self, item: Items) -> None:
        confirm: str = get_non_empty_input(f"Do you want to buy {item[item_enm.FIELD.NAME.value]} (yes/no): ", "Error: Text cannot be empty")
        if confirm.lower() == "yes":
            os.system("cls")
            self.updated_coins(item)
            self.updated_items(item)
            msg_output(f"You have successfully bought the item")
        else:
            os.system("cls")
            msg_output("No changes were made.")

    def updated_coins(self, item) -> None:
        current_coins = int(self.profile[0][profile_enm.FIELD.COINS.value])
        item_cost = int(item[item_enm.FIELD.COINS.value])
        updated_coins = current_coins - item_cost
        self.profile[0][profile_enm.FIELD.COINS.value] = updated_coins
        self.profile_file_handler.update_profile_in_file(profile_enm.ACTION_TYPE.UPDATE_COINS.value, self.profile)

    def updated_items(self, item) -> None:
        new_items: list = eval(self.profile[0][profile_enm.FIELD.ITEMS.value])
        new_items.append(item[item_enm.FIELD.ITEM.value])
        self.profile[0][profile_enm.FIELD.ITEMS.value] = new_items
        self.profile_file_handler.update_profile_in_file(profile_enm.ACTION_TYPE.ADD_ITEM.value, self.profile)


def buy_item() -> None:
    item = BuyItem.get_id()
    if item:
        item.buy()
    return None

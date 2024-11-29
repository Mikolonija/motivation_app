import csv, os
from utils import config
from utils.enums import profile_enm, task_enm
from utils.helpers import msg_output
from utils.types import Profile, Task


class ProfileFileHandler:
    def save_in_file(self, profile: list[Profile]) -> None:
        fieldnames: list = self.get_fieldnames()
        os.makedirs(os.path.dirname(config.FILE_PROFILE_PATH), exist_ok=True)
        with open(config.FILE_PROFILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for current_profile in profile:
                writer.writerow(current_profile)

    def get_profile_info(self) -> list[Profile] | list:
        if os.path.exists(config.FILE_PROFILE_PATH):
            with open(config.FILE_PROFILE_PATH, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                profile = [row for row in reader]
                return profile
        else:
            return []

    def get_fieldnames(self) -> list:
        return [field.value for field in profile_enm.FIELD]

    def build_profile(
        self, first_name: str, last_name: str, physical: int = 100, smart: int = 100, lifestyle: int = 100, coins: int = 0, items: list = []
    ):
        new_profile: Profile = {
            profile_enm.FIELD.FIRST_NAME.value: first_name,
            profile_enm.FIELD.LAST_NAME.value: last_name,
            profile_enm.FIELD.PHYSICAL.value: physical,
            profile_enm.FIELD.SMART.value: smart,
            profile_enm.FIELD.LIFESTYLE.value: lifestyle,
            profile_enm.FIELD.COINS.value: coins,
            profile_enm.FIELD.ITEMS.value: items,
        }
        return [new_profile]

    def check_does_profile_exist(self) -> None:
        current_profile: Profile = self.get_profile_info()
        if not current_profile:
            new_profile = self.build_profile("First name", "Last name")
            self.save_in_file(new_profile)

    def update_profile_level_and_coins(self, task: Task) -> None:
        self.check_does_profile_exist()
        match task[task_enm.FIELD.CATEGORY.value]:
            case task_enm.CATEGORY_TYPE.EVERYDAY_ESSENTIALS.value:
                self.update_profile_in_file(profile_enm.ACTION_TYPE.UPDATE_LIFESTYLE.value)
            case task_enm.CATEGORY_TYPE.GROWTH_LEARNING.value:
                self.update_profile_in_file(profile_enm.ACTION_TYPE.UPDATE_SMART.value)
            case task_enm.CATEGORY_TYPE.HEALTH_FITNESS.value:
                self.update_profile_in_file(profile_enm.ACTION_TYPE.UPDATE_PHYSICAL.value)
        self.update_profile_in_file(profile_enm.ACTION_TYPE.ADD_COINS.value)

    def update_profile_in_file(self, action_type: str, update_profile: list[Profile] | None = None) -> bool:
        current_profile: Profile = self.get_profile_info()
        for profile in current_profile:
            self.update_field(update_profile, profile, action_type)
            self.save_in_file(current_profile)
            return True
        msg_output("Error: Failed to update the profile field. Please try again.")
        return False

    def update_field(self, update_profile: Profile, profile: Profile, action_type: str) -> None:
        match action_type:
            case profile_enm.ACTION_TYPE.UPDATE_LIFESTYLE.value:
                profile[profile_enm.FIELD.LIFESTYLE.value] = int(profile[profile_enm.FIELD.LIFESTYLE.value]) + profile_enm.POINTS.LIFESTYLE.value
                msg_output(f"Your {profile_enm.FIELD.LIFESTYLE.name} level has been updated.")
            case profile_enm.ACTION_TYPE.UPDATE_SMART.value:
                profile[profile_enm.FIELD.SMART.value] = int(profile[profile_enm.FIELD.SMART.value]) + profile_enm.POINTS.SMART.value
                msg_output(f"Your {profile_enm.FIELD.SMART.name} level has been updated.")
            case profile_enm.ACTION_TYPE.UPDATE_PHYSICAL.value:
                profile[profile_enm.FIELD.PHYSICAL.value] = int(profile[profile_enm.FIELD.PHYSICAL.value]) + profile_enm.POINTS.PHYSICAL.value
                msg_output(f"Your {profile_enm.FIELD.PHYSICAL.name} level has been updated.")
            case profile_enm.ACTION_TYPE.ADD_COINS.value:
                profile[profile_enm.FIELD.COINS.value] = int(profile[profile_enm.FIELD.COINS.value]) + profile_enm.POINTS.COINS.value
                msg_output(f"You have received {profile_enm.POINTS.COINS.value} coins.")
            case profile_enm.ACTION_TYPE.UPDATE_FIRST_NAME.value:
                profile[profile_enm.FIELD.FIRST_NAME.value] = update_profile[0][profile_enm.FIELD.FIRST_NAME.value]
                msg_output(f"Profile {profile_enm.FIELD.FIRST_NAME.name} was successfully updated")
            case profile_enm.ACTION_TYPE.UPDATE_LAST_NAME.value:
                profile[profile_enm.FIELD.LAST_NAME.value] = update_profile[0][profile_enm.FIELD.LAST_NAME.value]
                msg_output(f"Profile {profile_enm.FIELD.LAST_NAME.name} was successfully updated")
            case profile_enm.ACTION_TYPE.ADD_ITEM.value:
                profile[profile_enm.FIELD.ITEMS.value] = update_profile[0][profile_enm.FIELD.ITEMS.value]
                msg_output("Item successfully added to the profile.")
            case profile_enm.ACTION_TYPE.UPDATE_COINS.value:
                profile[profile_enm.FIELD.COINS.value] = update_profile[0][profile_enm.FIELD.COINS.value]
                msg_output("Coins successfully updated in the profile.")

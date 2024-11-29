import os
from modules.file_operations.profile_file_handler import ProfileFileHandler
from utils import config
from utils.enums import profile_enm
from utils.helpers import msg_output
from utils.types import Profile
from tabulate import tabulate


class ProfileView:
    def __init__(self, profile_file_handler=ProfileFileHandler()) -> None:
        self.profile_file_handler = profile_file_handler
        self.profile_info: list[Profile] | list = self.profile_file_handler.get_profile_info()

    def __str__(self):
        if not os.path.exists(config.FILE_TASKS_PATH):
            return f"Error: Cannot view profile because the {config.FILE_PROFILE_PATH} file does not exist."
        elif len(self.profile_info) <= 0:
            return f"Error: Data does not exist from file {config.FILE_PROFILE_PATH}."
        else:
            self.create_level()
            return tabulate(self.profile_info, headers="keys", tablefmt="grid")

    def create_level(self) -> None:
        level_physical = profile_enm.FIELD.PHYSICAL.value
        level_smart = profile_enm.FIELD.SMART.value
        level_lifestyle = profile_enm.FIELD.LIFESTYLE.value
        for profile in self.profile_info:
            profile[level_physical] = self.calculate_level(profile, profile_enm.FIELD.PHYSICAL.value)
            profile[level_smart] = self.calculate_level(profile, profile_enm.FIELD.SMART.value)
            profile[level_lifestyle] = self.calculate_level(profile, profile_enm.FIELD.LIFESTYLE.value)

    def calculate_level(self, profile: Profile, field) -> str:
        raw_score = int(profile.get(field))
        scaling_factor: int = 100
        level = raw_score // scaling_factor
        return f"Level {level} (Score: {raw_score})"


def profile_viewing():
    profile_view = ProfileView()
    if profile_view:
        msg_output(profile_view)
    return None

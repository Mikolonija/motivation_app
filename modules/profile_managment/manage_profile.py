import os
from modules.file_operations.profile_file_handler import ProfileFileHandler
from utils import config, descriptions
from utils.enums import profile_enm
from utils.helpers import build_profile, get_non_empty_input, get_non_empty_input_with_default, msg_output
from utils.types import Profile


class ManageProfile:
    def __init__(self, mode_type: str, profile_file_handler=ProfileFileHandler()) -> None:
        self.mode_type: str = mode_type
        self.profile_file_handler = profile_file_handler
        self.current_profile: list[Profile] | list = self.profile_file_handler.get_profile_info()

    @classmethod
    def get_profile_mode(cls):
        print("\nAttention: To stop the action and back to menu, you can press (ctrl + C) or type (ctrl + Z) and press Enter")
        profile_file_handler = ProfileFileHandler()
        current_profile: list[Profile] | list = profile_file_handler.get_profile_info()
        if not current_profile:
            return cls(profile_enm.MODE_TYPE.ADD.value)
        else:
            return cls(profile_enm.MODE_TYPE.EDIT.value)

    def modify_profile(self) -> None:
        if self.mode_type == profile_enm.MODE_TYPE.ADD.value:
            print("\nYou don't have a profile. Please use the Profile Creation Wizard to create a profile!")
            first_name: str = get_non_empty_input(f"\nPlease enter your first name: ", "Error: First name cannot be empty. Please try again.")
            last_name: str = get_non_empty_input(f"Please enter your last name: ", "Error: Last name cannot be empty. Please try again.")
            profile: list[Profile] = build_profile(first_name, last_name)
            self.profile_file_handler.save_in_file(profile)
            os.system("cls")
            msg_output(f"Profile was successfully created at file {config.FILE_PROFILE_PATH}")
        else:
            print_profile_edit_type_choices()
            current_type: str = self.edit_type_selection()
            self.handle_edit_type(current_type)
            manage_profile()

    def edit_type_selection(self) -> str:
        while True:
            choice: str = get_non_empty_input(
                f"\nPlease enter action type (1-{len(descriptions.profile_edit_type_descriptions)}): ", "Error: Cannot be empty "
            )
            if choice not in [
                profile_enm.ACTION_TYPE.UPDATE_FIRST_NAME.value,
                profile_enm.ACTION_TYPE.UPDATE_LAST_NAME.value,
            ]:
                msg_output(
                    f"Error: Please enter {profile_enm.ACTION_TYPE.UPDATE_FIRST_NAME.value} to edit first name, {profile_enm.ACTION_TYPE.UPDATE_LAST_NAME.value} to edit last name. Try again."
                )
                continue
            return choice

    def handle_edit_type(self, current_type: str) -> None:
        if current_type == profile_enm.ACTION_TYPE.UPDATE_FIRST_NAME.value:
            self.edit_first_name()
        else:
            self.edit_last_name()

    def edit_first_name(self) -> None:
        first_name: str = get_non_empty_input_with_default(
            f"Edit first name: ", self.current_profile[0][profile_enm.FIELD.FIRST_NAME.value], "Error: First name cannot be empty "
        )
        old_value: str = self.current_profile[0][profile_enm.FIELD.FIRST_NAME.value]
        self.current_profile[0][profile_enm.FIELD.FIRST_NAME.value] = first_name
        self.isValid(first_name, old_value, profile_enm.ACTION_TYPE.UPDATE_FIRST_NAME.value)

    def edit_last_name(self) -> None:
        last_name: str = get_non_empty_input_with_default(
            f"Edit last name: ", self.current_profile[0][profile_enm.FIELD.LAST_NAME.value], "Error: Last name cannot be empty "
        )
        old_value: str = self.current_profile[0][profile_enm.FIELD.LAST_NAME.value]
        self.current_profile[0][profile_enm.FIELD.LAST_NAME.value] = last_name
        self.isValid(last_name, old_value, profile_enm.ACTION_TYPE.UPDATE_LAST_NAME.value)

    def isValid(self, new_value: str, old_value: str, action_type: str) -> None:
        if new_value == old_value.strip():
            os.system("cls")
            msg_output("No changes were made. The value you entered is identical to the previous one.")
        else:
            self.update_profile(new_value, old_value, action_type)

    def update_profile(self, new_value: str, old_value: str, action_type: str) -> None:
        confirm: str = get_non_empty_input(f"Do you want to change '{old_value}' to '{new_value}' ? (yes/no): ", "Error: Text cannot be empty")
        if confirm.lower() == "yes":
            os.system("cls")
            self.profile_file_handler.update_profile_in_file(action_type, self.current_profile)
        else:
            os.system("cls")
            msg_output("No changes were made.")


def print_profile_edit_type_choices() -> None:
    print("Select the action type:")
    for key, value in descriptions.profile_edit_type_descriptions.items():
        print(f"{key}: {value}")


def manage_profile() -> None:
    profile = ManageProfile.get_profile_mode()
    if profile:
        profile.modify_profile()
    return None

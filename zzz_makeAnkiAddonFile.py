# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import os
import zipfile
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from config.change_log import OLD_CHANGE_LOG
    from config.patrons_list import PATRONS_LIST
    # from shige_config.popup_config import NEW_FEATURE
    # from shige_config.endroll.listOfSupportedPatrons import CREATE_OR_FIXED

ADDON_NAME ="Custom Debug Info"

def create_ankiaddon():
    current_dir = os.getcwd()

    today = datetime.today().strftime("%Y%m%d%H%M")

    zip_name = f"addon_{today}.zip"

    exclude_dirs = ["__pycache__", ".vscode", ".git", "user_files"] #🟢user_files
    exclude_full_dirs = []
    # exclude_full_dirs = [os.path.join(current_dir, "simpleaudio_patched.libs")]

    exclude_exts = [".ankiaddon", ".zip"]
    exclude_files = ["meta.json", zip_name, "zzz_template_00.md", ".gitignore","zzz_makeAnkiAddonFile.py"]

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(current_dir):
            filtered_dirs = []
            for sub_dir in dirs:
                full_sub_dir_path = os.path.join(root, sub_dir)
                if sub_dir not in exclude_dirs and full_sub_dir_path not in exclude_full_dirs:
                    filtered_dirs.append(sub_dir)

            dirs[:] = filtered_dirs
            for file in files:
                if file not in exclude_files and os.path.splitext(file)[1] not in exclude_exts:
                    print(f"Adding file to zip: {os.path.join(root, file)}")

                    zipf.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file), current_dir))

    os.rename(zip_name, f"{ADDON_NAME}_{today}.ankiaddon")

    if os.path.exists(zip_name):
        with zipfile.ZipFile(zip_name, "r") as zipf:
            is_empty = len(zipf.namelist()) == 0

        if is_empty:
            os.remove(zip_name)

create_ankiaddon()
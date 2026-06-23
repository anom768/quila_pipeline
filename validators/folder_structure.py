import os
import bpy
from ..sop_rules import REQUIRED_FOLDERS, get_file_mode
from . import Issue


def validate(context):
    issues = []
    filepath = bpy.data.filepath

    if not filepath:
        return issues

    mode = get_file_mode(filepath)
    current_folder = os.path.dirname(filepath)

    if mode == "wip":
        current_folder_name = os.path.basename(current_folder)
        if current_folder_name != "WIP":
            issues.append(Issue(
                category="Folder Structure",
                message=(
                    f"File WIP seharusnya berada tepat di dalam folder bernama 'WIP', "
                    f"bukan di '{current_folder_name}'."
                ),
            ))
            return issues
        object_folder = os.path.dirname(current_folder)
    else:
        # Mode final: file seharusnya berada langsung di folder utama object
        object_folder = current_folder

    if not os.path.isdir(object_folder):
        issues.append(Issue(
            category="Folder Structure",
            message=f"Folder utama object '{object_folder}' tidak ditemukan.",
        ))
        return issues

    existing_entries = set(os.listdir(object_folder))

    for folder in REQUIRED_FOLDERS:
        if folder not in existing_entries:
            issues.append(Issue(
                category="Folder Structure",
                message=f"Folder wajib '{folder}' tidak ditemukan di '{object_folder}'.",
            ))

    return issues
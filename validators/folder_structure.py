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
        object_folder = current_folder

    if not os.path.isdir(object_folder):
        issues.append(Issue(
            category="Folder Structure",
            message=f"Folder utama object '{object_folder}' tidak ditemukan.",
        ))
        return issues

    existing_entries_lower = {}
    for entry in os.listdir(object_folder):
        existing_entries_lower.setdefault(entry.lower(), entry)

    for folder in REQUIRED_FOLDERS:
        actual_entry = existing_entries_lower.get(folder.lower())

        if actual_entry is None:
            issues.append(Issue(
                category="Folder Structure",
                message=f"Folder wajib '{folder}' tidak ditemukan di '{object_folder}'.",
            ))
        elif actual_entry != folder:
            issues.append(Issue(
                category="Folder Structure",
                message=(
                    f"Nama folder '{actual_entry}' tidak boleh huruf kecil, "
                    f"seharusnya '{folder}' (huruf besar semua)."
                ),
            ))

    # BARU — Cek folder ekstra yang tidak diizinkan
    allowed_lower = {f.lower() for f in REQUIRED_FOLDERS}
    for entry in os.listdir(object_folder):
        entry_path = os.path.join(object_folder, entry)
        if os.path.isdir(entry_path) and entry.lower() not in allowed_lower:
            issues.append(Issue(
                category="Folder Structure",
                message=(
                    f"Folder '{entry}' tidak diizinkan di sini. "
                    f"Hanya boleh ada: {', '.join(REQUIRED_FOLDERS)}."
                ),
            ))

    return issues
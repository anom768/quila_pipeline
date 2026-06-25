import os
import re
import bpy
from ..sop_rules import REQUIRED_FOLDERS, get_file_mode, get_expected_object_name
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

    # Cek nama folder utama: harus UPPERCASE dari object_name, hanya huruf/angka/underscore
    expected_object_name = get_expected_object_name(filepath)
    actual_root_name = os.path.basename(object_folder)

    if expected_object_name:
        expected_root_name = expected_object_name.upper()

        # Cek karakter tidak valid (spasi, strip, dll) — cek ini duluan
        if not re.match(r'^[A-Z0-9_]+$', actual_root_name):
            issues.append(Issue(
                category="Folder Structure",
                message=(
                    f"Nama folder utama '{actual_root_name}' mengandung karakter tidak valid. "
                    f"Hanya boleh huruf besar, angka, dan underscore (misal: '{expected_root_name}')."
                ),
            ))
        elif actual_root_name != expected_root_name:
            # Nama valid tapi tidak cocok dengan yang seharusnya
            if actual_root_name == expected_object_name:
                # Kasusnya: nama benar tapi lowercase
                issues.append(Issue(
                    category="Folder Structure",
                    message=(
                        f"Nama folder utama '{actual_root_name}' harus UPPERCASE, "
                        f"seharusnya '{expected_root_name}'."
                    ),
                ))
            else:
                # Nama berbeda sama sekali dari object_name
                issues.append(Issue(
                    category="Folder Structure",
                    message=(
                        f"Nama folder utama '{actual_root_name}' tidak sesuai tugas "
                        f"(seharusnya '{expected_root_name}')."
                    ),
                ))

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

    for folder in REQUIRED_FOLDERS:
        actual_entry = existing_entries_lower.get(folder.lower())
        if actual_entry is None:
            continue

        subfolder_path = os.path.join(object_folder, actual_entry)
        if not os.path.isdir(subfolder_path):
            continue

        for inner_entry in os.listdir(subfolder_path):
            inner_path = os.path.join(subfolder_path, inner_entry)
            if os.path.isdir(inner_path):
                issues.append(Issue(
                    category="Folder Structure",
                    message=(
                        f"Folder '{inner_entry}' tidak boleh ada di dalam '{actual_entry}'. "
                        f"Folder ini hanya boleh berisi file, bukan folder lain."
                    ),
                ))

    return issues
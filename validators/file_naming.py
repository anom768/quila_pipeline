import os
import bpy
from ..sop_rules import get_file_mode, parse_filename_by_mode
from ..csv_loader import get_current_assigned_object_name
from .issue import Issue


def validate(context):
    issues = []
    filepath = bpy.data.filepath

    if not filepath:
        issues.append(Issue(
            category="File Naming",
            message="File belum disimpan. Simpan file dengan format WIP sebelum melakukan check.",
        ))
        return issues

    filename = os.path.basename(filepath)
    mode = get_file_mode(filepath)
    match = parse_filename_by_mode(filename, mode)

    if not match:
        expected_format = (
            "[object_name]_(variantxx)_[wipxx].blend" if mode == "wip"
            else "[object_name]_(variantxx).blend"
        )
        issues.append(Issue(
            category="File Naming",
            message=f"Nama file '{filename}' tidak sesuai format '{expected_format}'.",
        ))
        return issues

    object_name = match.group("object_name")
    expected_object_name = get_current_assigned_object_name(context)

    if expected_object_name is None:
        issues.append(Issue(
            category="File Naming",
            message="Pilih Tugas dan Artist terlebih dahulu sebelum melakukan check.",
        ))
    elif object_name != expected_object_name:
        issues.append(Issue(
            category="File Naming",
            message=(
                f"Nama file tidak sesuai tugas: nama file mengandung '{object_name}', "
                f"seharusnya '{expected_object_name}'."
            ),
        ))

    return issues

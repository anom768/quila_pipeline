import os
import bpy
from ..sop_rules import FILE_NAME_PATTERN
from ..csv_loader import get_current_assigned_object_name
from . import Issue


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
    match = FILE_NAME_PATTERN.match(filename)

    if not match:
        issues.append(Issue(
            category="File Naming",
            message=(
                f"Nama file '{filename}' tidak sesuai format "
                f"'[object_name]_(variantxx)_[wipxx].blend'."
            ),
        ))
        return issues

    object_name = match.group("object_name")
    expected_object_name = get_current_assigned_object_name(context)

    if expected_object_name and object_name != expected_object_name:
        issues.append(Issue(
            category="File Naming",
            message=(
                f"object_name '{object_name}' tidak sesuai dengan tugas yang dipilih "
                f"(seharusnya '{expected_object_name}')."
            ),
        ))

    return issues
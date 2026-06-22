import os
import bpy
from ..sop_rules import FILE_NAME_PATTERN
from ..csv_loader import get_tasks_for_student
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

    props = context.scene.quila_props
    student_name = props.student_name

    if student_name and student_name != "NONE":
        assigned_tasks = get_tasks_for_student(context, student_name)
        if assigned_tasks and object_name not in assigned_tasks:
            issues.append(Issue(
                category="File Naming",
                message=(
                    f"object_name '{object_name}' tidak terdaftar sebagai tugas "
                    f"untuk student '{student_name}'. Tugas terdaftar: {', '.join(assigned_tasks)}."
                ),
            ))

    return issues
import os
import bpy
from ..sop_rules import RENDER_NAME_PATTERN, get_file_mode
from . import Issue


def validate(context):
    issues = []
    filepath = bpy.data.filepath

    if not filepath:
        return issues

    mode = get_file_mode(filepath)
    current_folder = os.path.dirname(filepath)

    if mode == "wip":
        object_folder = os.path.dirname(current_folder)
    else:
        object_folder = current_folder

    render_folder = os.path.join(object_folder, "RENDER")

    if not os.path.isdir(render_folder):
        # Sudah ditangani validator folder structure
        return issues

    for entry in os.listdir(render_folder):
        full_path = os.path.join(render_folder, entry)
        if not os.path.isfile(full_path):
            continue

        name_without_ext = os.path.splitext(entry)[0]

        if not RENDER_NAME_PATTERN.match(name_without_ext):
            issues.append(Issue(
                category="Render Naming",
                message=(
                    f"File render '{entry}' tidak sesuai format "
                    f"'[object_name]_(variantxx)_[prevxx]'."
                ),
                target_name=entry,
            ))

    return issues
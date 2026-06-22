import os
import bpy
from ..sop_rules import RENDER_NAME_PATTERN
from . import Issue


def validate(context):
    issues = []
    filepath = bpy.data.filepath

    if not filepath:
        return issues

    wip_folder = os.path.dirname(filepath)
    object_folder = os.path.dirname(wip_folder)
    render_folder = os.path.join(object_folder, "RENDER")

    if not os.path.isdir(render_folder):
        # Sudah ditangani validator folder structure (v02)
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
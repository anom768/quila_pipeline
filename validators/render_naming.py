import os
import bpy
from ..sop_rules import RENDER_NAME_PATTERN, get_file_mode, get_expected_object_name
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
        return issues

    expected_object_name = get_expected_object_name(filepath)

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
                target_name=render_folder,
                action_type="open_render_folder"
            ))
            continue

        if expected_object_name and not name_without_ext.startswith(expected_object_name):
            issues.append(Issue(
                category="Render Naming",
                message=(
                    f"File render '{entry}' namanya tidak sesuai dengan object_name "
                    f"yang aktif (seharusnya diawali '{expected_object_name}')."
                ),
                target_name=render_folder,
                action_type="open_render_folder"
            ))

    return issues
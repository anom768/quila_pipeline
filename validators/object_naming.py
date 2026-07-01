import bpy
from ..sop_rules import OBJECT_NAME_PATTERN
from . import Issue


def validate(context):
    issues = []

    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue

        if not OBJECT_NAME_PATTERN.match(obj.name):
            issues.append(Issue(
                category="Object Naming",
                message=(
                    f"Nama object '{obj.name}' tidak sesuai format "
                    f"'geo_part_name_(variantxx)'."
                ),
                target_name=obj.name,
                action_type="select_object",
            ))

    return issues
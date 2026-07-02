import bpy
from ..sop_rules import OBJECT_NAME_PATTERN, get_expected_object_name
from .issue import Issue


def validate(context):
    issues = []
    expected_collection = get_expected_object_name(bpy.data.filepath)

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

        if expected_collection:
            col_names = [c.name for c in obj.users_collection]
            if expected_collection not in col_names:
                if not col_names:
                    location_info = "tidak ada di collection manapun (langsung di Scene root)"
                else:
                    location_info = f"berada di collection: {', '.join(col_names)}"
                issues.append(Issue(
                    category="Object Naming",
                    message=(
                        f"Object '{obj.name}' harus berada di dalam collection "
                        f"'{expected_collection}', tapi {location_info}."
                    ),
                    target_name=obj.name,
                    action_type="select_object",
                ))

    return issues

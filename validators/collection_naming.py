import bpy
from ..sop_rules import get_expected_object_name, LGT_CAM_COLLECTION_NAME
from . import Issue


def validate(context):
    issues = []
    expected_name = get_expected_object_name(bpy.data.filepath)

    if expected_name is None:
        # Sudah ditangani validator file naming (v01), tidak perlu duplikasi error
        return issues

    all_collections = bpy.data.collections

    collection_names = [c.name for c in all_collections]
    if expected_name not in collection_names:
        issues.append(Issue(
            category="Collection Naming",
            message=f"Collection bernama '{expected_name}' (sesuai nama file) tidak ditemukan.",
        ))

    for col in all_collections:
        if col.name in (expected_name, LGT_CAM_COLLECTION_NAME):
            continue
        issues.append(Issue(
            category="Collection Naming",
            message=(
                f"Collection '{col.name}' tidak sesuai SOP "
                f"(harus '{expected_name}' atau '{LGT_CAM_COLLECTION_NAME}')."
            ),
            target_name=col.name,
        ))

    object_collection = bpy.data.collections.get(expected_name)
    if object_collection:
        for obj in object_collection.objects:
            if obj.type in {"LIGHT", "CAMERA"}:
                issues.append(Issue(
                    category="Collection Naming",
                    message=(
                        f"Object '{obj.name}' bertipe {obj.type} ada di collection "
                        f"'{expected_name}'. Light & Camera harus di collection "
                        f"'{LGT_CAM_COLLECTION_NAME}'."
                    ),
                    target_name=obj.name,
                ))

    return issues
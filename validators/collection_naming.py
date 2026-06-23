import bpy
from ..sop_rules import get_expected_object_name, LGT_CAM_COLLECTION_NAME
from . import Issue


def validate(context):
    issues = []
    expected_name = get_expected_object_name(bpy.data.filepath)

    if expected_name is None:
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

    lgt_cam_collection = bpy.data.collections.get(LGT_CAM_COLLECTION_NAME)

    for obj in bpy.data.objects:
        if obj.type not in {"LIGHT", "CAMERA"}:
            continue

        is_in_lgt_cam = (
            lgt_cam_collection is not None
            and lgt_cam_collection in obj.users_collection
        )

        if not is_in_lgt_cam:
            issues.append(Issue(
                category="Collection Naming",
                message=(
                    f"Object '{obj.name}' bertipe {obj.type} harus berada di collection "
                    f"'{LGT_CAM_COLLECTION_NAME}'."
                ),
                target_name=obj.name,
            ))

    return issues
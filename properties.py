import bpy
from .csv_loader import get_student_enum_items


class QuilaIssueItem(bpy.types.PropertyGroup):
    """Satu baris hasil temuan error dari validator"""

    category: bpy.props.StringProperty(name="Category")
    message: bpy.props.StringProperty(name="Message")
    target_name: bpy.props.StringProperty(name="Target Name")


class QuilaSceneProperties(bpy.types.PropertyGroup):
    """Data yang tersimpan per-file (.blend), nempel di Scene"""

    student_name: bpy.props.EnumProperty(
        name="Student",
        description="Pilih nama student yang sedang mengerjakan file ini",
        items=get_student_enum_items,
    )

    is_valid: bpy.props.BoolProperty(
        name="Is Valid",
        description="True kalau hasil Check terakhir tidak ada error sama sekali",
        default=False,
    )

    has_been_checked: bpy.props.BoolProperty(
        name="Has Been Checked",
        description="True kalau tombol Check sudah pernah dijalankan minimal sekali",
        default=False,
    )

    validation_results: bpy.props.CollectionProperty(
        type=QuilaIssueItem,
        name="Validation Results",
    )
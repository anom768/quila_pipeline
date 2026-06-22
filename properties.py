import bpy


class QuilaIssueItem(bpy.types.PropertyGroup):
    """Satu baris hasil temuan error dari validator"""

    category: bpy.props.StringProperty(name="Category")
    message: bpy.props.StringProperty(name="Message")
    target_name: bpy.props.StringProperty(name="Target Name")


class QuilaSceneProperties(bpy.types.PropertyGroup):
    """Data yang tersimpan per-file (.blend), nempel di Scene"""

    student_name: bpy.props.StringProperty(
        name="Student",
        description="Nama student yang sedang mengerjakan file ini",
        default="",
    )

    is_valid: bpy.props.BoolProperty(
        name="Is Valid",
        description="True kalau hasil Check terakhir tidak ada error sama sekali",
        default=False,
    )

    validation_results: bpy.props.CollectionProperty(
        type=QuilaIssueItem,
        name="Validation Results",
    )
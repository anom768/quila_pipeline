import bpy
from .csv_loader import get_tugas_enum_items, get_artist_enum_items


class QuilaIssueItem(bpy.types.PropertyGroup):
    """Satu baris hasil temuan error dari validator"""

    category: bpy.props.StringProperty(name="Category")
    message: bpy.props.StringProperty(name="Message")
    target_name: bpy.props.StringProperty(name="Target Name")
    action_type: bpy.props.StringProperty(name="Action Type")


class QuilaSceneProperties(bpy.types.PropertyGroup):
    """Data yang tersimpan per-file (.blend), nempel di Scene"""

    tugas_ke: bpy.props.EnumProperty(
        name="Tugas",
        description="Pilih tugas ke berapa yang sedang dikerjakan",
        items=get_tugas_enum_items,
    )

    artist_name: bpy.props.EnumProperty(
        name="Artist",
        description="Pilih nama artist yang sedang mengerjakan file ini",
        items=get_artist_enum_items,
    )

    is_valid: bpy.props.BoolProperty(
        name="Is Valid",
        description="True kalau hasil pengecekan terakhir tidak ada error sama sekali",
        default=False,
    )

    has_been_checked: bpy.props.BoolProperty(
        name="Has Been Checked",
        description="True kalau pengecekan sudah pernah dijalankan minimal sekali",
        default=False,
    )

    validation_results: bpy.props.CollectionProperty(
        type=QuilaIssueItem,
        name="Validation Results",
    )
bl_info = {
    "name": "Quila Pipeline",
    "author": "Bangkit Anom Sedhayu | bangkitunom87@gmail.com",
    "version": (0, 1, 0),
    "blender": (4, 5, 1),
    "location": "View3D > Sidebar (N-Panel) > Quila",
    "description": "Pipeline checker untuk standarisasi naming & struktur file Blender",
    "category": "Pipeline",
}

import bpy
from .properties import QuilaIssueItem, QuilaSceneProperties
from .preferences import QuilaAddonPreferences
from .operators.op_check import QUILA_OT_check_all
from .operators.op_mark_final import QUILA_OT_mark_as_final
from .operators.op_select_target import QUILA_OT_select_target
from .ui.panel import QUILA_PT_main_panel

classes = (
    QuilaIssueItem,
    QuilaSceneProperties,
    QuilaAddonPreferences,
    QUILA_OT_check_all,
    QUILA_OT_mark_as_final,
    QUILA_OT_select_target,
    QUILA_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.quila_props = bpy.props.PointerProperty(type=QuilaSceneProperties)

    print("Quila Pipeline: addon berhasil di-enable")


def unregister():
    del bpy.types.Scene.quila_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("Quila Pipeline: addon di-disable")
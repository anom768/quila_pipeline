bl_info = {
    "name": "Quila Pipeline",
    "author": "Bangkit Anom Sedhayu | bangkitunom87@gmail.com",
    "version": (0, 1, 2),
    "blender": (4, 5, 1),
    "location": "View3D > Sidebar (N-Panel) > Quila",
    "description": "Pipeline checker untuk standarisasi naming & struktur file Blender",
    "category": "Pipeline",
}

import bpy
from .properties import QuilaIssueItem, QuilaSceneProperties
from .operators.op_publish import QUILA_OT_publish
from .operators.op_create_project import QUILA_OT_create_project
from .ui.panel import QUILA_PT_main_panel

classes = (
    QuilaIssueItem,
    QuilaSceneProperties,
    QUILA_OT_publish,
    QUILA_OT_create_project,
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
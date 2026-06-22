import bpy

class QUILA_PT_main_panel(bpy.types.Panel):
    """Panel utama Quila Pipeline di N-Panel viewport"""

    bl_idname = "QUILA_PT_main_panel"
    bl_label = "Quila Pipeline"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Quila"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Quila Pipeline Checker")
        layout.label(text="(belum ada fitur, baru tampilan)")
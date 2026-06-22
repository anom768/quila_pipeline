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
        props = context.scene.quila_props

        layout.label(text="Quila Pipeline Checker")
        layout.prop(props, "student_name")

        layout.separator()
        layout.operator("quila.check_all", icon="CHECKMARK")

        layout.separator()

        if not props.has_been_checked:
            layout.label(text="Belum ada hasil check.", icon="INFO")
        elif props.is_valid:
            layout.label(text="Semua pengecekan lolos.", icon="CHECKMARK")
        else:
            box = layout.box()
            box.label(text=f"Ditemukan {len(props.validation_results)} masalah:", icon="ERROR")
            for item in props.validation_results:
                box.label(text=f"[{item.category}] {item.message}")
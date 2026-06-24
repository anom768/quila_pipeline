import bpy
from collections import defaultdict
from .helpers import get_wrap_width_chars, draw_wrapped_text
from ..csv_loader import get_current_assigned_object_name


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
        layout.prop(props, "tugas_ke")
        layout.prop(props, "artist_name")

        object_name = get_current_assigned_object_name(context)
        info_box = layout.box()
        if object_name:
            info_box.label(text=f"Object: {object_name}", icon="OBJECT_DATA")
        else:
            info_box.label(text="Object: (pilih Tugas & Artist dulu)", icon="OBJECT_DATA")

        layout.separator()
        # Label tombol dinamis: "Publish" di mode WIP, "Check" di mode Final
        filepath = bpy.data.filepath
        from ..sop_rules import get_file_mode
        mode = get_file_mode(filepath) if filepath else "wip"

        if mode == "final":
            layout.operator("quila.publish", text="Check SOP", icon="CHECKMARK")
        else:
            layout.operator("quila.publish", text="Publish", icon="EXPORT")

        layout.separator()

        if not props.has_been_checked:
            layout.label(text="Belum ada hasil check.", icon="INFO")
        elif props.is_valid:
            layout.label(text="Semua pengecekan lolos.", icon="CHECKMARK")
        else:
            wrap_width = get_wrap_width_chars(context)
            grouped = defaultdict(list)
            for item in props.validation_results:
                grouped[item.category].append(item)

            for category, items in grouped.items():
                box = layout.box()
                box.label(text=f"{category} ({len(items)})", icon="ERROR")
                for item in items:
                    row = box.row()
                    col = row.column()
                    draw_wrapped_text(col, item.message, wrap_width)
                    if item.target_name:
                        op = row.operator(
                            "quila.select_target", text="", icon="RESTRICT_SELECT_OFF"
                        )
                        op.target_name = item.target_name
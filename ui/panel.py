import bpy
from collections import defaultdict
from .helpers import get_wrap_width_chars, draw_wrapped_text
from ..csv_loader import get_current_assigned_object_name
from ..sop_rules import get_file_mode

def _get_action_icon(action_type):
    """Return nama icon Blender sesuai action_type."""
    icons = {
        "select_object":      "OBJECT_DATA",
        "highlight_collection": "OUTLINER_COLLECTION",
        "open_folder":        "FILE_FOLDER",
        "open_render_folder": "FILE_FOLDER",
        "open_texture_file":  "IMAGE_DATA",
        "open_image_editor":  "IMAGE",
        "open_shader_editor": "MATERIAL",
    }
    return icons.get(action_type, "RIGHTARROW")

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

        filepath = bpy.data.filepath
        is_new_file = not filepath
        mode = None if is_new_file else get_file_mode(filepath)

        layout.label(text="Quila Pipeline Checker")

        dropdown_section = layout.column()
        dropdown_section.enabled = is_new_file
        dropdown_section.prop(props, "tugas_ke")
        dropdown_section.prop(props, "artist_name")

        if not is_new_file and mode == "final":
            layout.label(text="Tugas & Artist terkunci (file sudah final)", icon="LOCKED")
        elif not is_new_file:
            layout.label(text="Tugas & Artist terkunci (file WIP sudah disimpan)", icon="LOCKED")

        object_name = get_current_assigned_object_name(context)
        info_box = layout.box()
        if object_name:
            info_box.label(text=f"Object: {object_name}", icon="OBJECT_DATA")
        else:
            info_box.label(text="Object: (pilih Tugas & Artist dulu)", icon="OBJECT_DATA")

        layout.separator()

        if is_new_file:
            layout.operator("quila.create_project", icon="NEWFOLDER")
        elif mode == "final":
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
                    row = box.row(align=True)
                    col = row.column()
                    col.scale_x = 1.0
                    draw_wrapped_text(col, item.message, wrap_width, bullet=True)

                    if item.action_type and item.target_name:
                        btn = row.operator(
                            "quila.select_target",
                            text="",
                            icon=_get_action_icon(item.action_type),
                        )
                        btn.target_name = item.target_name
                        btn.action_type = item.action_type
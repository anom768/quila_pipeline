import os
import bpy
from ..path_config import get_base_path_for_tugas
from ..csv_loader import get_current_assigned_object_name
from ..sop_rules import REQUIRED_FOLDERS


class QUILA_OT_create_project(bpy.types.Operator):
    """Generate struktur folder project, lalu simpan file ini sebagai WIP pertama"""

    bl_idname = "quila.create_project"
    bl_label = "Create Project"
    bl_description = (
        "buat proyek baru"
    )

    @classmethod
    def poll(cls, context):
        props = context.scene.quila_props
        if props.tugas_ke == "NONE" or props.artist_name == "NONE":
            return False
        return True

    def execute(self, context):
        props = context.scene.quila_props

        object_name = get_current_assigned_object_name(context)
        if not object_name:
            self.report({'ERROR'}, "Object name tidak ditemukan untuk kombinasi Tugas+Artist ini.")
            return {'CANCELLED'}

        base_path = get_base_path_for_tugas(props.tugas_ke)
        if not base_path:
            self.report(
                {'ERROR'},
                f"Path untuk Tugas {props.tugas_ke} belum diset di config/paths.json.",
            )
            return {'CANCELLED'}

        if not os.path.isdir(base_path):
            self.report({'ERROR'}, f"Path dasar '{base_path}' tidak ditemukan/tidak bisa diakses.")
            return {'CANCELLED'}

        object_folder = os.path.join(base_path, object_name.upper())

        try:
            os.makedirs(object_folder, exist_ok=True)
            for folder in REQUIRED_FOLDERS:
                os.makedirs(os.path.join(object_folder, folder), exist_ok=True)
        except Exception as e:
            self.report({'ERROR'}, f"Gagal membuat folder: {e}")
            return {'CANCELLED'}

        wip_folder = os.path.join(object_folder, "WIP")
        wip_filename = f"{object_name}_wip01.blend"
        wip_filepath = os.path.join(wip_folder, wip_filename)

        if os.path.isfile(wip_filepath):
            self.report(
                {'WARNING'},
                f"File '{wip_filename}' sudah ada. "
            )
            return {'CANCELLED'}

        bpy.ops.wm.save_as_mainfile(filepath=wip_filepath, check_existing=False)

        self.report({'INFO'}, f"Project berhasil dibuat: {wip_filepath}")
        return {'FINISHED'}
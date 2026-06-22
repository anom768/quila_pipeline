import os
import bpy
from ..sop_rules import FILE_NAME_PATTERN


class QUILA_OT_mark_as_final(bpy.types.Operator):
    """Simpan copy file ini sebagai versi final (hapus suffix _wipXX)"""

    bl_idname = "quila.mark_as_final"
    bl_label = "Mark as Final"
    bl_description = "Simpan salinan file ini sebagai versi final di folder utama object"

    @classmethod
    def poll(cls, context):
        return context.scene.quila_props.is_valid

    def execute(self, context):
        filepath = bpy.data.filepath
        filename = os.path.basename(filepath)
        match = FILE_NAME_PATTERN.match(filename)

        if not match:
            self.report({'ERROR'}, "Nama file WIP tidak sesuai format, tidak bisa di-mark as final.")
            return {'CANCELLED'}

        object_name = match.group("object_name")
        variant = match.group("variant")

        if variant:
            final_filename = f"{object_name}_v{variant}.blend"
        else:
            final_filename = f"{object_name}.blend"

        wip_folder = os.path.dirname(filepath)
        object_folder = os.path.dirname(wip_folder)

        if not os.path.isdir(object_folder):
            self.report({'ERROR'}, f"Folder utama object '{object_folder}' tidak ditemukan.")
            return {'CANCELLED'}

        final_path = os.path.join(object_folder, final_filename)

        bpy.ops.wm.save_as_mainfile(
            filepath=final_path,
            copy=True,
            check_existing=False,
        )

        self.report({'INFO'}, f"File final disimpan: {final_filename}")

        return {'FINISHED'}

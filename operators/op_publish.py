import os
import bpy
from ..validators import run_all
from ..sop_rules import FILE_NAME_PATTERN, get_file_mode
from ..csv_loader import is_csv_ready


class QUILA_OT_publish(bpy.types.Operator):
    """Jalankan semua validasi SOP; kalau lolos, buat file final"""

    bl_idname = "quila.publish"
    bl_label = "Publish"
    bl_description = "Jalankan semua pengecekan SOP (hanya bisa dijalankan di Object Mode)"

    @classmethod
    def poll(cls, context):
        """Tombol aktif hanya kalau:
        - Sedang di Object Mode (bukan Edit Mode atau mode lain)
        - CSV siap
        - Tugas + Artist sudah dipilih
        """
        try:
            if context.mode != 'OBJECT':
                return False

            if not is_csv_ready(context):
                return False

            props = context.scene.quila_props
            if props.tugas_ke == "NONE" or props.artist_name == "NONE":
                return False

            return True
        except Exception:
            return False

    def execute(self, context):
        props = context.scene.quila_props

        issues = run_all(context)

        props.validation_results.clear()
        for issue in issues:
            item = props.validation_results.add()
            item.category = issue.category
            item.message = issue.message
            item.target_name = issue.target_name

        props.is_valid = (len(issues) == 0)
        props.has_been_checked = True

        if not props.is_valid:
            self.report({'ERROR'}, f"Ditemukan {len(issues)} masalah. Publish dibatalkan.")
            return {'FINISHED'}

        return self._create_final_file(context)

    def _create_final_file(self, context):
        filepath = bpy.data.filepath
        mode = get_file_mode(filepath)

        if mode == "final":
            self.report(
                {'INFO'},
                "Semua pengecekan lolos!"
            )
            return {'FINISHED'}

        filename = os.path.basename(filepath)
        match = FILE_NAME_PATTERN.match(filename)

        if not match:
            self.report({'ERROR'}, "Nama file tidak sesuai format, tidak bisa publish.")
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

        # Simpan file WIP yang sedang aktif terlebih dahulu
        bpy.ops.wm.save_mainfile()

        # Buat salinan file final (copy=True: active file tetap menunjuk ke WIP)
        bpy.ops.wm.save_as_mainfile(
            filepath=final_path,
            copy=True,
            check_existing=False,
        )

        self.report({'INFO'}, f"Semua pengecekan lolos! File final disimpan: {final_filename}")
        return {'FINISHED'}

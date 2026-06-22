import bpy
from ..validators import run_all


class QUILA_OT_check_all(bpy.types.Operator):
    """Jalankan semua validator SOP dan tampilkan hasilnya di Panel"""

    bl_idname = "quila.check_all"
    bl_label = "Check"
    bl_description = "Jalankan semua pengecekan SOP (naming, folder, mesh, dll)"

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

        if props.is_valid:
            self.report({'INFO'}, "Semua pengecekan lolos! File sudah sesuai SOP.")
        else:
            self.report({'ERROR'}, f"Ditemukan {len(issues)} masalah. Lihat detail di panel.")

        return {'FINISHED'}
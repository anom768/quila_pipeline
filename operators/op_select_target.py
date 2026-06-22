import bpy


class QUILA_OT_select_target(bpy.types.Operator):
    """Pilih & fokus ke object yang disebut di salah satu hasil error"""

    bl_idname = "quila.select_target"
    bl_label = "Select Object"
    bl_description = "Pilih dan fokus ke object yang bermasalah"

    target_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.data.objects.get(self.target_name)

        if obj is None:
            self.report(
                {'WARNING'},
                f"'{self.target_name}' bukan nama object di scene, tidak bisa di-select.",
            )
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                region = next(
                    (r for r in area.regions if r.type == 'WINDOW'), None
                )
                if region is None:
                    continue
                with context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected()
                break

        self.report({'INFO'}, f"Object '{self.target_name}' dipilih.")
        return {'FINISHED'}

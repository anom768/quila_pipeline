import bpy


class QuilaAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    csv_path: bpy.props.StringProperty(
        name="CSV Daftar Tugas",
        description="Lokasi file CSV berisi daftar student dan object_name yang ditugaskan",
        subtype="FILE_PATH",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "csv_path")
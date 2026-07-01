import os
import subprocess
import bpy


class QUILA_OT_select_target(bpy.types.Operator):
    """Aksi navigasi/select sesuai jenis error"""

    bl_idname = "quila.select_target"
    bl_label = "Select"
    bl_description = "Navigasi ke lokasi atau object yang bermasalah"

    target_name: bpy.props.StringProperty()
    action_type: bpy.props.StringProperty()

    def execute(self, context):
        action = self.action_type
        target = self.target_name

        if not action or not target:
            self.report({'WARNING'}, "Tidak ada aksi yang bisa dijalankan untuk error ini.")
            return {'CANCELLED'}

        if action == "select_object":
            return self._select_object(context, target)
        elif action == "highlight_collection":
            return self._highlight_collection(context, target)
        elif action == "open_folder":
            return self._open_folder(target)
        elif action == "open_render_folder":
            return self._open_folder(target)
        elif action == "open_texture_file":
            return self._open_file_in_explorer(target)
        elif action == "open_image_editor":
            return self._open_image_editor(context, target)
        elif action == "open_shader_editor":
            return self._open_shader_editor(context, target)
        else:
            self.report({'WARNING'}, f"Action type '{action}' tidak dikenal.")
            return {'CANCELLED'}

    # ------------------------------------------------------------------ #
    # SELECT OBJECT
    # ------------------------------------------------------------------ #

    def _select_object(self, context, obj_name):
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            self.report({'WARNING'}, f"Object '{obj_name}' tidak ditemukan di scene.")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                region = next((r for r in area.regions if r.type == 'WINDOW'), None)
                if region:
                    with context.temp_override(area=area, region=region):
                        bpy.ops.view3d.view_selected()
                break

        self.report({'INFO'}, f"Object '{obj_name}' dipilih.")
        return {'FINISHED'}

    # ------------------------------------------------------------------ #
    # HIGHLIGHT COLLECTION DI OUTLINER
    # ------------------------------------------------------------------ #

    def _highlight_collection(self, context, col_name):
        col = bpy.data.collections.get(col_name)
        if col is None:
            self.report({'WARNING'}, f"Collection '{col_name}' tidak ditemukan.")
            return {'CANCELLED'}

        # Set active layer collection di view layer supaya collection ter-highlight
        def find_layer_collection(layer_col, name):
            if layer_col.name == name:
                return layer_col
            for child in layer_col.children:
                result = find_layer_collection(child, name)
                if result:
                    return result
            return None

        lc = find_layer_collection(context.view_layer.layer_collection, col_name)
        if lc:
            context.view_layer.active_layer_collection = lc
            self.report({'INFO'}, f"Collection '{col_name}' di-highlight di Outliner.")
        else:
            self.report({'WARNING'}, f"Collection '{col_name}' tidak ditemukan di layer collection.")
            return {'CANCELLED'}

        return {'FINISHED'}

    # ------------------------------------------------------------------ #
    # BUKA FILE EXPLORER KE FOLDER
    # ------------------------------------------------------------------ #

    def _open_folder(self, folder_path):
        if not os.path.isdir(folder_path):
            self.report({'WARNING'}, f"Folder '{folder_path}' tidak ditemukan.")
            return {'CANCELLED'}

        try:
            # Windows: explorer langsung ke folder
            os.startfile(folder_path)
        except Exception as e:
            self.report({'ERROR'}, f"Gagal membuka folder: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Membuka folder: {folder_path}")
        return {'FINISHED'}

    # ------------------------------------------------------------------ #
    # BUKA FILE EXPLORER DAN SOROT FILE TERTENTU
    # ------------------------------------------------------------------ #

    def _open_file_in_explorer(self, file_path):
        abs_path = bpy.path.abspath(file_path)

        if not os.path.isfile(abs_path):
            # File tidak ada — buka folder induknya saja
            folder = os.path.dirname(abs_path)
            if os.path.isdir(folder):
                try:
                    os.startfile(folder)
                    self.report({'WARNING'}, f"File tidak ditemukan, membuka folder: {folder}")
                except Exception as e:
                    self.report({'ERROR'}, f"Gagal membuka folder: {e}")
                    return {'CANCELLED'}
            else:
                self.report({'WARNING'}, f"File dan foldernya tidak ditemukan: {abs_path}")
                return {'CANCELLED'}
        else:
            try:
                # /select, membuat Explorer menyorot (highlight) file itu
                subprocess.Popen(f'explorer /select,"{abs_path}"')
            except Exception as e:
                self.report({'ERROR'}, f"Gagal membuka file explorer: {e}")
                return {'CANCELLED'}

            self.report({'INFO'}, f"Membuka file explorer ke: {abs_path}")

        return {'FINISHED'}

    # ------------------------------------------------------------------ #
    # BUKA IMAGE EDITOR DAN TAMPILKAN IMAGE
    # ------------------------------------------------------------------ #

    def _open_image_editor(self, context, img_name):
        img = bpy.data.images.get(img_name)
        if img is None:
            self.report({'WARNING'}, f"Image '{img_name}' tidak ditemukan di Blender.")
            return {'CANCELLED'}

        # Cari area yang sudah Image Editor, pakai itu duluan
        target_area = None
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                target_area = area
                break

        # Kalau tidak ada, cari area VIEW_3D dan ubah jadi IMAGE_EDITOR
        if target_area is None:
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    target_area = area
                    break

        if target_area is None:
            self.report({'WARNING'}, "Tidak ada area yang bisa dipakai untuk Image Editor.")
            return {'CANCELLED'}

        target_area.type = 'IMAGE_EDITOR'
        target_area.spaces.active.image = img

        self.report({'INFO'}, f"Image '{img_name}' ditampilkan di Image Editor.")
        return {'FINISHED'}

    # ------------------------------------------------------------------ #
    # BUKA SHADER EDITOR DAN SET MATERIAL AKTIF
    # ------------------------------------------------------------------ #

    def _open_shader_editor(self, context, mat_name):
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            self.report({'WARNING'}, f"Material '{mat_name}' tidak ditemukan.")
            return {'CANCELLED'}

        # Cari object yang punya material ini, set sebagai active
        owner_obj = None
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material and slot.material.name == mat_name:
                        owner_obj = obj
                        break
            if owner_obj:
                break

        if owner_obj:
            bpy.ops.object.select_all(action='DESELECT')
            owner_obj.select_set(True)
            context.view_layer.objects.active = owner_obj
            # Set slot material yang sesuai sebagai aktif
            for i, slot in enumerate(owner_obj.material_slots):
                if slot.material and slot.material.name == mat_name:
                    owner_obj.active_material_index = i
                    break

        # Cari area Shader Editor, atau ubah area yang ada
        target_area = None
        for area in context.screen.areas:
            if area.type == 'NODE_EDITOR':
                space = area.spaces.active
                if hasattr(space, 'shader_type'):
                    target_area = area
                    break

        if target_area is None:
            for area in context.screen.areas:
                if area.type not in {'VIEW_3D', 'PROPERTIES', 'OUTLINER'}:
                    target_area = area
                    break

        if target_area:
            target_area.type = 'NODE_EDITOR'
            space = target_area.spaces.active
            space.tree_type = 'ShaderNodeTree'
            space.shader_type = 'OBJECT'

        self.report({'INFO'}, f"Material '{mat_name}' dibuka di Shader Editor.")
        return {'FINISHED'}
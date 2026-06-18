bl_info = {
    "name": "Quila Pipeline",
    "author": "Bangkit Anom Sedhayu | bangkitunom87@gmail.com",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar (N-Panel) > Quila",
    "description": "Pipeline checker untuk standarisasi naming & struktur file Blender",
    "category": "Pipeline",
}


def register():
    print("Quila Pipeline: addon berhasil di-enable")


def unregister():
    print("Quila Pipeline: addon di-disable")
import bmesh
import bpy
from . import Issue


def _has_ngon(bm):
    return any(len(face.verts) > 4 for face in bm.faces)


def _signed_volume(bm):
    """Hitung signed volume mesh untuk deteksi flipped normals.
    Mesh tertutup (manifold) dengan normal yang benar (mengarah keluar)
    akan menghasilkan volume positif. Volume negatif mengindikasikan
    kemungkinan normal yang terbalik."""
    volume = 0.0
    for face in bm.faces:
        verts = face.verts
        if len(verts) < 3:
            continue
        v0 = verts[0].co
        for i in range(1, len(verts) - 1):
            v1 = verts[i].co
            v2 = verts[i + 1].co
            volume += v0.dot(v1.cross(v2)) / 6.0
    return volume


def validate(context):
    issues = []

    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        if _has_ngon(bm):
            issues.append(Issue(
                category="Mesh Rules",
                message=f"Object '{obj.name}' memiliki n-gon (face dengan lebih dari 4 sisi).",
                target_name=obj.name,
                action_type="select_object",
            ))

        if _signed_volume(bm) < 0:
            issues.append(Issue(
                category="Mesh Rules",
                message=f"Object '{obj.name}' terdeteksi memiliki normal yang terbalik (flipped).",
                target_name=obj.name,
                action_type="select_object",
            ))

        bm.free()

    return issues
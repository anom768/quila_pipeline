import os
import re
import bpy
from ..sop_rules import TEXTURE_NAME_PATTERN, get_file_mode
from .issue import Issue


_BLENDER_DUPLICATE_SUFFIX = re.compile(r"\.\d{3}$")

_IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".tga", ".bmp",
    ".tiff", ".tif", ".exr", ".gif", ".webp",
}


def _has_image_extension(name):
    _, ext = os.path.splitext(name)
    return ext.lower() in _IMAGE_EXTENSIONS


def _get_expected_texture_folder():
    """Return path folder TEXTURE project ini berdasarkan lokasi file .blend aktif.
    Return None kalau file belum disimpan."""
    filepath = bpy.data.filepath
    if not filepath:
        return None

    mode = get_file_mode(filepath)
    current_folder = os.path.dirname(filepath)
    object_folder = os.path.dirname(current_folder) if mode == "wip" else current_folder
    return os.path.normpath(os.path.join(object_folder, "TEXTURE"))


def _check_internal_name_format(img, expected_basename):
    """Cek nama internal Blender (img.name):
    1. Tidak boleh mengandung ekstensi file
    2. Harus sama dengan nama file di disk (kalau expected_basename diisi)

    Return (issues, cleaned_name, has_extension_issue)."""
    issues = []
    cleaned_name = _BLENDER_DUPLICATE_SUFFIX.sub("", img.name)
    has_extension_issue = _has_image_extension(cleaned_name)

    if has_extension_issue:
        issues.append(Issue(
            category="Texture Naming",
            message=(
                f"Nama image '{img.name}' di Blender tidak boleh mengandung "
                f"ekstensi file (.png/.jpg/dst). Rename tanpa ekstensi."
            ),
            target_name=img.name,
            action_type="open_image_editor",
        ))
        return issues, cleaned_name, has_extension_issue

    if expected_basename is not None and cleaned_name != expected_basename:
        issues.append(Issue(
            category="Texture Naming",
            message=(
                f"Nama internal texture di Blender ('{img.name}') tidak sama dengan "
                f"nama file di disk ('{expected_basename}'). "
                f"Rename image di Blender agar sama dengan nama file."
            ),
            target_name=img.name,
            action_type="open_image_editor",
        ))

    return issues, cleaned_name, has_extension_issue


def validate(context):
    issues = []
    expected_texture_folder = _get_expected_texture_folder()

    for img in bpy.data.images:
        if img.source == "FILE":
            if not img.filepath:
                continue

            abs_path = bpy.path.abspath(img.filepath)
            filename = os.path.basename(abs_path)
            file_basename = os.path.splitext(filename)[0]

            if not os.path.isfile(abs_path):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"File texture '{filename}' tidak ditemukan di disk. "
                        f"File mungkin sudah dipindah atau di-rename."
                    ),
                    target_name=abs_path,
                    action_type="open_texture_file",
                ))
                continue

            if expected_texture_folder is not None:
                norm_abs = os.path.normpath(abs_path)
                if not norm_abs.startswith(expected_texture_folder + os.sep):
                    issues.append(Issue(
                        category="Texture Naming",
                        message=(
                            f"File texture '{filename}' tidak berada di folder TEXTURE "
                            f"project ini. Pindahkan ke '{expected_texture_folder}'."
                        ),
                        target_name=abs_path,
                        action_type="open_texture_file",
                    ))

            if not TEXTURE_NAME_PATTERN.match(file_basename):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama file texture '{filename}' tidak sesuai format "
                        f"'tex_texture_name_type'."
                    ),
                    target_name=abs_path,
                    action_type="open_texture_file",
                ))

            name_issues, _, _ = _check_internal_name_format(img, file_basename)
            issues.extend(name_issues)

        elif img.source == "GENERATED":
            name_issues, cleaned_name, has_extension_issue = _check_internal_name_format(img, None)
            issues.extend(name_issues)

            if not has_extension_issue and not TEXTURE_NAME_PATTERN.match(cleaned_name):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama image '{img.name}' (generated, tidak dari file disk) "
                        f"tidak sesuai format 'tex_texture_name_type'."
                    ),
                    target_name=img.name,
                    action_type="open_image_editor",
                ))

    # Cek node Image Texture yang tidak punya image
    for mat in bpy.data.materials:
        if not mat.use_nodes or mat.node_tree is None:
            continue
        for node in mat.node_tree.nodes:
            if node.type == "TEX_IMAGE" and node.image is None:
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Node 'Image Texture' di material '{mat.name}' "
                        f"tidak ada image-nya. Assign image atau hapus node tersebut."
                    ),
                    target_name=mat.name,
                    action_type="open_material_properties",
                ))

    return issues

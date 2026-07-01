import os
import re
import bpy
from ..sop_rules import TEXTURE_NAME_PATTERN
from . import Issue


# Suffix duplikat Blender: .001, .002, dst
_BLENDER_DUPLICATE_SUFFIX = re.compile(r"\.\d{3}$")

_IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".tga", ".bmp",
    ".tiff", ".tif", ".exr", ".gif", ".webp",
}


def _has_image_extension(name):
    _, ext = os.path.splitext(name)
    return ext.lower() in _IMAGE_EXTENSIONS


def _get_expected_texture_folder():
    """Return path folder TEXTURE yang seharusnya untuk project ini,
    berdasarkan lokasi file .blend yang sedang aktif.
    Return None kalau filepath belum ada (file belum disimpan)."""
    filepath = bpy.data.filepath
    if not filepath:
        return None

    from ..sop_rules import get_file_mode
    mode = get_file_mode(filepath)
    current_folder = os.path.dirname(filepath)

    if mode == "wip":
        object_folder = os.path.dirname(current_folder)
    else:
        object_folder = current_folder

    return os.path.normpath(os.path.join(object_folder, "TEXTURE"))


def _check_internal_name_format(img, expected_basename_for_compare):
    """Cek nama internal Blender (img.name): tidak boleh mengandung ekstensi,
    lalu (kalau ada nama pembanding) cek kecocokan dengan nama file di disk.

    Return (issues, internal_name, has_extension_issue)."""
    issues = []
    internal_name = _BLENDER_DUPLICATE_SUFFIX.sub("", img.name)
    has_extension_issue = _has_image_extension(internal_name)

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
        return issues, internal_name, has_extension_issue

    if expected_basename_for_compare is not None and internal_name != expected_basename_for_compare:
        issues.append(Issue(
            category="Texture Naming",
            message=(
                f"Nama internal texture di Blender ('{img.name}') tidak sama dengan "
                f"nama file di disk ('{expected_basename_for_compare}'). "
                f"Rename image di Blender agar sama dengan nama file."
            ),
            target_name=img.name,
            action_type="open_image_editor",
        ))

    return issues, internal_name, has_extension_issue


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
                        f"File texture '{filename}' tidak ditemukan di disk "
                        f"(path: '{abs_path}'). File mungkin sudah dipindah atau di-rename."
                    ),
                    target_name=img.name,
                    action_type="open_texture_file",
                ))
                continue

            # Cek apakah file berasal dari folder TEXTURE project ini
            if expected_texture_folder is not None:
                norm_abs = os.path.normpath(abs_path)
                if not norm_abs.startswith(expected_texture_folder + os.sep):
                    issues.append(Issue(
                        category="Texture Naming",
                        message=(
                            f"File texture '{filename}' tidak berada di folder TEXTURE "
                            f"project ini ('{expected_texture_folder}'). "
                            f"Pindahkan file ke folder TEXTURE yang benar."
                        ),
                        target_name=img.name,
                        action_type="open_texture_file",
                    ))

            if not TEXTURE_NAME_PATTERN.match(file_basename):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama file texture '{filename}' tidak sesuai format "
                        f"'tex_texture_name_type'."
                    ),
                    target_name=img.name,
                    action_type="open_texture_file",
                ))

            name_issues, _, _ = _check_internal_name_format(img, file_basename)
            issues.extend(name_issues)

        elif img.source == "GENERATED":
            name_issues, internal_name, has_extension_issue = _check_internal_name_format(img, None)
            issues.extend(name_issues)

            if not has_extension_issue and not TEXTURE_NAME_PATTERN.match(internal_name):
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
                ))

    return issues
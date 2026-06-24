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
        ))

    return issues, internal_name, has_extension_issue


def validate(context):
    issues = []

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
                ))
                continue

            if not TEXTURE_NAME_PATTERN.match(file_basename):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama file texture '{filename}' tidak sesuai format "
                        f"'tex_texture_name_type'."
                    ),
                    target_name=img.name,
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
                ))

    return issues
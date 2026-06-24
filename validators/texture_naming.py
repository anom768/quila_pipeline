import os
import re
import bpy
from ..sop_rules import TEXTURE_NAME_PATTERN
from . import Issue


# Suffix duplikat Blender: .001, .002, dst
_BLENDER_DUPLICATE_SUFFIX = re.compile(r"\.\d{3}$")


def validate(context):
    issues = []

    for img in bpy.data.images:
        # Skip generated image — tidak relevan untuk validasi SOP file naming
        if img.source != "FILE":
            continue

        if not img.filepath:
            continue

        # Resolve path relative Blender ke absolute path di disk
        abs_path = bpy.path.abspath(img.filepath)
        filename = os.path.basename(abs_path)
        file_basename = os.path.splitext(filename)[0]

        # Cek apakah file benar-benar ada di disk
        if not os.path.isfile(abs_path):
            issues.append(Issue(
                category="Texture Naming",
                message=(
                    f"File texture '{filename}' tidak ditemukan di disk "
                    f"(path: '{abs_path}'). File mungkin sudah dipindah atau di-rename."
                ),
                target_name=img.name,
            ))
            # Tidak lanjut validasi nama kalau file sudah tidak ada
            continue

        # Cek format nama file
        if not TEXTURE_NAME_PATTERN.match(file_basename):
            issues.append(Issue(
                category="Texture Naming",
                message=(
                    f"Nama file texture '{filename}' tidak sesuai format "
                    f"'tex_texture_name_type'."
                ),
                target_name=img.name,
            ))

        # Cek nama internal Blender vs nama file disk
        # Strip suffix duplikat Blender (.001, .002, dst) sebelum bandingkan
        internal_name = _BLENDER_DUPLICATE_SUFFIX.sub("", img.name)
        if internal_name != file_basename:
            issues.append(Issue(
                category="Texture Naming",
                message=(
                    f"Nama internal texture di Blender ('{img.name}') tidak sama dengan "
                    f"nama file di disk ('{file_basename}'). "
                    f"Rename image di Blender agar sama dengan nama file."
                ),
                target_name=img.name,
            ))

    return issues
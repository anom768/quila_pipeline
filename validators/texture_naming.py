import os
import bpy
from ..sop_rules import TEXTURE_NAME_PATTERN
from . import Issue


def validate(context):
    issues = []

    for img in bpy.data.images:
        if img.source == "FILE" and img.filepath:
            filename = os.path.basename(img.filepath)
            file_basename = os.path.splitext(filename)[0]

            if not TEXTURE_NAME_PATTERN.match(file_basename):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama file texture '{filename}' tidak sesuai format "
                        f"'tex_texture_name_type'."
                    ),
                    target_name=img.name,
                ))

            if img.name not in (filename, file_basename):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama internal texture di Blender ('{img.name}') tidak sama dengan "
                        f"nama file di disk ('{filename}')."
                    ),
                    target_name=img.name,
                ))

        elif img.source == "GENERATED":
            if not TEXTURE_NAME_PATTERN.match(img.name):
                issues.append(Issue(
                    category="Texture Naming",
                    message=(
                        f"Nama image '{img.name}' (generated, tidak dari file disk) "
                        f"tidak sesuai format 'tex_texture_name_type'."
                    ),
                    target_name=img.name,
                ))

    return issues
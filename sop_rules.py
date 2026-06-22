import os
import re


# ===== File Naming =====
# Format WIP: [object_name]_(variantxx)_[wipxx].blend
FILE_NAME_PATTERN = re.compile(
    r"^(?P<object_name>[a-z0-9]+(?:_[a-z0-9]+)*)"
    r"(?:_v(?P<variant>\d{2}))?"
    r"_wip(?P<wip>\d{2})"
    r"\.blend$"
)

# Format Final (tanpa _wipxx) — dipakai nanti di Fase 6
FINAL_FILE_NAME_PATTERN = re.compile(
    r"^(?P<object_name>[a-z0-9]+(?:_[a-z0-9]+)*)"
    r"(?:_v(?P<variant>\d{2}))?"
    r"\.blend$"
)

# ===== Folder Structure =====
REQUIRED_FOLDERS = ["REF", "WIP", "RENDER", "TEXTURE", "EXPORT"]

# ===== Object Naming =====
OBJECT_NAME_PATTERN = re.compile(r"^geo_[a-z0-9]+(?:_[a-z0-9]+)*$")

# ===== Material Naming =====
MATERIAL_NAME_PATTERN = re.compile(r"^shd_[a-z0-9]+(?:_[a-z0-9]+)*$")

# ===== Texture Naming =====
TEXTURE_TYPES = ["basecolor", "normal", "metal", "roughness", "height", "opacity", "ao", "emissive"]
TEXTURE_NAME_PATTERN = re.compile(
    r"^tex_[a-z0-9]+(?:_[a-z0-9]+)*_(" + "|".join(TEXTURE_TYPES) + r")$"
)

# ===== Render Naming =====
RENDER_NAME_PATTERN = re.compile(
    r"^[a-z0-9]+(?:_[a-z0-9]+)*(?:_v\d{2})?_prev\d{2}$"
)

# ===== Collection Khusus =====
LGT_CAM_COLLECTION_NAME = "lgt&cam"


def get_expected_object_name(filepath):
    """Ambil object_name (+ variant kalau ada) dari nama file WIP.
    Dipakai untuk mencocokkan nama collection & render.
    Return None kalau filename tidak sesuai format."""
    if not filepath:
        return None

    filename = os.path.basename(filepath)
    match = FILE_NAME_PATTERN.match(filename)

    if not match:
        return None

    object_name = match.group("object_name")
    variant = match.group("variant")

    if variant:
        return f"{object_name}_v{variant}"
    return object_name
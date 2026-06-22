import bpy
from ..sop_rules import MATERIAL_NAME_PATTERN
from . import Issue


def validate(context):
    issues = []

    for mat in bpy.data.materials:
        if not MATERIAL_NAME_PATTERN.match(mat.name):
            issues.append(Issue(
                category="Material Naming",
                message=f"Nama material '{mat.name}' tidak sesuai format 'shd_shader_name'.",
                target_name=mat.name,
            ))

    return issues
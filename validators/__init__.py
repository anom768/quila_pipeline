from dataclasses import dataclass


@dataclass
class Issue:
    category: str
    message: str
    target_name: str = ""
    action_type: str = ""


from . import file_naming
from . import folder_structure
from . import collection_naming
from . import object_naming
from . import mesh_rules
from . import material_naming
from . import texture_naming
from . import render_naming


VALIDATORS = (
    file_naming,
    folder_structure,
    collection_naming,
    object_naming,
    mesh_rules,
    material_naming,
    texture_naming,
    render_naming
)


def run_all(context):
    """Jalankan semua validator berurutan, ambil hanya 1 issue pertama per validator.
    Tujuannya supaya student fokus memperbaiki satu masalah per kategori per klik,
    tidak overwhelmed dengan semua error sekaligus."""
    all_issues = []
    for validator_module in VALIDATORS:
        issues = validator_module.validate(context)
        if issues:
            all_issues.append(issues[0])
    return all_issues
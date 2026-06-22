from dataclasses import dataclass


@dataclass
class Issue:
    category: str
    message: str
    target_name: str = ""


from . import file_naming
from . import folder_structure


VALIDATORS = (
    file_naming,
    folder_structure
)


def run_all(context):
    """Jalankan semua validator berurutan, kumpulkan semua Issue jadi satu list."""
    all_issues = []
    for validator_module in VALIDATORS:
        issues = validator_module.validate(context)
        all_issues.extend(issues)
    return all_issues
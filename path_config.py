import json
import os


def get_config_folder():
    """Path folder config/ di dalam folder addon ini sendiri."""
    addon_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(addon_root, "config")


def get_paths_json_path():
    return os.path.join(get_config_folder(), "paths.json")


def load_task_paths():
    """Baca config/paths.json. Return dict {'tugas1': 'path', ...}, kosong kalau error/tidak ada."""
    path = get_paths_json_path()

    if not os.path.isfile(path):
        return {}

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Quila Pipeline: gagal membaca paths.json - {e}")
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def get_base_path_for_tugas(tugas_ke):
    """tugas_ke adalah string angka (misal '1', '2'), sesuai nilai EnumProperty.
    Return path string, atau None kalau tidak ketemu."""
    paths = load_task_paths()
    key = f"tugas{tugas_ke}"
    return paths.get(key)
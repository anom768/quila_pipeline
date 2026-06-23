import csv
import os
import bpy
import re


TASK_CSV_PATTERN = re.compile(r"^csv_tugas(\d+)\.csv$", re.IGNORECASE)


def get_addon_preferences(context):
    """Ambil AddonPreferences milik addon ini, untuk akses csv_path"""
    return context.preferences.addons[__package__].preferences


def load_csv_data(context):
    """Baca file CSV dari path di Addon Preferences.
    Return list of dict (satu dict per baris). Kosong kalau file tidak ada/error."""
    prefs = get_addon_preferences(context)
    path = prefs.csv_path

    if not path or not os.path.isfile(path):
        return []

    rows = []
    try:
        # encoding "utf-8-sig" dipakai karena file CSV hasil export dari
        # Excel/Google Sheets di Windows sering menyisipkan karakter BOM
        # tersembunyi di awal file, yang bisa membuat header kolom pertama
        # terbaca salah kalau pakai encoding "utf-8" biasa.
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Quila Pipeline: gagal membaca CSV - {e}")
        return []

    return rows


def get_student_names(context):
    """Return daftar nama student unik dari CSV, terurut alfabet"""
    rows = load_csv_data(context)
    names = sorted({
        row["student_name"].strip()
        for row in rows
        if row.get("student_name")
    })
    return names


def get_tasks_for_student(context, student_name):
    """Return daftar object_name yang ditugaskan ke student tertentu"""
    rows = load_csv_data(context)
    return [
        row["object_name"].strip()
        for row in rows
        if row.get("student_name", "").strip() == student_name
    ]


_student_enum_cache = []


def get_student_enum_items(self, context):
    """Callback untuk EnumProperty: generate pilihan dropdown dari CSV.
    Hasilnya disimpan di variable global supaya tidak hilang dari memori
    (lihat catatan gotcha di bagian Konsep)."""
    global _student_enum_cache

    names = get_student_names(context)

    if not names:
        _student_enum_cache = [("NONE", "(CSV belum diset / kosong)", "")]
    else:
        _student_enum_cache = [(name, name, "") for name in names]

    return _student_enum_cache

def get_csv_folder():
    """Path folder csv/ yang berada di dalam folder addon ini sendiri."""
    addon_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(addon_root, "csv")


def discover_task_csv_files():
    """Cari semua file csv_tugasN.csv di folder csv/ milik addon.
    Return list of tuple (nomor_tugas, filepath), terurut dari nomor terkecil."""
    folder = get_csv_folder()

    if not os.path.isdir(folder):
        return []

    found = []
    for filename in os.listdir(folder):
        match = TASK_CSV_PATTERN.match(filename)
        if match:
            tugas_number = int(match.group(1))
            found.append((tugas_number, os.path.join(folder, filename)))

    found.sort(key=lambda item: item[0])
    return found


def load_task_csv(filepath):
    """Baca satu file CSV tugas tertentu.
    Return list of dict {'artist': ..., 'object_name': ...}."""
    if not filepath or not os.path.isfile(filepath):
        return []

    rows = []
    try:
        with open(filepath, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Quila Pipeline: gagal membaca CSV '{filepath}' - {e}")
        return []

    return rows


def get_artist_names(filepath):
    """Return daftar nama artist unik dari satu file CSV tugas, terurut alfabet."""
    rows = load_task_csv(filepath)
    names = sorted({
        row["artist"].strip()
        for row in rows
        if row.get("artist") and row["artist"].strip()
    })
    return names


def get_object_name_for_artist(filepath, artist_name):
    """Cari object_name yang ditugaskan ke artist tertentu, di file CSV tugas ini.
    Return string object_name, atau None kalau tidak ketemu."""
    rows = load_task_csv(filepath)
    for row in rows:
        if row.get("artist", "").strip() == artist_name:
            object_name = row.get("object_name", "").strip()
            if object_name:
                return object_name
    return None
import csv
import os
import re
import time
import bpy


# Format single: csv_tugasX_name.csv
# Format group:  csv_tugasX_name_group.csv
# Cek group DULU supaya tidak tertangkap pattern single
_GROUP_PATTERN = re.compile(r"^csv_tugas(\d+)_(.+)_group\.csv$", re.IGNORECASE)
_SINGLE_PATTERN = re.compile(r"^csv_tugas(\d+)_(.+)\.csv$", re.IGNORECASE)

_tugas_enum_cache = []
_artist_enum_cache = []

# Cache discover_task_csv_files — hindari os.listdir berulang setiap frame UI
_discover_cache = None
_discover_cache_time = 0.0
_DISCOVER_CACHE_TTL = 5.0  # detik


# ================================================================ #
# FOLDER CSV
# ================================================================ #

def get_csv_folder():
    """Path folder csv/ di dalam folder addon ini sendiri."""
    addon_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(addon_root, "csv")


# ================================================================ #
# DISCOVER & LOAD
# ================================================================ #

def discover_task_csv_files():
    """Cari semua file CSV tugas di folder csv/.
    Return list of tuple: (nomor_tugas, materi_label, filepath, is_group)
    Terurut berdasarkan nomor tugas terkecil.

    Hasil di-cache selama 5 detik untuk menghindari os.listdir() berlebihan
    saat UI Blender digambar ulang setiap frame."""
    global _discover_cache, _discover_cache_time

    now = time.monotonic()
    if _discover_cache is not None and (now - _discover_cache_time) < _DISCOVER_CACHE_TTL:
        return _discover_cache

    folder = get_csv_folder()
    found = []

    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            match = _GROUP_PATTERN.match(filename)
            if match:
                number = int(match.group(1))
                label = match.group(2).replace("_", " ").title()
                found.append((number, label, os.path.join(folder, filename), True))
                continue

            match = _SINGLE_PATTERN.match(filename)
            if match:
                number = int(match.group(1))
                label = match.group(2).replace("_", " ").title()
                found.append((number, label, os.path.join(folder, filename), False))

        found.sort(key=lambda item: item[0])

    _discover_cache = found
    _discover_cache_time = now
    return _discover_cache


def load_task_csv(filepath):
    """Baca satu file CSV. Return list of dict."""
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


def _get_file_info(tugas_ke):
    """Helper: ambil (filepath, is_group) untuk tugas_ke yang dipilih.
    Return (None, None) kalau tidak ketemu."""
    files = {number: (fp, ig) for number, _, fp, ig in discover_task_csv_files()}
    try:
        return files.get(int(tugas_ke), (None, None))
    except (ValueError, TypeError):
        return None, None


# ================================================================ #
# ARTIST NAMES — Single
# ================================================================ #

def _get_artist_names_single(filepath):
    """Return list nama artist unik dari CSV format single, terurut alfabet."""
    rows = load_task_csv(filepath)
    return sorted({
        row["artist"].strip()
        for row in rows
        if row.get("artist") and row["artist"].strip()
    })


# ================================================================ #
# ARTIST PAIRS — Group
# ================================================================ #

def _get_artist_pairs(filepath):
    """Return list tuple (identifier, label) dari CSV format group.
    identifier = 'artist1|artist2', label = 'Artist1 & Artist2'."""
    rows = load_task_csv(filepath)
    pairs = []
    seen = set()
    for row in rows:
        a1 = row.get("artist1", "").strip()
        a2 = row.get("artist2", "").strip()
        if a1 and a2:
            key = f"{a1}|{a2}"
            if key not in seen:
                seen.add(key)
                pairs.append((key, f"{a1} & {a2}"))
    return pairs


# ================================================================ #
# OBJECT NAME — Single
# ================================================================ #

def _get_object_name_single(filepath, artist_name):
    """Cari object_name untuk artist tertentu di CSV single."""
    rows = load_task_csv(filepath)
    for row in rows:
        if row.get("artist", "").strip() == artist_name:
            return row.get("object_name", "").strip() or None
    return None


# ================================================================ #
# OBJECT NAME — Group
# ================================================================ #

def _get_object_name_group(filepath, artist_identifier):
    """Cari object_name untuk pasangan artist di CSV group.
    artist_identifier format: 'artist1|artist2'."""
    parts = artist_identifier.split("|")
    if len(parts) != 2:
        return None

    a1, a2 = parts[0].strip(), parts[1].strip()
    rows = load_task_csv(filepath)

    for row in rows:
        if row.get("artist1", "").strip() == a1 and row.get("artist2", "").strip() == a2:
            return row.get("object_name", "").strip() or None
    return None


# ================================================================ #
# ENUM ITEMS — Tugas
# ================================================================ #

def get_tugas_enum_items(self, context):
    """Callback EnumProperty dropdown Tugas.
    Label: 'Tugas X - Name Materi' (+ ' [Group]' kalau format group)."""
    global _tugas_enum_cache

    files = discover_task_csv_files()

    if not files:
        _tugas_enum_cache = [("NONE", "(Tidak ada file CSV tugas)", "")]
    else:
        _tugas_enum_cache = [("NONE", "-- Pilih Tugas --", "")] + [
            (
                str(number),
                f"Tugas {number} - {label}" + (" [Group]" if is_group else ""),
                "",
            )
            for number, label, _, is_group in files
        ]

    return _tugas_enum_cache


# ================================================================ #
# ENUM ITEMS — Artist
# ================================================================ #

def get_artist_enum_items(self, context):
    """Callback EnumProperty dropdown Artist.
    Format single: nama satu-satu.
    Format group: nama pasangan 'Artist1 & Artist2'."""
    global _artist_enum_cache

    filepath, is_group = _get_file_info(self.tugas_ke)

    if not filepath:
        _artist_enum_cache = [("NONE", "(Pilih Tugas dulu)", "")]
        return _artist_enum_cache

    if is_group:
        pairs = _get_artist_pairs(filepath)
        if not pairs:
            _artist_enum_cache = [("NONE", "(CSV group kosong)", "")]
        else:
            _artist_enum_cache = [("NONE", "-- Pilih Group --", "")] + [
                (identifier, label, "") for identifier, label in pairs
            ]
    else:
        names = _get_artist_names_single(filepath)
        if not names:
            _artist_enum_cache = [("NONE", "(CSV kosong)", "")]
        else:
            _artist_enum_cache = [("NONE", "-- Pilih Artist --", "")] + [
                (name, name, "") for name in names
            ]

    return _artist_enum_cache


# ================================================================ #
# GET SELECTED CSV PATH
# ================================================================ #

def get_selected_csv_path(context):
    """Return filepath CSV sesuai dropdown Tugas yang dipilih."""
    filepath, _ = _get_file_info(context.scene.quila_props.tugas_ke)
    return filepath


# ================================================================ #
# GET ASSIGNED OBJECT NAME
# ================================================================ #

def get_current_assigned_object_name(context):
    """Return object_name hasil kombinasi Tugas+Artist yang dipilih.
    Menangani format single maupun group secara otomatis."""
    props = context.scene.quila_props

    if props.tugas_ke == "NONE" or props.artist_name == "NONE":
        return None

    filepath, is_group = _get_file_info(props.tugas_ke)
    if not filepath:
        return None

    if is_group:
        return _get_object_name_group(filepath, props.artist_name)
    return _get_object_name_single(filepath, props.artist_name)


# ================================================================ #
# IS CSV READY
# ================================================================ #

def is_csv_ready(context):
    """Return True kalau ada minimal satu CSV tugas yang terbaca dan punya data.
    Dipakai oleh poll() operator untuk enable/disable tombol."""
    files = discover_task_csv_files()
    if not files:
        return False

    for _, _, filepath, _ in files:
        if load_task_csv(filepath):
            return True

    return False

import csv
import os
import bpy
import re


# Format nama file: csv_tugasX_(name_materi).csv
# Contoh: csv_tugas1_kursi_taman.csv, csv_tugas2_meja_makan.csv
TASK_CSV_PATTERN = re.compile(r"^csv_tugas(\d+)_(.+)\.csv$", re.IGNORECASE)
_tugas_enum_cache = []


def get_csv_folder():
    """Path folder csv/ yang berada di dalam folder addon ini sendiri."""
    addon_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(addon_root, "csv")


def discover_task_csv_files():
    """Cari semua file csv_tugasX_(name_materi).csv di folder csv/ milik addon.
    Return list of tuple (nomor_tugas, label_materi, filepath), terurut dari nomor terkecil.

    Contoh: csv_tugas1_kursi_taman.csv
    → (1, 'Kursi Taman', '/path/csv_tugas1_kursi_taman.csv')
    """
    folder = get_csv_folder()

    if not os.path.isdir(folder):
        return []

    found = []
    for filename in os.listdir(folder):
        match = TASK_CSV_PATTERN.match(filename)
        if match:
            tugas_number = int(match.group(1))
            # Ubah underscore jadi spasi, capitalize tiap kata untuk label dropdown
            materi_raw = match.group(2)
            materi_label = materi_raw.replace("_", " ").title()
            found.append((tugas_number, materi_label, os.path.join(folder, filename)))

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


def get_tugas_enum_items(self, context):
    """Callback EnumProperty: daftar pilihan dropdown Tugas.
    Label: 'Tugas X - Name Materi' (dari nama file csv_tugasX_(name_materi).csv)."""
    global _tugas_enum_cache

    files = discover_task_csv_files()

    if not files:
        _tugas_enum_cache = [("NONE", "(Tidak ada file CSV tugas)", "")]
    else:
        _tugas_enum_cache = [("NONE", "-- Pilih Tugas --", "")] + [
            (str(number), f"Tugas {number} - {materi_label}", "")
            for number, materi_label, _ in files
        ]

    return _tugas_enum_cache


_artist_enum_cache = []


def get_artist_enum_items(self, context):
    """Callback EnumProperty: daftar pilihan dropdown Artist,
    tergantung dropdown Tugas (self.tugas_ke) yang sedang dipilih."""
    global _artist_enum_cache

    # Ubah ke dict: {nomor: filepath}
    files = {number: filepath for number, _, filepath in discover_task_csv_files()}

    try:
        selected_tugas = int(self.tugas_ke)
    except (ValueError, TypeError):
        selected_tugas = None

    filepath = files.get(selected_tugas)

    if not filepath:
        _artist_enum_cache = [("NONE", "(Pilih Tugas dulu)", "")]
        return _artist_enum_cache

    names = get_artist_names(filepath)

    if not names:
        _artist_enum_cache = [("NONE", "(CSV kosong)", "")]
    else:
        _artist_enum_cache = [("NONE", "-- Pilih Artist --", "")] + [
            (name, name, "") for name in names
        ]

    return _artist_enum_cache


def get_selected_csv_path(context):
    """Return filepath csv sesuai dropdown Tugas yang sedang dipilih di Scene."""
    props = context.scene.quila_props
    files = {number: filepath for number, _, filepath in discover_task_csv_files()}

    try:
        selected_tugas = int(props.tugas_ke)
    except (ValueError, TypeError):
        return None

    return files.get(selected_tugas)


def get_current_assigned_object_name(context):
    """Return object_name hasil kombinasi Tugas+Artist yang sedang dipilih.
    None kalau salah satu belum dipilih atau tidak ketemu di CSV."""
    props = context.scene.quila_props

    if props.tugas_ke == "NONE":
        return None

    if props.artist_name == "NONE":
        return None

    filepath = get_selected_csv_path(context)

    if not filepath:
        return None

    return get_object_name_for_artist(filepath, props.artist_name)


def is_csv_ready(context):
    """Return True kalau ada minimal satu CSV tugas yang terbaca dan punya data.
    Dipakai oleh poll() operator untuk enable/disable tombol."""
    files = discover_task_csv_files()
    if not files:
        return False

    for _, _, filepath in files:
        rows = load_task_csv(filepath)
        if rows:
            return True

    return False

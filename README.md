# Quila Pipeline

Addon Blender untuk Quila Academy — alat bantu standarisasi naming convention, struktur folder, dan validasi SOP untuk pekerjaan 3D yang dikerjakan student (PKL SMK) di bawah bimbingan mentor.

---

## Daftar Isi

1. [Gambaran Umum](#gambaran-umum)
2. [Instalasi](#instalasi)
3. [Setup Awal (Wajib Sebelum Dipakai)](#setup-awal-wajib-sebelum-dipakai)
4. [Cara Pakai](#cara-pakai)
5. [Struktur Folder Project yang Dihasilkan](#struktur-folder-project-yang-dihasilkan)
6. [Daftar Validasi SOP](#daftar-validasi-sop)
7. [Tombol Select Target](#tombol-select-target)
8. [Struktur Kode Addon](#struktur-kode-addon)
9. [Keterbatasan yang Diketahui](#keterbatasan-yang-diketahui)
10. [Troubleshooting](#troubleshooting)
11. [Riwayat Pengembangan](#riwayat-pengembangan)

---

## Gambaran Umum

Quila Pipeline membantu mentor menjaga konsistensi pekerjaan 3D student tanpa harus mengecek manual satu per satu. Addon ini menyediakan:

- **Generate struktur folder otomatis** sesuai SOP, langsung dari kombinasi Tugas + Artist yang dipilih
- **8 kategori validasi otomatis**: naming file, struktur folder, collection, object, mesh (n-gon/flipped normal), material, texture, dan render
- **Satu tombol kerja** yang berubah sesuai konteks: *Create Project* → *Publish* → *Check SOP*
- **Tombol Select Target** di setiap baris error — navigasi langsung ke object, folder, material, atau image yang bermasalah
- **Dua format tugas**: single artist per object, atau group (2 artist per object)
- **Sumber data terpusat**: daftar tugas (CSV) dan lokasi penyimpanan project (JSON) disimpan di dalam folder addon sendiri, otomatis terbaca tanpa setting manual berulang di tiap PC

---

## Instalasi

1. Salin seluruh folder `quila_pipeline/` ke folder addon Blender:
   ```
   %APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\
   ```
   (atau ke folder `addons/` di lokasi `BLENDER_USER_SCRIPTS` kalau dipasang dari server lab)
2. Buka Blender → **Edit > Preferences > Add-ons** → cari "Quila Pipeline" → centang untuk mengaktifkan
3. Buka N-Panel (tekan `N` di viewport 3D) → tab **Quila** akan muncul

---

## Setup Awal (Wajib Sebelum Dipakai)

Addon ini **tidak akan berfungsi dengan benar** sampai dua file konfigurasi berikut disiapkan oleh mentor/admin:

### 1. `csv/` — Daftar Tugas per Artist

Buat satu file CSV per batch tugas, ditaruh di `quila_pipeline/csv/`. Ada **dua format** yang didukung:

#### Format Single (satu artist per object)

Nama file: `csv_tugasx_name.csv`
Contoh: `csv_tugas1_kursi_taman.csv`

```
artist,object_name
Andi,kursi_taman
Budi,meja_taman
Citra,rak_buku
```

Dropdown Artist menampilkan nama satu-satu (`Andi`, `Budi`, dst).

#### Format Group (dua artist per object)

Nama file: `csv_tugasx_name_group.csv`
Contoh: `csv_tugas2_lampu_meja_group.csv`

```
artist1,artist2,object_name
Andi,Budi,lampu_meja
Citra,Dedi,rak_buku
```

Dropdown Artist menampilkan pasangan (`Andi & Budi`, `Citra & Dedi`, dst).

> Addon mendeteksi format secara otomatis dari nama file — `_group` di akhir nama file (sebelum `.csv`) menandakan format group. Dropdown Tugas menampilkan label `[Group]` untuk file format group.

### 2. `config/paths.json` — Lokasi Penyimpanan Project per Tugas

Buat file `quila_pipeline/config/paths.json`, isinya menentukan **di mana** struktur folder project akan di-generate untuk tiap tugas:

```json
{
    "tugas1": "D:/Proyek/Tugas1",
    "tugas2": "D:/Proyek/Tugas2"
}
```

> Path dasar (misal `D:/Proyek/Tugas1`) **harus sudah ada** di disk sebelum dipakai — addon tidak akan membuat folder dasar ini sendiri, hanya folder project di dalamnya. Ini pengaman dari typo path yang bisa membuat folder terbuat di lokasi yang salah.

---

## Cara Pakai

### A. Workflow Student (Mode WIP)

1. Buka Blender baru (file belum pernah disimpan)
2. Di N-Panel tab Quila, pilih **Tugas** lalu pilih **Artist** (atau **Group** kalau format group) — kotak "Object" otomatis menampilkan nama object yang harus dikerjakan
3. Klik **Create Project** — addon otomatis:
   - Membuat folder `[OBJECT_NAME]/` beserta subfolder `REF/WIP/RENDER/TEXTURE/EXPORT`
   - Menyimpan file Blender ini sebagai `[object_name]_wip01.blend` di folder `WIP/`
4. Dropdown Tugas/Artist sekarang **terkunci** — file sudah resmi terhubung ke project ini
5. Lanjutkan modeling, texturing, dst. Tombol Publish **hanya aktif di Object Mode** (tidak bisa diklik saat Edit Mode)
6. Klik **Publish** untuk menjalankan seluruh validasi SOP:
   - Kalau ada masalah → ditampilkan di Panel per kategori dengan tombol Select Target di tiap baris error
   - Kalau semua lolos → file WIP otomatis di-save, lalu dibuat **salinan file final** ke folder `[OBJECT_NAME]/` (file WIP yang aktif tetap WIP, tidak berpindah)
7. Ulangi langkah 5-6 setiap ada revisi — file final menimpa versi sebelumnya secara otomatis

### B. Workflow Mentor (Mode Final)

1. Buka file final (`[object_name].blend`, ada di root folder `[OBJECT_NAME]/`, bukan di dalam `WIP/`)
2. Tombol di Panel otomatis berubah jadi **Check SOP** — dropdown Tugas/Artist juga otomatis terkunci
3. Klik **Check SOP** — addon menjalankan validasi yang sama, tapi **tidak** membuat file apapun

---

## Struktur Folder Project yang Dihasilkan

```
[OBJECT_NAME]/              (huruf besar semua — UPPERCASE dari object_name)
├── REF/
├── WIP/
│   └── object_name_wip01.blend, wip02.blend, dst
├── RENDER/
│   └── object_name_prev01.png, dst
├── TEXTURE/
│   └── tex_namatexture_basecolor.png, dst
├── EXPORT/
└── object_name.blend        (file final, dibuat otomatis oleh Publish)
```

> Nama folder root (`[OBJECT_NAME]`) **huruf besar semua** (UPPERCASE dari object_name), sementara nama file, collection, dan object di dalamnya tetap **huruf kecil** sesuai SOP. Ini konvensi yang disengaja — bukan kesalahan.

---

## Daftar Validasi SOP

Semua validasi dijalankan setiap klik Publish/Check SOP. Semuanya bersifat **blocking** dan menampilkan **1 error pertama per kategori** per klik (student fokus membenarkan satu masalah dulu sebelum lanjut):

| Kategori | Yang Divalidasi |
|---|---|
| **File Naming** | Format nama file (`object_name_(variant)_wipXX.blend` untuk WIP, `object_name_(variant).blend` untuk Final); `object_name` harus cocok dengan tugas yang dipilih |
| **Folder Structure** | File WIP harus di dalam folder `WIP/`; nama folder root harus UPPERCASE dan cocok `object_name`; folder wajib (`REF/WIP/RENDER/TEXTURE/EXPORT`) harus ada dengan huruf besar semua; tidak boleh ada folder ekstra di level manapun (termasuk nested di dalam folder wajib) |
| **Collection Naming** | Collection utama harus sesuai nama file; tidak boleh ada collection lain selain itu dan `lgt&cam`; `lgt&cam` tidak boleh nested di dalam collection object; semua Light/Camera wajib di collection `lgt&cam` |
| **Object Naming** | Semua object Mesh harus diawali `geo_`; harus berada di dalam collection yang sesuai |
| **Mesh Rules** | Tidak boleh ada n-gon (face > 4 sisi); tidak boleh ada normal yang terbalik (flipped) |
| **Material Naming** | Semua material harus diawali `shd_` |
| **Texture Naming** | File texture tidak boleh missing; harus berada di folder `TEXTURE/` project ini; format nama harus `tex_nama_tipe`; nama internal di Blender harus sama dengan nama file (tanpa ekstensi, tanpa suffix duplikat `.001`); Generated Image juga divalidasi formatnya; node Image Texture tidak boleh kosong |
| **Render Naming** | File di folder `RENDER/` harus berformat `object_name_(variant)_prevXX` dan diawali nama object yang sesuai |

---

## Tombol Select Target

Setiap baris error di Panel punya tombol kecil di kanan (ikonnya berbeda per kategori). Klik tombol ini untuk navigasi langsung ke lokasi atau item yang bermasalah:

| Kategori Error | Aksi Tombol | Ikon |
|---|---|---|
| Folder Structure | Buka File Explorer ke folder yang bermasalah | 📁 |
| Collection Naming (collection) | Highlight collection di Outliner | 🗂 |
| Collection Naming (Light/Camera) | Select object di viewport + fokus | 🔵 |
| Object Naming | Select object di viewport + fokus | 🔵 |
| Mesh Rules | Select object di viewport + fokus | 🔵 |
| Material Naming | Buka Properties panel ke tab Material | 🟡 |
| Texture (file disk) | Buka File Explorer, sorot file texture | 🖼 |
| Texture (internal Blender) | Buka Image Editor, tampilkan image | 🖼 |
| Texture (node kosong) | Buka Properties panel ke tab Material | 🟡 |
| Render Naming | Buka File Explorer ke folder RENDER | 📁 |

---

## Struktur Kode Addon

```
quila_pipeline/
├── __init__.py                    # bl_info, register/unregister
├── properties.py                   # PropertyGroup: tugas_ke, artist_name, hasil validasi
├── sop_rules.py                     # Regex pattern SOP + deteksi mode WIP/Final
├── csv_loader.py                    # Baca CSV, dropdown Tugas & Artist (single & group)
├── path_config.py                   # Baca config/paths.json
├── csv/                               # Data: file CSV tugas (single & group)
├── config/                            # Data: paths.json lokasi project per tugas
├── validators/
│   ├── __init__.py                    # run_all() — registry semua validator
│   ├── issue.py                       # Dataclass Issue (category, message, target_name, action_type)
│   ├── file_naming.py
│   ├── folder_structure.py
│   ├── collection_naming.py
│   ├── object_naming.py
│   ├── mesh_rules.py
│   ├── material_naming.py
│   ├── texture_naming.py
│   └── render_naming.py
├── operators/
│   ├── op_publish.py                  # Tombol Publish / Check SOP
│   ├── op_create_project.py           # Tombol Create Project
│   └── op_select_target.py            # Tombol Select Target (navigasi per action_type)
└── ui/
    ├── helpers.py                      # Word-wrap manual untuk pesan panjang
    └── panel.py                         # N-Panel utama
```

### Fungsi Kunci

| Fungsi | Lokasi | Kegunaan |
|---|---|---|
| `get_file_mode(filepath)` | `sop_rules.py` | Deteksi `"wip"`/`"final"` dari suffix `_wipXX` di nama file |
| `get_expected_object_name(filepath)` | `sop_rules.py` | Ambil `object_name` (+variant) dari nama file, mode-aware |
| `discover_task_csv_files()` | `csv_loader.py` | Scan folder `csv/`, return list file CSV + info format (di-cache 5 detik) |
| `get_current_assigned_object_name(context)` | `csv_loader.py` | Object name dari kombinasi dropdown Tugas+Artist, menangani single & group |
| `is_csv_ready(context)` | `csv_loader.py` | Cek minimal satu CSV valid, dipakai `poll()` untuk enable/disable tombol |
| `get_base_path_for_tugas(tugas_ke)` | `path_config.py` | Path dasar folder project untuk Create Project |

### `action_type` yang Didukung `op_select_target.py`

| `action_type` | Aksi |
|---|---|
| `select_object` | Select object di viewport + fokus |
| `highlight_collection` | Highlight collection di Outliner |
| `open_folder` | Buka File Explorer ke folder |
| `open_render_folder` | Buka File Explorer ke folder RENDER |
| `open_texture_file` | Buka File Explorer, sorot file texture |
| `open_image_editor` | Buka Image Editor, tampilkan image |
| `open_material_properties` | Select object pemilik material + buka tab Material di Properties |

---

## Keterbatasan yang Diketahui

- **Deteksi flipped normal** (`mesh_rules.py`) memakai heuristik *signed volume* — akurat untuk mesh solid/tertutup, kurang akurat untuk mesh terbuka (misal plane datar) atau mesh dengan beberapa bagian terpisah. Gunakan **Overlay > Face Orientation** di viewport sebagai cross-check visual.
- **Hanya 1 error per kategori per klik** — kalau satu kategori punya banyak masalah, student melihatnya satu per satu setiap klik Publish/Check SOP.
- **Image Editor (Select Target texture)** — kalau tidak ada area bertipe Image Editor yang terbuka, addon akan mengubah area yang ada menjadi Image Editor. Untuk hasil terbaik, pakai workspace **Shading** yang sudah punya Image Editor bawaan.
- **CSV dan `config/paths.json`** adalah data hidup yang dikelola mentor — saat update kode addon, jangan menimpa folder `csv/` dan `config/` secara tidak sengaja.
- **`discover_task_csv_files()` di-cache 5 detik** — perubahan nama/isi file CSV di folder `csv/` baru terdeteksi setelah 5 detik (refresh otomatis, tidak perlu restart Blender).

---

## Troubleshooting

| Masalah | Kemungkinan Sebab |
|---|---|
| Dropdown Tugas kosong | Tidak ada file `csv_tugasx_name.csv` di folder `csv/` — cek nama file sesuai format |
| Dropdown Artist kosong setelah pilih Tugas | Header CSV salah — pastikan `artist,object_name` (single) atau `artist1,artist2,object_name` (group) |
| Label `[Group]` tidak muncul | Nama file harus diakhiri `_group.csv` persis, bukan `_groups.csv` atau `_Group.csv` |
| Tombol Create Project/Publish abu-abu | Tugas dan/atau Artist belum dipilih, atau tidak ada CSV yang valid |
| Tombol Publish abu-abu padahal sudah pilih Artist | Blender sedang di Edit Mode — keluar ke Object Mode dulu |
| Create Project error "Path dasar tidak ditemukan" | Folder di `config/paths.json` belum dibuat manual di disk |
| File WIP dianggap mode "Final" | Cek suffix `_wipXX` di nama file sebelum `.blend` — deteksi mode dari pola nama file |
| Folder root dianggap salah nama | Harus **UPPERCASE** persis dari `object_name` (misal `kursi_taman` → `KURSI_TAMAN`) |
| Texture "tidak ditemukan" padahal ada | File harus berada **di dalam** folder `TEXTURE/` milik project ini |
| Select Target material tidak berfungsi | Object pemilik material mungkin di-hide atau tidak ada di scene aktif |

Untuk debugging lebih dalam, gunakan **Python Console** di workspace Scripting:

```python
import bpy
from quila_pipeline.validators import run_all
for issue in run_all(bpy.context):
    print(issue)
```

---

## Riwayat Pengembangan

Addon ini dibangun melalui **10 fase awal** (Fase 0-10): skeleton addon, properties, CSV loader, 8 validator SOP, operator Check, operator Mark as Final, UI Panel, testing, deployment, dan maintenance.

Kemudian mengalami beberapa gelombang **revisi**:

**Revisi 1-6** — Fondasi baru: CSV jadi file-per-tugas, UI dropdown Artist+Tugas, tombol Publish (gabungan Check+Mark as Final), mode ganda WIP/Final, bug fix testing awal, update dokumen deployment server.

**Revisi 7-11** — Perbaikan deteksi mode WIP/Final (berbasis nama file, bukan folder), pesan error lebih jelas, validasi folder ekstra, perbaikan texture naming, tombol dinamis + CSV guard.

**Revisi 12-14** — Gating tombol & lock dropdown di mode Final, validasi folder rekursif ke subfolder, perbaikan Generated Image & pesan error ekstensi.

**Revisi 15-17** — Tombol Create Project + generate folder otomatis dari `paths.json`, validasi nama folder root harus UPPERCASE, ikon bullet untuk multiple error di Panel.

**Revisi 18 (Revisi 25)** — Tambah field `action_type` ke dataclass `Issue` dan `QuilaIssueItem`, update semua validator untuk mengisi `action_type` yang sesuai.

**Revisi 19 (Revisi 26)** — Operator `op_select_target.py` dengan 7 jenis aksi berbeda per `action_type`, tombol Select Target di tiap baris error di Panel.

**Revisi 27** — Format CSV baru: `csv_tugasx_name_group.csv` untuk tugas berpasangan (2 artist per object), dropdown Artist menampilkan pasangan, `csv_loader.py` mendeteksi format otomatis.

**Perbaikan bug & clean code terakhir** — Fix urutan logika deteksi folder UPPERCASE, fix mismatch `action_type` material, fix node Image Texture kosong tanpa `action_type`, `Issue` dipindah ke `validators/issue.py`, cache `discover_task_csv_files()` untuk performa UI.

Dokumentasi detail tiap fase dan revisi tersedia di folder `docs/` dan `docs/revise/`.

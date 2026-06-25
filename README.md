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
7. [Struktur Kode Addon](#struktur-kode-addon)
8. [Keterbatasan yang Diketahui](#keterbatasan-yang-diketahui)
9. [Troubleshooting](#troubleshooting)
10. [Riwayat Pengembangan](#riwayat-pengembangan)

---

## Gambaran Umum

Quila Pipeline membantu mentor menjaga konsistensi pekerjaan 3D student tanpa harus mengecek manual satu per satu. Addon ini menyediakan:

- **Generate struktur folder otomatis** sesuai SOP, langsung dari kombinasi Tugas + Artist yang dipilih
- **8 kategori validasi otomatis**: naming file, struktur folder, collection, object, mesh (n-gon/flipped normal), material, texture, dan render
- **Satu tombol kerja** yang berubah sesuai konteks: *Create Project* → *Publish* → *Check SOP*
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

### 1. `csv/csv_tugasN.csv` — Daftar Tugas per Artist

Buat satu file CSV per batch tugas, ditaruh di `quila_pipeline/csv/`, dengan nama **persis** `csv_tugas1.csv`, `csv_tugas2.csv`, dst (angka menyesuaikan jumlah tugas). Format isi:

```
artist,object_name
Andi,kursi_taman
Budi,meja_taman
Citra,rak_buku
```

> Kolom wajib: `artist` dan `object_name`. Satu baris = satu artist dengan satu object_name untuk tugas itu.

### 2. `config/paths.json` — Lokasi Penyimpanan Project per Tugas

Buat file `quila_pipeline/config/paths.json`, isinya menentukan **di mana** struktur folder project akan di-generate untuk tiap tugas:

```json
{
    "tugas1": "D:/Proyek/Tugas1",
    "tugas2": "D:/Proyek/Tugas2"
}
```

> Path dasar (misal `D:/Proyek/Tugas1`) **harus sudah ada** di disk sebelum dipakai — addon tidak akan membuat folder dasar ini sendiri, hanya folder project di dalamnya (sebagai pengaman dari typo path yang bisa membuat folder salah tempat).

---

## Cara Pakai

### A. Workflow Student (Mode WIP)

1. Buka Blender baru (file belum pernah disimpan)
2. Di N-Panel tab Quila, pilih **Tugas** lalu pilih **Artist** — kotak "Object" akan otomatis menampilkan nama object yang harus dikerjakan
3. Klik **Create Project** — addon otomatis:
   - Membuat folder `[OBJECT_NAME]/` beserta subfolder `REF/WIP/RENDER/TEXTURE/EXPORT`
   - Menyimpan file Blender ini sebagai `[object_name]_wip01.blend` di folder `WIP/`
4. Dropdown Tugas/Artist sekarang **terkunci** (tidak bisa diubah lagi), karena file sudah resmi terhubung ke project ini
5. Lanjutkan modeling, texturing, dst seperti biasa
6. Kapan saja, klik **Publish** untuk menjalankan seluruh validasi SOP:
   - Kalau ada masalah → ditampilkan di Panel per kategori, tidak ada file dibuat
   - Kalau semua lolos → file WIP otomatis ikut tersimpan (`save`), lalu dibuat **salinan file final** ke folder `[OBJECT_NAME]/` (file WIP yang sedang aktif tetap WIP, tidak ikut "berpindah")
7. Ulangi langkah 5-6 setiap ada revisi — file final akan menimpa versi sebelumnya secara otomatis

### B. Workflow Mentor (Mode Final)

1. Buka file final (`[object_name].blend`, ada di root folder `[OBJECT_NAME]/`, bukan di dalam `WIP/`)
2. Tombol di Panel otomatis berubah jadi **Check SOP** (bukan Publish) — dropdown Tugas/Artist juga otomatis terkunci
3. Klik **Check SOP** — addon menjalankan validasi yang sama, tapi **tidak** membuat file apapun, murni untuk verifikasi ulang bahwa file final masih sesuai SOP

---

## Struktur Folder Project yang Dihasilkan

```
[OBJECT_NAME]/              (huruf besar semua, dari Create Project otomatis)
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

> **Catatan penting:** nama folder root (`[OBJECT_NAME]`) sengaja dibuat **huruf besar semua** (uppercase dari object_name), sementara nama file, collection, dan object di dalamnya tetap **huruf kecil** sesuai konvensi SOP biasa. Ini perbedaan konvensi yang disengaja antara nama folder (uppercase) dan nama internal/file (lowercase) — bukan kesalahan.

---

## Daftar Validasi SOP

Semua validasi berikut dijalankan setiap klik Publish/Check SOP, **semuanya bersifat blocking** (tidak ada yang sekadar warning):

| Kategori | Yang Divalidasi |
|---|---|
| **File Naming** | Format nama file (`object_name_(variant)_wipXX.blend` untuk WIP, `object_name_(variant).blend` untuk Final); `object_name` harus cocok dengan tugas yang dipilih di dropdown |
| **Folder Structure** | Lokasi file WIP harus di folder `WIP/`; nama folder root harus uppercase dan cocok object_name; folder wajib (`REF/WIP/RENDER/TEXTURE/EXPORT`) harus ada dengan huruf besar semua; tidak boleh ada folder ekstra (di level manapun, termasuk nested di dalam folder wajib) |
| **Collection Naming** | Collection utama harus sesuai nama file; tidak boleh ada collection lain selain itu dan `lgt&cam`; collection `lgt&cam` tidak boleh nested di dalam collection object; semua Light/Camera wajib berada di collection `lgt&cam` |
| **Object Naming** | Semua object Mesh harus diawali `geo_` |
| **Mesh Rules** | Tidak boleh ada n-gon (face > 4 sisi); tidak boleh ada normal yang terbalik (flipped) |
| **Material Naming** | Semua material harus diawali `shd_` |
| **Texture Naming** | File texture harus ada di disk (tidak missing); harus berada di folder `TEXTURE/` project ini; format nama harus `tex_nama_tipe`; nama internal di Blender harus sama dengan nama file (tanpa ekstensi); Generated Image (bukan dari file) juga ikut divalidasi formatnya; node Image Texture tidak boleh kosong tanpa image |
| **Render Naming** | File di folder `RENDER/` harus berformat `object_name_(variant)_prevXX`, dan harus diawali nama object yang sesuai |

> **Catatan desain:** sejak versi terbaru, `run_all()` hanya mengambil **1 error pertama** dari tiap kategori validator (bukan menampilkan semua error sekaligus per kategori) — ini keputusan sengaja, supaya student fokus membenarkan satu masalah dulu sebelum lanjut ke masalah berikutnya, tidak overwhelmed. Tampilan ikon bullet (`•`) di Panel tetap ada untuk mengantisipasi kalau desain ini diubah lagi di masa depan jadi "tampilkan semua error".

---

## Struktur Kode Addon

```
quila_pipeline/
├── __init__.py                 # bl_info, register/unregister
├── properties.py                # PropertyGroup: tugas_ke, artist_name, hasil validasi
├── sop_rules.py                  # Semua regex pattern SOP + deteksi mode WIP/Final
├── csv_loader.py                 # Baca csv/csv_tugasN.csv, dropdown Tugas & Artist
├── path_config.py                # Baca config/paths.json
├── csv/                            # Data: daftar tugas per artist
├── config/                         # Data: lokasi folder project per tugas
├── validators/
│   ├── __init__.py                 # Issue (dataclass) + run_all()
│   ├── file_naming.py
│   ├── folder_structure.py
│   ├── collection_naming.py
│   ├── object_naming.py
│   ├── mesh_rules.py
│   ├── material_naming.py
│   ├── texture_naming.py
│   └── render_naming.py
├── operators/
│   ├── op_publish.py               # Tombol Publish / Check SOP
│   └── op_create_project.py        # Tombol Create Project
└── ui/
    ├── helpers.py                   # Word-wrap manual untuk pesan panjang
    └── panel.py                      # N-Panel utama
```

### Fungsi Kunci yang Sering Dipakai Ulang

| Fungsi | Lokasi | Fungsi |
|---|---|---|
| `get_file_mode(filepath)` | `sop_rules.py` | Deteksi `"wip"`/`"final"` dari pola nama file (`_wipXX` di akhir) |
| `get_expected_object_name(filepath)` | `sop_rules.py` | Ambil `object_name` (+variant) dari nama file, mode-aware |
| `get_current_assigned_object_name(context)` | `csv_loader.py` | Object name hasil kombinasi dropdown Tugas+Artist saat ini |
| `is_csv_ready(context)` | `csv_loader.py` | Cek minimal satu CSV tugas valid, dipakai untuk `poll()` |
| `get_base_path_for_tugas(tugas_ke)` | `path_config.py` | Path dasar folder project untuk Create Project |

---

## Keterbatasan yang Diketahui

- **Deteksi flipped normal** (`mesh_rules.py`) memakai heuristik *signed volume* — akurat untuk mesh solid/tertutup, kurang akurat untuk mesh terbuka (misal plane datar) atau mesh dengan beberapa bagian terpisah yang saling "membatalkan" dalam hitungan volume total. Pelengkap manual: aktifkan **Overlay > Face Orientation** di viewport untuk cross-check visual.
- **Hanya 1 error per kategori ditampilkan per klik** (lihat catatan di bagian Daftar Validasi SOP) — kalau satu kategori punya banyak masalah, student akan melihatnya satu per satu setiap klik Publish/Check SOP, bukan semua sekaligus.
- **Tombol "Select object"** (lompat ke object bermasalah di viewport) sudah dihapus dari versi ini — `target_name` di setiap `Issue` masih ada di struktur data, tapi tidak lagi dipakai untuk fitur apapun di Panel.
- **Path di `config/paths.json` dan CSV di `csv/`** adalah data hidup yang dikelola mentor — kalau melakukan update kode addon di kemudian hari, jangan menimpa folder `csv/` dan `config/` secara tidak sengaja (lihat bagian Maintenance di dokumen revisi sebelumnya).

---

## Troubleshooting

| Masalah | Kemungkinan Sebab |
|---|---|
| Dropdown Tugas/Artist kosong | File `csv/csv_tugasN.csv` belum ada/format salah — cek nama kolom persis `artist,object_name` |
| Tombol Create Project/Publish abu-abu | Tugas dan/atau Artist belum dipilih (masih `"NONE"`), atau CSV tidak ada data sama sekali |
| Create Project error "Path dasar tidak ditemukan" | Folder di `config/paths.json` belum dibuat manual di disk |
| File WIP dianggap mode "Final" | Cek nama file masih ada suffix `_wipXX` sebelum `.blend` — deteksi mode berdasarkan pola nama file, bukan folder |
| Folder utama dianggap salah nama padahal sudah benar | Pastikan ditulis **huruf besar semua**, persis sama dengan `object_name` (di-uppercase) |
| Texture dianggap "tidak ditemukan" padahal ada | Pastikan file ada **di dalam** folder `TEXTURE/` milik project ini, bukan di lokasi lain |

Untuk debugging lebih dalam, gunakan **Python Console** di workspace Scripting:
```python
import bpy
from quila_pipeline.validators import run_all
for issue in run_all(bpy.context):
    print(issue)
```

---

## Riwayat Pengembangan

Addon ini dibangun melalui 10 fase awal (skeleton, properties, CSV, validators, operator Check, Mark as Final, UI lengkap, testing, deployment, maintenance), lalu mengalami beberapa gelombang revisi besar:

- **Revisi 1-6**: restrukturisasi CSV jadi file-per-tugas, UI dropdown Artist+Tugas, tombol Publish (gabungan Check+Mark as Final), mode ganda WIP/Final, bug fix dari testing awal, update dokumen deployment
- **Revisi 7-11**: perbaikan deteksi mode WIP/Final agar berbasis nama file (bukan folder), pesan error yang lebih jelas, validasi folder ekstra, perbaikan texture naming, tombol dinamis + CSV guard
- **Revisi 12-14**: gating tombol & lock dropdown di mode Final, validasi folder rekursif, perbaikan Generated Image & pesan ekstensi
- **Revisi 15-17**: tombol Create Project + generate folder otomatis, validasi nama folder utama, ikon bullet untuk multiple error

Dokumentasi detail tiap fase/revisi tersedia di folder `docs/` dan `docs/revise/`.

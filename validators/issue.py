from dataclasses import dataclass


@dataclass
class Issue:
    """Satu temuan masalah dari validator.

    Attributes:
        category:    Nama kategori validator (misal "File Naming", "Mesh Rules")
        message:     Pesan error yang ditampilkan ke user
        target_name: Nama object/collection/material/image/path yang bermasalah
        action_type: Jenis aksi tombol Select (lihat op_select_target.py)
    """
    category: str
    message: str
    target_name: str = ""
    action_type: str = ""

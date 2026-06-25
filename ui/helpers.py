import textwrap


def get_wrap_width_chars(context):
    """Estimasi kasar berapa karakter yang muat di lebar N-Panel saat ini."""
    region_width = context.region.width
    chars = max(20, int(region_width / 7))
    return chars


def draw_wrapped_text(layout, text, width_chars, bullet=False):
    """Tampilkan teks panjang sebagai beberapa baris label (manual word-wrap).

    Kalau bullet=True, baris pertama diberi tanda '•' di depan — berguna
    untuk memperjelas batas antar masalah ketika satu kategori error
    punya lebih dari satu masalah sekaligus."""
    lines = textwrap.wrap(text, width_chars)

    for i, line in enumerate(lines):
        if bullet and i == 0:
            layout.label(text=f"• {line}")
        else:
            layout.label(text=line)
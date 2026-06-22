import textwrap


def get_wrap_width_chars(context):
    """Estimasi kasar berapa karakter yang muat di lebar N-Panel saat ini."""
    region_width = context.region.width
    chars = max(20, int(region_width / 7))
    return chars


def draw_wrapped_text(layout, text, width_chars):
    """Tampilkan teks panjang sebagai beberapa baris label (manual word-wrap)."""
    for line in textwrap.wrap(text, width_chars):
        layout.label(text=line)
from pygame import font
from settings.screen import X_SCALE

DEFAULT_FONT_TYPE = 'Arial'
DEFAULT_FONT_SIZE = int(15 * X_SCALE)


def custom_font_size(size: int, font_name=None):
    font_name = font_name if font_name else DEFAULT_FONT_TYPE
    return font.SysFont(font_name, size)


DEFAULT_FONT = font.SysFont(DEFAULT_FONT_TYPE, DEFAULT_FONT_SIZE)

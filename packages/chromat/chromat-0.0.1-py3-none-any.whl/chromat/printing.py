# from colorsys import hsv_to_rgb, rgb_to_hsv

from rich.console import Console
from rich.theme import Theme


def init_console():
    custom_theme = Theme(
        {"title": "bold not italic #F18EC6", "body": "#CCCCCC"}, inherit=False
    )

    return Console(theme=custom_theme)

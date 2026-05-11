from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    app_background: str = "#ECEFF3"
    sidebar: str = "#F1F3F5"
    surface: str = "#FFFFFF"
    surface_alt: str = "#F7F8FA"
    card: str = "#FFFFFF"
    card_soft: str = "#F3F5F8"
    border: str = "#CCD4DD"
    border_strong: str = "#B9C4D0"
    text: str = "#243241"
    text_muted: str = "#526170"
    text_subtle: str = "#708090"
    accent: str = "#4C78C8"
    accent_soft: str = "#6E90D1"
    accent_hover: str = "#3E68B6"
    sidebar_item_hover: str = "#E7EBF0"
    sidebar_item_active: str = "#DCE4EE"
    header_dark: str = "#25313F"
    header_text: str = "#F5F7FA"

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


def modern_legacy_palette() -> ColorPalette:
    return ColorPalette(
        app_background="#ECEFF3",
        sidebar="#F1F3F5",
        surface="#FFFFFF",
        surface_alt="#F7F8FA",
        card="#FFFFFF",
        card_soft="#F3F5F8",
        border="#CCD4DD",
        border_strong="#B9C4D0",
        text="#243241",
        text_muted="#526170",
        text_subtle="#708090",
        accent="#4C78C8",
        accent_soft="#6E90D1",
        accent_hover="#3E68B6",
        sidebar_item_hover="#E7EBF0",
        sidebar_item_active="#DCE4EE",
        header_dark="#25313F",
        header_text="#F5F7FA",
    )


def v2_classic_palette() -> ColorPalette:
    return ColorPalette(
        app_background="#F2EBDD",
        sidebar="#2B3950",
        surface="#F6EFE3",
        surface_alt="#FBF7F0",
        card="#EFE4D3",
        card_soft="#E6D9C7",
        border="#D4B18A",
        border_strong="#C89463",
        text="#2E2B26",
        text_muted="#5F5448",
        text_subtle="#7A6F63",
        accent="#E6763B",
        accent_soft="#F09A68",
        accent_hover="#D5672E",
        sidebar_item_hover="#364763",
        sidebar_item_active="#E6763B",
        header_dark="#2B3950",
        header_text="#F9F3E9",
    )

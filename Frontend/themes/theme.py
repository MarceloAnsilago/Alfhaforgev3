from dataclasses import dataclass

import customtkinter as ctk

from themes.colors import ColorPalette


@dataclass(frozen=True)
class TypographyScale:
    title: tuple[str, int] = ("Segoe UI", 20)
    subtitle: tuple[str, int] = ("Segoe UI", 15)
    body: tuple[str, int] = ("Segoe UI", 13)
    label: tuple[str, int] = ("Segoe UI", 11)
    caption: tuple[str, int] = ("Segoe UI", 12)


class UITheme:
    def __init__(self) -> None:
        self.colors = ColorPalette()
        self.typography = TypographyScale()

    def font(self, role: str, weight: str = "normal") -> ctk.CTkFont:
        family, size = getattr(self.typography, role)
        return ctk.CTkFont(family=family, size=size, weight=weight)


def configure_ctk(theme: UITheme) -> None:
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    ctk.ThemeManager.theme["CTk"]["fg_color"] = [theme.colors.app_background, theme.colors.app_background]
    ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = [theme.colors.surface, theme.colors.surface]
    ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"] = [theme.colors.surface, theme.colors.surface]
    ctk.ThemeManager.theme["CTkLabel"]["text_color"] = [theme.colors.text, theme.colors.text]
    ctk.ThemeManager.theme["CTkButton"]["fg_color"] = [theme.colors.accent, theme.colors.accent]
    ctk.ThemeManager.theme["CTkButton"]["hover_color"] = [theme.colors.accent_hover, theme.colors.accent_hover]
    ctk.ThemeManager.theme["CTkButton"]["text_color"] = [theme.colors.text, theme.colors.text]
    ctk.ThemeManager.theme["CTkEntry"]["fg_color"] = [theme.colors.surface_alt, theme.colors.surface_alt]
    ctk.ThemeManager.theme["CTkEntry"]["border_color"] = [theme.colors.border, theme.colors.border]

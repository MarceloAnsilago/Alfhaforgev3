import customtkinter as ctk

from themes.theme import UITheme


class TopHeader(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme, on_apply=None) -> None:
        super().__init__(
            master,
            fg_color=theme.colors.surface,
            corner_radius=0,
            height=54,
            border_width=1,
            border_color=theme.colors.border,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_propagate(False)
        self._theme = theme

        stripe = ctk.CTkFrame(
            self,
            fg_color=theme.colors.accent,
            corner_radius=0,
            height=3,
            border_width=0,
        )
        stripe.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 8))

        ctk.CTkLabel(
            self,
            text="Construtor | AlphaForge V3",
            text_color=theme.colors.text,
            font=theme.font("subtitle", weight="normal"),
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(10, 6))

        self._status = ctk.CTkLabel(
            self,
            text="Bridge inativo",
            text_color=theme.colors.text_muted,
            font=theme.font("label"),
            anchor="e",
        )
        self._status.grid(row=1, column=1, sticky="e", padx=(0, 10), pady=(10, 6))

        self._apply_button = ctk.CTkButton(
            self,
            text="Aplicar no EA",
            command=on_apply,
            height=32,
            width=132,
            corner_radius=0,
            fg_color=theme.colors.accent,
            hover_color=theme.colors.accent_hover,
            text_color=theme.colors.header_text,
            font=theme.font("label", weight="bold"),
        )
        self._apply_button.grid(row=1, column=2, sticky="e", padx=(0, 12), pady=(10, 6))

    def set_status(self, text: str, success: bool = True) -> None:
        color = self._theme.colors.text if success else self._theme.colors.accent_soft
        self._status.configure(text=text, text_color=color)

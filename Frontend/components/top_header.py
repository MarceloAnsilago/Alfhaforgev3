import customtkinter as ctk

from themes.theme import UITheme


class TopHeader(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(
            master,
            fg_color=theme.colors.surface,
            corner_radius=0,
            height=54,
            border_width=1,
            border_color=theme.colors.border,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

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

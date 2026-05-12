import customtkinter as ctk

from themes.theme import UITheme


class TopHeader(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(
            master,
            fg_color=theme.colors.surface,
            corner_radius=0,
            height=56,
            border_width=1,
            border_color=theme.colors.border,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        stripe = ctk.CTkFrame(
            self,
            fg_color=theme.colors.accent,
            corner_radius=0,
            height=5,
            border_width=0,
        )
        stripe.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            self,
            text="Construtor (Easy GUI) | EasyPanel V3",
            text_color=theme.colors.text,
            font=theme.font("subtitle", weight="normal"),
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            self,
            text="Palheta V2 aplicada sobre a estrutura atual do CTk",
            text_color=theme.colors.text_subtle,
            font=theme.font("label"),
            anchor="w",
        ).grid(row=2, column=0, sticky="w", padx=12, pady=(0, 8))

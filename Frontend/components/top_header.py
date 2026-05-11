import customtkinter as ctk

from themes.theme import UITheme


class TopHeader(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(
            master,
            fg_color=theme.colors.header_dark,
            corner_radius=0,
            height=28,
            border_width=0,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        ctk.CTkLabel(
            self,
            text="AlphaForge V3 | Modal de teste",
            text_color=theme.colors.header_text,
            font=theme.font("label", weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=4)

import customtkinter as ctk

from themes.theme import UITheme


class BreakEvenView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._type_var = ctk.StringVar(value="Pontos")

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure((0, 1, 2), weight=1, uniform="break-even")

        self._build_header()
        self._build_card()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(
            self._scroll,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=6, pady=(4, 10))
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)

        self._add_label(header, 0, "Padrao", padx=16, pady=(16, 4))

        stop_type = self._create_combo(
            header,
            ["Pontos", "Percentual"],
            self._type_var,
        )
        stop_type.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Escolha como o break even sera interpretado nas configuracoes abaixo.",
            justify="left",
            anchor="w",
            wraplength=720,
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
        ).grid(row=1, column=1, sticky="ew", padx=(8, 16), pady=(0, 16))

    def _build_card(self) -> None:
        card = ctk.CTkFrame(
            self._scroll,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=1, column=0, sticky="nsew", padx=6, pady=4)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text="Break even",
            anchor="w",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))

        self._enabled_checkbox = self._create_checkbox(card, "Ativar break even")
        self._enabled_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))

        self._add_label(card, 2, "Inicio")
        self._start_entry = self._create_entry(card, "0.0")
        self._start_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 4, "Distancia")
        self._distance_entry = self._create_entry(card, "100.0")
        self._distance_entry.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

    def _create_checkbox(self, master, text: str) -> ctk.CTkCheckBox:
        return ctk.CTkCheckBox(
            master,
            text=text,
            fg_color=self._theme.colors.accent,
            hover_color=self._theme.colors.accent_hover,
            border_color=self._theme.colors.border_strong,
            text_color=self._theme.colors.text,
            font=self._theme.font("body"),
        )

    def _create_combo(
        self,
        master,
        values: list[str],
        variable: ctk.StringVar,
    ) -> ctk.CTkComboBox:
        return ctk.CTkComboBox(
            master,
            values=values,
            variable=variable,
            height=32,
            corner_radius=0,
            border_width=1,
            fg_color=self._theme.colors.surface_alt,
            border_color=self._theme.colors.border,
            button_color=self._theme.colors.accent,
            button_hover_color=self._theme.colors.accent_hover,
            dropdown_fg_color=self._theme.colors.surface,
            dropdown_hover_color=self._theme.colors.sidebar_item_hover,
            dropdown_text_color=self._theme.colors.text,
            text_color=self._theme.colors.text,
            font=self._theme.font("body"),
            state="readonly",
        )

    def _create_entry(self, master, value: str) -> ctk.CTkEntry:
        entry = ctk.CTkEntry(
            master,
            height=32,
            corner_radius=0,
            border_width=1,
            fg_color=self._theme.colors.surface_alt,
            border_color=self._theme.colors.border,
            text_color=self._theme.colors.text,
            font=self._theme.font("body"),
        )
        entry.insert(0, value)
        return entry

    def _add_label(self, master, row: int, text: str, padx: int = 16, pady: tuple[int, int] = (0, 4)) -> None:
        ctk.CTkLabel(
            master,
            text=text,
            anchor="w",
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("label"),
        ).grid(row=row, column=0, columnspan=2, sticky="ew", padx=padx, pady=pady)

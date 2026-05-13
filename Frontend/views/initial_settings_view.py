import customtkinter as ctk

from models.initial_settings import build_initial_settings_options
from themes.theme import UITheme


class InitialSettingsView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme
        self._form_options = build_initial_settings_options()
        self._combo_refs: dict[str, ctk.CTkComboBox] = {}
        self._time_refs: dict[str, tuple[ctk.CTkComboBox, ctk.CTkComboBox]] = {}
        self._entry_refs: dict[str, ctk.StringVar] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="card")

        self._name_var = ctk.StringVar(value="Minha estrategia")
        self._magic_var = ctk.StringVar(value=self._build_magic_value(self._name_var.get()))
        self._name_var.trace_add("write", self._on_name_change)

        self._build_cards()

    def _build_cards(self) -> None:
        self._build_basic_card()
        self._build_direction_card()
        self._build_schedule_card()
        self._build_config_card()

    def _build_basic_card(self) -> None:
        card = self._create_card(0, "Informacoes basicas")
        self._add_entry(card, 0, "Nome da estrategia", self._name_var)
        self._add_entry(card, 1, "Magic number", self._magic_var, readonly=True)
        self._add_combo(card, 2, "Mercado desejado", self._form_options.mercados, "B3")
        self._add_combo(card, 3, "Tipo operacional", self._form_options.tipos_operacionais, "Day trade")
        self._add_combo(card, 4, "Modo de processamento", self._form_options.modos_processamento, "Cada tick")

    def _build_direction_card(self) -> None:
        card = self._create_card(1, "Direcao operacional")
        self._add_combo(card, 0, "Operar na compra", self._form_options.sim_nao, "Sim")
        self._add_combo(card, 1, "Operar na venda", self._form_options.sim_nao, "Sim")

    def _build_schedule_card(self) -> None:
        card = self._create_card(2, "Horario e zeragem")
        self._add_time_row(card, 0, "Inicio das operacoes", "09", "00")
        self._add_time_row(card, 1, "Fim das operacoes", "17", "00")

        divider = ctk.CTkFrame(card, fg_color=self._theme.colors.border, height=1)
        divider.grid(row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 16))

        self._add_combo(card, 6, "Zerar posicoes", self._form_options.sim_nao, "Nao")
        self._add_time_row(card, 7, "Horario de zeragem", "17", "30")

    def _build_config_card(self) -> None:
        card = self._create_card(3, "Configuracao inicial")
        self._add_combo(card, 0, "Tempo grafico", self._form_options.tempos_graficos, "Corrente")
        self._add_entry(card, 1, "Volume inicial", ctk.StringVar(value="1.00"))
        self._add_entry(card, 2, "Spread maximo", ctk.StringVar(value="10"))

    def _create_card(self, column: int, title: str) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            self._scroll,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=6, pady=4)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            anchor="w",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))
        return card

    def _add_entry(
        self,
        card: ctk.CTkFrame,
        index: int,
        label: str,
        variable: ctk.StringVar,
        readonly: bool = False,
    ) -> None:
        row = 1 + (index * 2)
        self._add_label(card, row, label)

        entry = ctk.CTkEntry(
            card,
            textvariable=variable,
            height=32,
            corner_radius=0,
            border_width=1,
            fg_color=self._theme.colors.surface_alt,
            border_color=self._theme.colors.border,
            text_color=self._theme.colors.text,
            font=self._theme.font("body"),
        )
        entry.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))
        if readonly:
            entry.configure(state="readonly")
        self._entry_refs[label] = variable

    def _add_combo(
        self,
        card: ctk.CTkFrame,
        index: int,
        label: str,
        values: list[str],
        default: str,
    ) -> None:
        row = 1 + (index * 2)
        self._add_label(card, row, label)

        combo = ctk.CTkComboBox(
            card,
            values=values,
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
        combo.set(default)
        combo.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))
        self._combo_refs[label] = combo

    def _add_time_row(
        self,
        card: ctk.CTkFrame,
        index: int,
        label: str,
        hour_default: str,
        minute_default: str,
    ) -> None:
        row = 1 + (index * 2)
        self._add_label(card, row, label)

        hours = [f"{hour:02d}" for hour in range(24)]
        minutes = [f"{minute:02d}" for minute in range(60)]

        hour_combo = ctk.CTkComboBox(
            card,
            values=hours,
            height=32,
            width=92,
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
        hour_combo.set(hour_default)
        hour_combo.grid(row=row + 1, column=0, sticky="ew", padx=(16, 8), pady=(0, 12))

        minute_wrap = ctk.CTkFrame(card, fg_color="transparent")
        minute_wrap.grid(row=row + 1, column=1, sticky="ew", padx=(8, 16), pady=(0, 12))
        minute_wrap.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            minute_wrap,
            text=":",
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("subtitle", weight="bold"),
            width=14,
        ).grid(row=0, column=0, padx=(0, 8))

        minute_combo = ctk.CTkComboBox(
            minute_wrap,
            values=minutes,
            height=32,
            width=92,
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
        minute_combo.set(minute_default)
        minute_combo.grid(row=0, column=1, sticky="ew")
        self._time_refs[label] = (hour_combo, minute_combo)

    def _add_label(self, card: ctk.CTkFrame, row: int, text: str) -> None:
        ctk.CTkLabel(
            card,
            text=text,
            anchor="w",
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("label"),
        ).grid(row=row, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 4))

    def _build_magic_value(self, name: str) -> str:
        cleaned = "".join(char for char in name if char.isalnum())
        if not cleaned:
            return "0"
        total = sum(ord(char) for char in cleaned.upper())
        return str(100000 + total)

    def _on_name_change(self, *_args) -> None:
        self._magic_var.set(self._build_magic_value(self._name_var.get()))

    def export_config(self) -> dict[str, str]:
        start_hour, start_minute = self._time_refs["Inicio das operacoes"]
        end_hour, end_minute = self._time_refs["Fim das operacoes"]
        reset_hour, reset_minute = self._time_refs["Horario de zeragem"]
        return {
            "strategy_name": self._name_var.get(),
            "magic_number": self._magic_var.get(),
            "market": self._combo_refs["Mercado desejado"].get(),
            "operation_type": self._combo_refs["Tipo operacional"].get(),
            "processing_mode": self._combo_refs["Modo de processamento"].get(),
            "allow_buy": self._combo_refs["Operar na compra"].get(),
            "allow_sell": self._combo_refs["Operar na venda"].get(),
            "start_time": f"{start_hour.get()}:{start_minute.get()}",
            "end_time": f"{end_hour.get()}:{end_minute.get()}",
            "reset_positions": self._combo_refs["Zerar posicoes"].get(),
            "reset_time": f"{reset_hour.get()}:{reset_minute.get()}",
            "chart_timeframe": self._combo_refs["Tempo grafico"].get(),
            "initial_volume": self._entry_refs["Volume inicial"].get(),
            "max_spread": self._entry_refs["Spread maximo"].get(),
        }

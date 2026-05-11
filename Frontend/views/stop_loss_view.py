import customtkinter as ctk

from themes.theme import UITheme


class StopLossView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._mode = "fixed"
        self._calc_method = "ref"
        self._calc_tab_var = ctk.StringVar(value="Ref.")
        self._type_var = ctk.StringVar(value="Pontos")

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure((0, 1, 2), weight=1, uniform="stop-loss")

        self._build_header()
        self._build_fixed_card()
        self._build_calc_card()
        self._build_multiplier_card()

        self._set_mode("fixed")
        self._set_calc_method("ref")

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

        self._add_label(header, 0, "Tipo de stop", padx=16, pady=(16, 4))

        stop_type = self._create_combo(
            header,
            ["Pontos", "Percentual"],
            self._type_var,
        )
        stop_type.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Escolha como a distancia do stop sera interpretada nas configuracoes abaixo.",
            justify="left",
            anchor="w",
            wraplength=680,
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
        ).grid(row=1, column=1, sticky="ew", padx=(8, 16), pady=(0, 16))

    def _build_fixed_card(self) -> None:
        card = self._create_card(1, 0, "Stop loss (fixo)")
        self._fixed_checkbox = self._create_checkbox(
            card,
            "Usar stop loss fixo",
            lambda: self._set_mode("fixed"),
        )
        self._fixed_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))

        self._add_label(card, 2, "Distancia do stop")
        self._fixed_distance = self._create_entry(card, "100.0")
        self._fixed_distance.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))

    def _build_calc_card(self) -> None:
        card = self._create_card(1, 1, "Stop loss (calculo)")
        self._calc_checkbox = self._create_checkbox(
            card,
            "Usar calculo",
            lambda: self._set_mode("calc"),
        )
        self._calc_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 12))

        tabs_shell = ctk.CTkFrame(
            card,
            fg_color=self._theme.colors.surface_alt,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        tabs_shell.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=16, pady=(0, 16))
        tabs_shell.grid_columnconfigure(0, weight=1)
        tabs_shell.grid_rowconfigure(1, weight=1)
        card.grid_rowconfigure(2, weight=1)

        self._calc_tabs = ctk.CTkSegmentedButton(
            tabs_shell,
            values=["Ref.", "Med.", "Max/Min"],
            variable=self._calc_tab_var,
            command=self._on_tab_change,
            height=34,
            corner_radius=0,
            fg_color=self._theme.colors.sidebar_item_hover,
            selected_color=self._theme.colors.accent,
            selected_hover_color=self._theme.colors.accent_hover,
            unselected_color=self._theme.colors.surface,
            unselected_hover_color=self._theme.colors.card_soft,
            text_color=self._theme.colors.text,
            text_color_disabled=self._theme.colors.text_subtle,
            font=self._theme.font("label", weight="bold"),
        )
        self._calc_tabs.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self._calc_panels = ctk.CTkFrame(tabs_shell, fg_color="transparent")
        self._calc_panels.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self._calc_panels.grid_columnconfigure(0, weight=1)
        self._calc_panels.grid_rowconfigure(0, weight=1)

        self._calc_ref_panel = self._create_calc_panel()
        self._calc_ref_panel.grid_columnconfigure(0, weight=1)
        self._calc_ref_checkbox = self._create_checkbox(
            self._calc_ref_panel,
            "Referencia",
            lambda: self._set_calc_method("ref"),
        )
        self._calc_ref_checkbox.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 10))
        self._add_label(self._calc_ref_panel, 1, "Referencia:", padx=12)
        self._calc_ref_base = self._create_combo(
            self._calc_ref_panel,
            ["Maxima", "Minima", "Abertura", "Fechamento"],
            ctk.StringVar(value="Maxima"),
        )
        self._calc_ref_base.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_ref_panel, 3, "Candle:", padx=12)
        self._calc_ref_candle = self._create_combo(
            self._calc_ref_panel,
            ["Atual", "Ultimo", "Penultimo", "Antepenultimo"],
            ctk.StringVar(value="Atual"),
        )
        self._calc_ref_candle.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_ref_panel, 5, "Distancia:", padx=12)
        self._calc_ref_distance = self._create_entry(self._calc_ref_panel, "0.0")
        self._calc_ref_distance.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_ref_panel, 7, "Expirar:", padx=12)
        self._calc_ref_expire = self._create_combo(
            self._calc_ref_panel,
            ["Nao expirar", "1 candle", "2 candles", "3 candles", "4 candles"],
            ctk.StringVar(value="Nao expirar"),
        )
        self._calc_ref_expire.grid(row=8, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._calc_med_panel = self._create_calc_panel()
        self._calc_med_panel.grid_columnconfigure(0, weight=1)
        self._calc_med_checkbox = self._create_checkbox(
            self._calc_med_panel,
            "Media",
            lambda: self._set_calc_method("med"),
        )
        self._calc_med_checkbox.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 10))
        self._add_label(self._calc_med_panel, 1, "Qtd candles", padx=12)
        self._calc_med_candles = self._create_entry(self._calc_med_panel, "3")
        self._calc_med_candles.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_med_panel, 3, "Referencia:", padx=12)
        self._calc_med_base = self._create_combo(
            self._calc_med_panel,
            ["Maxima", "Minima", "Abertura", "Fechamento"],
            ctk.StringVar(value="Maxima"),
        )
        self._calc_med_base.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_med_panel, 5, "Distancia:", padx=12)
        self._calc_med_distance = self._create_entry(self._calc_med_panel, "0.0")
        self._calc_med_distance.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_med_panel, 7, "Expirar:", padx=12)
        self._calc_med_expire = self._create_combo(
            self._calc_med_panel,
            ["Nao expirar", "1 candle", "2 candles", "3 candles", "4 candles"],
            ctk.StringVar(value="Nao expirar"),
        )
        self._calc_med_expire.grid(row=8, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._calc_max_panel = self._create_calc_panel()
        self._calc_max_panel.grid_columnconfigure(0, weight=1)
        self._calc_max_checkbox = self._create_checkbox(
            self._calc_max_panel,
            "Max/Min",
            lambda: self._set_calc_method("maxmin"),
        )
        self._calc_max_checkbox.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 10))
        self._add_label(self._calc_max_panel, 1, "Base:", padx=12)
        self._calc_max_base = self._create_combo(
            self._calc_max_panel,
            ["Maxima", "Minima", "Abertura", "Fechamento"],
            ctk.StringVar(value="Maxima"),
        )
        self._calc_max_base.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._calc_max_panel, 3, "Dos ultimos:", padx=12)
        self._calc_max_count = self._create_entry(self._calc_max_panel, "3")
        self._calc_max_count.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._calc_panel_map = {
            "ref": self._calc_ref_panel,
            "med": self._calc_med_panel,
            "maxmin": self._calc_max_panel,
        }

    def _build_multiplier_card(self) -> None:
        card = self._create_card(1, 2, "Stop loss (multiplicador)")
        self._mult_checkbox = self._create_checkbox(
            card,
            "Usar multiplicador",
            lambda: self._set_mode("mult"),
        )
        self._mult_checkbox.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))

        self._add_label(card, 2, "Base da referencia")
        self._mult_base = self._create_combo(
            card,
            ["Corpo do candle", "Range (pavio a pavio)"],
            ctk.StringVar(value="Corpo do candle"),
        )
        self._mult_base.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 4, "Candle de referencia")
        self._mult_candle = self._create_combo(
            card,
            ["Atual", "Ultimo", "Penultimo", "Antepenultimo"],
            ctk.StringVar(value="Penultimo"),
        )
        self._mult_candle.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 6, "Multiplicador")
        self._mult_value = self._create_entry(card, "1.0")
        self._mult_value.grid(row=7, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))

    def _create_card(self, row: int, column: int, title: str) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            self._scroll,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=row, column=column, sticky="nsew", padx=6, pady=4)
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

    def _create_calc_panel(self) -> ctk.CTkFrame:
        panel = ctk.CTkFrame(
            self._calc_panels,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        return panel

    def _create_checkbox(self, master, text: str, command) -> ctk.CTkCheckBox:
        checkbox = ctk.CTkCheckBox(
            master,
            text=text,
            fg_color=self._theme.colors.accent,
            hover_color=self._theme.colors.accent_hover,
            border_color=self._theme.colors.border_strong,
            text_color=self._theme.colors.text,
            font=self._theme.font("body"),
            command=command,
        )
        return checkbox

    def _create_combo(
        self,
        master,
        values: list[str],
        variable: ctk.StringVar,
    ) -> ctk.CTkComboBox:
        combo = ctk.CTkComboBox(
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
        return combo

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

    def _on_tab_change(self, selected: str) -> None:
        mapping = {"Ref.": "ref", "Med.": "med", "Max/Min": "maxmin"}
        self._set_calc_method(mapping[selected])

    def _set_mode(self, mode: str) -> None:
        self._mode = mode

        if mode == "fixed":
            self._fixed_checkbox.select()
            self._calc_checkbox.deselect()
            self._mult_checkbox.deselect()
        elif mode == "calc":
            self._fixed_checkbox.deselect()
            self._calc_checkbox.select()
            self._mult_checkbox.deselect()
        else:
            self._fixed_checkbox.deselect()
            self._calc_checkbox.deselect()
            self._mult_checkbox.select()

        self._fixed_distance.configure(state="normal" if mode == "fixed" else "disabled")
        self._mult_base.configure(state="readonly" if mode == "mult" else "disabled")
        self._mult_candle.configure(state="readonly" if mode == "mult" else "disabled")
        self._mult_value.configure(state="normal" if mode == "mult" else "disabled")
        self._calc_tabs.configure(state="normal" if mode == "calc" else "disabled")

        self._sync_calc_method_controls()

    def _set_calc_method(self, method: str) -> None:
        self._calc_method = method
        labels = {"ref": "Ref.", "med": "Med.", "maxmin": "Max/Min"}
        self._calc_tab_var.set(labels[method])

        self._calc_ref_checkbox.select() if method == "ref" else self._calc_ref_checkbox.deselect()
        self._calc_med_checkbox.select() if method == "med" else self._calc_med_checkbox.deselect()
        self._calc_max_checkbox.select() if method == "maxmin" else self._calc_max_checkbox.deselect()

        for name, panel in self._calc_panel_map.items():
            if name == method:
                panel.grid(row=0, column=0, sticky="nsew")
            else:
                panel.grid_forget()

        self._sync_calc_method_controls()

    def _sync_calc_method_controls(self) -> None:
        calc_enabled = self._mode == "calc"
        ref_enabled = calc_enabled and self._calc_method == "ref"
        med_enabled = calc_enabled and self._calc_method == "med"
        max_enabled = calc_enabled and self._calc_method == "maxmin"

        self._calc_ref_checkbox.configure(state="normal" if calc_enabled else "disabled")
        self._calc_med_checkbox.configure(state="normal" if calc_enabled else "disabled")
        self._calc_max_checkbox.configure(state="normal" if calc_enabled else "disabled")

        self._calc_ref_base.configure(state="readonly" if ref_enabled else "disabled")
        self._calc_ref_candle.configure(state="readonly" if ref_enabled else "disabled")
        self._calc_ref_expire.configure(state="readonly" if ref_enabled else "disabled")
        self._calc_ref_distance.configure(state="normal" if ref_enabled else "disabled")

        self._calc_med_base.configure(state="readonly" if med_enabled else "disabled")
        self._calc_med_expire.configure(state="readonly" if med_enabled else "disabled")
        self._calc_med_candles.configure(state="normal" if med_enabled else "disabled")
        self._calc_med_distance.configure(state="normal" if med_enabled else "disabled")

        self._calc_max_base.configure(state="readonly" if max_enabled else "disabled")
        self._calc_max_count.configure(state="normal" if max_enabled else "disabled")

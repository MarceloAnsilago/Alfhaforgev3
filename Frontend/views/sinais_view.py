import customtkinter as ctk

from models.initial_settings import build_initial_settings_options
from themes.theme import UITheme


class SinaisView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme
        self._initial_options = build_initial_settings_options()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._tab_var = ctk.StringVar(value="Sinais")

        self._tabs = ctk.CTkSegmentedButton(
            self,
            values=["Sinais", "Montar sinais"],
            variable=self._tab_var,
            command=self._on_tab_change,
            height=34,
            corner_radius=0,
            fg_color=self._theme.colors.header_dark,
            selected_color=self._theme.colors.accent,
            selected_hover_color=self._theme.colors.accent_hover,
            unselected_color=self._theme.colors.header_dark,
            unselected_hover_color=self._theme.colors.sidebar_item_hover,
            text_color=self._theme.colors.header_text,
            text_color_disabled=self._theme.colors.card_soft,
            font=self._theme.font("label", weight="bold"),
        )
        self._tabs.grid(row=0, column=0, sticky="ew", pady=(4, 10))

        self._body = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self._body.grid(row=1, column=0, sticky="nsew")
        self._body.grid_columnconfigure(0, weight=1)
        self._body.grid_rowconfigure(0, weight=1)

        self._sinais_panel = self._create_sinais_panel()
        self._montar_panel = self._create_panel(
            "Montar sinais",
            "Estrutura base pronta. Na proxima etapa entram os slots e a composicao logica dos sinais.",
        )

        self._set_tab("Sinais")

    def _create_sinais_panel(self) -> ctk.CTkFrame:
        panel = ctk.CTkFrame(
            self._body,
            fg_color=self._theme.colors.card_soft,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        panel.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="sinais-grid")
        panel.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            panel,
            text="Sinais",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=5, sticky="ew", padx=18, pady=(18, 6))

        ctk.CTkLabel(
            panel,
            text="Primeira etapa da construcao dos sinais. O card de tipo de ordens foi migrado do V2.",
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
            justify="left",
            anchor="w",
            wraplength=980,
        ).grid(row=1, column=0, columnspan=5, sticky="ew", padx=18, pady=(0, 18))

        self._build_tipo_ordens_card(panel)
        self._build_filtro_card(panel)
        self._build_canais_card(panel)

        return panel

    def _build_tipo_ordens_card(self, panel: ctk.CTkFrame) -> None:
        card = ctk.CTkFrame(
            panel,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=2, column=0, sticky="nsew", padx=(18, 6), pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)
        card.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            card,
            text="Tipo de ordens",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))

        self._ordem_mode = ctk.StringVar(value="Mercado")
        self._ordem_market = self._create_checkbox(
            card,
            "Mercado",
            lambda: self._set_ordem_mode("Mercado"),
        )
        self._ordem_market.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        self._ordem_limit = self._create_checkbox(
            card,
            "Limite",
            lambda: self._set_ordem_mode("Limite"),
        )
        self._ordem_limit.grid(row=1, column=1, sticky="w", padx=(0, 16), pady=(0, 12))

        self._ord_tab_var = ctk.StringVar(value="Referencia")
        self._ord_tabs = ctk.CTkSegmentedButton(
            card,
            values=["Referencia", "Media"],
            variable=self._ord_tab_var,
            command=self._on_ord_tab_change,
            height=32,
            corner_radius=0,
            fg_color=self._theme.colors.header_dark,
            selected_color=self._theme.colors.accent,
            selected_hover_color=self._theme.colors.accent_hover,
            unselected_color=self._theme.colors.header_dark,
            unselected_hover_color=self._theme.colors.sidebar_item_hover,
            text_color=self._theme.colors.header_text,
            text_color_disabled=self._theme.colors.card_soft,
            font=self._theme.font("label", weight="bold"),
        )
        self._ord_tabs.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._ord_panel_shell = ctk.CTkFrame(
            card,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self._ord_panel_shell.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=16, pady=(0, 16))
        self._ord_panel_shell.grid_columnconfigure(0, weight=1)
        self._ord_panel_shell.grid_rowconfigure(0, weight=1)

        self._ord_ref_panel = self._create_subpanel(self._ord_panel_shell)
        self._ord_ref_panel.grid_columnconfigure(0, weight=1)
        self._ord_ref_check = self._create_checkbox(
            self._ord_ref_panel,
            "Referencia",
            lambda: self._set_ord_tab("Referencia"),
        )
        self._ord_ref_check.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 10))
        self._add_label(self._ord_ref_panel, 1, "Referencia:", padx=12)
        self._ord_ref_base = self._create_combo(
            self._ord_ref_panel,
            ["Maxima", "Minima", "Abertura", "Fechamento"],
            ctk.StringVar(value="Maxima"),
        )
        self._ord_ref_base.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._ord_ref_panel, 3, "Candle:", padx=12)
        self._ord_ref_candle = self._create_combo(
            self._ord_ref_panel,
            ["Atual", "Ultimo", "Penultimo", "Antepenultimo"],
            ctk.StringVar(value="Atual"),
        )
        self._ord_ref_candle.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._ord_ref_panel, 5, "Distancia", padx=12)
        self._ord_ref_distance = self._create_entry(self._ord_ref_panel, "0")
        self._ord_ref_distance.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._ord_ref_panel, 7, "Expirar:", padx=12)
        self._ord_ref_expire = self._create_combo(
            self._ord_ref_panel,
            ["Nao expirar", "1 candle", "2 candles", "3 candles", "4 candles"],
            ctk.StringVar(value="Nao expirar"),
        )
        self._ord_ref_expire.grid(row=8, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._ord_media_panel = self._create_subpanel(self._ord_panel_shell)
        self._ord_media_panel.grid_columnconfigure(0, weight=1)
        self._ord_media_check = self._create_checkbox(
            self._ord_media_panel,
            "Media",
            lambda: self._set_ord_tab("Media"),
        )
        self._ord_media_check.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 10))
        self._add_label(self._ord_media_panel, 1, "Cand. media", padx=12)
        self._ord_media_candles = self._create_entry(self._ord_media_panel, "0")
        self._ord_media_candles.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._ord_media_panel, 3, "Referencia:", padx=12)
        self._ord_media_base = self._create_combo(
            self._ord_media_panel,
            ["Maxima", "Minima", "Abertura", "Fechamento"],
            ctk.StringVar(value="Maxima"),
        )
        self._ord_media_base.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._ord_media_panel, 5, "Distancia", padx=12)
        self._ord_media_distance = self._create_entry(self._ord_media_panel, "0")
        self._ord_media_distance.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._ord_media_panel, 7, "Expirar:", padx=12)
        self._ord_media_expire = self._create_combo(
            self._ord_media_panel,
            ["Nao expirar", "1 candle", "2 candles", "3 candles", "4 candles"],
            ctk.StringVar(value="Nao expirar"),
        )
        self._ord_media_expire.grid(row=8, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._set_ordem_mode("Mercado")
        self._set_ord_tab("Referencia")

    def _build_filtro_card(self, panel: ctk.CTkFrame) -> None:
        card = ctk.CTkFrame(
            panel,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=2, column=1, sticky="nsew", padx=6, pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text="Usar filtro",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))

        self._filtro_enabled = self._create_checkbox(card, "Ativar filtro", lambda: None)
        self._filtro_enabled.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))

        self._add_label(card, 2, "Medir em")
        self._filtro_measure = self._create_combo(
            card,
            ["Pontos", "Percentual"],
            ctk.StringVar(value="Pontos"),
        )
        self._filtro_measure.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 4, "Tempo grafico")
        self._filtro_timeframe = self._create_combo(
            card,
            self._initial_options.tempos_graficos,
            ctk.StringVar(value="Corrente"),
        )
        self._filtro_timeframe.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        filtro_labels = ["Tam. min da vela", "Tam. max", "Min. pavios", "Max. pavios"]
        filtro_defaults = ["0", "0", "0", "0"]
        self._filtro_entries = []
        row = 6
        for label, default in zip(filtro_labels, filtro_defaults):
            self._add_label(card, row, label)
            entry = self._create_entry(card, default)
            entry.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))
            self._filtro_entries.append(entry)
            row += 2

    def _build_canais_card(self, panel: ctk.CTkFrame) -> None:
        card = ctk.CTkFrame(
            panel,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=2, column=2, sticky="nsew", padx=6, pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text="Canais de bandas",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))

        self._add_label(card, 1, "Usar canais de bandas?", pady=(0, 6))
        self._canais_mode = ctk.StringVar(value="Nao")
        self._canais_yes = self._create_checkbox(
            card,
            "Sim",
            lambda: self._set_canais_mode("Sim"),
        )
        self._canais_yes.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

        self._canais_no = self._create_checkbox(
            card,
            "Nao",
            lambda: self._set_canais_mode("Nao"),
        )
        self._canais_no.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=(0, 12))

        self._add_label(card, 3, "Indicador")
        self._canais_indicador = self._create_combo(
            card,
            ["Bandas de Bollinger", "Envelope", "Keltner", "Donchian", "Canal ATR"],
            ctk.StringVar(value="Bandas de Bollinger"),
        )
        self._canais_indicador.grid(row=4, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 5, "Sinais")
        self._canais_sinal = self._create_combo(
            card,
            [
                "Fechou fora",
                "Fechou dentro e saiu",
                "Fechou dentro e fechou fora",
                "Fechou fora e voltou",
                "Fechou fora e fechou dentro",
                "Estando fora",
            ],
            ctk.StringVar(value="Fechou fora"),
        )
        self._canais_sinal.grid(row=6, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 7, "Periodo")
        self._canais_periodo = self._create_entry(card, "20")
        self._canais_periodo.grid(row=8, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 9, "Desvio")
        self._canais_desvio = self._create_entry(card, "2.0")
        self._canais_desvio.grid(row=10, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 11, "Deslocamento")
        self._canais_deslocamento = self._create_entry(card, "0")
        self._canais_deslocamento.grid(row=12, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 13, "Modo de preco")
        self._canais_preco = self._create_combo(
            card,
            ["Fechamento", "Abertura", "Maximo", "Minimo", "Mediano", "Tipico", "Medio"],
            ctk.StringVar(value="Fechamento"),
        )
        self._canais_preco.grid(row=14, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

        self._set_canais_mode("Nao")

    def _create_panel(self, title: str, description: str) -> ctk.CTkFrame:
        panel = ctk.CTkFrame(
            self._body,
            fg_color=self._theme.colors.card_soft,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            panel,
            text=title,
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 6))

        ctk.CTkLabel(
            panel,
            text=description,
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
            justify="left",
            anchor="w",
            wraplength=900,
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))

        content_placeholder = ctk.CTkFrame(
            panel,
            fg_color=self._theme.colors.surface,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        content_placeholder.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        content_placeholder.grid_columnconfigure(0, weight=1)
        content_placeholder.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            content_placeholder,
            text="Area reservada para a proxima etapa.",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("body"),
            justify="center",
        ).grid(row=0, column=0)

        return panel

    def _create_subpanel(self, master) -> ctk.CTkFrame:
        return ctk.CTkFrame(
            master,
            fg_color=self._theme.colors.surface,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )

    def _create_checkbox(self, master, text: str, command) -> ctk.CTkCheckBox:
        return ctk.CTkCheckBox(
            master,
            text=text,
            fg_color=self._theme.colors.accent,
            hover_color=self._theme.colors.accent_hover,
            border_color=self._theme.colors.border_strong,
            text_color=self._theme.colors.text,
            font=self._theme.font("body"),
            command=command,
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

    def _on_tab_change(self, selected: str) -> None:
        self._set_tab(selected)

    def _on_ord_tab_change(self, selected: str) -> None:
        self._set_ord_tab(selected)

    def _set_tab(self, name: str) -> None:
        self._tab_var.set(name)

        if name == "Sinais":
            self._montar_panel.grid_forget()
            self._sinais_panel.grid(row=0, column=0, sticky="nsew")
            return

        self._sinais_panel.grid_forget()
        self._montar_panel.grid(row=0, column=0, sticky="nsew")

    def _set_ordem_mode(self, mode: str) -> None:
        self._ordem_mode.set(mode)
        self._ordem_market.select() if mode == "Mercado" else self._ordem_market.deselect()
        self._ordem_limit.select() if mode == "Limite" else self._ordem_limit.deselect()
        self._sync_ordem_controls()

    def _set_ord_tab(self, tab_name: str) -> None:
        self._ord_tab_var.set(tab_name)

        self._ord_ref_check.select() if tab_name == "Referencia" else self._ord_ref_check.deselect()
        self._ord_media_check.select() if tab_name == "Media" else self._ord_media_check.deselect()

        if tab_name == "Referencia":
            self._ord_media_panel.grid_forget()
            self._ord_ref_panel.grid(row=0, column=0, sticky="nsew")
            self._sync_ordem_controls()
            return

        self._ord_ref_panel.grid_forget()
        self._ord_media_panel.grid(row=0, column=0, sticky="nsew")
        self._sync_ordem_controls()

    def _set_canais_mode(self, mode: str) -> None:
        self._canais_mode.set(mode)
        enabled = mode == "Sim"
        self._canais_yes.select() if enabled else self._canais_yes.deselect()
        self._canais_no.select() if not enabled else self._canais_no.deselect()

        self._canais_indicador.configure(state="readonly" if enabled else "disabled")
        self._canais_sinal.configure(state="readonly" if enabled else "disabled")
        self._canais_periodo.configure(state="normal" if enabled else "disabled")
        self._canais_desvio.configure(state="normal" if enabled else "disabled")
        self._canais_deslocamento.configure(state="normal" if enabled else "disabled")
        self._canais_preco.configure(state="readonly" if enabled else "disabled")

    def _sync_ordem_controls(self) -> None:
        tabs_enabled = self._ordem_mode.get() == "Limite"
        self._ord_tabs.configure(state="normal" if tabs_enabled else "disabled")
        self._ord_ref_check.configure(state="normal" if tabs_enabled else "disabled")
        self._ord_media_check.configure(state="normal" if tabs_enabled else "disabled")

        ref_enabled = tabs_enabled and self._ord_tab_var.get() == "Referencia"
        media_enabled = tabs_enabled and self._ord_tab_var.get() == "Media"

        self._ord_ref_base.configure(state="readonly" if ref_enabled else "disabled")
        self._ord_ref_candle.configure(state="readonly" if ref_enabled else "disabled")
        self._ord_ref_distance.configure(state="normal" if ref_enabled else "disabled")
        self._ord_ref_expire.configure(state="readonly" if ref_enabled else "disabled")

        self._ord_media_candles.configure(state="normal" if media_enabled else "disabled")
        self._ord_media_base.configure(state="readonly" if media_enabled else "disabled")
        self._ord_media_distance.configure(state="normal" if media_enabled else "disabled")
        self._ord_media_expire.configure(state="readonly" if media_enabled else "disabled")

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
        self._build_cruzamentos_card(panel)
        self._build_sobre_card(panel)

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

    def _build_cruzamentos_card(self, panel: ctk.CTkFrame) -> None:
        card = ctk.CTkFrame(
            panel,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=2, column=3, sticky="nsew", padx=6, pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)
        card.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(
            card,
            text="Cruzamentos",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))

        self._add_label(card, 1, "Usar cruzamentos", pady=(0, 6))
        self._cruz_mode = ctk.StringVar(value="Nao")
        self._cruz_yes = self._create_checkbox(
            card,
            "Sim",
            lambda: self._set_cruz_mode("Sim"),
        )
        self._cruz_yes.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

        self._cruz_no = self._create_checkbox(
            card,
            "Nao",
            lambda: self._set_cruz_mode("Nao"),
        )
        self._cruz_no.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=(0, 12))

        self._cruz_tab_var = ctk.StringVar(value="Geral")
        self._cruz_tabs = ctk.CTkSegmentedButton(
            card,
            values=["Geral", "Rapida", "Lenta"],
            variable=self._cruz_tab_var,
            command=self._on_cruz_tab_change,
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
        self._cruz_tabs.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._cruz_shell = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0, border_width=0)
        self._cruz_shell.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=16, pady=(0, 16))
        self._cruz_shell.grid_columnconfigure(0, weight=1)
        self._cruz_shell.grid_rowconfigure(0, weight=1)

        cruz_indic_items = [
            "Nao usar",
            "Fechamento da vela",
            "Abertura da vela",
            "Maxima da vela",
            "Minima da vela",
            "Media movel",
            "VIDYA",
            "DEMA",
            "TEMA",
            "FRAMA",
        ]
        cruz_signal_items = ["Cruzamento para baixo", "Cruzamento para cima", "Ambos"]
        cruz_price_items = ["Fechamento", "Abertura", "Maximo", "Minimo", "Mediano", "Tipico", "Medio"]
        cruz_ma_items = ["Simples", "Exponencial", "Suavizada", "Linear ponderada", "Smoothed"]

        self._cruz_geral_panel = self._create_subpanel(self._cruz_shell)
        self._cruz_geral_panel.grid_columnconfigure(0, weight=1)
        self._add_label(self._cruz_geral_panel, 0, "Linha rapida", padx=12, pady=(12, 4))
        self._cruz_fast_combo = self._create_combo(
            self._cruz_geral_panel,
            cruz_indic_items,
            ctk.StringVar(value="Nao usar"),
        )
        self._cruz_fast_combo.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_geral_panel, 2, "Sinal", padx=12)
        self._cruz_signal_combo = self._create_combo(
            self._cruz_geral_panel,
            cruz_signal_items,
            ctk.StringVar(value="Cruzamento para baixo"),
        )
        self._cruz_signal_combo.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_geral_panel, 4, "Linha lenta", padx=12)
        self._cruz_slow_combo = self._create_combo(
            self._cruz_geral_panel,
            cruz_indic_items,
            ctk.StringVar(value="Nao usar"),
        )
        self._cruz_slow_combo.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 10))
        ctk.CTkLabel(
            self._cruz_geral_panel,
            text="As abas Rapida e Lenta acompanham o indicador escolhido aqui.",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("label"),
            justify="left",
            wraplength=220,
            anchor="w",
        ).grid(row=6, column=0, sticky="ew", padx=12, pady=(4, 12))

        self._cruz_rapida_panel = self._create_subpanel(self._cruz_shell)
        self._cruz_rapida_panel.grid_columnconfigure(0, weight=1)
        self._add_label(self._cruz_rapida_panel, 0, "Indicador rapido", padx=12, pady=(12, 4))
        self._cruz_fast_indicator = self._create_combo(
            self._cruz_rapida_panel,
            cruz_indic_items,
            ctk.StringVar(value="Nao usar"),
        )
        self._cruz_fast_indicator.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._cruz_fast_params = self._create_subpanel(self._cruz_rapida_panel)
        self._cruz_fast_params.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self._cruz_fast_params.grid_columnconfigure(0, weight=1)
        self._add_label(self._cruz_fast_params, 0, "Periodo", padx=12, pady=(12, 4))
        self._cruz_fast_period = self._create_entry(self._cruz_fast_params, "14")
        self._cruz_fast_period.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_fast_params, 2, "Deslocamento", padx=12)
        self._cruz_fast_shift = self._create_entry(self._cruz_fast_params, "0")
        self._cruz_fast_shift.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_fast_params, 4, "Tipo de media", padx=12)
        self._cruz_fast_ma_type = self._create_combo(
            self._cruz_fast_params,
            cruz_ma_items,
            ctk.StringVar(value="Simples"),
        )
        self._cruz_fast_ma_type.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_fast_params, 6, "Modo de preco", padx=12)
        self._cruz_fast_price = self._create_combo(
            self._cruz_fast_params,
            cruz_price_items,
            ctk.StringVar(value="Fechamento"),
        )
        self._cruz_fast_price.grid(row=7, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._cruz_lenta_panel = self._create_subpanel(self._cruz_shell)
        self._cruz_lenta_panel.grid_columnconfigure(0, weight=1)
        self._add_label(self._cruz_lenta_panel, 0, "Indicador lento", padx=12, pady=(12, 4))
        self._cruz_slow_indicator = self._create_combo(
            self._cruz_lenta_panel,
            cruz_indic_items,
            ctk.StringVar(value="Fechamento da vela"),
        )
        self._cruz_slow_indicator.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._cruz_slow_params = self._create_subpanel(self._cruz_lenta_panel)
        self._cruz_slow_params.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self._cruz_slow_params.grid_columnconfigure(0, weight=1)
        self._add_label(self._cruz_slow_params, 0, "Periodo", padx=12, pady=(12, 4))
        self._cruz_slow_period = self._create_entry(self._cruz_slow_params, "21")
        self._cruz_slow_period.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_slow_params, 2, "Deslocamento", padx=12)
        self._cruz_slow_shift = self._create_entry(self._cruz_slow_params, "0")
        self._cruz_slow_shift.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_slow_params, 4, "Tipo de media", padx=12)
        self._cruz_slow_ma_type = self._create_combo(
            self._cruz_slow_params,
            cruz_ma_items,
            ctk.StringVar(value="Simples"),
        )
        self._cruz_slow_ma_type.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._cruz_slow_params, 6, "Modo de preco", padx=12)
        self._cruz_slow_price = self._create_combo(
            self._cruz_slow_params,
            cruz_price_items,
            ctk.StringVar(value="Fechamento"),
        )
        self._cruz_slow_price.grid(row=7, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._set_cruz_mode("Nao")
        self._set_cruz_tab("Geral")

    def _build_sobre_card(self, panel: ctk.CTkFrame) -> None:
        card = ctk.CTkFrame(
            panel,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=2, column=4, sticky="nsew", padx=(6, 18), pady=(0, 18))
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)
        card.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            card,
            text="Sobrecomprado / sobrevendido",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 16))

        self._sobre_enabled = self._create_checkbox(card, "Usar sobrecomprado / sobrevenda", lambda: self._toggle_sobre())
        self._sobre_enabled.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 12))

        self._sobre_tab_var = ctk.StringVar(value="Indicador")
        self._sobre_tabs = ctk.CTkSegmentedButton(
            card,
            values=["Indicador", "Parametros"],
            variable=self._sobre_tab_var,
            command=self._on_sobre_tab_change,
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
        self._sobre_tabs.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._sobre_shell = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0, border_width=0)
        self._sobre_shell.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=16, pady=(0, 16))
        self._sobre_shell.grid_columnconfigure(0, weight=1)
        self._sobre_shell.grid_rowconfigure(0, weight=1)

        sobre_indic_items = [
            "MACD",
            "Estocastico",
            "RSI",
            "DeMarker",
            "Regressao linear",
            "Desvio da media",
            "MFI",
            "Bears Power",
            "Bulls Power",
            "CCI",
            "Ichimoku Tenkan-sen",
            "Ichimoku Kijun-sen",
            "Ichimoku Senkou Span A",
            "Ichimoku Senkou Span B",
            "Ichimoku Chinkou Spa",
        ]
        sobre_entry_items = ["Ao entrar", "Ao sair", "Estando"]
        sobre_sentido_items = ["Sobrecompra compra", "Sobrecompra venda"]
        sobre_price_items = ["Fechamento", "Abertura", "Maximo", "Minimo", "Mediano", "Tipico", "Medio"]
        sobre_ma_items = ["Simples", "Exponencial", "Suavizada", "Linear ponderada", "Smoothed"]
        sobre_stoch_type_items = ["Minimo/Maximo", "Fechamento/Abertura"]
        sobre_volume_items = ["Tick", "Real"]

        self._sobre_indicator_panel = self._create_subpanel(self._sobre_shell)
        self._sobre_indicator_panel.grid_columnconfigure(0, weight=1)
        self._add_label(self._sobre_indicator_panel, 0, "Indicador", padx=12, pady=(12, 4))
        self._sobre_indicator_combo = self._create_combo(
            self._sobre_indicator_panel,
            sobre_indic_items,
            ctk.StringVar(value="MACD"),
        )
        self._sobre_indicator_combo.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._sobre_indicator_panel, 2, "Entrada", padx=12)
        self._sobre_entry_combo = self._create_combo(
            self._sobre_indicator_panel,
            sobre_entry_items,
            ctk.StringVar(value="Ao entrar"),
        )
        self._sobre_entry_combo.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._sobre_indicator_panel, 4, "Sobrecompra", padx=12)
        self._sobre_overbought = self._create_entry(self._sobre_indicator_panel, "2")
        self._sobre_overbought.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._sobre_indicator_panel, 6, "Sobrevenda", padx=12)
        self._sobre_oversold = self._create_entry(self._sobre_indicator_panel, "-2")
        self._sobre_oversold.grid(row=7, column=0, sticky="ew", padx=12, pady=(0, 10))
        self._add_label(self._sobre_indicator_panel, 8, "Sentido", padx=12)
        self._sobre_direction_combo = self._create_combo(
            self._sobre_indicator_panel,
            sobre_sentido_items,
            ctk.StringVar(value="Sobrecompra compra"),
        )
        self._sobre_direction_combo.grid(row=9, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._sobre_params_panel = self._create_subpanel(self._sobre_shell)
        self._sobre_params_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            self._sobre_params_panel,
            text="Os parametros acompanham o indicador selecionado na aba ao lado.",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("label"),
            justify="left",
            wraplength=220,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 12))

        self._sobre_param_groups: dict[str, list[ctk.CTkBaseClass]] = {}
        self._sobre_param_fields: dict[str, list[tuple[str, str, list[str] | None]]] = {
            "MACD": [
                ("EMA rapida", "12", None),
                ("EMA lenta", "16", None),
                ("Sinal", "9", None),
                ("Modo de preco", "Fechamento", sobre_price_items),
            ],
            "Estocastico": [
                ("K", "5", None),
                ("D", "3", None),
                ("Slowing", "3", None),
                ("Media", "Simples", sobre_ma_items),
                ("Tipo", "Minimo/Maximo", sobre_stoch_type_items),
            ],
            "RSI": [
                ("Periodo", "14", None),
                ("Modo de preco", "Fechamento", sobre_price_items),
            ],
            "DeMarker": [
                ("Periodo", "14", None),
            ],
            "Regressao linear": [
                ("Periodo", "20", None),
                ("Tipo de regressao", "Simples", sobre_ma_items),
                ("Modo de fechamento", "Fechamento", sobre_price_items),
            ],
            "Desvio da media": [
                ("Periodo", "20", None),
                ("Tipo de desvio", "Simples", sobre_ma_items),
                ("Modo de fechamento", "Fechamento", sobre_price_items),
            ],
            "MFI": [
                ("Periodo", "14", None),
                ("Volume", "Tick", sobre_volume_items),
            ],
            "Bears Power": [
                ("Periodo", "14", None),
            ],
            "Bulls Power": [
                ("Periodo", "14", None),
            ],
            "CCI": [
                ("Periodo", "14", None),
                ("Modo de preco", "Fechamento", sobre_price_items),
            ],
            "Ichimoku Tenkan-sen": [
                ("Tenkan-sen", "9", None),
                ("Kijun-sen", "26", None),
                ("Senkou Span B", "52", None),
            ],
            "Ichimoku Kijun-sen": [
                ("Tenkan-sen", "9", None),
                ("Kijun-sen", "26", None),
                ("Senkou Span B", "52", None),
            ],
            "Ichimoku Senkou Span A": [
                ("Tenkan-sen", "9", None),
                ("Kijun-sen", "26", None),
                ("Senkou Span B", "52", None),
            ],
            "Ichimoku Senkou Span B": [
                ("Tenkan-sen", "9", None),
                ("Kijun-sen", "26", None),
                ("Senkou Span B", "52", None),
            ],
            "Ichimoku Chinkou Spa": [
                ("Tenkan-sen", "9", None),
                ("Kijun-sen", "26", None),
                ("Senkou Span B", "52", None),
            ],
        }
        self._build_sobre_param_forms()

        self._sobre_indicator_combo.configure(command=self._on_sobre_indicator_change)
        self._set_sobre_tab("Indicador")
        self._show_sobre_param_group(self._sobre_indicator_combo.get())
        self._sync_sobre_controls()

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

    def _build_sobre_param_forms(self) -> None:
        for indicator_name, fields in self._sobre_param_fields.items():
            widgets: list[ctk.CTkBaseClass] = []
            row = 1
            title = ctk.CTkLabel(
                self._sobre_params_panel,
                text=indicator_name,
                text_color=self._theme.colors.text,
                font=self._theme.font("body", weight="bold"),
                anchor="w",
            )
            title.grid(row=row, column=0, sticky="ew", padx=12, pady=(0, 10))
            widgets.append(title)
            row += 1

            for label_text, default_value, combo_values in fields:
                label = ctk.CTkLabel(
                    self._sobre_params_panel,
                    text=label_text,
                    anchor="w",
                    text_color=self._theme.colors.text_muted,
                    font=self._theme.font("label"),
                )
                label.grid(row=row, column=0, sticky="ew", padx=12, pady=(0, 4))
                widgets.append(label)
                row += 1

                if combo_values is None:
                    control = self._create_entry(self._sobre_params_panel, default_value)
                else:
                    control = self._create_combo(
                        self._sobre_params_panel,
                        combo_values,
                        ctk.StringVar(value=default_value),
                    )
                control.grid(row=row, column=0, sticky="ew", padx=12, pady=(0, 10))
                widgets.append(control)
                row += 1

            self._sobre_param_groups[indicator_name] = widgets

    def _on_tab_change(self, selected: str) -> None:
        self._set_tab(selected)

    def _on_ord_tab_change(self, selected: str) -> None:
        self._set_ord_tab(selected)

    def _on_cruz_tab_change(self, selected: str) -> None:
        self._set_cruz_tab(selected)

    def _on_sobre_tab_change(self, selected: str) -> None:
        self._set_sobre_tab(selected)

    def _on_sobre_indicator_change(self, selected: str) -> None:
        self._show_sobre_param_group(selected)
        self._sync_sobre_controls()

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

    def _set_cruz_mode(self, mode: str) -> None:
        self._cruz_mode.set(mode)
        enabled = mode == "Sim"
        self._cruz_yes.select() if enabled else self._cruz_yes.deselect()
        self._cruz_no.select() if not enabled else self._cruz_no.deselect()
        self._cruz_tabs.configure(state="normal" if enabled else "disabled")
        self._sync_cruz_controls()

    def _set_cruz_tab(self, tab_name: str) -> None:
        self._cruz_tab_var.set(tab_name)
        self._cruz_geral_panel.grid_forget()
        self._cruz_rapida_panel.grid_forget()
        self._cruz_lenta_panel.grid_forget()

        if tab_name == "Geral":
            self._cruz_geral_panel.grid(row=0, column=0, sticky="nsew")
        elif tab_name == "Rapida":
            self._cruz_rapida_panel.grid(row=0, column=0, sticky="nsew")
        else:
            self._cruz_lenta_panel.grid(row=0, column=0, sticky="nsew")

        self._sync_cruz_controls()

    def _set_sobre_tab(self, tab_name: str) -> None:
        self._sobre_tab_var.set(tab_name)
        self._sobre_indicator_panel.grid_forget()
        self._sobre_params_panel.grid_forget()

        if tab_name == "Indicador":
            self._sobre_indicator_panel.grid(row=0, column=0, sticky="nsew")
        else:
            self._sobre_params_panel.grid(row=0, column=0, sticky="nsew")

        self._sync_sobre_controls()

    def _sync_cruz_controls(self) -> None:
        enabled = self._cruz_mode.get() == "Sim"
        active_tab = self._cruz_tab_var.get()

        self._cruz_fast_combo.configure(state="readonly" if enabled and active_tab == "Geral" else "disabled")
        self._cruz_signal_combo.configure(state="readonly" if enabled and active_tab == "Geral" else "disabled")
        self._cruz_slow_combo.configure(state="readonly" if enabled and active_tab == "Geral" else "disabled")

        fast_enabled = enabled and active_tab == "Rapida"
        self._cruz_fast_indicator.configure(state="readonly" if fast_enabled else "disabled")
        self._cruz_fast_period.configure(state="normal" if fast_enabled else "disabled")
        self._cruz_fast_shift.configure(state="normal" if fast_enabled else "disabled")
        self._cruz_fast_ma_type.configure(state="readonly" if fast_enabled else "disabled")
        self._cruz_fast_price.configure(state="readonly" if fast_enabled else "disabled")

        slow_enabled = enabled and active_tab == "Lenta"
        self._cruz_slow_indicator.configure(state="readonly" if slow_enabled else "disabled")
        self._cruz_slow_period.configure(state="normal" if slow_enabled else "disabled")
        self._cruz_slow_shift.configure(state="normal" if slow_enabled else "disabled")
        self._cruz_slow_ma_type.configure(state="readonly" if slow_enabled else "disabled")
        self._cruz_slow_price.configure(state="readonly" if slow_enabled else "disabled")

    def _toggle_sobre(self) -> None:
        self._sync_sobre_controls()

    def _show_sobre_param_group(self, indicator_name: str) -> None:
        for widgets in self._sobre_param_groups.values():
            for widget in widgets:
                widget.grid_remove()

        widgets = self._sobre_param_groups.get(indicator_name, [])
        for widget in widgets:
            widget.grid()

    def _sync_sobre_controls(self) -> None:
        enabled = self._sobre_enabled.get() == 1
        indicador_tab = self._sobre_tab_var.get() == "Indicador"
        parametros_tab = self._sobre_tab_var.get() == "Parametros"

        self._sobre_tabs.configure(state="normal" if enabled else "disabled")
        self._sobre_indicator_combo.configure(state="readonly" if enabled and indicador_tab else "disabled")
        self._sobre_entry_combo.configure(state="readonly" if enabled and indicador_tab else "disabled")
        self._sobre_overbought.configure(state="normal" if enabled and indicador_tab else "disabled")
        self._sobre_oversold.configure(state="normal" if enabled and indicador_tab else "disabled")
        self._sobre_direction_combo.configure(state="readonly" if enabled and indicador_tab else "disabled")

        current_indicator = self._sobre_indicator_combo.get()
        for indicator_name, widgets in self._sobre_param_groups.items():
            group_enabled = enabled and parametros_tab and indicator_name == current_indicator
            for widget in widgets:
                if isinstance(widget, ctk.CTkEntry):
                    widget.configure(state="normal" if group_enabled else "disabled")
                elif isinstance(widget, ctk.CTkComboBox):
                    widget.configure(state="readonly" if group_enabled else "disabled")

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

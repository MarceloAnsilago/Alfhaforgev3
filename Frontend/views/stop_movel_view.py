import customtkinter as ctk

from themes.theme import UITheme


class StopMovelView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._signal_var = ctk.StringVar(value="Compra")
        self._type_var = ctk.StringVar(value="Pontos")
        self._mode = "padrao"

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure((0, 1, 2), weight=1, uniform="stop-movel")

        self._build_header()
        self._build_padrao_card()
        self._build_candles_card()
        self._build_indicador_card()

        self._set_signal("Compra")
        self._set_mode("padrao")

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
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=1)

        self._add_label(header, 0, "Direcao do sinal", padx=16, pady=(16, 4))

        buy_check = self._create_checkbox(
            header,
            "Criar sinal de compra",
            lambda: self._set_signal("Compra"),
        )
        buy_check.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self._buy_check = buy_check

        sell_check = self._create_checkbox(
            header,
            "Criar sinal de venda",
            lambda: self._set_signal("Venda"),
        )
        sell_check.grid(row=1, column=1, sticky="w", padx=(0, 16), pady=(0, 8))
        self._sell_check = sell_check

        self._signal_info = ctk.CTkLabel(
            header,
            text="Configurando regras de stop movel para sinais de compra.",
            justify="left",
            anchor="w",
            wraplength=760,
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
        )
        self._signal_info.grid(row=2, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(header, 3, "Tipo de stop", padx=16)

        stop_type = self._create_combo(
            header,
            ["Pontos", "Percentual"],
            self._type_var,
        )
        stop_type.grid(row=4, column=0, sticky="w", padx=16, pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Escolha como a distancia do stop movel sera interpretada nos modos abaixo.",
            justify="left",
            anchor="w",
            wraplength=680,
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
        ).grid(row=4, column=1, columnspan=2, sticky="ew", padx=(8, 16), pady=(0, 16))

    def _build_padrao_card(self) -> None:
        card = self._create_card(1, 0, "Stop movel (padrao)")
        mode_check = self._create_checkbox(
            card,
            "Usar padrao",
            lambda: self._set_mode("padrao"),
        )
        mode_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))
        self._padrao_check = mode_check

        self._add_label(card, 2, "Adicionar a favor")
        self._padrao_add = self._create_entry(card, "0")
        self._padrao_add.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 4, "Passo")
        self._padrao_step = self._create_entry(card, "0")
        self._padrao_step.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))

    def _build_candles_card(self) -> None:
        card = self._create_card(1, 1, "Stop movel (candles)")
        mode_check = self._create_checkbox(
            card,
            "Candle a candle",
            lambda: self._set_mode("candles"),
        )
        mode_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))
        self._candles_check = mode_check

        candle_base = ["Atual", "Ultimo", "Penultimo", "Antepenultimo"]
        price_base = ["Maxima", "Minima", "Abertura", "Fechamento"]

        self._add_label(card, 2, "Disparo de distancia")
        self._candles_trigger = self._create_entry(card, "0.0")
        self._candles_trigger.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 4, "Posicao de referencia")
        self._candles_position = self._create_combo(card, candle_base, ctk.StringVar(value="Atual"))
        self._candles_position.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 6, "Base do candle")
        self._candles_price = self._create_combo(card, price_base, ctk.StringVar(value="Minima"))
        self._candles_price.grid(row=7, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 8, "Distancia do stop")
        self._candles_distance = self._create_entry(card, "0.0")
        self._candles_distance.grid(row=9, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))

    def _build_indicador_card(self) -> None:
        card = self._create_card(1, 2, "Stop movel (indicador)")
        mode_check = self._create_checkbox(
            card,
            "Usar indicador",
            lambda: self._set_mode("indicador"),
        )
        mode_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))
        self._indicador_check = mode_check

        self._add_label(card, 2, "Disparo de distancia")
        self._indicador_trigger = self._create_entry(card, "0.0")
        self._indicador_trigger.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))

        self._add_label(card, 4, "Indicador")
        self._indicador_type = self._create_combo(
            card,
            ["ATR", "Media movel", "Parabolic SAR", "Bandas de Bollinger", "Envelopes"],
            ctk.StringVar(value="ATR"),
        )
        self._indicador_type.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))

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

    def _set_signal(self, signal: str) -> None:
        self._signal_var.set(signal)
        is_buy = signal == "Compra"
        if is_buy:
            self._buy_check.select()
            self._sell_check.deselect()
            text = "Configurando regras de stop movel para sinais de compra."
        else:
            self._buy_check.deselect()
            self._sell_check.select()
            text = "Configurando regras de stop movel para sinais de venda."
        self._signal_info.configure(text=text)

    def _set_mode(self, mode: str) -> None:
        self._mode = mode

        self._padrao_check.select() if mode == "padrao" else self._padrao_check.deselect()
        self._candles_check.select() if mode == "candles" else self._candles_check.deselect()
        self._indicador_check.select() if mode == "indicador" else self._indicador_check.deselect()

        self._padrao_add.configure(state="normal" if mode == "padrao" else "disabled")
        self._padrao_step.configure(state="normal" if mode == "padrao" else "disabled")

        self._candles_trigger.configure(state="normal" if mode == "candles" else "disabled")
        self._candles_position.configure(state="readonly" if mode == "candles" else "disabled")
        self._candles_price.configure(state="readonly" if mode == "candles" else "disabled")
        self._candles_distance.configure(state="normal" if mode == "candles" else "disabled")

        self._indicador_trigger.configure(state="normal" if mode == "indicador" else "disabled")
        self._indicador_type.configure(state="readonly" if mode == "indicador" else "disabled")

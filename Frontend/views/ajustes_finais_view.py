import customtkinter as ctk

from themes.theme import UITheme


class AjustesFinaisView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme
        self._option_vars: list[ctk.StringVar] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure(0, weight=1)

        self._build_card()

    def _build_card(self) -> None:
        card = ctk.CTkFrame(
            self._scroll,
            fg_color=self._theme.colors.card,
            corner_radius=0,
            border_width=1,
            border_color=self._theme.colors.border,
        )
        card.grid(row=0, column=0, sticky="ew", padx=6, pady=(4, 10))
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            card,
            text="Ajustes finais",
            anchor="w",
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
        ).grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 6))

        ctk.CTkLabel(
            card,
            text="Migracao direta do V2: defina as regras finais de comportamento da estrategia com respostas Sim/Nao.",
            justify="left",
            anchor="w",
            wraplength=860,
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
        ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

        options = [
            "Cancelar pendente de entrada se aparecer sinal oposto",
            "Reposicionar stoploss no aumento a favor da operacao",
            "Reposicionar takeprofit no aumento contra a operacao",
            "Movimentar stoploss com base no preco medio",
            "Movimentar takeprofit com base no preco medio",
            "Usar preco medio como referencia das parciais",
            "Impedir sinal de saida na vela que gerou entrada",
            "Impedir sinal de entrada na vela que gerou saida",
            "Recalcular o preco medio com base nas saidas parciais",
        ]

        for index, option_text in enumerate(options, start=2):
            variable = ctk.StringVar(value="Nao")
            self._option_vars.append(variable)

            ctk.CTkLabel(
                card,
                text=option_text,
                anchor="w",
                justify="left",
                wraplength=740,
                text_color=self._theme.colors.text,
                font=self._theme.font("body"),
            ).grid(row=index, column=0, sticky="ew", padx=(16, 12), pady=(0, 12))

            combo = self._create_combo(card, ["Nao", "Sim"], variable)
            combo.grid(row=index, column=1, sticky="e", padx=(0, 16), pady=(0, 12))

    def export_config(self) -> list[dict[str, str]]:
        labels = [
            "cancelar_pendente_sinal_oposto",
            "reposicionar_stoploss_aumento_favor",
            "reposicionar_takeprofit_aumento_contra",
            "movimentar_stoploss_preco_medio",
            "movimentar_takeprofit_preco_medio",
            "usar_preco_medio_parciais",
            "impedir_saida_na_vela_entrada",
            "impedir_entrada_na_vela_saida",
            "recalcular_preco_medio_parciais",
        ]
        return [
            {
                "key": key,
                "value": variable.get(),
            }
            for key, variable in zip(labels, self._option_vars)
        ]

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
            width=120,
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

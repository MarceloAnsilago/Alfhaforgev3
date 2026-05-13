import customtkinter as ctk

from models.navigation import NavigationItem
from themes.theme import UITheme
from views.ajustes_finais_view import AjustesFinaisView
from views.break_even_view import BreakEvenView
from views.initial_settings_view import InitialSettingsView
from views.saidas_parciais_view import SaidasParciaisView
from views.sinais_view import SinaisView
from views.take_profit_view import TakeProfitView
from views.stop_movel_view import StopMovelView
from views.stop_loss_view import StopLossView
from views.trailing_stop_view import TrailingStopView


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme
        self._view_cache: dict[str, ctk.CTkBaseClass] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._hero = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self._hero.grid(row=0, column=0, sticky="ew")
        self._hero.grid_columnconfigure(0, weight=1)

        self._title = ctk.CTkLabel(
            self._hero,
            text="",
            anchor="w",
            text_color=theme.colors.text,
            font=theme.font("title"),
        )
        self._title.grid(row=0, column=0, sticky="ew", padx=0, pady=(12, 4))

        self._description = ctk.CTkLabel(
            self._hero,
            text="",
            justify="left",
            anchor="w",
            wraplength=780,
            text_color=theme.colors.text_muted,
            font=theme.font("body"),
        )
        self._description.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 8))

        self._placeholder = ctk.CTkFrame(
            self,
            fg_color=theme.colors.card_soft,
            corner_radius=0,
            border_width=1,
            border_color=theme.colors.border,
        )
        self._placeholder.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self._placeholder.grid_columnconfigure(0, weight=1)
        self._placeholder.grid_rowconfigure(0, weight=1)
        self._current_body = None

    def set_section(self, item: NavigationItem) -> None:
        self._title.configure(text=item.label)
        self._description.configure(text=item.description)
        self._render_body(item)

    def export_bridge_payload(self) -> dict[str, str]:
        payload = {
            "active_section": self._active_section_id(),
        }

        initial_view = self._view_cache.get("inf_iniciais")
        if initial_view is not None and hasattr(initial_view, "export_config"):
            config = initial_view.export_config()
            for key, value in config.items():
                payload[key] = str(value)

        ajustes_view = self._view_cache.get("ajustes_finais")
        if ajustes_view is not None and hasattr(ajustes_view, "export_config"):
            ajustes = ajustes_view.export_config()
            payload["final_adjustments_count"] = str(len(ajustes))

        sinais_view = self._view_cache.get("sinais")
        if sinais_view is not None and hasattr(sinais_view, "export_montar_signals_dict"):
            montar = sinais_view.export_montar_signals_dict()
            payload["signal_groups_count"] = str(len(montar.get("groups", [])))
            payload["signal_logic_rows_count"] = str(len(montar.get("logic_rows", [])))

        return payload

    def _render_body(self, item: NavigationItem) -> None:
        if self._current_body is not None:
            self._current_body.grid_remove()

        body = self._view_cache.get(item.item_id)
        if body is None:
            body = self._build_view(item)
            self._view_cache[item.item_id] = body

        body.grid()
        self._current_body = body

    def _build_view(self, item: NavigationItem) -> ctk.CTkBaseClass:
        if item.item_id == "inf_iniciais":
            return self._create_view(InitialSettingsView)

        if item.item_id == "stop_loss":
            return self._create_view(StopLossView)

        if item.item_id == "stop_movel":
            return self._create_view(StopMovelView)

        if item.item_id == "take_profit":
            return self._create_view(TakeProfitView)

        if item.item_id == "break_even":
            return self._create_view(BreakEvenView)

        if item.item_id == "trailing_stop":
            return self._create_view(TrailingStopView)

        if item.item_id == "saidas_parciais":
            return self._create_view(SaidasParciaisView)

        if item.item_id == "sinais":
            return self._create_view(SinaisView)

        if item.item_id == "ajustes_finais":
            return self._create_view(AjustesFinaisView)

        content = ctk.CTkFrame(self._placeholder, fg_color="transparent")
        content.grid(row=0, column=0, sticky="")

        ctk.CTkLabel(
            content,
            text=item.label,
            text_color=self._theme.colors.text,
            font=self._theme.font("subtitle"),
        ).pack(anchor="center")

        ctk.CTkLabel(
            content,
            text="Conteudo ainda nao implementado.",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("body"),
            justify="center",
            wraplength=520,
        ).pack(anchor="center", pady=(10, 0))
        return content

    def _create_view(self, view_class):
        view = view_class(self._placeholder, self._theme)
        view.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
        view.grid_remove()
        return view

    def _active_section_id(self) -> str:
        for item_id, body in self._view_cache.items():
            if body == self._current_body:
                return item_id
        return ""

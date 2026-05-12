import customtkinter as ctk

from models.navigation import NavigationItem
from themes.theme import UITheme
from views.initial_settings_view import InitialSettingsView
from views.stop_movel_view import StopMovelView
from views.stop_loss_view import StopLossView


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, theme: UITheme) -> None:
        super().__init__(master, fg_color="transparent")
        self._theme = theme

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

    def _render_body(self, item: NavigationItem) -> None:
        if self._current_body is not None:
            self._current_body.destroy()

        if item.item_id == "inf_iniciais":
            self._current_body = InitialSettingsView(self._placeholder, self._theme)
            self._current_body.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
            return

        if item.item_id == "stop_loss":
            self._current_body = StopLossView(self._placeholder, self._theme)
            self._current_body.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
            return

        if item.item_id == "stop_movel":
            self._current_body = StopMovelView(self._placeholder, self._theme)
            self._current_body.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
            return

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
        self._current_body = content

import customtkinter as ctk

from models.navigation import NavigationItem
from themes.theme import UITheme


class SidebarNavItem(ctk.CTkFrame):
    def __init__(self, master, item: NavigationItem, theme: UITheme, command) -> None:
        super().__init__(
            master,
            fg_color=theme.colors.sidebar,
            corner_radius=0,
            border_width=0,
            height=34,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self._item = item
        self._theme = theme
        self._command = command
        self._active = False

        self._label = ctk.CTkLabel(
            self,
            text=item.label,
            anchor="w",
            text_color=theme.colors.text_muted,
            font=theme.font("body"),
        )
        self._label.grid(row=0, column=0, sticky="ew", padx=12, pady=7)

        self._bind_recursive("<Enter>", self._on_enter)
        self._bind_recursive("<Leave>", self._on_leave)
        self._bind_recursive("<Button-1>", self._on_click)

    def set_active(self, active: bool) -> None:
        self._active = active
        if active:
            self.configure(fg_color=self._theme.colors.sidebar_item_active)
            self._label.configure(
                text_color=self._theme.colors.text,
                font=self._theme.font("body", weight="bold"),
            )
            return

        self.configure(fg_color=self._theme.colors.sidebar)
        self._label.configure(
            text_color=self._theme.colors.text_muted,
            font=self._theme.font("body"),
        )

    def _bind_recursive(self, sequence: str, callback) -> None:
        for widget in [self, self._label]:
            widget.bind(sequence, callback)

    def _on_enter(self, _event) -> None:
        if not self._active:
            self.configure(fg_color=self._theme.colors.sidebar_item_hover)

    def _on_leave(self, _event) -> None:
        if not self._active:
            self.set_active(False)

    def _on_click(self, _event) -> None:
        self._command(self._item)


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, items: list[NavigationItem], theme: UITheme, on_select) -> None:
        super().__init__(
            master,
            fg_color=theme.colors.sidebar,
            corner_radius=0,
            border_width=1,
            border_color=theme.colors.border,
            width=210,
        )
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._items = items
        self._theme = theme
        self._on_select = on_select
        self._buttons: dict[str, SidebarNavItem] = {}

        self._build_brand()
        self._build_navigation()
        self._build_footer()

    def set_active(self, item_id: str) -> None:
        for key, button in self._buttons.items():
            button.set_active(key == item_id)

    def _build_brand(self) -> None:
        brand_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        brand_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(16, 10))

        ctk.CTkLabel(
            brand_frame,
            text="ALPHAFORGE V3",
            text_color=self._theme.colors.text,
            font=self._theme.font("label", weight="bold"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand_frame,
            text="Estrutura inicial",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("caption"),
        ).pack(anchor="w", pady=(2, 0))

    def _build_navigation(self) -> None:
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(4, 0))
        nav_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            nav_frame,
            text="Abas",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("label", weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=4, pady=(0, 10))

        for index, item in enumerate(self._items, start=1):
            button = SidebarNavItem(nav_frame, item, self._theme, self._handle_select)
            button.grid(row=index, column=0, sticky="ew", pady=1)
            self._buttons[item.item_id] = button

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        footer.grid(row=2, column=0, sticky="sew", padx=12, pady=12)

        ctk.CTkLabel(
            footer,
            text="MVP sem integracao",
            anchor="w",
            text_color=self._theme.colors.text_subtle,
            font=self._theme.font("caption"),
        ).pack(anchor="w")

    def _handle_select(self, item: NavigationItem) -> None:
        self.set_active(item.item_id)
        self._on_select(item)

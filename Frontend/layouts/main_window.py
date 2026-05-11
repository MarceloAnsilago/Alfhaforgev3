import customtkinter as ctk

from components.sidebar import Sidebar
from components.top_header import TopHeader
from models.navigation import NavigationItem, build_navigation_items
from themes.theme import UITheme, configure_ctk
from views.dashboard_view import DashboardView


class AlphaForgeApp(ctk.CTk):
    def __init__(self) -> None:
        self._theme = UITheme()
        configure_ctk(self._theme)
        super().__init__()

        self._navigation_items = build_navigation_items()
        self._active_item = self._navigation_items[0]

        self.title("AlphaForge V3")
        self.geometry("1440x900")
        self.minsize(1180, 760)
        self.configure(fg_color=self._theme.colors.app_background)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_shell()
        self._select_item(self._active_item)

    def run(self) -> None:
        self.mainloop()

    def _build_shell(self) -> None:
        self._sidebar = Sidebar(
            self,
            items=self._navigation_items,
            theme=self._theme,
            on_select=self._select_item,
        )
        self._sidebar.grid(row=0, column=0, sticky="nsw")

        main_shell = ctk.CTkFrame(
            self,
            fg_color=self._theme.colors.app_background,
            corner_radius=0,
        )
        main_shell.grid(row=0, column=1, sticky="nsew")
        main_shell.grid_rowconfigure(1, weight=1)
        main_shell.grid_columnconfigure(0, weight=1)

        header = TopHeader(main_shell, self._theme)
        header.grid(row=0, column=0, sticky="ew")

        self._content = DashboardView(main_shell, self._theme)
        self._content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 16))

    def _select_item(self, item: NavigationItem) -> None:
        self._active_item = item
        self._sidebar.set_active(item.item_id)
        self._content.set_section(item)

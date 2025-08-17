import time
import tkinter as tk
from typing import Optional

try:
    import customtkinter as ctk
except ImportError as e:
    raise SystemExit(
        "Missing dependency: customtkinter. Install with: pip install customtkinter"
    ) from e

from app.core.config import AppConfig
from app.core.simulation import Simulation
from app.ui.views.sidebar_view import SidebarView
from app.ui.views.playfield_view import PlayfieldView


class Application(ctk.CTk):
    """Top-level application window that composes UI and simulation.

    This is a safe sandbox GUI and does not integrate with any game.
    """

    def __init__(self, config: AppConfig) -> None:
        super().__init__()

        # Appearance and theme
        ctk.set_appearance_mode(config.appearance_mode)
        ctk.set_default_color_theme(config.color_theme)

        # Window
        self.title(config.app_title)
        self.geometry(f"{config.width}x{config.height}")
        self.minsize(980, 640)

        # Grid layout: [sidebar][playfield]
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Simulation state
        self.simulation = Simulation(play_width=760, play_height=660)
        self._last_time: float = time.perf_counter()

        # Sidebar
        self.sidebar = SidebarView(
            self,
            width=config.sidebar_width,
            on_toggle_run=self._on_toggle_run,
            on_reset=self._on_reset,
            on_auto_aim_changed=self._on_auto_aim_changed,
            on_aim_speed_changed=self._on_aim_speed_changed,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # Playfield
        self.playfield = PlayfieldView(self)
        self.playfield.grid(row=0, column=1, sticky="nsew")
        self.playfield.on_size_changed = self._on_playfield_size

        # Kick off tick loop
        self.after(16, self._tick)

    # ----- Callbacks from sidebar -----
    def _on_toggle_run(self, should_run: bool) -> None:
        self.simulation.running = should_run

    def _on_reset(self) -> None:
        self.simulation.reset()

    def _on_auto_aim_changed(self, enabled: bool) -> None:
        self.simulation.set_auto_aim_enabled(enabled)

    def _on_aim_speed_changed(self, rads_per_sec: float) -> None:
        self.simulation.set_aim_speed(rads_per_sec)

    # ----- Callback from playfield -----
    def _on_playfield_size(self, width: int, height: int) -> None:
        self.simulation.set_area_size(width, height)

    # ----- Main loop -----
    def _tick(self) -> None:
        now = time.perf_counter()
        dt = now - self._last_time
        self._last_time = now

        if self.simulation.running:
            self.simulation.update(dt)

        self.playfield.draw(self.simulation)
        self.after(16, self._tick)
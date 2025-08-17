try:
    import customtkinter as ctk
except ImportError as e:
    raise SystemExit(
        "Missing dependency: customtkinter. Install with: pip install customtkinter"
    ) from e


class SidebarView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width: int,
        on_toggle_run,
        on_reset,
        on_auto_aim_changed,
        on_aim_speed_changed,
    ) -> None:
        super().__init__(master, width=width, corner_radius=0)
        self.grid_propagate(False)

        self._running = True
        self._on_toggle_run = on_toggle_run
        self._on_reset = on_reset
        self._on_auto_aim_changed = on_auto_aim_changed
        self._on_aim_speed_changed = on_aim_speed_changed

        # Layout
        self.grid_rowconfigure(99, weight=1)

        title = ctk.CTkLabel(self, text="Practice Panel", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, padx=18, pady=(16, 8), sticky="w")

        sub = ctk.CTkLabel(
            self,
            text="Sandbox only • No game access",
            text_color=("gray70", "gray65"),
            font=ctk.CTkFont(size=12),
        )
        sub.grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

        # Auto aim switch
        self.auto_aim_var = ctk.BooleanVar(value=True)
        self.auto_aim = ctk.CTkSwitch(self, text="Auto Aim (sandbox)", variable=self.auto_aim_var, command=self._on_auto_aim)
        self.auto_aim.grid(row=2, column=0, padx=18, pady=(4, 8), sticky="we")

        # Aim speed
        ctk.CTkLabel(self, text="Aim Speed (rad/s)").grid(row=3, column=0, padx=18, pady=(0, 6), sticky="w")
        self.aim_speed_var = ctk.DoubleVar(value=2.2)
        self.aim_speed_slider = ctk.CTkSlider(self, from_=0.2, to=6.0, number_of_steps=58, variable=self.aim_speed_var, command=self._on_aim_speed)
        self.aim_speed_slider.grid(row=4, column=0, padx=18, pady=(0, 6), sticky="we")
        self.aim_speed_value = ctk.CTkLabel(self, text=f"{self.aim_speed_var.get():.2f}")
        self.aim_speed_value.grid(row=5, column=0, padx=18, pady=(0, 12), sticky="e")

        # Run/pause + reset
        self.run_btn = ctk.CTkButton(self, text="Pause Simulation", command=self._toggle_run)
        self.run_btn.grid(row=6, column=0, padx=18, pady=(4, 6), sticky="we")

        self.reset_btn = ctk.CTkButton(self, text="Reset Sandbox", command=self._reset)
        self.reset_btn.grid(row=7, column=0, padx=18, pady=(0, 10), sticky="we")

    # ----- Event handlers -----
    def _toggle_run(self) -> None:
        self._running = not self._running
        self.run_btn.configure(text=("Resume Simulation" if not self._running else "Pause Simulation"))
        if callable(self._on_toggle_run):
            self._on_toggle_run(self._running)

    def _reset(self) -> None:
        if callable(self._on_reset):
            self._on_reset()

    def _on_auto_aim(self) -> None:
        enabled = bool(self.auto_aim_var.get())
        if callable(self._on_auto_aim_changed):
            self._on_auto_aim_changed(enabled)

    def _on_aim_speed(self, _v: float) -> None:
        value = float(self.aim_speed_var.get())
        self.aim_speed_value.configure(text=f"{value:.2f}")
        if callable(self._on_aim_speed_changed):
            self._on_aim_speed_changed(value)